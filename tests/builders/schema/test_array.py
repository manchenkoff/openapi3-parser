import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.errors import ParserError
from openapi_parser.specification import Array, DataType, String

string_schema = String(type=DataType.STRING)

data_provider = (
    (
        {
            "type": "array",
            "items": {
                "type": "string",
            }
        },
        Array(type=DataType.ARRAY, items=string_schema),
    ),
    (
        {
            "type": "array",
            "maxItems": "1",
            "minItems": "0",
            "uniqueItems": False,
            "items": {
                "type": "string",
            },
        },
        Array(
            type=DataType.ARRAY,
            max_items=1,
            min_items=0,
            unique_items=False,
            items=string_schema,
        ),
    ),
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_array_builder(data: dict, expected: Array):
    factory = SchemaFactory()
    assert expected == factory.create(data)


def test_create_error():
    data = {"type": "array"}
    factory = SchemaFactory()

    with pytest.raises(ParserError, match="Arrays must contain 'items' definition"):
        factory.create(data)
