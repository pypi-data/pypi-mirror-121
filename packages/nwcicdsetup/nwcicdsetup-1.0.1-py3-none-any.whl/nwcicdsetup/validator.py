import os
import re
import sys
from itertools import chain
from pathlib import Path
from typing import Any, Dict

import yaml

from .circlecicontext import CircleCIContext
from .nwservice import NWDeployment, NWService, NWServiceContext, NWTask
from .validationschema import base_config_validate


async def validate(general_config: str):
    cwd = Path(".")
    print(f"current working dir is: {cwd.resolve()}")
    configs = list(cwd.rglob("cicd.yml"))
    print(f"found {len(configs)} 'cicd.yml'")

    try:

        def validate_attr_dependencies(cwd: Path, service: NWService, task: Any):
            for d in task.dependencies:
                path = Path(d.removesuffix("*")).relative_to(cwd)
                path_exists(service, task, str(path))

        def path_exists(service: NWService, task: NWTask, path: str):
            if not os.path.exists(path):
                raise Exception(
                    f"{service.context.config_path}/{task.name}: Could not find '{path}'")

        def valdiate_deployment_attr_infra_yml_path(cwd: Path, service: NWService, d: NWDeployment):
            if len(d.infra_yml_path):
                path = Path(os.path.join(service.context.service_path,
                                         d.infra_yml_path)).relative_to(cwd)
                if not os.path.isfile(path):
                    raise Exception(
                        f"{service.context.config_path}: Could not find yaml file for '{d.infra_yml_path}'")

        def validate_attr_requires(services: Dict[str, NWService], service: NWService, task: Any):
            for id in task.requires:
                service_id, task_id = id.split(":")
                requires_all = bool(re.search("[\\*]+", task_id))

                # validate the service and the jobs to find
                if not service_id in services or (not requires_all and not task_id in services[service_id].all_jobs):
                    raise Exception(
                        f"{service.context.config_path}: Nothing found for reference '{id}'")

        if os.path.exists(general_config):
            with open(general_config, mode="rb") as base_config:
                base_config_validate(yaml.safe_load(base_config))
        circleci_context = CircleCIContext.create_dummy_env()

        services: Dict[str, NWService] = {}
        services |= {s.name: s for s in [NWService(
            NWServiceContext(circleci_context, services, str(configPath.relative_to(cwd)), str(cwd.resolve())))
            for configPath in configs]}
        for service in services.values():
            for task in chain(service.tasks.values(), service.deployments.values()):
                validate_attr_requires(services, service, task)
                validate_attr_dependencies(cwd, service, task)

            for deployment in service.deployments.values():
                valdiate_deployment_attr_infra_yml_path(
                    cwd, service, deployment)
            for task in service.tasks.values():
                path_exists(service, task, task.path)
    except Exception as e:
        print("invalid")
        sys.exit(str(e))
    print("valid")
