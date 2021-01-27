import logging
from typing import Dict

from . import OperationBuilder, ParameterBuilder
from .common import extract_typed_props, PropertyMeta
from ..enumeration import OperationMethod
from ..specification import Path

logger = logging.getLogger(__name__)


class PathBuilder:
    operation_builder: OperationBuilder
    parameter_builder: ParameterBuilder

    def __init__(self, operation_builder: OperationBuilder, parameter_builder: ParameterBuilder) -> None:
        self.operation_builder = operation_builder
        self.parameter_builder = parameter_builder

    def build_list(self, data: Dict[str, dict]) -> list[Path]:
        return [
            self._build_path(url, path)
            for url, path in data.items()
        ]

    def _build_path(self, url: str, data: dict) -> Path:
        logger.info(f"Path item parsing [url={url}]")

        attrs_map = {
            "summary": PropertyMeta(name="summary", cast=str),
            "description": PropertyMeta(name="description", cast=str),
            "parameters": PropertyMeta(name="parameters", cast=self.parameter_builder.build_list),
        }

        attrs = extract_typed_props(data, attrs_map)

        attrs['url'] = url

        attrs["operations"] = [
            self.operation_builder.build(method, data[method.value])
            for method in OperationMethod
            if method.value in data
        ]

        return Path(**attrs)
