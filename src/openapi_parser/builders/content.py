import logging
from typing import Type, Union, Any

from .schema import SchemaFactory
from ..enumeration import ContentType
from ..loose_types import LooseContentType
from ..specification import Content

logger = logging.getLogger(__name__)

ContentTypeType = Union[Type[ContentType], Type[LooseContentType]]


class ContentBuilder:
    schema_factory: SchemaFactory
    strict_enum: bool

    def __init__(self, schema_factory: SchemaFactory, strict_enum: bool = True) -> None:
        self.schema_factory = schema_factory
        self.strict_enum = strict_enum

    def build_list(self, data: dict) -> list[Content]:
        return [
            self._create_content(content_type, content_value.get('schema', {}),
                                 content_value.get('example', None),
                                 content_value.get('examples', {}))
            for content_type, content_value
            in data.items()
        ]

    def _create_content(self, content_type: str, schema: dict, example: Any, examples: dict) -> Content:
        logger.debug(f"Content building [type={content_type}]")
        ContentTypeCls: ContentTypeType = ContentType if self.strict_enum else LooseContentType
        return Content(
            type=ContentTypeCls(content_type),
            schema=self.schema_factory.create(schema),
            example=example,
            examples=examples
        )
