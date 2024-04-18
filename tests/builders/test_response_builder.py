from typing import Any, Union
from unittest.mock import MagicMock

import pytest

from openapi_parser.builders import ContentBuilder, HeaderBuilder, ResponseBuilder
from openapi_parser.enumeration import DataType
from openapi_parser.mime_types import ContentType
from openapi_parser.specification import Content, Header, \
    Integer, Object, Property, Response, String


def _get_builder_mock(expected_value: Any) -> Union[ContentBuilder, HeaderBuilder]:
    mock_object = MagicMock()
    mock_object.build_list.return_value = expected_value

    return mock_object


content_schema = [
    Content(
        type=ContentType.JSON,
        schema=Object(
            type=DataType.OBJECT,
            properties=[
                Property(name="login", schema=String(type=DataType.STRING))
            ]
        )
    )
]

header_schema = [
    Header(
        name="X-Rate-Limit-Limit",
        description="The number of allowed requests in the current period",
        schema=Integer(type=DataType.INTEGER)
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
                    }
                }
            },
            "headers": {
                "X-Rate-Limit-Limit": {
                    "description": "The number of allowed requests in the current period",
                    "schema": {
                        "type": "integer"
                    }
                }
            }
        },
        Response(
            code=200,
            description="A string response",
            content=content_schema,
            headers=header_schema,
            is_default=False,
        ),
        _get_builder_mock(content_schema),
        _get_builder_mock(header_schema),
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'content_builder', 'header_builder'], data_provider)
def test_build(data: dict, expected: Response, content_builder: ContentBuilder, header_builder: HeaderBuilder) -> None:
    builder = ResponseBuilder(content_builder, header_builder)

    assert expected == builder.build(expected.code, data)


def test_build_default_response() -> None:
    builder = ResponseBuilder(
        _get_builder_mock(None),
        _get_builder_mock(None),
    )

    response_data = {"description": "A string response"}
    actual = builder.build("default", response_data)

    assert actual.is_default
    assert actual.code is None
