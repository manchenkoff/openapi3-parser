from . import SchemaFactory
from ..enumeration import ParameterLocation
from ..specification import Parameter


class ParameterBuilder:
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build(self, data: dict) -> Parameter:
        attrs = {
            "name": data["name"],
            "location": ParameterLocation(data["in"]),
            "required": data["required"],
            "schema": self.schema_factory.create(data['schema']),
        }

        if data.get("description") is not None:
            attrs["description"] = data["description"]

        if data.get("deprecated") is not None:
            attrs["deprecated"] = data["deprecated"]

        return Parameter(**attrs)
