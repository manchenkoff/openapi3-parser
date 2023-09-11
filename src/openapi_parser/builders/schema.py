import logging
from typing import Any, Callable, Dict

from ..enumeration import DataType, IntegerFormat, NumberFormat, StringFormat
from ..errors import ParserError
from ..loose_types import LooseIntegerFormat, LooseNumberFormat, LooseStringFormat
from ..specification import (
    AnyOf,
    Array,
    Boolean,
    Discriminator,
    Integer,
    Null,
    Number,
    Object,
    OneOf,
    Property,
    Schema,
    String,
)
from .common import (
    PropertyMeta,
    extract_extension_attributes,
    extract_typed_props,
    merge_schema,
)

SchemaBuilderMethod = Callable[[dict], Schema]

ALL_OF_SCHEMAS_KEY = 'allOf'

logger = logging.getLogger(__name__)


def extract_attrs(data: dict, attrs_map: Dict[str, PropertyMeta]) -> Dict[str, Any]:
    """Extract attributes of schema description with specific type-casting mapping

    Args:
        data (dict): Source dictionary with schema data
        attrs_map (Dict[str, PropertyMeta]): Type-casting mapping

    Returns:
        Dict[str, Any]: Extracted dictionary with typed values
    """
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

    if attrs['extensions']:
        logger.debug(f"Extracted custom properties [{attrs['extensions'].keys()}]")

    return attrs


def merge_all_of_schemas(original_data: dict) -> dict:
    """Recursive merge schemas with 'allOf' type into single schema dictionary

    Args:
        original_data (dict): Dictionary with schema description

    Returns:
        dict: Merged dictionary of schema item
    """
    if ALL_OF_SCHEMAS_KEY not in original_data.keys():
        return original_data

    logger.debug(f"Merging 'allOf' schemas")

    schema_dict: dict = {}

    for nested_schema_dict in original_data[ALL_OF_SCHEMAS_KEY]:
        merged_nested_schema = merge_all_of_schemas(nested_schema_dict)
        schema_dict = merge_schema(schema_dict, merged_nested_schema)

    return schema_dict


class SchemaFactory:
    _builders: Dict[DataType, SchemaBuilderMethod]
    strict_enum: bool

    def __init__(self, strict_enum: bool = True) -> None:
        self.strict_enum = strict_enum
        self._builders = {
            DataType.NULL: self._null,
            DataType.INTEGER: self._integer,
            DataType.NUMBER: self._number,
            DataType.STRING: self._string,
            DataType.BOOLEAN: self._boolean,
            DataType.ARRAY: self._array,
            DataType.OBJECT: self._object,
            DataType.ONE_OF: self._one_of,
            DataType.ANY_OF: self._any_of,
        }

    def create(self, data: dict) -> Schema:
        data = merge_all_of_schemas(data)

        if 'oneOf' in data.keys():
            data['type'] = DataType.ONE_OF

        if 'anyOf' in data.keys():
            data['type'] = DataType.ANY_OF

        try:
            schema_type = data['type']
        except KeyError:
            logger.warning(msg="Implicit type assignment: schema does not contain 'type' property")
            schema_type = DataType.ANY_OF

        try:
            data_type = DataType(schema_type)
        except ValueError:
            raise ParserError(f"Invalid schema type '{schema_type}'") from None

        try:
            builder_func = self._builders[data_type]
        except KeyError:
            raise ParserError(f"Unsupported schema type: '{schema_type}'") from None

        logger.debug(f"Building schema [type={data_type}]")

        return builder_func(data)

    def _null(self, data: dict) -> Null:
        return Null(**extract_attrs(data, {}))

    def _integer(self, data: dict) -> Integer:
        format_cast = IntegerFormat if self.strict_enum else LooseIntegerFormat
        attrs_map = {
            "multiple_of": PropertyMeta(name="multipleOf", cast=int),
            "maximum": PropertyMeta(name="maximum", cast=int),
            "exclusive_maximum": PropertyMeta(name="exclusiveMaximum", cast=int),
            "minimum": PropertyMeta(name="minimum", cast=int),
            "exclusive_minimum": PropertyMeta(name="exclusiveMinimum", cast=int),
            "format": PropertyMeta(name="format", cast=format_cast),
        }

        return Integer(**extract_attrs(data, attrs_map))

    def _number(self, data: dict) -> Number:
        format_cast = NumberFormat if self.strict_enum else LooseNumberFormat
        attrs_map = {
            "multiple_of": PropertyMeta(name="multipleOf", cast=float),
            "maximum": PropertyMeta(name="maximum", cast=float),
            "exclusive_maximum": PropertyMeta(name="exclusiveMaximum", cast=float),
            "minimum": PropertyMeta(name="minimum", cast=float),
            "exclusive_minimum": PropertyMeta(name="exclusiveMinimum", cast=float),
            "format": PropertyMeta(name="format", cast=format_cast),
        }

        return Number(**extract_attrs(data, attrs_map))

    def _string(self, data: dict) -> String:
        format_cast = StringFormat if self.strict_enum else LooseStringFormat
        attrs_map = {
            "max_length": PropertyMeta(name="maxLength", cast=int),
            "min_length": PropertyMeta(name="minLength", cast=int),
            "pattern": PropertyMeta(name="pattern", cast=None),
            "format": PropertyMeta(name="format", cast=format_cast),
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

        return Array(**extract_attrs(data, attrs_map))

    def _object(self, data: dict) -> Object:
        def build_properties(object_attrs: dict) -> list[Property]:
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

        return Object(**extract_attrs(data, attrs_map))

    def _one_of(self, data: dict) -> OneOf:
        def create_inner_schemas(schemas: list) -> list[Schema]:
            return [self.create(x) for x in schemas]

        def build_discriminator(discriminator_data: dict) -> Discriminator:
            discriminator = Discriminator(property_name=discriminator_data['propertyName'])

            if 'mapping' in discriminator_data:
                discriminator.mapping = {
                    key: self.create(schema) for key, schema
                    in discriminator_data['mapping'].items()
                }

            return discriminator

        attrs_map = {
            "schemas": PropertyMeta(name="oneOf", cast=create_inner_schemas),
            "discriminator": PropertyMeta(name="discriminator", cast=build_discriminator),
        }

        return OneOf(**extract_attrs(data, attrs_map))

    def _any_of(self, data: dict) -> AnyOf:
        def create_inner_schemas(schemas:list) -> list[Schema]:
            return [self.create(x) for x in schemas]

        attrs_map = {
            "schemas": PropertyMeta(name="anyOf", cast=create_inner_schemas)
        }

        if "type" in data:
            return AnyOf(**extract_attrs(data, attrs_map))

        possible_implicit_types = (
            DataType.INTEGER, DataType.NUMBER, DataType.STRING, DataType.BOOLEAN, DataType.ARRAY, DataType.OBJECT
        )
        schemas = [
            schema_factory({**data, **{"type": data_type}}) 
            for data_type, schema_factory in self._builders.items()
            if data_type in possible_implicit_types
        ]

        return AnyOf(type=DataType.ANY_OF, schemas=schemas)


