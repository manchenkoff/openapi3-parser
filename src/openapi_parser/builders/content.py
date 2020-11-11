from . import SchemaFactory
from ..enumeration import MediaType
from ..specification import Content, ContentType


class ContentBuilder:
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build_collection(self, data: dict) -> ContentType:
        return {
            MediaType(content_type): self.build(content_value)
            for content_type, content_value in data.items()
        }

    def build(self, data: dict) -> Content:
        return Content(schema=self.schema_factory.create(data['schema']))
