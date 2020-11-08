from typing import Optional

from ..specification import Server, ServerList


class ServerBuilder:
    @staticmethod
    def _build_server(data: dict) -> Server:
        attrs = {
            "url": data['url'],
            "description": data.get('description'),
            "variables": data.get('variables', {}),
        }

        return Server(**attrs)

    def build_list(self, data_list: Optional[list]) -> ServerList:
        if data_list is None:
            return []

        return [self._build_server(item) for item in data_list]
