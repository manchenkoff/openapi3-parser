"""Content builder for OpenAPI request/response bodies."""

import logging
from typing import Any

from openapi_parser.builders.encoding import EncodingBuilder
from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import ContentType
from openapi_parser.loose_types import LooseContentType
from openapi_parser.specification import Content

logger = logging.getLogger(__name__)

ContentTypeType = type[ContentType] | type[LooseContentType]


class ContentBuilder:
    """Builds content objects for request/response bodies."""

    _schema_factory: SchemaFactory
    _encoding_builder: EncodingBuilder
    _strict_enum: bool

    def __init__(
        self,
        schema_factory: SchemaFactory,
        encoding_builder: EncodingBuilder,
        strict_enum: bool = True,
    ) -> None:
        """Initialize content builder.

        Args:
            schema_factory: Factory for creating schema objects
            encoding_builder: Builder for encoding objects
            strict_enum: Whether to validate enums strictly
        """
        self._schema_factory = schema_factory
        self._encoding_builder = encoding_builder
        self._strict_enum = strict_enum

    def build_list(self, data: dict[str, Any]) -> list[Content]:
        """Build a list of content objects from a dict of media types."""
        return [
            self._create_content(
                content_type,
                content_value,
            )
            for content_type, content_value in data.items()
        ]

    def _create_content(
        self,
        content_type: str,
        content_value: dict[str, Any],
    ) -> Content:
        logger.debug(f"Content building [type={content_type}]")

        ContentTypeCls: ContentTypeType = (
            ContentType if self._strict_enum else LooseContentType
        )

        encoding = (
            self._encoding_builder.build_dict(content_value["encoding"])
            if content_value.get("encoding")
            else None
        )

        return Content(
            type=ContentTypeCls(content_type),
            schema=self._schema_factory.create(content_value.get("schema", {})),
            example=content_value.get("example"),
            examples=content_value.get("examples", {}),
            encoding=encoding,
        )
