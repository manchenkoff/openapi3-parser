from collections import namedtuple
from typing import Any, Callable, Dict, Optional

from ..enumeration import DataType, IntegerFormat, NumberFormat, StringFormat
from ..errors import ParserError
from ..specification import Array, Integer, Number, Object, Property, Schema, String

SchemaBuilderMethod = Callable[[dict], Schema]

PropertyInfoType = namedtuple('PropertyInfoType', ['type', 'name'])


def get_common_attrs(data: dict) -> dict:
    attrs_map = {
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
        for key, name in attrs_map.items()
        if data.get(name) is not None
    }

    attrs['type'] = DataType(attrs['type'])

    return attrs


def get_custom_attrs(data: dict, attrs_map: Dict[str, PropertyInfoType]) -> Dict[str, Any]:
    def cast_value(name: str, value: Any, value_type: Optional[type]) -> Any:
        if not value_type:
            return value

        try:
            return value_type(value)
        except ValueError:
            raise ParserError(f"Invalid '{name}' property value for type: {value_type}")

    custom_attrs = {
        attr_name: cast_value(attr_info.name, data[attr_info.name], attr_info.type)
        for attr_name, attr_info in attrs_map.items()
        if data.get(attr_info.name) is not None
    }

    return custom_attrs


def extract_attrs(data: dict, attrs_map: Dict[str, PropertyInfoType]) -> Dict[str, Any]:
    attrs = get_common_attrs(data)
    attrs.update(get_custom_attrs(data, attrs_map))

    return attrs


class SchemaFactory:
    _builders: Dict[DataType, SchemaBuilderMethod]

    def __init__(self) -> None:
        self._builders = {
            DataType.INTEGER: self._integer,
            DataType.NUMBER: self._number,
            DataType.STRING: self._string,
            DataType.ARRAY: self._array,
            DataType.OBJECT: self._object,
        }

    def create(self, data: dict) -> Schema:
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
            "multiple_of": PropertyInfoType(name="multipleOf", type=int),
            "maximum": PropertyInfoType(name="maximum", type=int),
            "exclusive_maximum": PropertyInfoType(name="exclusiveMaximum", type=int),
            "minimum": PropertyInfoType(name="minimum", type=int),
            "exclusive_minimum": PropertyInfoType(name="exclusiveMinimum", type=int),
            "format": PropertyInfoType(name="format", type=IntegerFormat),
        }

        return Integer(**extract_attrs(data, attrs_map))

    @staticmethod
    def _number(data: dict) -> Number:
        attrs_map = {
            "multiple_of": PropertyInfoType(name="multipleOf", type=float),
            "maximum": PropertyInfoType(name="maximum", type=float),
            "exclusive_maximum": PropertyInfoType(name="exclusiveMaximum", type=float),
            "minimum": PropertyInfoType(name="minimum", type=float),
            "exclusive_minimum": PropertyInfoType(name="exclusiveMinimum", type=float),
            "format": PropertyInfoType(name="format", type=NumberFormat),
        }

        return Number(**extract_attrs(data, attrs_map))

    @staticmethod
    def _string(data: dict) -> String:
        attrs_map = {
            "max_length": PropertyInfoType(name="maxLength", type=int),
            "min_length": PropertyInfoType(name="minLength", type=int),
            "pattern": PropertyInfoType(name="pattern", type=None),
            "format": PropertyInfoType(name="format", type=StringFormat),
        }

        return String(**extract_attrs(data, attrs_map))

    def _array(self, data: dict) -> Array:
        attrs_map = {
            "max_items": PropertyInfoType(name="maxItems", type=int),
            "min_items": PropertyInfoType(name="minItems", type=int),
            "unique_items": PropertyInfoType(name="uniqueItems", type=None),
            "items": PropertyInfoType(name="items", type=None),
        }

        attrs = extract_attrs(data, attrs_map)

        try:
            attrs['items'] = self.create(attrs['items'])
        except KeyError:
            raise ParserError("Arrays must contain 'items' definition")

        return Array(**attrs)

    def _object(self, data: dict) -> Object:
        def build_parameters(object_attrs: dict) -> None:
            if not object_attrs.get('properties'):
                return

            object_attrs['properties'] = [
                Property(name, self.create(schema))
                for name, schema in object_attrs['properties'].items()
            ]

        attrs_map = {
            "max_properties": PropertyInfoType(name="maxProperties", type=int),
            "min_properties": PropertyInfoType(name="minProperties", type=int),
            "required": PropertyInfoType(name="required", type=None),
            "properties": PropertyInfoType(name="properties", type=None),
        }

        attrs = extract_attrs(data, attrs_map)
        build_parameters(attrs)

        return Object(**attrs)
