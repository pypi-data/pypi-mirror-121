from enum import Enum, unique


@unique
class NWTasktype(Enum):

    DOTNET_SERVICE = "dotnet-service"  # generate dotnet service yaml
    PYTHON = "python"  # generate python yaml
    UNIT_TEST = "unit-test"  # generate unit test only yml
    DOCKER_BUILD = "docker-build" # generate a docker build/push only yml
