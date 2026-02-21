from enum import Enum


class OperatingSystem(str, Enum):
    LINUX = "Linux"
    MAC = "Darwin"
    WINDOWS = "Windows"


ROLES = [
    "user",
    "admin"
]


WORKSPACE_NAME = "workspace-aifoundary-poc"
LAKEHOUSE_NAME = "aifoundary_lakehouse_v1"
root_path = f"{LAKEHOUSE_NAME}.Lakehouse"