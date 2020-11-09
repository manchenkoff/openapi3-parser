import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.specification import DataType, String, StringFormat

data_provider = (
    (
        {
            "type": "string",
        },
        String(type=DataType.STRING)
    ),
    (
        {
            "type": "string",
            "maxLength": 1,
            "minLength": 0,
            "pattern": "[0-9]",
            "format": "uuid",
        },
        String(
            type=DataType.STRING,
            max_length=1,
            min_length=0,
            pattern="[0-9]",
            format=StringFormat.UUID,
        )
    ),
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_integer_builder(data: dict, expected: String):
    factory = SchemaFactory()
    assert expected == factory.create(data)
