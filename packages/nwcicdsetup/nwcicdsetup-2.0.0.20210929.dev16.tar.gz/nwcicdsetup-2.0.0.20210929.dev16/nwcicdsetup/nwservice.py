import asyncio
import json
import os
import re
import subprocess
from enum import Enum, unique
from io import FileIO
from itertools import chain
from pathlib import Path
from typing import Any, Coroutine, Dict, List, Optional, Set, Tuple, Union

import yaml
from schema import SchemaError

from nwcicdsetup.circleci import check_change_async, check_dotnet_change_async
from nwcicdsetup.circlecicontext import CircleCIContext
from nwcicdsetup.validationschema import service_validate


@unique
class Context(Enum):
    FEATURE = 0
    DEV = 1
    TEST = 2
    STAGE = 3
    PRODUCTION = 4


class NWServiceContext:
    """Giving overall information this generation is running on"""

    def __init__(
            self,
            circleci_context: CircleCIContext,
            services: Dict[str, "NWService"],
            general_config: Dict[str, Any],
            cwd: str,
            global_dependencies: List[str] = [],
            fake_deploy: bool = False,
            force: bool = False):

        self.config_path: str
        """path from the root to the parsed config.yml of this service"""
        self.cwd = cwd.replace("\\", "/")
        """current working directory"""
        self.fake_deploy: bool = fake_deploy
        """replace deployment logic with a Nicolas Cage"""
        self.force: bool = force
        """indicating to force a rebuild for all jobs (builds & deployments)"""
        self.global_dependencies = list(global_dependencies)
        """dependencies which cause a global rebuild"""
        self.services: Dict[str, NWService] = services
        """all services mapped via their ids"""
        self.circleci_context = circleci_context
        """we write this ref here on purpose so we see changes from the outside class internally"""

        self.general_config = dict(general_config)
        """key/value pairs containing all general and cicd commands, executors etc. to link via tasks/deployments"""

    @property
    def branch(self) -> str:
        """returns the name of the current branch this is running on"""
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
    """Encapsulation of the cicd.yml files which is maintaining and accessing task/deployment data"""

    def __init__(self, context: "NWServiceContext", config_path: str):
        self.context: NWServiceContext = context
        """context information"""
        self.deployments: Dict[str, NWDeployment] = {}
        """parsed 'deployments' section of the cicd.yml controlling the deployment part"""
        self.name: str = ""
        """name of the parsed cicd.yml - assigned from its 'name' atttribute"""
        self.tasks: Dict[str, NWTask] = {}
        """parsed 'tasks' section of the cicd.yml mainly controlling the building part"""
        self.path = os.path.dirname(
            config_path.replace("\\\\", "/").replace("\\", "/"))
        """path to the cicd.yml file relative from the root"""

        try:
            print(f"process config '{self.path}'")
            nodes = service_validate(yaml.safe_load(FileIO(config_path, "rb")),
                                     context.general_config)
            self.__dict__.update(nodes)  # fill self.member values

            # convert the given dictionaries according to the given schema into an well defined object
            if "tasks" in nodes:
                self.tasks = {name: NWTask(name=name, service=self, members=members) for task in nodes["tasks"]
                              for name, members in task.items()}
            if "deployments" in nodes:
                self.deployments = {name: NWDeployment(name=name, service=self, members=members) for d in nodes["deployments"]
                                    for name, members in d.items()}
        except SchemaError as e:
            print(f"Error when processing {self.path}")
            raise e

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
        """returns a dictionary containing all tasks and deployment jobs or this service"""
        return self.tasks | self.deployments

    @property
    async def get_task_change_info_async(self) -> Tuple[bool, Dict[str, Any]]:
        """get information about task change; returns a Tuple(True, reasons of change)"""

        if self.context.force:
            return (True, {"Forced":  "All apps changed"})

        async def to_result(t: Coroutine[Any, Any, bool], name: str) -> Tuple[bool, str]:
            return (await t, name)

        app_changed_info: Dict[str, Any] = {}
        result = await asyncio.gather(*[to_result(app.is_changed_async, app.name) for app in self.tasks.values()])
        changed_result = list(filter(lambda x: x[0], result))

        is_changed = any(changed_result)
        if(is_changed):
            app_changed_info |= {"Tasks changed": list(map(
                lambda x: x[1], changed_result))}

        return (is_changed, app_changed_info)

    async def check_changes_for_required(self, depency_ids: List[str]) -> Tuple[bool, Dict[str, Any]]:
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

        async def to_result(t: Coroutine[Any, Any, bool], id: str) -> Tuple[bool, Dict[str, Any]]:
            return (await t, {"required task": id})

        tasks = [to_result(t, id) for id in depency_ids for t in tasks_for(id)]
        results = list(await asyncio.gather(*tasks))
        changed = any(filter(lambda x: x[0], results))

        if changed:
            info: Dict[str, Any] = {}
            for result in results:
                info |= result[1]
            return (True, info)
        return (False, {})


class NWTask:

    def __init__(self, name: str, service: "NWService", members: Dict[str, Any]):
        self._is_changed: Optional[bool] = None
        """private flag caching a previous call to is_changed_asyn()"""
        self.change_info: Dict[str, Any] = {}
        """changeset information available after first call to is_changed_async()"""
        self.commands: List[Dict[str, Dict[str, Union[str, float, bool]]]] = []
        """command and parameters this task will be linked to"""
        self.dependencies: List[str] = []
        """dependencies that will considered to determine changeset and trigger the job"""
        self.executor: str
        """executor to be used for the generated job"""
        self.path: str = ""
        """path of this task relative from cicd.yml"""
        self.resource_class: str
        """the resource class used for job generation"""
        self.requires: List[str] = []
        """tasks/deployments we consider to determine changeset and wait on job completion in workflow generation"""
        self.service: NWService = service
        """parent cicd.yml/nwservice that generated this task"""
        self.vanilla_name: str = name
        """the unprocessed task name"""

        self.__dict__.update(members)
        self.path = os.path.normpath(os.path.join(service.path, self.path)
                                     ).replace("\\", "/")

        self.name = f"{self.service.name}-{name}-{next(iter(self.commands[0]))}-job"
        """name of the task including the service name"""

        # always add the tasks directory as dependency
        self.dependencies.append(self.path + "/*")

    @property
    def command_steps(self) -> List[Union[str, Dict[str, Any]]]:
        steps: List[Union[str, Dict[str, Any]]] = []
        for command_entry in self.commands:
            for command, parameters in command_entry.items():
                step = {
                    command:
                    {
                        name: value for name,
                        value in parameters.items()
                    }
                }
                steps.append(step)
        return steps

    @property
    def is_feature_branch(self) -> bool:
        return self.service.context.job_context == Context.FEATURE

    @property
    async def should_execute_async(self) -> bool:
        """Returns true if dependencies changed"""
        return await self.is_changed_async

    @property
    async def is_changed_async(self) -> bool:
        if self.service.context.force:
            self.change_info = {"Forced": ""}
            return True

        if self._is_changed is None:
            dotnet_result = await check_dotnet_change_async(
                self.service.context.circleci_context,
                self.path)
            dependency_result = await check_change_async(
                self.service.context.circleci_context,
                self.name, self.dependencies, name="dependencies")

            global_result = await check_change_async(
                self.service.context.circleci_context,
                self.name, self.service.context.global_dependencies, name="global")

            required_dependencies_result = await self.service.check_changes_for_required(self.requires)

            self.change_info |= dotnet_result[1]
            self.change_info |= dependency_result[1]
            self.change_info |= global_result[1]
            self.change_info |= required_dependencies_result[1]

            self._is_changed = dotnet_result[0] or dependency_result[
                0] or global_result[0] or required_dependencies_result[0]

            if self._is_changed:
                print(
                    f'Detected relevant changes for {self.name}:\n{json.dumps(self.change_info, indent=2)}')
            else:
                print(f"Detected not relevant changes for {self.name}")

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
                self.vanilla_name, Path(self.service.path))
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


class NWDeployment(NWTask):

    def __init__(self, name: str, service: "NWService", members: Dict[str, Any] = {}):
        super().__init__(name, service, members)

        self.__dict__.update(members)
        self.name = f"{service.name}-{name}-deploy-job"

        for command_entry in self.commands:
            for command in command_entry.values():
                infra_path = str(command["infra_yml_path"])
                path = os.path.join(self.service.path,
                                    f'{os.path.dirname(str(infra_path))}/*').replace("\\", "/").replace("//", "/")
                self.dependencies.append(path)
        self.dependencies = list(set(self.dependencies))

    @property
    async def should_execute_async(self) -> bool:
        """Returns true if any linked deployment dependencies changed and we are not on a feature branch"""
        return await self.is_changed_async and not self.is_feature_branch and not self.service.context.fake_deploy

    @property
    async def is_changed_async(self) -> bool:
        """Returns true if any of the given local file dependencies, an services task or any linked 'requires'-jobs changed"""
        if self.service.context.force:
            self.change_info = {"Forced": ""}
            return True

        if self._is_changed == None:
            # check local file dependency change
            dependency_result = await check_change_async(
                self.service.context.circleci_context,
                self.name,
                self.dependencies, name="dependencies")
            self.change_info |= dependency_result[1]

            # check services task change
            task_result = await self.service.get_task_change_info_async
            self.change_info |= task_result[1]

            # check dependencies pulled in via the 'requires' attribute
            required_result = await self.service.check_changes_for_required(self.requires)
            self.change_info |= required_result[1]

            self._is_changed = dependency_result[0] or task_result[0] or required_result[0]

            if self._is_changed:
                print(
                    f'Detected relevant changes for {self.name}:\n{json.dumps(self.change_info, indent=2)}')
            else:
                print(f"Detected not relevant changes for {self.name}")

        return self._is_changed
