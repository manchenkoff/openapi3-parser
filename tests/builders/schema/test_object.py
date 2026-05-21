from typing import Any

import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import DataType
from openapi_parser.specification import Object, Property, String

string_schema = String(type=DataType.STRING)

data_provider = (
    (
        {
            "type": "object",
        },
        Object(type=DataType.OBJECT),
    ),
    (
        {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {
                    "type": "string",
                },
            },
        },
        Object(
            type=DataType.OBJECT,
            required=["name"],
            properties=[Property("name", string_schema)],
        ),
    ),
)


@pytest.mark.parametrize(["data", "expected"], data_provider)
def test_object_builder(data: dict[str, Any], expected: Object) -> None:
    factory = SchemaFactory()
    assert expected == factory.create(data)
