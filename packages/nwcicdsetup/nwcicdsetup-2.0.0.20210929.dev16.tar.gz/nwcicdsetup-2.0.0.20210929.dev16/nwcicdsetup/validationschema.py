import re
from typing import Any, Dict, List, Set

from schema import And, Optional, Or, Schema, SchemaError, Use


def service_validate(data: Dict[str, Any], general_config: Dict[str, Any]) -> Dict[str, Any]:
    commands: Dict[str, Any] = general_config["commands"]

    def validate_command(validate_command: Dict[str, Any]) -> bool:

        # check valid referenced commands and parameters
        parameters: Dict[str, Any]
        for name, parameters in validate_command.items():
            if not name in commands:
                raise SchemaError(
                    f"Command '{name}' not found in general config")
            for parameter_name in parameters.keys():
                if not parameter_name in commands[name]["parameters"]:
                    raise SchemaError(
                        f"Parameter '{parameter_name}' not found in command '{name}'")

            # check that all expected command values have been set
            config_parameters: Dict[str, Any] = commands[name]["parameters"]
            for param_name in config_parameters:
                if not param_name in validate_command[name]:
                    raise SchemaError(
                        f"Command '{name}' expects parameter value for '{param_name}'")

        return True

    def unique_object(values: List[Dict[str, Any]]) -> bool:
        items: Set[str] = set()
        for v in values:
            for k in v.keys():
                if k in items:
                    return False
                items.add(k)
        return True

    id_check: Any = re.compile(
        "[A-Za-z0-9_\\-\\/\\@]+:([A-Za-z0-9_\\-\\/\\@]+|\\*)$")

    def is_id(value: str) -> bool:
        return id_check.match(value)

    current_path = ""

    def store_path(path: str) -> str:
        nonlocal current_path
        current_path = path
        return path

    def task_default(additional_parameter: Dict[Any, Any] = {}) -> Dict[Any, Any]:
        return {
            # path to the tasks main folder; set as current working dir if not specificallly set;
            # path relative to cicd.yml file; by default set to the cicd.yml directory
            Optional("path", default="."): And(str, Use(store_path)),
            # commands to be looked up in the linked general-config.yml
            "commands": [
                And({
                    str:  # command name
                    {
                        # commandname:value pairs:

                        # all commands have a default no-output-timer
                        Optional("no_output_timeout", default="10m"): str,
                        # the directory the job is run on; relative to service directory
                        Optional("working_dir", default=lambda: current_path): str,
                        str: Or(str, float, bool)  # miscelanious parameters
                    } | additional_parameter
                }, validate_command)
            ],
            Optional("resource_class", default="small"): And(str, Or("small", "medium", "medium+", "large", "xlarge", "2xlarge", "2xlarge+")),
            Optional("executor", default="ubuntu"): And(str, Or("ubuntu", "aws-lambda"), error="You can choose between 'ubuntu' and 'aws-lambda'"),
            # triggers the job execution on change; relative path from root dir; for example: services/scheduling/apps/api/*
            Optional("dependencies"): [str],
            # list of task references that will be considered when determining the changeset; is used to create job dependencies in workflow jobs
            Optional("requires"): [And(str, is_id)]
        }

    serviceSchema = Schema({
        "name": str,  # Unique name of the service containing all the apps; relevant for references
        Optional("tasks"):
        And([
            {
                # Task that can be referenced via "ServiceName:TaskName"
                str: task_default()
            }
        ], And(unique_object, error="Found duplicate key in tasks")),
        Optional("deployments"):
        And([
            {
                # custom deployment that can be referenced in workflows via 'serviceName:deploymentName'
                str: task_default(additional_parameter={
                    "infra_yml_path": str  # we force the infra_yml_path attribute on deployments
                })
            }
        ], And(unique_object, error="Found duplicate key in deployments"))
    })
    return serviceSchema.validate(data)  # type: ignore


def general_config_validate(data: Dict[str, Any]) -> Dict[str, Any]:
    general_config_schema = Schema({
        "version": Or(str, float),
        "machine": {"python": {"version": Or(str, float)}},
        "executors":
        {
            "ubuntu": any,
            "aws-lambda": any
        },
        Optional("commands"): {
            str: {  # all commands must have a parameters section
                "parameters":
                {
                    # workign_dir for commands is mandatory
                    "working_dir": {"type": "string"},
                    Optional(str):
                    {
                        "type": Or("string", "boolean", "integer"),
                        Optional("default"): Or(str, bool, float)
                    }
                },
                str: any  # all other keys we don't care
            },
            And("empty_job", error="You have to provide a command for 'empty_job'"):
            {
                "parameters":
                {
                    "job_name": {"type": "string"},
                    "reason": {"type": "string"}
                },
                "steps": [{"run": any}]
            },
            And("changeset_info", error="You have to provide a command for 'changeset_info'"):
            {
                "parameters":
                {
                    "file_name": {"type": "string"},
                    "data": {"type": "string"}
                },
                "steps": [{"run": any}, {str: any}]
            }
        },
        Optional("parameters"): any
    })
    return general_config_schema.validate(data)  # type: ignore
