from backend.controller.advices.BaseController import BaseController
from backend.annotations.method.GetEndpoint import GetEndpoint
from backend.annotations.method.SwaggerTypeGroup import SwaggerTypeGroup
from abc import ABC, abstractmethod

@BaseController(value="/api/v1/")
class HealthControllerV1(ABC):

    @GetEndpoint(
        value="/health",
        tagName="Health Check",
        description="Check API health",
        group=SwaggerTypeGroup.DEFAULT
    )
    @abstractmethod
    def health_check(self):
        pass
