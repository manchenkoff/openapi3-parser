from typing import Dict

from . import OperationBuilder, ParameterBuilder
from .common import extract_typed_props, PropertyMeta
from ..enumeration import OperationMethod
from ..specification import Path, PathItem, PathList


class PathBuilder:
    operation_builder: OperationBuilder
    parameter_builder: ParameterBuilder

    def __init__(self, operation_builder: OperationBuilder, parameter_builder: ParameterBuilder) -> None:
        self.operation_builder = operation_builder
        self.parameter_builder = parameter_builder

    def build_collection(self, data: Dict[str, dict]) -> PathList:
        return [
            Path(url, self._build_path_item(path))
            for url, path in data.items()
        ]

    def _build_path_item(self, data: dict) -> PathItem:
        attrs_map = {
            "summary": PropertyMeta(name="summary", cast=str),
            "description": PropertyMeta(name="description", cast=str),
            "parameters": PropertyMeta(name="parameters", cast=self.parameter_builder.build_collection),
        }

        attrs = extract_typed_props(data, attrs_map)

        attrs["operations"] = {
            method: self.operation_builder.build(data[method.value])
            for method in OperationMethod
            if method.value in data
        }

        return PathItem(**attrs)
