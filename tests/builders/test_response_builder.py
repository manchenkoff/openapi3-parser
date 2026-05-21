from typing import Any
from unittest.mock import MagicMock

import pytest

from openapi_parser.builders.content import ContentBuilder
from openapi_parser.builders.header import HeaderBuilder
from openapi_parser.builders.response import ResponseBuilder
from openapi_parser.enumeration import ContentType, DataType
from openapi_parser.specification import (
    Content,
    Header,
    Integer,
    Object,
    Property,
    Response,
    String,
)


def _get_content_builder_mock(expected_value: Any) -> ContentBuilder:
    mock_object = MagicMock()
    mock_object.build_list.return_value = expected_value

    return mock_object


def _get_header_builder_mock(expected_value: Any) -> HeaderBuilder:
    mock_object = MagicMock()
    mock_object.build_list.return_value = expected_value

    return mock_object


content_schema = [
    Content(
        type=ContentType.JSON,
        schema=Object(
            type=DataType.OBJECT,
            properties=[Property(name="login", schema=String(type=DataType.STRING))],
        ),
    )
]

header_schema = [
    Header(
        name="X-Rate-Limit-Limit",
        description="The number of allowed requests in the current period",
        schema=Integer(type=DataType.INTEGER),
    )
]

data_provider = (
    (
        {
            "description": "A string response",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "string",
                    },
                    "example": "an example",
                }
            },
            "headers": {
                "X-Rate-Limit-Limit": {
                    "description": "The number of allowed requests in the current period",
                    "schema": {"type": "integer"},
                }
            },
        },
        Response(
            code=200,
            description="A string response",
            content=content_schema,
            headers=header_schema,
            is_default=False,
        ),
        _get_content_builder_mock(content_schema),
        _get_header_builder_mock(header_schema),
    ),
)


@pytest.mark.parametrize(
    ["data", "expected", "content_builder", "header_builder"],
    data_provider,
)
def test_build(
    data: dict[str, Any],
    expected: Response,
    content_builder: ContentBuilder,
    header_builder: HeaderBuilder,
) -> None:
    builder = ResponseBuilder(content_builder, header_builder)

    assert expected.code is not None
    assert expected == builder.build(expected.code, data)


def test_build_default_response() -> None:
    builder = ResponseBuilder(
        _get_content_builder_mock(None),
        _get_header_builder_mock(None),
    )

    response_data = {"description": "A string response"}
    actual = builder.build("default", response_data)

    assert actual.is_default
    assert actual.code is None


def test_build_no_content_or_headers() -> None:
    builder = ResponseBuilder(
        _get_content_builder_mock(None),
        _get_header_builder_mock(None),
    )

    actual = builder.build(200, {"description": "No content response"})

    assert actual.code == 200
    assert actual.description == "No content response"
    assert not actual.is_default
    assert actual.content is None
    assert actual.headers == []


def test_build_with_code_as_string() -> None:
    builder = ResponseBuilder(
        _get_content_builder_mock([]),
        _get_header_builder_mock([]),
    )

    actual = builder.build("404", {"description": "Not found"})

    assert actual.code == 404
    assert not actual.is_default


@pytest.mark.parametrize("code", [201, 204, 301, 400, 404, 500])
def test_build_with_various_codes(code: int) -> None:
    builder = ResponseBuilder(
        _get_content_builder_mock(None),
        _get_header_builder_mock(None),
    )

    actual = builder.build(code, {"description": f"Response {code}"})

    assert actual.code == code
    assert actual.description == f"Response {code}"
