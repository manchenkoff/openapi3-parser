from . import SchemaFactory
from .common import extract_typed_props, PropertyMeta
from ..specification import Header, HeaderCollection


class HeaderBuilder:
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build_collection(self, data: dict) -> HeaderCollection:
        return {
            header_name: self.build(header_value)
            for header_name, header_value in data.items()
        }

    def build(self, data: dict) -> Header:
        attrs_map = {
            "schema": PropertyMeta(name="schema", cast=self.schema_factory.create),
            "description": PropertyMeta(name="description", cast=str),
            "deprecated": PropertyMeta(name="deprecated", cast=None),
            "required": PropertyMeta(name="required", cast=None),
        }

        attrs = extract_typed_props(data, attrs_map)

        return Header(**attrs)
