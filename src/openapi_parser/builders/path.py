"""Path builder for API endpoint paths."""

import logging
from typing import Any

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_extension_attributes,
    extract_typed_props,
)
from openapi_parser.builders.operation import OperationBuilder
from openapi_parser.builders.parameter import ParameterBuilder
from openapi_parser.enumeration import OperationMethod
from openapi_parser.logging import log_ctx
from openapi_parser.specification import Path

logger = logging.getLogger(__name__)


class PathBuilder:
    """Builds path objects from raw specification data."""

    _operation_builder: OperationBuilder
    _parameter_builder: ParameterBuilder

    def __init__(
        self,
        operation_builder: OperationBuilder,
        parameter_builder: ParameterBuilder,
    ) -> None:
        """Initialize path builder.

        Args:
            operation_builder: Builder for operation objects
            parameter_builder: Builder for parameter objects
        """
        self._operation_builder = operation_builder
        self._parameter_builder = parameter_builder

    def build_list(
        self,
        data: dict[str, dict[str, Any]],
    ) -> list[Path]:
        """Build a list of paths from a raw dict of path definitions."""
        return [self._build_path(url, path) for url, path in data.items()]

    def _build_path(self, url: str, data: dict[str, Any]) -> Path:
        with log_ctx("paths", url):
            logger.info(f"Path item parsing [url={url}]")

            attrs_map = {
                "summary": PropertyMeta(name="summary", cast=str),
                "description": PropertyMeta(name="description", cast=str),
                "parameters": PropertyMeta(
                    name="parameters",
                    cast=self._parameter_builder.build_list,
                ),
            }

            attrs = extract_typed_props(data, attrs_map)

            attrs["url"] = url

            attrs["operations"] = [
                self._operation_builder.build(
                    method,
                    data[method.value],
                )
                for method in OperationMethod
                if method.value in data
            ]

            if attrs.get("parameters"):
                for operation in attrs["operations"]:
                    merged = operation.parameters + attrs["parameters"]
                    object.__setattr__(operation, "parameters", merged)

            attrs["extensions"] = extract_extension_attributes(data)

            if attrs["extensions"]:
                logger.debug(
                    f"Extracted custom properties [{attrs['extensions'].keys()}]"
                )

            return Path(**attrs)
