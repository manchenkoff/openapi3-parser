"""Header builder for response headers."""

import logging
from typing import Any

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_extension_attributes,
    extract_typed_props,
)
from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.specification import Header

logger = logging.getLogger(__name__)


class HeaderBuilder:
    """Builds header objects from raw specification data."""

    _schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        """Initialize header builder.

        Args:
            schema_factory: Factory for creating schema objects
        """
        self._schema_factory = schema_factory

    def build_list(self, data: dict[str, Any]) -> list[Header]:
        """Build a list of headers from a dict of header definitions."""
        return [
            self._build(header_name, header_value)
            for header_name, header_value in data.items()
        ]

    def _build(self, name: str, data: dict[str, Any]) -> Header:
        logger.debug(f"Header parsing: {name}")

        attrs_map = {
            "schema": PropertyMeta(name="schema", cast=self._schema_factory.create),
            "description": PropertyMeta(name="description", cast=str),
            "deprecated": PropertyMeta(name="deprecated", cast=bool),
            "required": PropertyMeta(name="required", cast=bool),
        }

        attrs = extract_typed_props(data, attrs_map)

        attrs["name"] = name
        attrs["extensions"] = extract_extension_attributes(data)

        if attrs["extensions"]:
            logger.debug(f"Extracted custom properties [{attrs['extensions'].keys()}]")

        return Header(**attrs)
