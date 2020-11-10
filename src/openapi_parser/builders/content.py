from typing import Any, Dict

from . import SchemaFactory
from ..specification import Content


class ContentBuilder:
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build(self, data: dict) -> Content:
        attrs: Dict[str, Any]

        attrs = {
            "schema": self.schema_factory.create(data['schema']),
        }

        return Content(**attrs)
