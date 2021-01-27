import logging

from . import SchemaFactory
from ..enumeration import ContentType
from ..specification import Content

logger = logging.getLogger(__name__)


class ContentBuilder:
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build_list(self, data: dict) -> list[Content]:
        return [
            self._create_content(content_type, content_value['schema'])
            for content_type, content_value
            in data.items()
        ]

    def _create_content(self, content_type: str, content_value: dict) -> Content:
        logger.debug(f"Content building [type={content_type}]")

        return Content(
            type=ContentType(content_type),
            schema=self.schema_factory.create(content_value)
        )
