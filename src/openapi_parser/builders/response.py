"""Response builder for API responses."""

import logging
from typing import Any

from openapi_parser.builders.common import PropertyMeta, extract_typed_props
from openapi_parser.builders.content import ContentBuilder
from openapi_parser.builders.header import HeaderBuilder
from openapi_parser.builders.link import LinkBuilder
from openapi_parser.specification import Response

logger = logging.getLogger(__name__)


class ResponseBuilder:
    """Builds response objects from raw specification data."""

    _content_builder: ContentBuilder
    _header_builder: HeaderBuilder
    _link_builder: LinkBuilder

    def __init__(
        self,
        content_builder: ContentBuilder,
        header_builder: HeaderBuilder,
        link_builder: LinkBuilder,
    ) -> None:
        """Initialize response builder.

        Args:
            content_builder: Builder for content objects
            header_builder: Builder for header objects
            link_builder: Builder for link objects
        """
        self._content_builder = content_builder
        self._header_builder = header_builder
        self._link_builder = link_builder

    def build(self, code: int | str, data: dict[str, Any]) -> Response:
        """Build a Response from a status code and raw data dict."""
        logger.debug(f"Response building [code={code}]")

        attrs_map = {
            "description": PropertyMeta(name="description", cast=str),
            "content": PropertyMeta(
                name="content",
                cast=self._content_builder.build_list,
            ),
            "headers": PropertyMeta(
                name="headers",
                cast=self._header_builder.build_list,
            ),
            "links": PropertyMeta(
                name="links",
                cast=self._link_builder.build_dict,
            ),
        }

        attrs = extract_typed_props(data, attrs_map)

        attrs["is_default"] = code == "default"

        try:
            attrs["code"] = int(code)
        except ValueError:
            logger.debug(f"Response code is not an integer [code={code}]")

        return Response(**attrs)
