import asyncio
from typing import Any, Dict, List, Union

from .nwtasktype import NWTasktype
from .nwservice import NWDeployment, NWService, NWTask

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
        resolve_yml_async = {
            NWTasktype.DOTNET_SERVICE: self.dotnet_service_template_async,
            NWTasktype.PYTHON: self.python_template_async,
            NWTasktype.UNIT_TEST: self.unittest_template_async,
            NWTasktype.DOCKER_BUILD: self.docker_template_async
        }
        if await task.is_changed_async:
            return await resolve_yml_async[task.type](task)
        return {}

    async def deployment_to_yml_async(self, deployment: NWDeployment) -> Dict[str, Any]:
        if await deployment.is_changed_async:
            return await self.deployment_template_async(deployment)
        return {}

    async def deployments_to_yaml_async(self, deployments: Dict[str, NWDeployment]) -> Dict[str, Any]:
        async def exec(d: NWDeployment) -> Dict[str, Any]:
            return {d.name: await self.deployment_to_yml_async(d)}

        generated: Dict[str, Any] = {}
        for d in await asyncio.gather(*[exec(deployment) for deployment in deployments.values()]):
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

    async def dotnet_service_template_async(self, task: NWTask) -> Dict[str, Any]:
        steps: List[Union[str, Dict[str, Any]]] = [
            "checkout",
            self.yml_remote_docker,
            self.yml_project_context_job(task),
            self.yml_build_job_dotnet(task),
            self.yml_dotnet_test_job(task)
        ]

        return await self.create_job_async(task, steps)

    async def python_template_async(self, task: NWTask) -> Dict[str, Any]:
        # add a test step here?!
        steps: List[Union[str, Dict[str, Any]]] = [
            "checkout",
            self.yml_remote_docker,
            self.yml_project_context_job(task),
            self.yml_build_job_python(task)
        ]
        return await self.create_job_async(task, steps)

    async def docker_template_async(self, task: NWTask) -> Dict[str, Any]:
        steps: List[Union[str, Dict[str, Any]]] = [
            "checkout",
            self.yml_remote_docker,
            self.yml_project_context_job(task),
            self.yml_build_job_docker(task)
        ]
        return await self.create_job_async(task, steps)

    async def unittest_template_async(self, task: NWTask) -> Dict[str, Any]:
        if not await task.is_changed_async:
            return self.yml_empty_job(task, "Unit-Tests")

        yml_obj: Dict[str, Any] = {
            task.name:
            {
                "executor": task.executor,
                "resource_class": "xlarge",
                "steps": [
                    "checkout",
                    self.yml_remote_docker,
                    self.yml_dotnet_test_job(task)
                ]
            }
        }
        return yml_obj

    async def deployment_template_async(self, deployment: NWDeployment) -> Dict[str, Any]:
        if not await deployment.is_deploy_expected_async or deployment.is_feature_branch:
            # empty deployment
            reason = "# No changes to code, infrastructure or dependencies detected"
            if deployment.is_feature_branch:
                reason = "# you are working on a feature branch"
            elif deployment.context.fake_deploy:
                reason = f"\necho -e '{FAKE_DEPLOY_MSG}'"

            return {
                "docker": [{"image": "cimg/base:stable"}],
                "resource_class": "small",
                "steps": [{"empty_deploy": {"reason": reason}}]
            }

        deploy_job = {
            "run": {
                "command": deployment.command,
                "name": "Deploy",
                "no_output_timeout": deployment.no_output_timeout,
                "working_directory": deployment.context.service_path
            }
        } if len(deployment.command) else {
            "deploy":
            {
                "infra_yml_path": deployment.infra_yml_path,
                "path": deployment.context.service_path,
                "no_output_timeout": deployment.no_output_timeout,
                "stack_name": deployment.stack_name
            }
        }

        return {
            "executor": deployment.executor,
            # "docker": [{"image": deployment "cimg/base:stable"}],
            "resource_class": "small",
            "steps": [
                "checkout",
                self.yml_remote_docker,
                deploy_job
            ]
        }

    async def create_job_async(self, task: NWTask, steps: List[Union[str, Dict[str, Any]]]) -> Dict[str, Any]:
        if not await task.is_changed_async:
            return self.yml_empty_job(task, "Build")

        yml_obj = {
            "executor": task.executor,
            "resource_class": "xlarge",
            "steps": steps
        }

        self.add_docker_push(task, steps)
        return {task.name: yml_obj}

    def add_docker_push(self, task: NWTask, steps: List[Union[str, Dict[str, Any]]]):
        if not task.is_feature_branch:
            job = {}
            if len(task.command_push):
                # create own job for custom commands
                job = {
                    "run":
                    {
                        "working_directory": task.path,
                        "name": "Docker Push",
                        "no_output_timeout": task.no_output_timeout,
                        "command": task.command_push
                    }
                }
            else:
                job = {
                    "docker_push":
                    {
                        "path": task.path,
                        "image_name": task.image_name,
                        "no_output_timeout": task.no_output_timeout,
                        "regions": ' '.join(task.regions)
                    }
                }
            steps.append(job)

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

    def yml_build_job_dotnet(self, task: NWTask) -> Dict[str, Any]:
        if len(task.command_build):
            return self.yml_custom_build_job(task)
        return {
            "dotnet_build":
            {
                "path": task.path,
                "image_name": task.image_name,
                "no_output_timeout": task.no_output_timeout,
                "runtime": task.runtime
            }
        }

    def yml_build_job_docker(self, task: NWTask) -> Dict[str, Any]:
        if len(task.command_build):
            return self.yml_custom_build_job(task)
        return {
            "docker_build":
            {
                "path": task.path,
                "image_name": task.image_name,
                "no_output_timeout": task.no_output_timeout
            }
        }

    def yml_build_job_python(self, task: NWTask) -> Dict[str, Any]:
        if len(task.command_build):
            return self.yml_custom_build_job(task)
        return {
            "python_build":
            {
                "path": task.path,
                "image_name": task.image_name,
                "no_output_timeout": task.no_output_timeout
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

    ################################################################
    ######################### NOT USED #############################
    ################################################################

    def yml_cache_restore_job(self, cache_key: str) -> Dict[str, Any]:
        return {
            "restore_cache":
            {
                "name": "Try to restore cache",
                "key": cache_key
            }
        }

    def yml_cache_check_job(self, work_dir: str) -> Dict[str, Any]:
        return {
            "run":
            {
                "name": "Check cache",
                "working_directory": work_dir,
                "command": f"""
                echo working dir: $(pwd)

                ls
                if [ -d ".cache" ]; then
                    echo "Valid cache found - Skip execution"
                    circleci step halt
                else
                    echo "No valid cache found - Continue execution"
                fi
                """
            }
        }

    def yml_cache_create_job(self, work_dir: str, cache_key: str) -> Dict[str, Any]:
        return {
            "run":
            {
                "name": "Create cache",
                "working_directory": work_dir,
                "command": f"""
                    echo working dir: $(pwd)
                    ls
                    mkdir .cache
                    cd .cache
                    echo "{cache_key}" > cache_info
                    ls
                    """
            }
        }

    def yml_cache_save_job(self, work_dir: str, cache_key: str) -> Dict[str, Any]:
        return {
            "save_cache":
            {
                "name": "Save cache",
                "key": cache_key,
                "paths": [work_dir + "/.cache"]
            }
        }
