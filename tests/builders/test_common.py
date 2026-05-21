import pytest

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_typed_props,
    merge_schema,
)
from openapi_parser.enumeration import SecurityType
from openapi_parser.errors import ParserError


def test_extract_typed_props_cast_failure() -> None:
    attrs_map = {
        "type": PropertyMeta(name="type", cast=SecurityType),
    }

    with pytest.raises(ParserError, match="Invalid value for 'type' property"):
        extract_typed_props({"type": "invalid_enum"}, attrs_map)


def test_merge_schema_list_conflict() -> None:
    original = {"items": "not_a_list"}
    other = {"items": [1, 2]}

    result = merge_schema(original, other)

    assert result == {"items": [1, 2]}


def test_merge_schema_dict_conflict() -> None:
    original = {"schema": "not_a_dict"}
    other = {"schema": {"type": "object"}}

    result = merge_schema(original, other)

    assert result == {"schema": {"type": "object"}}
