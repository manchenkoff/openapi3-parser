from unittest.mock import MagicMock

import pytest

from openapi_parser.builders import SchemaFactory, ContentBuilder
from openapi_parser.enumeration import DataType
from openapi_parser.specification import Content, Integer, Schema, String


def _get_schema_factory_mock(expected_value: Schema) -> SchemaFactory:
    mock_object = MagicMock()
    mock_object.create.return_value = expected_value

    return mock_object


string_schema = String(type=DataType.STRING)
integer_schema = Integer(type=DataType.INTEGER)

data_provider = (
    (
        {
            "schema": {
                "type": "string"
            }
        },
        Content(schema=string_schema),
        _get_schema_factory_mock(string_schema)
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'schema_factory'], data_provider)
def test_build(data: dict, expected: Content, schema_factory: SchemaFactory):
    builder = ContentBuilder(schema_factory)

    assert expected == builder.build(data)
