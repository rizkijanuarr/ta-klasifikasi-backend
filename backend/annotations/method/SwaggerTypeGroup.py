from enum import Enum
from typing import Dict, List

class SwaggerTypeGroup(Enum):
    DEFAULT = ("Default Endpoint", "Endpoint terbuka")
    APPS_WEB = ("App Web", "Hanya Untuk apps Web")
    APPS_MOBILE = ("App Mobile", "Hanya Untuk apps Mobile")

    def __new__(cls, value: str, description: str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        return obj

    def get_value(self) -> str:
        return self.value

    def get_description(self) -> str:
        return self.description

    @staticmethod
    def swagger_type_group_list_map_get_default() -> Dict['SwaggerTypeGroup', List[str]]:
        swagger_type_group_list_map = {}
        for group in SwaggerTypeGroup:
            swagger_type_group_list_map.setdefault(group, [])
        return swagger_type_group_list_map
