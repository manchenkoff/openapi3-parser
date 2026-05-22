"""Link builder for response links."""

import logging
from typing import Any

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_extension_attributes,
    extract_typed_props,
)
from openapi_parser.specification import Link, Server

logger = logging.getLogger(__name__)


def build_server(value: dict[str, Any]) -> Server:
    """Build a Server object from raw data."""
    return Server(
        url=value["url"],
        description=value.get("description"),
    )


class LinkBuilder:
    """Builds link objects from raw specification data."""

    def build_dict(self, data: dict[str, dict[str, Any]]) -> dict[str, Link]:
        """Build a dict of links from a dict of raw link definitions."""
        return {
            link_name: self._build(link_data) for link_name, link_data in data.items()
        }

    def _build(self, data: dict[str, Any]) -> Link:
        logger.debug("Link building")

        attrs_map = {
            "operation_ref": PropertyMeta(name="operationRef", cast=str),
            "operation_id": PropertyMeta(name="operationId", cast=str),
            "parameters": PropertyMeta(name="parameters", cast=dict),
            "request_body": PropertyMeta(name="requestBody", cast=None),
            "description": PropertyMeta(name="description", cast=str),
            "server": PropertyMeta(name="server", cast=build_server),
        }

        attrs = extract_typed_props(data, attrs_map)
        attrs["extensions"] = extract_extension_attributes(data)

        if attrs["extensions"]:
            logger.debug(f"Extracted custom properties [{attrs['extensions'].keys()}]")

        return Link(**attrs)
