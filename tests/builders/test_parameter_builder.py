from unittest.mock import MagicMock

import pytest

from openapi_parser.builders import ParameterBuilder, SchemaFactory
from openapi_parser.enumeration import DataType, ParameterLocation, HeaderParameterStyle, QueryParameterStyle
from openapi_parser.specification import Parameter, Schema, String


def _get_schema_factory_mock(expected_value: Schema) -> SchemaFactory:
    mock_object = MagicMock()
    mock_object.create.return_value = expected_value

    return mock_object


string_schema = String(type=DataType.STRING)

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
        _get_schema_factory_mock(string_schema)
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
        _get_schema_factory_mock(string_schema)
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
        _get_schema_factory_mock(string_schema)
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
        _get_schema_factory_mock(string_schema)
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
        _get_schema_factory_mock(string_schema)
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'schema_factory'], schema_data_provider)
def test_build(data: dict, expected: Parameter, schema_factory: SchemaFactory):
    builder = ParameterBuilder(schema_factory)

    assert expected == builder.build(data)


@pytest.mark.parametrize(['data_list', 'expected', 'schema_factory'], collection_data_provider)
def test_build_collection(data_list: list, expected: list[Parameter], schema_factory: SchemaFactory):
    builder = ParameterBuilder(schema_factory)

    assert expected == builder.build_list(data_list)
