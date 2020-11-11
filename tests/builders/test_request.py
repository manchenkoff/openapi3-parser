from unittest.mock import MagicMock

import pytest

from openapi_parser.builders import ContentBuilder
from openapi_parser.enumeration import DataType, MediaType
from openapi_parser.specification import Content, Object, Property, RequestBody, String


def _get_content_builder_mock(expected_value: Content) -> ContentBuilder:
    mock_object = MagicMock()
    mock_object.build.return_value = expected_value

    return mock_object


content_schema = Content(
    schema=Object(
        type=DataType.OBJECT,
        properties=[
            Property(name="login", schema=String(type=DataType.STRING))
        ]
    )
)

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
        RequestBody(
            content={
                MediaType.JSON: content_schema,
            }
        ),
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
            content={
                MediaType.JSON: content_schema,
                MediaType.FORM: content_schema,
            }
        ),
        _get_content_builder_mock(content_schema)
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'content_builder'], data_provider)
def test_build(data: dict, expected: RequestBody, content_builder: ContentBuilder):
    pass
