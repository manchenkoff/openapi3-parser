from typing import Any

import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import DataType
from openapi_parser.specification import Array, String

string_schema = String(type=DataType.STRING)

data_provider = (
    (
        {
            "type": "array",
            "items": {
                "type": "string",
            },
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


@pytest.mark.parametrize(["data", "expected"], data_provider)
def test_array_builder(data: dict[str, Any], expected: Array) -> None:
    factory = SchemaFactory()
    assert expected == factory.create(data)
