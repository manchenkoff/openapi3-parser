from typing import Any, Dict

from . import SchemaFactory
from ..specification import Header


class HeaderBuilder:
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build(self, data: dict) -> Header:
        attrs: Dict[str, Any]

        attrs = {
            "schema": self.schema_factory.create(data['schema']),
        }

        if data.get("description") is not None:
            attrs["description"] = data["description"]

        if data.get("deprecated") is not None:
            attrs["deprecated"] = data["deprecated"]

        if data.get("required") is not None:
            attrs["required"] = data["required"]

        return Header(**attrs)
