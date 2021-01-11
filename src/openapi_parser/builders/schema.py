from typing import Any, Callable, Dict

from .common import extract_extension_attributes, extract_typed_props, merge_schema, PropertyMeta
from ..enumeration import DataType, IntegerFormat, NumberFormat, StringFormat
from ..errors import ParserError
from ..specification import Array, Boolean, Integer, Number, Object, Property, PropertyList, Schema, String

SchemaBuilderMethod = Callable[[dict], Schema]

ALL_OF_SCHEMAS_KEY = 'allOf'


def extract_attrs(data: dict, attrs_map: Dict[str, PropertyMeta]) -> Dict[str, Any]:
    base_attrs_map = {
        "type": "type",
        "title": "title",
        "enum": "enum",
        "example": "example",
        "description": "description",
        "default": "default",
        "nullable": "nullable",
        "read_only": "readOnly",
        "write_only": "writeOnly",
        "deprecated": "deprecated",
    }

    attrs = {
        key: data[name]
        for key, name in base_attrs_map.items()
        if data.get(name) is not None
    }

    attrs['type'] = DataType(attrs['type'])

    attrs.update(extract_typed_props(data, attrs_map))

    attrs['extensions'] = extract_extension_attributes(data)

    return attrs


def merge_all_of_schemas(original_data: dict) -> dict:
    if ALL_OF_SCHEMAS_KEY not in original_data.keys():
        return original_data

    schema_dict: dict = {}

    for nested_schema_dict in original_data[ALL_OF_SCHEMAS_KEY]:
        merged_nested_schema = merge_all_of_schemas(nested_schema_dict)
        schema_dict = merge_schema(schema_dict, merged_nested_schema)

    return schema_dict


class SchemaFactory:
    _builders: Dict[DataType, SchemaBuilderMethod]

    def __init__(self) -> None:
        self._builders = {
            DataType.INTEGER: self._integer,
            DataType.NUMBER: self._number,
            DataType.STRING: self._string,
            DataType.BOOLEAN: self._boolean,
            DataType.ARRAY: self._array,
            DataType.OBJECT: self._object,
        }

    def create(self, data: dict) -> Schema:
        data = merge_all_of_schemas(data)

        schema_type = data['type']

        try:
            data_type = DataType(schema_type)
        except ValueError:
            raise ParserError(f"Invalid schema type '{schema_type}'")

        try:
            builder_func = self._builders[data_type]
        except KeyError:
            raise ParserError(f"Unsupported schema type: '{schema_type}'")

        return builder_func(data)

    @staticmethod
    def _integer(data: dict) -> Integer:
        attrs_map = {
            "multiple_of": PropertyMeta(name="multipleOf", cast=int),
            "maximum": PropertyMeta(name="maximum", cast=int),
            "exclusive_maximum": PropertyMeta(name="exclusiveMaximum", cast=int),
            "minimum": PropertyMeta(name="minimum", cast=int),
            "exclusive_minimum": PropertyMeta(name="exclusiveMinimum", cast=int),
            "format": PropertyMeta(name="format", cast=IntegerFormat),
        }

        return Integer(**extract_attrs(data, attrs_map))

    @staticmethod
    def _number(data: dict) -> Number:
        attrs_map = {
            "multiple_of": PropertyMeta(name="multipleOf", cast=float),
            "maximum": PropertyMeta(name="maximum", cast=float),
            "exclusive_maximum": PropertyMeta(name="exclusiveMaximum", cast=float),
            "minimum": PropertyMeta(name="minimum", cast=float),
            "exclusive_minimum": PropertyMeta(name="exclusiveMinimum", cast=float),
            "format": PropertyMeta(name="format", cast=NumberFormat),
        }

        return Number(**extract_attrs(data, attrs_map))

    @staticmethod
    def _string(data: dict) -> String:
        attrs_map = {
            "max_length": PropertyMeta(name="maxLength", cast=int),
            "min_length": PropertyMeta(name="minLength", cast=int),
            "pattern": PropertyMeta(name="pattern", cast=None),
            "format": PropertyMeta(name="format", cast=StringFormat),
        }

        return String(**extract_attrs(data, attrs_map))

    @staticmethod
    def _boolean(data: dict) -> Boolean:
        return Boolean(**extract_attrs(data, {}))

    def _array(self, data: dict) -> Array:
        attrs_map = {
            "max_items": PropertyMeta(name="maxItems", cast=int),
            "min_items": PropertyMeta(name="minItems", cast=int),
            "unique_items": PropertyMeta(name="uniqueItems", cast=None),
            "items": PropertyMeta(name="items", cast=self.create),
        }

        attrs = extract_attrs(data, attrs_map)

        return Array(**attrs)

    def _object(self, data: dict) -> Object:
        def build_properties(object_attrs: dict) -> PropertyList:
            return [
                Property(name, self.create(schema))
                for name, schema in object_attrs.items()
            ]

        attrs_map = {
            "max_properties": PropertyMeta(name="maxProperties", cast=int),
            "min_properties": PropertyMeta(name="minProperties", cast=int),
            "required": PropertyMeta(name="required", cast=None),
            "properties": PropertyMeta(name="properties", cast=build_properties),
        }

        attrs = extract_attrs(data, attrs_map)

        return Object(**attrs)
