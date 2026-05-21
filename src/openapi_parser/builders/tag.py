"""Tag builder for API tag definitions."""

import logging
from typing import Any

from openapi_parser.builders.common import PropertyMeta, extract_typed_props
from openapi_parser.builders.external_doc import ExternalDocBuilder
from openapi_parser.errors import ParserError
from openapi_parser.specification import Tag

logger = logging.getLogger(__name__)


class TagBuilder:
    """Builds tag objects from raw specification data."""

    _external_doc_builder: ExternalDocBuilder

    def __init__(self, external_doc_builder: ExternalDocBuilder) -> None:
        """Initialize tag builder.

        Args:
            external_doc_builder: Builder for external docs
        """
        self._external_doc_builder = external_doc_builder

    def build_list(self, data_list: list[dict[str, Any]]) -> list[Tag]:
        """Build a list of Tag objects from a list of raw dicts."""
        return [self._build_tag(item) for item in data_list]

    def _build_tag(self, data: dict[str, Any]) -> Tag:
        name = data.get("name")

        if name is None:
            raise ParserError("Tag is missing required 'name' property")

        logger.debug(f"Tag building [{name}]")

        attrs_map = {
            "name": PropertyMeta(name="name", cast=str),
            "description": PropertyMeta(name="description", cast=str),
            "external_docs": PropertyMeta(
                name="externalDocs",
                cast=self._external_doc_builder.build,
            ),
        }

        attrs = extract_typed_props(data, attrs_map)

        return Tag(**attrs)
