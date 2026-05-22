"""Schema builder for type-casting and schema creation."""

import logging
from collections.abc import Callable
from typing import Any

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_extension_attributes,
    extract_typed_props,
    merge_schema,
)
from openapi_parser.enumeration import (
    DataType,
    IntegerFormat,
    NumberFormat,
    StringFormat,
)
from openapi_parser.errors import ParserError
from openapi_parser.loose_types import (
    LooseIntegerFormat,
    LooseNumberFormat,
    LooseStringFormat,
)
from openapi_parser.specification import (
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

SchemaBuilderMethod = Callable[[dict[str, Any]], Schema]

ALL_OF_SCHEMAS_KEY = "allOf"

logger = logging.getLogger(__name__)


def extract_attrs(
    data: dict[str, Any],
    attrs_map: dict[str, PropertyMeta],
) -> dict[str, Any]:
    """Extract attributes of schema description with specific type-casting mapping.

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

    attrs["type"] = DataType(attrs["type"])

    attrs.update(extract_typed_props(data, attrs_map))

    attrs["extensions"] = extract_extension_attributes(data)

    if attrs["extensions"]:
        logger.debug(f"Extracted custom properties [{attrs['extensions'].keys()}]")

    return attrs


def merge_all_of_schemas(original_data: dict[str, Any]) -> dict[str, Any]:
    """Recursive merge schemas with 'allOf' type into single schema dictionary.

    Args:
        original_data (dict): Dictionary with schema description

    Returns:
        dict: Merged dictionary of schema item
    """
    if ALL_OF_SCHEMAS_KEY not in original_data:
        return original_data

    logger.debug("Merging 'allOf' schemas")

    schema_dict: dict[str, Any] = {}

    for nested_schema_dict in original_data[ALL_OF_SCHEMAS_KEY]:
        merged_nested_schema = merge_all_of_schemas(nested_schema_dict)
        schema_dict = merge_schema(schema_dict, merged_nested_schema)

    return schema_dict


class SchemaFactory:
    """Factory for creating schema objects from raw dicts."""

    _builders: dict[DataType, SchemaBuilderMethod]
    _strict_enum: bool

    def __init__(self, strict_enum: bool = True) -> None:
        """Initialize schema factory.

        Args:
            strict_enum: Whether to validate enums strictly
        """
        self._strict_enum = strict_enum
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

    def create(self, data: dict[str, Any]) -> Schema:
        """Create a schema object from a raw dict."""
        data = merge_all_of_schemas(data)

        if "oneOf" in data:
            data["type"] = DataType.ONE_OF

        if "anyOf" in data:
            data["type"] = DataType.ANY_OF

        try:
            schema_type = data["type"]
        except KeyError:
            logger.warning(
                msg="Implicit type assignment: schema does not contain 'type' property",
            )
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

    def _null(self, data: dict[str, Any]) -> Null:
        return Null(**extract_attrs(data, {}))

    def _integer(self, data: dict[str, Any]) -> Integer:
        format_cast = IntegerFormat if self._strict_enum else LooseIntegerFormat

        attrs_map = {
            "multiple_of": PropertyMeta(name="multipleOf", cast=int),
            "maximum": PropertyMeta(name="maximum", cast=int),
            "exclusive_maximum": PropertyMeta(name="exclusiveMaximum", cast=int),
            "minimum": PropertyMeta(name="minimum", cast=int),
            "exclusive_minimum": PropertyMeta(name="exclusiveMinimum", cast=int),
            "format": PropertyMeta(name="format", cast=format_cast),
        }

        return Integer(**extract_attrs(data, attrs_map))

    def _number(self, data: dict[str, Any]) -> Number:
        format_cast = NumberFormat if self._strict_enum else LooseNumberFormat

        attrs_map = {
            "multiple_of": PropertyMeta(name="multipleOf", cast=float),
            "maximum": PropertyMeta(name="maximum", cast=float),
            "exclusive_maximum": PropertyMeta(name="exclusiveMaximum", cast=float),
            "minimum": PropertyMeta(name="minimum", cast=float),
            "exclusive_minimum": PropertyMeta(name="exclusiveMinimum", cast=float),
            "format": PropertyMeta(name="format", cast=format_cast),
        }

        return Number(**extract_attrs(data, attrs_map))

    def _string(self, data: dict[str, Any]) -> String:
        format_cast = StringFormat if self._strict_enum else LooseStringFormat

        attrs_map = {
            "max_length": PropertyMeta(name="maxLength", cast=int),
            "min_length": PropertyMeta(name="minLength", cast=int),
            "pattern": PropertyMeta(name="pattern", cast=str),
            "format": PropertyMeta(name="format", cast=format_cast),
        }

        return String(**extract_attrs(data, attrs_map))

    @staticmethod
    def _boolean(data: dict[str, Any]) -> Boolean:
        return Boolean(**extract_attrs(data, {}))

    def _array(self, data: dict[str, Any]) -> Array:
        attrs_map = {
            "max_items": PropertyMeta(name="maxItems", cast=int),
            "min_items": PropertyMeta(name="minItems", cast=int),
            "unique_items": PropertyMeta(name="uniqueItems", cast=bool),
            "items": PropertyMeta(name="items", cast=self.create),
        }

        return Array(**extract_attrs(data, attrs_map))

    def _object(self, data: dict[str, Any]) -> Object:
        def build_properties(object_attrs: dict[str, Any]) -> list[Property]:
            return [
                Property(name, self.create(schema))
                for name, schema in object_attrs.items()
            ]

        def build_additional_properties(
            value: bool | dict[str, Any],
        ) -> bool | Schema:
            if isinstance(value, bool):
                return value
            return self.create(value)

        attrs_map = {
            "max_properties": PropertyMeta(name="maxProperties", cast=int),
            "min_properties": PropertyMeta(name="minProperties", cast=int),
            "required": PropertyMeta(name="required", cast=list),
            "properties": PropertyMeta(name="properties", cast=build_properties),
            "additional_properties": PropertyMeta(
                name="additionalProperties",
                cast=build_additional_properties,
            ),
        }

        return Object(**extract_attrs(data, attrs_map))

    def _one_of(self, data: dict[str, Any]) -> OneOf:
        def create_inner_schemas(schemas: list[dict[str, Any]]) -> list[Schema]:
            return [self.create(x) for x in schemas]

        def build_discriminator(discriminator_data: dict[str, Any]) -> Discriminator:
            discriminator = Discriminator(
                property_name=discriminator_data["propertyName"],
            )

            if "mapping" in discriminator_data:
                discriminator.mapping = {
                    key: self.create(schema)
                    for key, schema in discriminator_data["mapping"].items()
                }

            return discriminator

        attrs_map = {
            "schemas": PropertyMeta(name="oneOf", cast=create_inner_schemas),
            "discriminator": PropertyMeta(
                name="discriminator",
                cast=build_discriminator,
            ),
        }

        return OneOf(**extract_attrs(data, attrs_map))

    def _any_of(self, data: dict[str, Any]) -> AnyOf:
        def create_inner_schemas(schemas: list[dict[str, Any]]) -> list[Schema]:
            return [self.create(x) for x in schemas]

        attrs_map = {"schemas": PropertyMeta(name="anyOf", cast=create_inner_schemas)}

        if "type" in data:
            return AnyOf(**extract_attrs(data, attrs_map))

        possible_implicit_types = (
            DataType.INTEGER,
            DataType.NUMBER,
            DataType.STRING,
            DataType.BOOLEAN,
            DataType.ARRAY,
            DataType.OBJECT,
        )

        schemas = [
            builder_func({**data, **{"type": data_type}})
            for data_type, builder_func in self._builders.items()
            if data_type in possible_implicit_types
        ]

        return AnyOf(type=DataType.ANY_OF, schemas=schemas)
