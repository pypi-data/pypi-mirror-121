import asyncio
import json
from os import name
from typing import Any, Dict, List, Union

from nwcicdsetup.nwservice import NWDeployment, NWService, NWTask

FAKE_DEPLOY_MSG: str = '''
~~~~           FAKE DEPLOY          ~~~~


░░░░░░░░░░░░░░▄▄▄▄▄▄▄▄▄▄▄▄░░░░░░░░░░░░░░
░░░░░░░░░░░░▄████████████████▄░░░░░░░░░░
░░░░░░░░░░▄██▀░░░░░░░▀▀████████▄░░░░░░░░
░░░░░░░░░▄█▀░░░░░░░░░░░░░▀▀██████▄░░░░░░
░░░░░░░░░███▄░░░░░░░░░░░░░░░▀██████░░░░░
░░░░░░░░▄░░▀▀█░░░░░░░░░░░░░░░░██████░░░░
░░░░░░░█▄██▀▄░░░░░▄███▄▄░░░░░░███████░░░
░░░░░░▄▀▀▀██▀░░░░░▄▄▄░░▀█░░░░█████████░░
░░░░░▄▀░░░░▄▀░▄░░█▄██▀▄░░░░░██████████░░
░░░░░█░░░░▀░░░█░░░▀▀▀▀▀░░░░░██████████▄░
░░░░░░░▄█▄░░░░░▄░░░░░░░░░░░░██████████▀░
░░░░░░█▀░░░░▀▀░░░░░░░░░░░░░███▀███████░░
░░░▄▄░▀░▄░░░░░░░░░░░░░░░░░░▀░░░██████░░░
██████░░█▄█▀░▄░░██░░░░░░░░░░░█▄█████▀░░░
██████░░░▀████▀░▀░░░░░░░░░░░▄▀█████████▄
██████░░░░░░░░░░░░░░░░░░░░▀▄████████████
██████░░▄░░░░░░░░░░░░░▄░░░██████████████
██████░░░░░░░░░░░░░▄█▀░░▄███████████████
███████▄▄░░░░░░░░░▀░░░▄▀▄███████████████

~~~~           FAKE DEPLOY          ~~~~
'''


class CircleCIYamlFactory:
    async def task_to_yaml_async(self, task: NWTask) -> Dict[str, Any]:
        if await task.should_execute_async:

            steps: List[Union[str, Dict[str, Any]]] = ["checkout"]
            steps += task.command_steps

            yml_obj = {
                "executor": task.executor,
                "resource_class": task.resource_class,
                "steps": steps
            }

            # self.add_docker_push(task, steps)
            return {task.name: yml_obj}

        # empty job
        reason = "# No changes to code, infrastructure or dependencies detected"
        if task.is_feature_branch:
            reason = "# you are working on a feature branch"
        elif isinstance(task, type(NWDeployment)) and task.service.context.fake_deploy:
            reason = f"\necho -e '{FAKE_DEPLOY_MSG}'"

        return {
            task.name:
            {
                "docker": [{"image": "cimg/base:stable"}],
                "resource_class": "small",
                "steps": [
                    {
                        "empty_job":
                        {
                            "job_name": task.name,
                            "reason": reason
                        }
                    }
                ]
            }
        }

    async def deployments_to_yaml_async(self, deployments: Dict[str, NWDeployment]) -> Dict[str, Any]:
        generated: Dict[str, Any] = {}
        for d in await asyncio.gather(*[self.task_to_yaml_async(deployment) for deployment in deployments.values()]):
            generated |= d
        return generated

    async def service_to_yaml_async(self, service: NWService) -> Dict[str, Any]:
        print(
            f"Generate jobs for service '{service.name}' @ {str(service.context.job_context)}")

        app_yaml = await asyncio.gather(*[self.task_to_yaml_async(task) for task in service.tasks.values()])
        jobs: Dict[str, Any] = {}
        for a in app_yaml:
            jobs |= a

        print(
            f"Generate deployments for service '{service.name}' @ {str(service.context.job_context)}")
        deployments: Dict[str, Any] = await self.deployments_to_yaml_async(service.deployments)
        jobs |= deployments

        return jobs

    # def add_docker_push(self, task: NWTask, steps: List[Union[str, Dict[str, Any]]]):
    #     if not task.is_feature_branch:
    #         job = {}
    #         if len(task.command_push):
    #             # create own job for custom commands
    #             job = {
    #                 "run":
    #                 {
    #                     "working_directory": task.path,
    #                     "name": "Docker Push",
    #                     "no_output_timeout": task.no_output_timeout,
    #                     "command": task.command_push
    #                 }
    #             }
    #         else:
    #             job = {
    #                 "docker_push":
    #                 {
    #                     "path": task.path,
    #                     "image_name": task.image_name,
    #                     "no_output_timeout": task.no_output_timeout,
    #                     "regions": ' '.join(task.regions)
    #                 }
    #             }
    #         steps.append(job)

    yml_remote_docker = {
        "setup_remote_docker":
        {
            "version": "19.03.13"
        }
    }

    def yml_dotnet_test_job(self, task: NWTask) -> Dict[str, Any]:
        return {"dotnet_test": {"path": task.test_path}}

    def yml_custom_build_job(self, task: NWTask) -> Dict[str, Any]:
        return {
            "run":
            {
                "command": task.command_build,
                "name": "Build",
                "no_output_timeout": task.no_output_timeout,
                "working_directory": task.path
            }
        }

    def yml_project_context_job(self, task: NWTask) -> Dict[str, Any]:
        return {"build_context": {"path": task.path}}

    def yml_empty_job(self, task: NWTask, job_name: str) -> Dict[str, Any]:
        return {
            task.name:
            {
                "docker": [{"image": "cimg/base:stable"}],
                "resource_class": "small",
                "steps": [
                    {
                        "empty_job": {"job_name": job_name}
                    }
                ]
            }
        }

    def yml_changeset_info(self, job: Union[NWTask, NWDeployment]) -> Dict[str, Any]:
        return {
            "changeset_info":
            {
                "file_name":  f"{job.name}.json",
                "data": f"Job execution info:\n{json.dumps(job.change_info, indent=4)}"
            }
        }
