import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import IntegerFormat
from openapi_parser.specification import DataType, Integer, AnyOf, String, StringFormat, Number, Boolean, Array, Object

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
            "description": "Can be any value - string, number, boolean, array or object."
        },
        AnyOf(
            type=DataType.ANY_OF,
            description="Can be any value - string, number, boolean, array or object.",
            schemas=[]
        )
    )
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_string_builder(data: dict, expected: String):
    factory = SchemaFactory()
    assert expected == factory.create(data)
