from .common import PropertyInfoType, extract_attrs_by_map
from ..specification import Server, ServerList


class ServerBuilder:
    @staticmethod
    def _build_server(data: dict) -> Server:
        attrs_map = {
            "url": PropertyInfoType(name="url", type=str),
            "description": PropertyInfoType(name="description", type=str),
            "variables": PropertyInfoType(name="variables", type=None),
        }

        attrs = extract_attrs_by_map(data, attrs_map)

        return Server(**attrs)

    def build_list(self, data_list: list) -> ServerList:
        return [self._build_server(item) for item in data_list]
