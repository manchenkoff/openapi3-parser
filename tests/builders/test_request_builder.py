from typing import Any
from unittest.mock import MagicMock

import pytest

from openapi_parser.builders.content import ContentBuilder
from openapi_parser.builders.request import RequestBuilder
from openapi_parser.enumeration import DataType
from openapi_parser.specification import Content, ContentType, Object, Property, RequestBody, String


def _get_content_builder_mock(expected_value: Any) -> ContentBuilder:
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

extended_content_schema = [
    Content(
        type=ContentType.JSON,
        schema=Object(
            type=DataType.OBJECT,
            properties=[
                Property(name="login", schema=String(type=DataType.STRING))
            ]
        )
    ),
    Content(
        type=ContentType.FORM,
        schema=Object(
            type=DataType.OBJECT,
            properties=[
                Property(name="login", schema=String(type=DataType.STRING))
            ]
        )
    ),
]

data_provider = (
    (
        {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "login": {
                                "type": "string",
                            }
                        }
                    },
                },
            }
        },
        RequestBody(content=content_schema),
        _get_content_builder_mock(content_schema)
    ),
    (
        {
            "description": "user to add to the system",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "login": {
                                "type": "string",
                            }
                        }
                    },
                },
                "application/x-www-form-urlencoded": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "login": {
                                "type": "string",
                            }
                        }
                    },
                }
            }
        },
        RequestBody(
            description="user to add to the system",
            content=extended_content_schema
        ),
        _get_content_builder_mock(extended_content_schema)
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'content_builder'], data_provider)
def test_build(data: dict, expected: RequestBody, content_builder: ContentBuilder):
    builder = RequestBuilder(content_builder)

    assert expected == builder.build(data)
