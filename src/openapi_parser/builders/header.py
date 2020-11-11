from . import SchemaFactory
from .common import extract_attrs_by_map, PropertyInfoType
from ..specification import Header, HeaderCollection


class HeaderBuilder:
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build(self, data: dict) -> Header:
        attrs_map = {
            "schema": PropertyInfoType(name="schema", type=self.schema_factory.create),
            "description": PropertyInfoType(name="description", type=str),
            "deprecated": PropertyInfoType(name="deprecated", type=None),
            "required": PropertyInfoType(name="required", type=None),
        }

        attrs = extract_attrs_by_map(data, attrs_map)

        return Header(**attrs)

    def build_collection(self, data: dict) -> HeaderCollection:
        return {
            header_name: self.build(header_value)
            for header_name, header_value in data.items()
        }
