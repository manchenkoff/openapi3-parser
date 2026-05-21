from typing import Any

import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import DataType
from openapi_parser.specification import Boolean

data_provider = (
    (
        {
            "type": "boolean",
        },
        Boolean(type=DataType.BOOLEAN),
    ),
    (
        {
            "type": "boolean",
            "default": True,
            "deprecated": False,
        },
        Boolean(type=DataType.BOOLEAN, default=True, deprecated=False),
    ),
)


@pytest.mark.parametrize(["data", "expected"], data_provider)
def test_boolean_builder(data: dict[str, Any], expected: Boolean) -> None:
    factory = SchemaFactory()
    assert expected == factory.create(data)
