import json
from unittest import mock

import pytest

from src.swagger_parser import Contact, Info, License, Specification
from src.swagger_parser.parser import Parser

SWAGGER_JSON_FILEPATH = './tests/data/swagger.json'


@pytest.fixture
def swagger_specification() -> Specification:
    info = Info(title="User example service",
                version="1.0.0",
                description="Example service specification to work with user storage",
                license=License(name="MIT"),
                contact=Contact(name="manchenkoff", email="artyom@manchenkoff.me"))

    return Specification(openapi="3.0.0",
                         info=info)


def _create_info_builder_mock(info: Info):
    info_builder = mock.Mock()
    info_builder.build = mock.MagicMock(return_value=info)

    return info_builder


def test_load_specification(swagger_specification: Specification):
    info_builder = _create_info_builder_mock(swagger_specification.info)

    parser = Parser(info_builder)

    with open(SWAGGER_JSON_FILEPATH) as input_json:
        swagger_json = json.load(input_json)

    assert swagger_specification == parser.load_specification(swagger_json)
