from typing import Any
from unittest import mock

import pytest

from openapi_parser.errors import ParserError
from openapi_parser.parser import Parser
from openapi_parser.resolver import OpenAPIResolver
from openapi_parser.specification import Specification

from .openapi_fixture import create_specification

SWAGGER_JSON_FILEPATH = "./tests/data/swagger.json"


@pytest.fixture()
def swagger_specification() -> Specification:
    return create_specification()


def _create_builder_mock(item: Any) -> mock.MagicMock:
    mock_object = mock.MagicMock()
    mock_object.build.return_value = item

    return mock_object


def _create_list_builder_mock(items: Any) -> mock.MagicMock:
    mock_object = mock.MagicMock()
    mock_object.build_list.return_value = items

    return mock_object


def _create_collection_builder_mock(collection: Any) -> mock.MagicMock:
    mock_object = mock.MagicMock()
    mock_object.build_collection.return_value = collection

    return mock_object


def test_load_specification(swagger_specification: Specification) -> None:
    info_builder = _create_builder_mock(swagger_specification.info)
    server_list_builder = _create_list_builder_mock(swagger_specification.servers)
    tag_list_builder = _create_list_builder_mock(swagger_specification.tags)
    external_doc_builder = _create_builder_mock(swagger_specification.external_docs)
    path_builder = _create_list_builder_mock(swagger_specification.paths)
    security_builder = _create_collection_builder_mock(
        swagger_specification.security_schemas,
    )
    schemas_builder = _create_collection_builder_mock(swagger_specification.schemas)

    parser = Parser(
        info_builder,
        server_list_builder,
        tag_list_builder,
        external_doc_builder,
        path_builder,
        security_builder,
        schemas_builder,
    )

    swagger_json = OpenAPIResolver(SWAGGER_JSON_FILEPATH).resolve()

    assert swagger_specification == parser.load_specification(swagger_json)


def test_load_specification_missing_openapi_version() -> None:
    parser = Parser(
        _create_builder_mock(None),
        _create_list_builder_mock([]),
        _create_list_builder_mock([]),
        _create_builder_mock(None),
        _create_list_builder_mock([]),
        _create_collection_builder_mock({}),
        _create_collection_builder_mock({}),
    )

    with pytest.raises(ParserError, match="Invalid OpenAPI version"):
        parser.load_specification({"info": {"title": "test", "version": "1.0.0"}})


def test_load_specification_missing_info() -> None:
    parser = Parser(
        _create_builder_mock(None),
        _create_list_builder_mock([]),
        _create_list_builder_mock([]),
        _create_builder_mock(None),
        _create_list_builder_mock([]),
        _create_collection_builder_mock({}),
        _create_collection_builder_mock({}),
    )

    with pytest.raises(ParserError, match="missing required 'info' property"):
        parser.load_specification({"openapi": "3.0.0"})
