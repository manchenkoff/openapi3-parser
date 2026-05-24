"""Request body builder."""

import logging
from typing import Any

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_typed_props,
)
from openapi_parser.builders.content import ContentBuilder
from openapi_parser.logging import log_ctx
from openapi_parser.specification import RequestBody

logger = logging.getLogger(__name__)


class RequestBuilder:
    """Builds request body objects."""

    _content_builder: ContentBuilder

    def __init__(self, content_builder: ContentBuilder) -> None:
        """Initialize request builder.

        Args:
            content_builder: Builder for content objects
        """
        self._content_builder = content_builder

    def build(self, data: dict[str, Any]) -> RequestBody:
        """Build a RequestBody from a raw dict."""
        with log_ctx("requestBody"):
            logger.debug("Request building")

            attrs_map = {
                "content": PropertyMeta(
                    name="content",
                    cast=self._content_builder.build_list,
                ),
                "description": PropertyMeta(name="description", cast=str),
                "required": PropertyMeta(name="required", cast=bool),
            }

            attrs = extract_typed_props(data, attrs_map)

            return RequestBody(**attrs)
