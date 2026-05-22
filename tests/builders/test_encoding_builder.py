from typing import Any
from unittest.mock import MagicMock

import pytest

from openapi_parser.builders.encoding import EncodingBuilder
from openapi_parser.builders.header import HeaderBuilder
from openapi_parser.enumeration import DataType
from openapi_parser.specification import Encoding, Header, Integer


def _get_header_builder_mock(expected_value: list[Header]) -> HeaderBuilder:
    mock_object = MagicMock()
    mock_object.build_list.return_value = expected_value

    return mock_object


data_provider = (
    (
        {
            "contentType": "text/plain",
        },
        Encoding(content_type="text/plain"),
    ),
    (
        {
            "contentType": "application/json",
            "style": "form",
            "explode": True,
            "allowReserved": False,
        },
        Encoding(
            content_type="application/json",
            style="form",
            explode=True,
            allow_reserved=False,
        ),
    ),
)


@pytest.mark.parametrize(["data", "expected"], data_provider)
def test_build(data: dict[str, Any], expected: Encoding) -> None:
    builder = EncodingBuilder(_get_header_builder_mock([]))

    result = builder._build(data)

    assert expected == result


def test_build_with_headers() -> None:
    headers = [
        Header(
            name="X-Rate-Limit-Limit",
            description="The number of allowed requests in the current period",
            schema=Integer(type=DataType.INTEGER),
        )
    ]
    builder = EncodingBuilder(_get_header_builder_mock(headers))

    result = builder._build(
        {
            "contentType": "application/json",
            "headers": {
                "X-Rate-Limit-Limit": {
                    "description": "The number of allowed requests in the current period",
                    "schema": {"type": "integer"},
                }
            },
        }
    )

    assert result.content_type == "application/json"
    assert result.headers == headers


def test_build_with_extensions() -> None:
    builder = EncodingBuilder(_get_header_builder_mock([]))

    result = builder._build(
        {
            "contentType": "text/plain",
            "x-custom-encoding": "value",
        }
    )

    assert result.content_type == "text/plain"
    assert result.extensions == {"custom_encoding": "value"}


def test_build_dict() -> None:
    builder = EncodingBuilder(_get_header_builder_mock([]))

    result = builder.build_dict(
        {
            "name": {
                "contentType": "text/plain",
            },
            "email": {
                "contentType": "application/json",
            },
        }
    )

    assert result == {
        "name": Encoding(content_type="text/plain"),
        "email": Encoding(content_type="application/json"),
    }
