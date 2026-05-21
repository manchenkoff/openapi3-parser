import pytest

from openapi_parser import parse
from openapi_parser.errors import ParserError
from openapi_parser.specification import Object, String

TEST_SCHEMA = "./tests/data/non-strict.yml"


def test_default_strict_enum_errors() -> None:
    with pytest.raises(ParserError):
        parse(TEST_SCHEMA)


def test_with_non_strict_enum_succeeds() -> None:
    specification = parse(TEST_SCHEMA, strict_enum=False)

    response_200, response_400 = specification.paths[0].operations[0].responses

    assert response_200.content is not None
    response_hal_json = response_200.content[0]
    assert response_hal_json.type.value == "application/hal+json"
    assert isinstance(response_hal_json.schema, Object)
    duration_property = response_hal_json.schema.properties[0]
    assert duration_property.name == "expectedDeliveryDuration"
    assert duration_property.schema.type.value == "string"
    assert isinstance(duration_property.schema, String)
    assert duration_property.schema.format is not None
    assert duration_property.schema.format.value == "duration"

    assert response_400.content is not None
    response_problem_json = response_400.content[0]
    assert response_problem_json.type.value == "application/problem+json"
