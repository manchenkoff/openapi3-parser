from typing import Optional
from unittest.mock import MagicMock

import pytest

from openapi_parser.builders.content import ContentBuilder
from openapi_parser.builders.parameter import ParameterBuilder
from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import DataType, ParameterLocation, HeaderParameterStyle, QueryParameterStyle, \
    ContentType
from openapi_parser.specification import Parameter, Schema, String, Content


def _get_schema_factory_mock(expected_value: Optional[Schema]) -> SchemaFactory:
    mock_object = MagicMock()
    mock_object.create.return_value = expected_value

    return mock_object


def _get_content_builder_mock(expected_value: Optional[list[Content]]) -> ContentBuilder:
    mock_object = MagicMock()
    mock_object.build_list.return_value = expected_value

    return mock_object


string_schema = String(type=DataType.STRING)
content_schema = Content(
    type=ContentType.JSON,
    schema=string_schema,
)

schema_data_provider = (
    (
        {
            "name": "token",
            "in": "header",
            "required": True,
            "style": "simple",
            "schema": {
                "type": "string",
            },
        },
        Parameter(
            name="token",
            location=ParameterLocation.HEADER,
            required=True,
            style=HeaderParameterStyle.SIMPLE,
            schema=string_schema,
            explode=False,
        ),
        _get_schema_factory_mock(string_schema),
        _get_content_builder_mock(None),
    ),
    (
        {
            "name": "token",
            "in": "header",
            "required": True,
            "description": "token to be passed as a header",
            "deprecated": True,
            "schema": {
                "type": "string",
            },
        },
        Parameter(
            name="token",
            location=ParameterLocation.HEADER,
            required=True,
            description="token to be passed as a header",
            deprecated=True,
            schema=string_schema,
            style=HeaderParameterStyle.SIMPLE,
            explode=False,
        ),
        _get_schema_factory_mock(string_schema),
        _get_content_builder_mock(None),
    ),
    (
        {
            "name": "tokensImplodedString",
            "in": "query",
            "required": True,
            "style": "form",
            "schema": {
                "type": "string",
            },
        },
        Parameter(
            name="tokensImplodedString",
            location=ParameterLocation.QUERY,
            required=True,
            style=QueryParameterStyle.FORM,
            explode=True,
            schema=string_schema,
        ),
        _get_schema_factory_mock(string_schema),
        _get_content_builder_mock(None),
    ),
    (
        {
            "name": "some_id",
            "in": "query",
            "required": True,
            "style": "form",
            "schema": {
                "type": "string",
            },
            "x-custom-go-tag": "binding:\"required\""
        },
        Parameter(
            name="some_id",
            location=ParameterLocation.QUERY,
            required=True,
            style=QueryParameterStyle.FORM,
            explode=True,
            schema=string_schema,
            extensions={"custom_go_tag": "binding:\"required\""}
        ),
        _get_schema_factory_mock(string_schema),
        _get_content_builder_mock(None),
    ),
)

collection_data_provider = (
    (
        [
            {
                "name": "token",
                "in": "header",
                "required": True,
                "schema": {
                    "type": "string",
                },
            },
            {
                "name": "token",
                "in": "header",
                "required": True,
                "description": "token to be passed as a header",
                "deprecated": True,
                "schema": {
                    "type": "string",
                },
            },
        ],
        [
            Parameter(
                name="token",
                location=ParameterLocation.HEADER,
                required=True,
                schema=string_schema,
                style=HeaderParameterStyle.SIMPLE,
                explode=False,
            ),
            Parameter(
                name="token",
                location=ParameterLocation.HEADER,
                required=True,
                description="token to be passed as a header",
                deprecated=True,
                schema=string_schema,
                style=HeaderParameterStyle.SIMPLE,
                explode=False,
            ),
        ],
        _get_schema_factory_mock(string_schema),
        _get_content_builder_mock(None),
    ),
    (
        [
            {
                "name": "content-token",
                "in": "header",
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "string",
                        },
                    }
                },
            },
            {
                "name": "schema-token",
                "in": "header",
                "required": True,
                "description": "token to be passed as a header",
                "deprecated": True,
                "schema": {
                    "type": "string",
                },
            },
        ],
        [
            Parameter(
                name="content-token",
                location=ParameterLocation.HEADER,
                required=True,
                content=[
                    Content(
                        type=ContentType.JSON,
                        schema=string_schema,
                    )
                ],
                style=HeaderParameterStyle.SIMPLE,
                explode=False,
            ),
            Parameter(
                name="schema-token",
                location=ParameterLocation.HEADER,
                required=True,
                description="token to be passed as a header",
                deprecated=True,
                schema=string_schema,
                style=HeaderParameterStyle.SIMPLE,
                explode=False,
            ),
        ],
        _get_schema_factory_mock(string_schema),
        _get_content_builder_mock([content_schema]),
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'schema_factory', 'content_builder'], schema_data_provider)
def test_build(
        data: dict,
        expected: Parameter,
        schema_factory: SchemaFactory,
        content_builder: ContentBuilder):
    builder = ParameterBuilder(schema_factory, content_builder)

    assert expected == builder.build(data)


@pytest.mark.parametrize(['data_list', 'expected', 'schema_factory', 'content_builder'], collection_data_provider)
def test_build_collection(
        data_list: list,
        expected: list[Parameter],
        schema_factory: SchemaFactory,
        content_builder: ContentBuilder):
    builder = ParameterBuilder(schema_factory, content_builder)

    assert expected == builder.build_list(data_list)
