"""Server builder for API server definitions."""

import logging
from typing import Any

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_extension_attributes,
    extract_typed_props,
)
from openapi_parser.errors import ParserError
from openapi_parser.specification import Server

logger = logging.getLogger(__name__)


class ServerBuilder:
    """Builds server objects from raw specification data."""

    def build_list(self, data_list: list[dict[str, Any]]) -> list[Server]:
        """Build a list of Server objects from a list of raw dicts."""
        return [self._build_server(item) for item in data_list]

    @staticmethod
    def _build_server(data: dict[str, Any]) -> Server:
        url = data.get("url")

        if url is None:
            raise ParserError("Server definition is missing required 'url' property")

        logger.debug(f"Server item parsing [{url}]")

        attrs_map = {
            "url": PropertyMeta(name="url", cast=str),
            "description": PropertyMeta(name="description", cast=str),
            "variables": PropertyMeta(name="variables", cast=dict),
        }

        attrs = extract_typed_props(data, attrs_map)
        attrs["extensions"] = extract_extension_attributes(data)

        if attrs["extensions"]:
            logger.debug(f"Extracted custom properties [{attrs['extensions'].keys()}]")

        return Server(**attrs)
