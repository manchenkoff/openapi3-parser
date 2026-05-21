from typing import Any

import pytest

from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import DataType
from openapi_parser.specification import Null

data_provider = (
    (
        {
            "type": "null",
        },
        Null(type=DataType.NULL),
    ),
)


@pytest.mark.parametrize(["data", "expected"], data_provider)
def test_null_builder(data: dict[str, Any], expected: Null) -> None:
    factory = SchemaFactory()
    assert expected == factory.create(data)
