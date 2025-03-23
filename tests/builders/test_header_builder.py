from unittest.mock import MagicMock

import pytest

from openapi_parser.builders.header import HeaderBuilder
from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import DataType
from openapi_parser.specification import Header, Integer, Schema, String


def _get_schema_factory_mock(expected_value: Schema) -> SchemaFactory:
    mock_object = MagicMock()
    mock_object.create.return_value = expected_value

    return mock_object


string_schema = String(type=DataType.STRING)
integer_schema = Integer(type=DataType.INTEGER)

collection_data_provider = (
    (
        {
            "X-Header": {
                "schema": {
                    "type": "string"
                }
            }
        },
        [
            Header(schema=string_schema, name="X-Header"),
        ],
        _get_schema_factory_mock(string_schema)
    ),
    (
        {
            "X-Header": {
                "description": "The number of allowed requests in the current period",
                "required": True,
                "deprecated": True,
                "schema": {
                    "type": "integer",
                },
            }
        },
        [
            Header(
                name="X-Header",
                required=True,
                description="The number of allowed requests in the current period",
                deprecated=True,
                schema=integer_schema
            )
        ],
        _get_schema_factory_mock(integer_schema)
    ),
    (
        {
            "X-Header": {
                "description": "The number of allowed requests in the current period",
                "required": True,
                "deprecated": True,
                "schema": {
                    "type": "integer",
                },
                "x-custom-go-tag": "json:\"x-header\""
            }
        },
        [
            Header(
                name="X-Header",
                required=True,
                description="The number of allowed requests in the current period",
                deprecated=True,
                schema=integer_schema,
                extensions={"custom_go_tag": "json:\"x-header\""}
            )
        ],
        _get_schema_factory_mock(integer_schema)
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'schema_factory'], collection_data_provider)
def test_build_collection(data: dict, expected: Header, schema_factory: SchemaFactory):
    builder = HeaderBuilder(schema_factory)

    assert expected == builder.build_list(data)
