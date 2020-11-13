from typing import List

from . import SchemaFactory
from .common import extract_typed_props, PropertyMeta
from ..enumeration import ParameterLocation
from ..specification import Parameter, ParameterList


class ParameterBuilder:
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build_collection(self, parameters: List[dict]) -> ParameterList:
        return [self.build(parameter) for parameter in parameters]

    def build(self, data: dict) -> Parameter:
        attrs_map = {
            "name": PropertyMeta(name="name", cast=str),
            "location": PropertyMeta(name="in", cast=ParameterLocation),
            "required": PropertyMeta(name="required", cast=None),
            "schema": PropertyMeta(name="schema", cast=self.schema_factory.create),
            "description": PropertyMeta(name="description", cast=str),
            "deprecated": PropertyMeta(name="deprecated", cast=None),
        }

        attrs = extract_typed_props(data, attrs_map)

        return Parameter(**attrs)
