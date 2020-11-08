import json
from unittest import mock

import pytest

from swagger_parser.specification import Contact, Info, License, Server, Specification, Tag
from swagger_parser.builders.server import ServerList
from swagger_parser.builders.tag import TagList
from swagger_parser.parser import Parser

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

    tag_list = [
        Tag(name="Users", description="User operations"),
    ]

    path_list = [
        # TODO: add DTOs
    ]

    return Specification(openapi="3.0.0",
                         info=info,
                         servers=server_list,
                         tags=tag_list,
                         paths=path_list)


def _create_info_builder_mock(info: Info):
    mock_object = mock.MagicMock()
    mock_object.build.return_value = info

    return mock_object


def _create_server_list_builder_mock(servers: ServerList):
    mock_object = mock.MagicMock()
    mock_object.build_list.return_value = servers

    return mock_object


def _create_tag_list_builder_mock(tags: TagList):
    mock_object = mock.MagicMock()
    mock_object.build_list.return_value = tags

    return mock_object


def test_load_specification(swagger_specification: Specification):
    info_builder = _create_info_builder_mock(swagger_specification.info)
    server_list_builder = _create_server_list_builder_mock(swagger_specification.servers)
    tag_list_builder = _create_tag_list_builder_mock(swagger_specification.tags)

    parser = Parser(info_builder,
                    server_list_builder,
                    tag_list_builder)

    with open(SWAGGER_JSON_FILEPATH) as input_json:
        swagger_json = json.load(input_json)

    assert swagger_specification == parser.load_specification(swagger_json)
