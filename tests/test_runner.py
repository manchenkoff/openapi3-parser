import pytest

from openapi_parser import parse
from openapi_parser.enumeration import DataType
from openapi_parser.specification import Array, Object, Specification
from tests.openapi_fixture import create_specification


@pytest.fixture()
def swagger_specification() -> Specification:
    return create_specification()


def test_run_parser(swagger_specification: Specification) -> None:
    actual_specification = parse("tests/data/swagger.yml")

    assert actual_specification == swagger_specification


def test_parse_recursive_schema() -> None:
    actual_specification = parse("tests/data/recursive.yml")

    assert actual_specification.version == "3.0.0"
    assert actual_specification.info.title == "Recursive schema test"
    assert "Equipment" in actual_specification.schemas
    assert "Feature" in actual_specification.schemas


def test_parse_recursive_schema_with_recursion_limit_2() -> None:
    spec = parse("tests/data/recursive.yml", recursion_limit=2)

    equipment = spec.schemas["Equipment"]
    assert isinstance(equipment, Object)

    features = equipment.properties[0]
    assert features.name == "Features"
    assert isinstance(features.schema, Array)

    feature_level_1 = features.schema.items
    assert isinstance(feature_level_1, Object)

    equipment_level_2_schema = feature_level_1.properties[0].schema
    assert isinstance(equipment_level_2_schema, Array)
    equipment_level_2 = equipment_level_2_schema.items
    assert isinstance(equipment_level_2, Object)
    assert equipment_level_2.type == DataType.OBJECT
    assert len(equipment_level_2.properties) == 2
    assert equipment_level_2.properties[0].name == "Features"

    feature_level_3_schema = equipment_level_2.properties[0].schema
    assert isinstance(feature_level_3_schema, Array)
    feature_level_3 = feature_level_3_schema.items
    assert isinstance(feature_level_3, Object)
    assert len(feature_level_3.properties) == 2
    assert feature_level_3.properties[0].name == "Equipments"

    equipment_level_4_schema = feature_level_3.properties[0].schema
    assert isinstance(equipment_level_4_schema, Array)
    equipment_level_4 = equipment_level_4_schema.items
    assert isinstance(equipment_level_4, Object)
    assert len(equipment_level_4.properties) == 2
    assert equipment_level_4.properties[0].name == "Features"

    placeholder_schema = equipment_level_4.properties[0].schema
    assert isinstance(placeholder_schema, Array)
    placeholder = placeholder_schema.items
    assert isinstance(placeholder, Object)
    assert len(placeholder.properties) == 0
