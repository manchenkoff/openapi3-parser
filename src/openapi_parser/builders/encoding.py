"""Encoding builder for request body property encodings."""

import logging
from typing import Any

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_extension_attributes,
    extract_typed_props,
)
from openapi_parser.builders.header import HeaderBuilder
from openapi_parser.logging import log_ctx
from openapi_parser.specification import Encoding

logger = logging.getLogger(__name__)


class EncodingBuilder:
    """Builds encoding objects from raw specification data."""

    _header_builder: HeaderBuilder

    def __init__(self, header_builder: HeaderBuilder) -> None:
        """Initialize encoding builder.

        Args:
            header_builder: Builder for header objects
        """
        self._header_builder = header_builder

    def build_dict(
        self,
        data: dict[str, dict[str, Any]],
    ) -> dict[str, Encoding]:
        """Build a dict of encodings from a dict of raw encoding definitions."""
        result: dict[str, Encoding] = {}

        for property_name, encoding_data in data.items():
            with log_ctx("encoding", property_name):
                result[property_name] = self._build(encoding_data)

        return result

    def _build(self, data: dict[str, Any]) -> Encoding:
        logger.debug("Encoding building")

        attrs_map = {
            "content_type": PropertyMeta(name="contentType", cast=str),
            "headers": PropertyMeta(
                name="headers",
                cast=self._header_builder.build_list,
            ),
            "style": PropertyMeta(name="style", cast=str),
            "explode": PropertyMeta(name="explode", cast=bool),
            "allow_reserved": PropertyMeta(name="allowReserved", cast=bool),
        }

        attrs = extract_typed_props(data, attrs_map)
        attrs["extensions"] = extract_extension_attributes(data)

        if attrs["extensions"]:
            logger.debug(f"Extracted custom properties [{attrs['extensions'].keys()}]")

        return Encoding(**attrs)
