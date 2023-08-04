import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import IntegerFormat
from openapi_parser.specification import DataType, Integer, AnyOf, String, StringFormat, Array, Number, Boolean, Object, Property

string_schema = String(type=DataType.STRING)
number_schema = Number(type=DataType.NUMBER)

data_provider = (
    (
        {
            "anyOf": [
                {
                    "type": "string",
                    "maxLength": 1,
                    "minLength": 0,
                    "pattern": "[0-9]",
                    "format": "uuid",
                },
                {
                    "type": "integer",
                    "format": "int32",
                }
            ],
        },
        AnyOf(
            type=DataType.ANY_OF,
            schemas=[
                String(
                    type=DataType.STRING,
                    max_length=1,
                    min_length=0,
                    pattern="[0-9]",
                    format=StringFormat.UUID,
                ),
                Integer(
                    type=DataType.INTEGER,
                    format=IntegerFormat.INT32,
                ),
            ]
        )
    ),
    (
        {
            "description": "Can be any type - string, number, integer, boolean, object and array"
        },
        AnyOf(
            type=DataType.ANY_OF,
            schemas=[
                Integer(type=DataType.INTEGER, description="Can be any type - string, number, integer, boolean, object and array",),
                Number(type=DataType.NUMBER, description="Can be any type - string, number, integer, boolean, object and array",),
                String(type=DataType.STRING, description="Can be any type - string, number, integer, boolean, object and array",),
                Boolean(type=DataType.BOOLEAN, description="Can be any type - string, number, integer, boolean, object and array",),
                Array(type=DataType.ARRAY, description="Can be any type - string, number, integer, boolean, object and array",),
                Object(type=DataType.OBJECT, properties=[], description="Can be any type - string, number, integer, boolean, object and array",)
            ]
        )
    ),
    (
        {
            "description": "Array with implicit type.",
            "items": {"type": "string"}
        },
        AnyOf(
            type=DataType.ANY_OF,
            schemas=[
                Integer(type=DataType.INTEGER, description="Array with implicit type."),
                Number(type=DataType.NUMBER, description="Array with implicit type."),
                String(type=DataType.STRING, description="Array with implicit type."),
                Boolean(type=DataType.BOOLEAN, description="Array with implicit type."),
                Array(type=DataType.ARRAY, items=string_schema, description="Array with implicit type."),
                Object(type=DataType.OBJECT, properties=[], description="Array with implicit type."),
            ]
        )
    ),
    (
        {
            "description": "Object with implicit type.",
            "properties": {
                "property1": {"type": "string"},
                "property2": {"type": "number"}
            }
        },
        AnyOf(
            type=DataType.ANY_OF,
            schemas=[
                Integer(type=DataType.INTEGER, description="Object with implicit type."),
                Number(type=DataType.NUMBER, description="Object with implicit type."),
                String(type=DataType.STRING, description="Object with implicit type."),
                Boolean(type=DataType.BOOLEAN, description="Object with implicit type."),
                Array(type=DataType.ARRAY, description="Object with implicit type."),
                Object(
                    type=DataType.OBJECT,
                    properties=[Property("property1", string_schema), Property("property2", number_schema)],
                    description="Object with implicit type."
                ),
            ]
        )
    )
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_string_builder(data: dict, expected: String):
    factory = SchemaFactory()
    assert expected == factory.create(data)
