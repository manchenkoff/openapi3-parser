import pytest

from openapi_parser import parse
from openapi_parser.specification import Specification
from tests.openapi_fixture import create_specification


@pytest.fixture()
def swagger_specification():
    return create_specification()


def test_run_parser(swagger_specification: Specification):
    actual_specification = parse('tests/data/swagger.yml')

    assert actual_specification == swagger_specification
