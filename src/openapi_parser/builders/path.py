from typing import Dict

from ..specification import Path, PathItem, PathList

KeyValueDict = Dict[str, dict]


class PathBuilder:
    @staticmethod
    def _create_path_item(operations: KeyValueDict) -> PathItem:
        attrs = {
            "summary": operations.get('summary'),
            "description": operations.get('description'),
            "operations": {},  # TODO: parse (dependency - OperationBuilder -> ExternalDocBuilder, RequestBuilder, ResponseBuilder, ParameterBuilder, SecurityBuilder)
            "parameters": [],  # TODO: parse (dependency - ParameterBuilder -> SchemaBuilder)
        }

        return PathItem(**attrs)

    def build(self, url: str, operations: KeyValueDict) -> Path:
        return Path(url, self._create_path_item(operations))

    def build_list(self, data: KeyValueDict) -> PathList:
        if data is None:
            return []

        return [self.build(url, operations) for url, operations in data.items()]
