"""Info section builder for OpenAPI metadata."""

import logging
from typing import Any

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_extension_attributes,
    extract_typed_props,
)
from openapi_parser.errors import ParserError
from openapi_parser.specification import Contact, Info, License

logger = logging.getLogger(__name__)


class InfoBuilder:
    """Builds Info, Contact, and License objects."""

    def build(self, data: dict[str, Any]) -> Info:
        """Build an Info object from a raw dict."""
        title = data.get("title")

        if title is None:
            raise ParserError("Info section is missing required 'title' property")

        logger.debug(f"Info section parsing [title={title}]")

        attrs_map = {
            "title": PropertyMeta(name="title", cast=str),
            "version": PropertyMeta(name="version", cast=str),
            "description": PropertyMeta(name="description", cast=str),
            "terms_of_service": PropertyMeta(name="termsOfService", cast=str),
            "license": PropertyMeta(name="license", cast=self._create_license),
            "contact": PropertyMeta(name="contact", cast=self._create_contact),
        }

        attrs = extract_typed_props(data, attrs_map)
        attrs["extensions"] = extract_extension_attributes(data)

        if attrs["extensions"]:
            logger.debug(f"Extracted custom properties [{attrs['extensions'].keys()}]")

        return Info(**attrs)

    @staticmethod
    def _create_license(data: dict[str, Any]) -> License:
        name = data.get("name")

        if name is None:
            raise ParserError("License section is missing required 'name' property")

        attrs = {
            "name": name,
            "url": data.get("url"),
        }

        return License(**attrs)

    @staticmethod
    def _create_contact(data: dict[str, Any]) -> Contact:
        attrs = {
            "name": data.get("name"),
            "url": data.get("url"),
            "email": data.get("email"),
        }

        return Contact(**attrs)
