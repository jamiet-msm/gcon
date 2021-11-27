from enum import Enum
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import List
from google.cloud.functions_v1.services.cloud_functions_service import (
    CloudFunctionsServiceClient,
)
from google.cloud.functions_v1.types import ListFunctionsRequest


class GCPResourceType(Enum):
    Function = 0


@dataclass
class GCPResource:
    name: str
    description: str
    gcpResourceType: GCPResourceType

    @property
    def display_name(self) -> str:
        return self.name


class GCPResources(metaclass=ABCMeta):
    @property
    @abstractmethod
    def resources(self) -> List[GCPResource]:
        pass


class GCPFunctionResource(GCPResource):
    @property
    def display_name(self) -> str:
        return self.name.rsplit("/", 1)[1]


class FunctionsResources(GCPResources):
    def __init__(self, project: str) -> None:
        self.project = project
        self.list_functions_request = ListFunctionsRequest(
            parent=f"projects/{project}/locations/-"
        )

    @property
    def resources(self) -> List[GCPResource]:
        functions_list = CloudFunctionsServiceClient().list_functions(
            self.list_functions_request
        )
        return [
            GCPFunctionResource(
                name=f.name,
                description=f.description,
                gcpResourceType=GCPResourceType.Function,
            )
            for f in functions_list
        ]
