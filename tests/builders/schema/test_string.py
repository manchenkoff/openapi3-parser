from typing import Any

import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import DataType, StringFormat
from openapi_parser.specification import String

data_provider = (
    (
        {
            "type": "string",
        },
        String(type=DataType.STRING),
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
        ),
    ),
    (
        {
            "type": "string",
            "x-custom-attr": "value",
        },
        String(type=DataType.STRING, extensions={"custom_attr": "value"}),
    ),
)


@pytest.mark.parametrize(["data", "expected"], data_provider)
def test_string_builder(data: dict[str, Any], expected: String) -> None:
    factory = SchemaFactory()
    assert expected == factory.create(data)
