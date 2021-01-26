from typing import Any, Union
from unittest.mock import MagicMock

import pytest

from openapi_parser.builders import ContentBuilder, HeaderBuilder, ResponseBuilder
from openapi_parser.enumeration import DataType
from openapi_parser.specification import Content, ContentType, Header, \
    Integer, Object, Property, RequestBody, Response, String


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
            headers=header_schema
        ),
        _get_builder_mock(content_schema),
        _get_builder_mock(header_schema),
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'content_builder', 'header_builder'], data_provider)
def test_build(data: dict, expected: RequestBody, content_builder: ContentBuilder, header_builder: HeaderBuilder):
    build = ResponseBuilder(content_builder, header_builder)

    assert expected == build.build(200, data)
