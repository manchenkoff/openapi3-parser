from typing import Any
from unittest.mock import MagicMock

import pytest

from openapi_parser.builders.content import ContentBuilder
from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import ContentType, DataType
from openapi_parser.specification import Content, Schema, String


def _get_schema_factory_mock(expected_value: Schema) -> SchemaFactory:
    mock_object = MagicMock()
    mock_object.create.return_value = expected_value

    return mock_object


string_schema = String(type=DataType.STRING)

collection_data_provider = (
    (
        {"application/json": {"schema": {"type": "string"}}},
        [Content(type=ContentType.JSON, schema=string_schema)],
        _get_schema_factory_mock(string_schema),
    ),
    (
        {"text/json": {"schema": {"type": "string"}}},
        [Content(type=ContentType.JSON_TEXT, schema=string_schema)],
        _get_schema_factory_mock(string_schema),
    ),
)


@pytest.mark.parametrize(
    ["data", "expected", "schema_factory"],
    collection_data_provider,
)
def test_build(
    data: dict[str, Any],
    expected: list[Content],
    schema_factory: SchemaFactory,
) -> None:
    builder = ContentBuilder(schema_factory)

    assert expected == builder.build_list(data)


def test_build_empty_dict() -> None:
    builder = ContentBuilder(_get_schema_factory_mock(string_schema))

    assert builder.build_list({}) == []


def test_build_with_example() -> None:
    schema_factory = _get_schema_factory_mock(string_schema)
    builder = ContentBuilder(schema_factory)

    result = builder.build_list(
        {
            "application/json": {
                "schema": {"type": "string"},
                "example": "hello world",
            }
        }
    )

    assert len(result) == 1
    assert result[0].example == "hello world"


def test_build_with_examples() -> None:
    schema_factory = _get_schema_factory_mock(string_schema)
    builder = ContentBuilder(schema_factory)
    examples = {"test": {"value": "hello"}}

    result = builder.build_list(
        {
            "application/json": {
                "schema": {"type": "string"},
                "examples": examples,
            }
        }
    )

    assert len(result) == 1
    assert result[0].examples == examples


def test_build_missing_schema() -> None:
    schema_factory_mock = MagicMock()
    builder = ContentBuilder(schema_factory_mock)

    builder.build_list({"application/json": {}})

    schema_factory_mock.create.assert_called_once_with({})


def test_build_multiple_content_types() -> None:
    schema_factory = MagicMock()
    schema_factory.create.side_effect = [string_schema, string_schema]
    builder = ContentBuilder(schema_factory)

    result = builder.build_list(
        {
            "application/json": {"schema": {"type": "string"}},
            "application/x-www-form-urlencoded": {"schema": {"type": "string"}},
        }
    )

    assert len(result) == 2
    assert result[0].type == ContentType.JSON
    assert result[1].type == ContentType.FORM


def test_build_non_strict_enum() -> None:
    schema_factory = _get_schema_factory_mock(string_schema)
    builder = ContentBuilder(schema_factory, strict_enum=False)

    result = builder.build_list(
        {
            "application/vnd.api+json": {"schema": {"type": "string"}},
        }
    )

    assert len(result) == 1
    assert result[0].type.value == "application/vnd.api+json"
