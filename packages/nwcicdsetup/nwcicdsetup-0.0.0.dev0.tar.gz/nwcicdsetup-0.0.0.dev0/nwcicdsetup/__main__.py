import argparse
import asyncio
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

from . import circleci
from .nwservice import NWService, NWServiceContext
from .validationschema import base_config_validate
from .yamlfactory import CircleCIYamlFactory


async def main(outfile: str, general_config: str, global_dependencies: List[str], fake_deploy: bool, force: bool, dummy_env: bool) -> None:
    circleci_context = await circleci.init_async(dummy_env)
    cwd = Path(".")
    configs = list(cwd.rglob("cicd.yml"))
    print(f"found {len(configs)} 'cicd.yml' in {cwd.resolve()}")

    if not os.path.exists(general_config):
        print(f"No file found for general config at '{general_config}'")
        exit(1)

    with open(general_config, mode="rb") as base_config_stream:
        base_config = base_config_validate(yaml.safe_load(base_config_stream))

    services: Dict[str, NWService] = {}
    services |= {s.name: s for s in [NWService(NWServiceContext(circleci_context, services, str(configPath.relative_to(
        cwd)), str(cwd.resolve()), global_dependencies, fake_deploy, force)) for configPath in configs]}

    # preserve entries from loaded base config
    workflow_name = "{}-build-deploy".format(
        NWServiceContext.branch_to_context(circleci_context.branch).name.lower())
    deploy_jobs: List[Dict[str, Any]] = []
    jobs: Dict[str, Any] = {}

    if "workflows" not in base_config:
        base_config["workflows"] = {workflow_name: {"jobs": deploy_jobs}}
    if workflow_name not in base_config["workflows"]:
        base_config["workflows"][workflow_name] = {"jobs": deploy_jobs}

    base_config["workflows"]["version"] = 2.1  # type: ignore

    if "jobs" not in base_config:
        base_config["jobs"] = jobs

    # generate jobs section
    yaml_factory = CircleCIYamlFactory()
    yml_tasks = [asyncio.create_task(
        yaml_factory.service_to_yaml_async(s)) for s in services.values()]
    for task_jobs in await asyncio.gather(*yml_tasks):
        jobs |= task_jobs

    # generate workflows section
    for build, deploy in [await fetch_workflow_async(services, s) for s in services.values()]:
        deploy_jobs += build
        deploy_jobs += deploy

    # output
    yaml_str: str = yaml.safe_dump(base_config, width=1000)  # type: ignore
    with open(os.path.join(cwd.resolve(), f"{outfile}"), mode="w") as config_file:
        config_file.write(yaml_str)
    print(f"Wrote configuration to {outfile}")


async def fetch_workflow_async(services: Dict[str, NWService], service: NWService) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    # this code should probably go somwhere into nwservice/task/deployment </3

    if not "yml_branch_filter" in globals():
        g = globals()
        g["yml_branch_filter"] = {"branches": {"only": service.context.branch}}
    yml_branch_filter = (globals())["yml_branch_filter"]

    def fetch_required(depency_ids: List[str]) -> List[str]:
        required: List[str] = []
        for id in depency_ids:
            service_id, job_id = id.split(":")

            # link all jobs from the service?
            requires_all = bool(re.search("[\\*]+", job_id))
            # validate the service and the tasks to find
            if not service_id in services:
                raise Exception(f"Nothing found for {service_id} in '{id}'")
            required_service = services[service_id]

            all_jobs = required_service.all_jobs
            if not job_id in all_jobs and not requires_all:
                raise Exception(f"Nothing found for {job_id} in '{id}'")

            if requires_all:
                required += [j.name for j in all_jobs.values()]
            else:
                required.append(all_jobs[job_id].name)
        return required

    def fetch_job(dependency_ids: List[str], name: str, custom_dependencies: List[str] = []) -> Dict[str, Any]:
        yml_obj = {"context": service.context_name,
                   "filters": yml_branch_filter}
        required = fetch_required(dependency_ids)
        if len(required) > 0:
            yml_obj["requires"] = required + custom_dependencies
        return {name: yml_obj}

    build_workflows: List[Dict[str, Any]] = []
    for task in service.tasks.values():
        build_workflows.append(fetch_job(task.requires, task.name))

    deployment_workflows: List[Dict[str, Any]] = []
    for dep in service.deployments.values():
        # each deployment depends on all internal jobs
        custom_dependencies = [t.name for t in service.tasks.values()]
        job = fetch_job(dep.requires, dep.name, custom_dependencies)
        deployment_workflows.append(job)

    return build_workflows, deployment_workflows


def str_presenter(dumper: Any, data: Any):
    if '\n' in data:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


if __name__ == "__main__":
    print(f"PyYaml version: {yaml.__version__}")

    parser = argparse.ArgumentParser("nwcicdsetup")
    parser.add_argument(
        "-o", "--out", type=str, required=True, help="File to write the configuration to")
    parser.add_argument(
        "-gc", "--general_config", required=True, type=str, help="Path to the config file describing basic functionality")
    parser.add_argument(
        "--global_dependencies", nargs="+", default=[], type=str, help="Global dependencies which force job execution if changed")
    parser.add_argument("--fake-deploy", action="store_true",
                        help="Replace the deploy commands with an echo output")
    parser.add_argument("--force", action="store_true",
                        help="Force full rebuild & deploy by executing all tasks")
    parser.add_argument("--dummy_env", action="store_true",
                        help="Fills CircleCI environment variables with dummy data")
    args = parser.parse_args()

    print(
        f"Global dependencies: {json.dumps(args.global_dependencies, indent=4)}")
    if args.force:
        print("<<< Forcing build and deployment >>>")
    if args.fake_deploy:
        print("<<< Using fake deploy >>>")
    if args.dummy_env:
        print("<<< Using dummy environment >>>")

    outfile = args.out
    print(f"writing config to '{outfile}'")
    general_config = args.general_config
    print(f"Load general config from '{general_config}'")

    yaml.add_representer(str, str_presenter)
    yaml.representer.SafeRepresenter.add_representer(  # type: ignore
        str, str_presenter)

    asyncio.get_event_loop().run_until_complete(main(
        outfile,
        general_config,
        args.global_dependencies,
        args.fake_deploy,
        args.force,
        args.dummy_env))
