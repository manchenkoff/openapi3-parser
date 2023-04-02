import pytest

from openapi_parser import parse
from openapi_parser.errors import ParserError

TEST_SCHEMA = './tests/data/non-strict.yml'


def test_default_strict_enum_errors() -> None:
    with pytest.raises(ParserError):
        parse(TEST_SCHEMA)


def test_with_non_strict_enum_succeeds() -> None:
    specification = parse(TEST_SCHEMA, strict_enum=False)

    response_200, response_400 = specification.paths[0].operations[0].responses

    response_hal_json = response_200.content[0]
    assert response_hal_json.type.value == "application/hal+json"
    duration_property = response_hal_json.schema.properties[0]
    assert duration_property.name == "expectedDeliveryDuration"
    assert duration_property.schema.type.value == "string"
    assert duration_property.schema.format.value == "duration"

    response_problem_json = response_400.content[0]
    assert response_problem_json.type.value == "application/problem+json"
