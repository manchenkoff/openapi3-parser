import json
from typing import List
from unittest import mock

import pytest

from src.swagger_parser import Contact, Info, License, Server, Specification
from src.swagger_parser.parser import Parser

SWAGGER_JSON_FILEPATH = './tests/data/swagger.json'


@pytest.fixture
def swagger_specification() -> Specification:
    info = Info(title="User example service",
                version="1.0.0",
                description="Example service specification to work with user storage",
                license=License(name="MIT"),
                contact=Contact(name="manchenkoff", email="artyom@manchenkoff.me"))

    server_list = [
        Server(url="https://users.app",
               description="production"),
        Server(url="http://stage.users.app",
               description="staging"),
        Server(url="http://users.local",
               description="development"),
    ]

    return Specification(openapi="3.0.0",
                         info=info,
                         servers=server_list)


def _create_info_builder_mock(info: Info):
    mock_object = mock.Mock()
    mock_object.build = mock.MagicMock(return_value=info)

    return mock_object


def _create_server_list_builder_mock(servers: List[Server]):
    mock_object = mock.Mock()
    mock_object.build_server_list = mock.MagicMock(return_value=servers)

    return mock_object


def test_load_specification(swagger_specification: Specification):
    info_builder = _create_info_builder_mock(swagger_specification.info)
    server_list_builder = _create_server_list_builder_mock(swagger_specification.servers)

    parser = Parser(info_builder,
                    server_list_builder)

    with open(SWAGGER_JSON_FILEPATH) as input_json:
        swagger_json = json.load(input_json)

    assert swagger_specification == parser.load_specification(swagger_json)
