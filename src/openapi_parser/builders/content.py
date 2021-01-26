from . import SchemaFactory
from ..enumeration import ContentType
from ..specification import Content


class ContentBuilder:
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build_list(self, data: dict) -> list[Content]:
        return [
            Content(
                type=ContentType(content_type),
                schema=self.schema_factory.create(content_value['schema'])
            )
            for content_type, content_value
            in data.items()
        ]
