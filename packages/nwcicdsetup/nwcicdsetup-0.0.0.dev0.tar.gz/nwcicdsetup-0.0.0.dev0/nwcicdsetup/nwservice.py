import asyncio
import json
import os
import re
import subprocess
from enum import Enum, unique
from io import FileIO
from itertools import chain
from pathlib import Path
from typing import Any, Coroutine, Dict, List, Optional, Set,  Union

import yaml
from schema import SchemaError

from . import circleci
from .circlecicontext import CircleCIContext
from .nwtasktype import NWTasktype
from .validationschema import service_validate


@unique
class Context(Enum):
    FEATURE = 0
    DEV = 1
    TEST = 2
    STAGE = 3
    PRODUCTION = 4


class NWServiceContext:

    def __init__(
            self,
            circleci_context: CircleCIContext,
            services: Dict[str, "NWService"],
            path: str,
            cwd: str,
            global_dependencies: List[str] = [],
            fake_deploy: bool = False,
            force: bool = False):

        self.config_path: str  # path from the root to the parsed config.yml of this service
        self.cwd = cwd.replace("\\", "/")  # current working directory
        # replace deployment logic with a Nicolas Cage
        self.fake_deploy: bool = fake_deploy
        # indicating to force a rebuild for all jobs (builds & deployments)
        self.force: bool = force
        # dependencies which cause a global rebuild
        self.global_dependencies = list(global_dependencies)
        # all services mapped via their ids
        self.services: Dict[str, NWService] = services
        # we write this ref here on purpose so we see changes from the outside class internally
        self.circleci_context = circleci_context
        path = os.path.normpath(path).replace("\\", "/")
        # path to the services directory
        self.service_path = os.path.dirname(path).replace("\\", "/")
        self.service_path = self.service_path if len(
            self.service_path) > 0 else "."
        self.config_path = path

    @property
    def branch(self) -> str:
        return self.circleci_context.branch

    @property
    def job_context(self) -> Context:
        return NWServiceContext.branch_to_context(self.branch)

    @staticmethod
    def branch_to_context(branch: str) -> Context:
        branch = branch.lower()
        if branch == "develop":
            return Context.DEV
        elif branch == "testing":
            return Context.TEST
        elif branch == "staging":
            return Context.STAGE
        elif branch == "master":
            return Context.PRODUCTION

        return Context.FEATURE


class NWService:

    def __init__(self, context: "NWServiceContext"):
        self._apps_changed: Optional[bool] = None
        self.context: NWServiceContext
        self.deployments: Dict[str, NWDeployment] = {}
        self.name: str = ""
        self.tasks: Dict[str, NWTask] = {}

        print(f"process config '{context.config_path}'")
        nodes: Dict[str, Any] = yaml.safe_load(
            FileIO(context.config_path, "rb"))
        try:
            nodes = service_validate(nodes)
        except SchemaError as e:
            print(f"error validating {context.config_path}")
            raise e

        self.__dict__.update(nodes)
        self.context = context

        # convert the given dictionaries according to the given schema into an well defined object
        if "tasks" in nodes:
            self.tasks = {name: NWTask(
                name, members, self) for task in nodes["tasks"] for name, members in task.items()}
        if "deployments" in nodes:
            self.deployments = {name: NWDeployment(self, context, f"{self.name}-{name}-deploy", members)
                                for d in nodes["deployments"] for name, members in d.items()}

        def validate():
            collection: Set[str] = set()
            duplicates: Set[str] = set()

            def check(x: str):
                if x in collection:
                    duplicates.add(x)
                collection.add(x)

            for x in chain(self.deployments.keys(), self.tasks.keys()):
                check(x)
            if any(duplicates):
                raise Exception(
                    f"Found non unique tasks/deployments ids on {self.name}: {json.dumps(list(duplicates), indent=4)}")
        validate()

    @property
    def context_name(self) -> str:
        c = self.context.job_context
        if c == Context.FEATURE:
            return "feature"
        if c == Context.DEV:
            return "dev"
        if c == Context.TEST:
            return "test"
        if c == Context.STAGE:
            return "stage"
        if c == Context.PRODUCTION:
            return "prod"
        raise Exception(f"Cant find context for {self.name}")

    @property
    def all_jobs(self) -> Dict[str, Union["NWTask", "NWDeployment"]]:
        return self.tasks | self.deployments

    @property
    async def did_apps_change_async(self) -> bool:
        if self.context.force:
            return True

        if self._apps_changed == None:
            self._apps_changed = any(await asyncio.gather(*[app.is_changed_async for app in self.tasks.values()]))
        return self._apps_changed

    async def check_changes_for_required(self, depency_ids: List[str]) -> bool:
        """retrieves change status of tasks and deployments via dependency_ids"""
        services = self.context.services

        def tasks_for(id: str) -> List[Coroutine[Any, Any, bool]]:
            service_id, job_id = id.split(":")

            # link all jobs from the service?
            requires_all = bool(
                re.search('[\\*]+', job_id))

            # validate the service and the tasks to find
            if not service_id in services:
                raise Exception(
                    f"No service found for {service_id} in '{id}'")

            service = services[service_id]
            all_jobs = service.all_jobs
            if not job_id in all_jobs and not requires_all:
                raise Exception(
                    f"No task/deployment found for {job_id} in '{id}'")

            tasks = [t.is_changed_async for t in [*service.tasks.values(), *service.deployments.values()]
                     ] if requires_all else [all_jobs[job_id].is_changed_async]
            return tasks

        tasks = [t for id in depency_ids for t in tasks_for(id)]
        results = await asyncio.gather(*tasks)
        return any(results)


class NWTask:

    def __init__(self, name: str, members: Dict[str, Any], service: "NWService"):
        self._is_changed: Optional[bool] = None
        self.command_build: str = ""  # command used for Build job
        self.command_push: str = ""  # command used for Push job
        # folder dependencies which will be checked for changes
        self.dependencies: List[str] = []
        self.executor: str  # executor used for the job
        self.image_name: str = ""
        self.no_output_timeout: str  # output timer used for the job
        self.path: str = ""  # path of this task relative from service dir
        self.regions: List[str] = []  # regions to be used for deployment
        self.requires: List[str] = []  # other tasks to wait on completion
        self.runtime: str = "linux-arm64"
        self.service: NWService = service  # parent service owning this task
        self.type: NWTasktype  # defines the type of this task
        self.vanilla_name: str = name  # just the raw task name

        self.__dict__.update(members)
        self.service_path = service.context.service_path
        self.path = os.path.normpath(
            os.path.join(service.context.service_path, self.path)).replace("\\", "/")

        if not len(self.image_name):
            self.image_name = f"{self.service.name}-{name}"

        job_appendix = "-build" if self.type == NWTasktype.PYTHON or self.type == NWTasktype.DOTNET_SERVICE else ""
        self.name = f"{self.service.name}-{name}-{self.type.value}{job_appendix}"

        # always add the tasks directory as dependency
        self.dependencies.append(self.path + "/*")

    @property
    def is_feature_branch(self) -> bool:
        return self.service.context.job_context == Context.FEATURE

    @property
    async def is_changed_async(self) -> bool:
        if self.service.context.force:
            return True

        if self._is_changed is None:
            all_dependencies = self.dependencies + self.service.context.global_dependencies
            self._is_changed = await circleci.check_changes_async(
                self.service.context.circleci_context,
                self.path,
                all_dependencies) or await self.service.check_changes_for_required(self.requires)
        return self._is_changed

    @property
    def test_path(self) -> str:
        # returns path to folder with a test project named "taskname.Test" otherwise the task path
        # searches on self.path and parents service path
        def find_with_name_on_path(name: str, path: Path) -> str:
            name = re.sub("[\\.\\-_]", "", name)
            folders = path.rglob(f"*.Test")  # case sensitive names
            service_result = list(filter(lambda a_path: re.match(
                f".*{name}.*", str(a_path), flags=re.IGNORECASE), folders))
            return str(service_result.pop()).replace("\\", "/") if len(service_result) else ""

        result = find_with_name_on_path(self.vanilla_name, Path(self.path))
        if not len(result):
            result = find_with_name_on_path(
                self.vanilla_name, Path(self.service_path))
        result = result if len(result) else self.path
        return result

    @property
    def get_cache_key(self) -> str:
        # creating a cache key with info about when this tasks
        # source directory has been modified the last time
        cmd = f"git log -n 1 --pretty=format:%H -- {self.path}"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        msg, _ = p.communicate()
        return f"{self.name}-{msg.decode()}"


class NWDeployment:

    def __init__(self, service: "NWService", context: "NWServiceContext", name: str, members: Dict[str, Any] = {}):
        self._infra_changed: Optional[bool] = None
        self.command: str = ""  # Command to override the default one
        # trigger task if source changes in this destination
        self.dependencies: List[str] = []
        self.infra_yml_path = ""  # Path to the infra.yml relative to the service folder
        self.name: str = name  # Unique name of the deployment job
        self.no_output_timeout: str = "33m"  # timeout for the job, default 33m
        # reference to other service tasks this deployment has to wait on
        self.requires: List[str] = []
        # the service owning this deployment
        self.service: NWService = service
        self.context = context

        self.stack_name: str = ""  # name of the stack to be used for deployment command
        self.executor: str = ""  # executor to be used for deployment job
        self.__dict__.update(members)
        self.infra_yml_path = self.infra_yml_path.replace(
            "\\", "/").replace("//", "/")

        # path to this services infrastructure
        path = os.path.normpath(os.path.join(
            self.context.service_path, 'infrastructure/*')).replace("\\", "/")
        self.dependencies.append(path)

    @property
    def is_feature_branch(self) -> bool:
        return self.service.context.job_context == Context.FEATURE

    @property
    async def is_deploy_expected_async(self) -> bool:
        """Returns true if any linked deployment dependencies changed and we are not on a feature branch"""
        return await self.is_changed_async and not self.is_feature_branch and not self.context.fake_deploy

    @property
    async def is_changed_async(self) -> bool:
        """Returns true if any of the given local file dependencies, an services task or any linked 'requires'-jobs changed"""
        if self.context.force:
            return True

        if self._infra_changed == None:
            # check local file dependency change
            self._infra_changed = await circleci.check_change_async(
                self.service.context.circleci_context,
                self.name,
                self.dependencies)
            # check services task change
            if not self._infra_changed:
                self._infra_changed = await self.service.did_apps_change_async
            # check dependencies pulled in via the 'requires' attribute
            if not self._infra_changed:
                self._infra_changed = await self.service.check_changes_for_required(self.requires)

        return self._infra_changed
