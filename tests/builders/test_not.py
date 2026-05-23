from typing import Any

import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import DataType
from openapi_parser.specification import (
    AnyOf,
    Array,
    Boolean,
    Integer,
    Number,
    Object,
    Property,
    Schema,
    String,
)

data_provider = (
    (
        {
            "type": "string",
            "not": {"type": "integer"},
        },
        String(
            type=DataType.STRING,
            not_schema=Integer(type=DataType.INTEGER),
        ),
    ),
    (
        {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "not": {"type": "integer"},
        },
        Object(
            type=DataType.OBJECT,
            properties=[
                Property(name="name", schema=String(type=DataType.STRING)),
            ],
            not_schema=Integer(type=DataType.INTEGER),
        ),
    ),
    (
        {
            "not": {"type": "integer"},
        },
        AnyOf(
            type=DataType.ANY_OF,
            schemas=[
                Integer(type=DataType.INTEGER),
                Number(type=DataType.NUMBER),
                String(type=DataType.STRING),
                Boolean(type=DataType.BOOLEAN),
                Array(type=DataType.ARRAY),
                Object(type=DataType.OBJECT),
            ],
            not_schema=Integer(type=DataType.INTEGER),
        ),
    ),
    (
        {
            "type": "string",
        },
        String(type=DataType.STRING),
    ),
)


@pytest.mark.parametrize(["data", "expected"], data_provider)
def test_not_builder(data: dict[str, Any], expected: Schema) -> None:
    factory = SchemaFactory()
    assert expected == factory.create(data)
