from typing import List

from ..specification import Server


class ServerBuilder:
    @staticmethod
    def _build_server(server_info: dict) -> Server:
        data = {
            "url": server_info['url'],
            "description": server_info.get('description'),
            "variables": server_info.get('variables', {}),
        }

        return Server(**data)

    def build_server_list(self, server_data_list: list) -> List[Server]:
        return [self._build_server(item) for item in server_data_list]
