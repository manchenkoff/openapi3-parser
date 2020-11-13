import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.specification import DataType, Integer, IntegerFormat

data_provider = (
    (
        {
            "type": "integer",
        },
        Integer(type=DataType.INTEGER)
    ),
    (
        {
            "type": "integer",
            "multipleOf": "0",
            "maximum": "0",
            "exclusiveMaximum": "0",
            "minimum": "0",
            "exclusiveMinimum": "0",
            "format": "int32",
        },
        Integer(
            type=DataType.INTEGER,
            multiple_of=0,
            maximum=0,
            exclusive_maximum=0,
            minimum=0,
            exclusive_minimum=0,
            format=IntegerFormat.INT32,
        )
    ),
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_integer_builder(data: dict, expected: Integer):
    factory = SchemaFactory()
    assert expected == factory.create(data)
