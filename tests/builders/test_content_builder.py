from unittest.mock import MagicMock

import pytest

from openapi_parser.builders import ContentBuilder, SchemaFactory
from openapi_parser.enumeration import ContentType, DataType
from openapi_parser.specification import Content, Integer, Schema, String


def _get_schema_factory_mock(expected_value: Schema) -> SchemaFactory:
    mock_object = MagicMock()
    mock_object.create.return_value = expected_value

    return mock_object


string_schema = String(type=DataType.STRING)
integer_schema = Integer(type=DataType.INTEGER)

collection_data_provider = (
    (
        {
            "application/json": {
                "schema": {
                    "type": "string"
                }
            }
        },
        [
            Content(type=ContentType.JSON, schema=string_schema, example=None, examples=[])
        ],
        _get_schema_factory_mock(string_schema)
    ),
    (
        {
            "text/json": {
                "schema": {
                    "type": "string"
                }
            }
        },
        [
            Content(type=ContentType.JSON_TEXT, schema=string_schema, example=None, examples=[])
        ],
        _get_schema_factory_mock(string_schema)
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'schema_factory'], collection_data_provider)
def test_build(data: dict, expected: Content, schema_factory: SchemaFactory):
    builder = ContentBuilder(schema_factory)

    assert expected == builder.build_list(data)
