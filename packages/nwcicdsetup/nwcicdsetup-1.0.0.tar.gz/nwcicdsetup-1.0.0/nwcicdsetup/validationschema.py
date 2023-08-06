import re
from typing import Any, Dict, List, Set

from schema import And, Optional, Or, Schema, Use

from .nwtasktype import NWTasktype


def convert_type(value: str) -> NWTasktype:
    return NWTasktype[value.upper().replace("-", "_")]


def unique_object(values: List[Dict[str, Any]]) -> bool:
    items: Set[str] = set()
    for v in values:
        for k in v.keys():
            if k in items:
                return False
            items.add(k)
    return True


id_check: Any = re.compile("[A-Za-z0-9_\\-\\/\\@]+:([A-Za-z0-9_\\-\\/\\@]+|\\*)$")


def is_id(value: str) -> bool:
    return id_check.match(value)


serviceSchema = Schema({
    "name": str,  # Unique name of the service containing all the apps; relevant for references
    Optional("tasks"):
    And([{
        # Task that can be referenced via "ServiceName:TaskName"
        str: {
            # path to the project folder; set as current working dir; relative to root directory
            # by default 'docker build' command is executed in here
            "path": str,
            # name of the docker image to create
            Optional("image_name"): str,
            # type of the task; see NWTasktype
            "type":  And(Use(convert_type), error="Invalid type. Please use on of the following: 'dotnet-service', 'python', 'docker-build', 'unit-test'"),
            Optional("executor", default="ubuntu"): And(str, Or("ubuntu", "aws-lambda"), error="You can choose between 'ubuntu' and 'aws-lambda'"),
            # command used to override the default build job from base-config.yml
            Optional("command_build"): str,
            # command used to override the default docker push job from base-config.yml
            Optional("command_push"): str,
            # timeout for the job, default 33m
            Optional("no_output_timeout", default="10m"): str,
            # docker push regions
            Optional("regions", default=["eu-west-1", "us-east-1"]): [str],
            # define the dotnet runtime; default: linux-arm64; for dotnet-service types only
            Optional("runtime"): str,
            # causes job execution on change; relative path from root dir; for example: services/scheduling/apps/api/*
            Optional("dependencies"): [str],
            # list of task/deployment references
            Optional("requires"): [And(str, is_id)]
        }
    }], And(unique_object, error="Found duplicate key in tasks")),
    Optional("deployments"): And([
        {
            # custom deployment that can be referenced in workflows via 'serviceName:deploymentName'
            str:
            {
                Or("infra_yml_path",  # Path to the infra.yml relative to the service folder
                   "command", only_one=True): str,  # Command to override the default one calling 'nwtools deploy-service'; executed in the services directory
                Optional("stack_name"): str,  # override the default stack name
                Optional("executor", default="ubuntu"): And(str, Or("ubuntu", "aws-lambda"), error="You can choose between 'ubuntu' and 'aws-lambda'"),
                # timeout for the job, default 33m
                Optional("no_output_timeout"): str,
                # causes job execution on change; relative path from root dir; for example: services/scheduling/apps/api/*
                Optional("dependencies"): [str],
                # list of task/deployment references
                Optional("requires"): [And(str, is_id)]
            }
        }
    ], And(unique_object, error="Found duplicate key in deployments"))
})

base_config_schema = Schema({
    "version": Or(str, float),
    "machine": {"python": {"version": Or(str, float)}},
    "executors":
    {
        "ubuntu": any,
        "aws-lambda": any
    },
    "commands":
    {
        "dotnet_test": {
            "parameters": {"path": any, "no_output_timeout": any},
            "steps": any
        },
        "dotnet_build": {
            "parameters": {"path": any, "image_name": any, "runtime": any, "no_output_timeout": any},
            "steps": any
        },
        "python_build": {
            "parameters": {"path": any, "image_name": any, "no_output_timeout": any},
            "steps": any
        },
        "docker_build": {
            "parameters": {"path": any, "image_name": any, "no_output_timeout": any},
            "steps": any
        },
        "docker_push": {
            "parameters": {"path": any, "image_name": any, "regions": any, "no_output_timeout": any},
            "steps": any
        },
        "deploy": {
            "parameters": {"path": any, "infra_yml_path": any, "stack_name": any, "no_output_timeout": any},
            "steps": any
        },
        "empty_deploy": {
            "parameters": {"reason": any},
            "steps": any
        },
        "empty_job": {
            "parameters": {"job_name": any},
            "steps": any
        },
        "build_context": {
            "parameters": {"path": any},
            "steps": any
        }
    },
    "parameters": {
        "force": any,
        "fake_deploy": any,
        "global_dependencies": any
    }
})


def service_validate(data: Dict[str, Any]) -> Dict[str, Any]:
    return serviceSchema.validate(data)  # type: ignore


def base_config_validate(data: Dict[str, Any]) -> Dict[str, Any]:
    return base_config_schema.validate(data)  # type: ignore
