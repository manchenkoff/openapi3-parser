import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.specification import DataType, Number, NumberFormat

data_provider = (
    (
        {
            "type": "number",
        },
        Number(type=DataType.NUMBER)
    ),
    (
        {
            "type": "number",
            "multipleOf": "0",
            "maximum": "0",
            "exclusiveMaximum": "0",
            "minimum": "0",
            "exclusiveMinimum": "0",
            "format": "float",
        },
        Number(
            type=DataType.NUMBER,
            multiple_of=0.0,
            maximum=0.0,
            exclusive_maximum=0.0,
            minimum=0.0,
            exclusive_minimum=0.0,
            format=NumberFormat.FLOAT,
        )
    ),
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_number_builder(data: dict, expected: Number):
    factory = SchemaFactory()
    assert expected == factory.create(data)
