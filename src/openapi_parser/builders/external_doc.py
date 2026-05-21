"""External documentation builder."""

import logging
from typing import Any

from openapi_parser.builders.common import extract_extension_attributes
from openapi_parser.errors import ParserError
from openapi_parser.specification import ExternalDoc

logger = logging.getLogger(__name__)


class ExternalDocBuilder:
    """Builds external documentation objects."""

    @staticmethod
    def build(data: dict[str, Any]) -> ExternalDoc:
        """Build an ExternalDoc from a raw dict."""
        url = data.get("url")

        if url is None:
            raise ParserError(
                "External documentation is missing required 'url' property"
            )

        logger.debug(f"External doc parsing: {url}")

        attrs = {
            "url": url,
            "description": data.get("description"),
            "extensions": extract_extension_attributes(data),
        }

        if attrs["extensions"]:
            logger.debug(f"Extracted custom properties [{attrs['extensions'].keys()}]")

        return ExternalDoc(**attrs)
