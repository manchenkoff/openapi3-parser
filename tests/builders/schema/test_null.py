import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.specification import DataType, Null

data_provider = (
    (
        {
            "type": "null",
        },
        Null(type=DataType.NULL)
    ),
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_boolean_builder(data: dict, expected: Null) -> None:
    factory = SchemaFactory()
    assert expected == factory.create(data)
