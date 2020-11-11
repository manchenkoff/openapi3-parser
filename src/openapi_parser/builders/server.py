from .common import PropertyMeta, extract_typed_props
from ..specification import Server, ServerList


class ServerBuilder:
    def build_list(self, data_list: list) -> ServerList:
        return [self._build_server(item) for item in data_list]

    @staticmethod
    def _build_server(data: dict) -> Server:
        attrs_map = {
            "url": PropertyMeta(name="url", cast=str),
            "description": PropertyMeta(name="description", cast=str),
            "variables": PropertyMeta(name="variables", cast=None),
        }

        attrs = extract_typed_props(data, attrs_map)

        return Server(**attrs)
