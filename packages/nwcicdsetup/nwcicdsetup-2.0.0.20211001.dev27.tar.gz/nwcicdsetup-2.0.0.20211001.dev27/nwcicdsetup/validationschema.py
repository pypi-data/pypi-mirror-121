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

            # check that all expected command values have been set if no default is specified
            config_parameters: Dict[str, Any] = commands[name]["parameters"]
            for param_name in config_parameters:
                if not param_name in validate_command[name] and "default" not in config_parameters[param_name]:
                    raise SchemaError(
                        f"Command '{name}' expects parameter value for '{param_name}'")

        return True

    def unique_task_ids(layers: List[Dict[str, Any]]) -> bool:
        """check all layers for unique task ids"""

        layer_items: Set[str] = set()
        for layer in layers:
            for layer_name, tasks in layer.items():
                for task_name in tasks:
                    if task_name in layer_items:
                        raise SchemaError(
                            f"Found duplicate task-id '{task_name}' in layer '{layer_name}'")
                    layer_items.add(task_name)
        return True

    requires_id: Any = re.compile(
        "[A-Za-z0-9_\\-\\/\\@]+:([A-Za-z0-9_\\-\\/\\@]+|\\*)$")

    def is_requires_id(value: str) -> bool:
        if requires_id.match(value):
            return True
        raise SchemaError(f"Id {value} doesn't requiret format {requires_id}")

    def convert_string_command(command_name: str) -> Dict[str, Any]:
        return {
            command_name: {
                "working_dir": "",
                "no_output_timeout": "10m"
            }
        }

    serviceSchema = Schema({
        "name": str,  # Unique name of the service containing all the apps; relevant for references
        "layers": And([  # layers definding an order of job execution
            {
                str:  # layer name
                {
                    # Task that can be referenced via "ServiceName:TaskName"
                    str:
                    {
                        # path to the tasks main folder; set as current working dir if not specificallly set;
                        # path relative to cicd.yml file; by default set to the cicd.yml directory
                        Optional("path", default=""): str,
                        # commands to be looked up in the linked general-config.yml
                        "commands": [
                            Optional(
                                And(str, Use(convert_string_command), validate_command)),
                            And({
                                # commandname:value pairs:
                                str:  # command name
                                {
                                    # all commands have a default no-output-timer
                                    Optional("no_output_timeout", default="10m"): str,
                                    # the directory the job is run on; relative to service directory
                                    Optional("working_dir", default=""): str,
                                    # miscelanious parameters
                                    str: Or(str, float, bool)
                                }
                            }, validate_command)
                        ],
                        Optional("resource_class", default="large"): And(str, Or("small", "medium", "medium+", "large", "xlarge", "2xlarge", "2xlarge+")),
                        Optional("executor", default="ubuntu"): And(str, Or("ubuntu", "aws-lambda"), error="You can choose between 'ubuntu' and 'aws-lambda'"),
                        # triggers the job execution on change; relative path from root dir; for example: services/scheduling/apps/api/*
                        Optional("dependencies"): [str],
                        # list of task references that will be considered when determining the changeset; is used to create job dependencies in workflow jobs
                        Optional("requires"): [And(str, is_requires_id)]
                    }
                }
            }
        ], unique_task_ids)
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
