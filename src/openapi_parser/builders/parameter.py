from typing import List

from . import SchemaFactory
from .common import extract_attrs_by_map, PropertyInfoType
from ..enumeration import ParameterLocation
from ..specification import Parameter, ParameterList


class ParameterBuilder:
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build(self, data: dict) -> Parameter:
        attrs_map = {
            "name": PropertyInfoType(name="name", type=str),
            "location": PropertyInfoType(name="in", type=ParameterLocation),
            "required": PropertyInfoType(name="required", type=None),
            "schema": PropertyInfoType(name="schema", type=self.schema_factory.create),
            "description": PropertyInfoType(name="description", type=str),
            "deprecated": PropertyInfoType(name="deprecated", type=None),
        }

        attrs = extract_attrs_by_map(data, attrs_map)

        return Parameter(**attrs)

    def build_collection(self, parameters: List[dict]) -> ParameterList:
        return [self.build(parameter) for parameter in parameters]
