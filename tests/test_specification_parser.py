from unittest import mock

import prance
import pytest

from swagger_parser import Contact, Info, License, Path, Server, Specification, Tag
from swagger_parser.parser import OperationParser, SpecificationParser


@pytest.fixture()
def specification_dict() -> dict:
    swagger_resolver = prance.ResolvingParser(
        './tests/data/swagger/swagger.yml',
        backend='openapi-spec-validator',
        strict=False,
        lazy=True
    )

    swagger_resolver.parse()

    return swagger_resolver.specification


def _get_operation_parser_mock() -> OperationParser:
    parser_mock = mock.Mock()
    parser_mock.parse_list = mock.MagicMock(return_value=())

    return parser_mock


def test_load_specification(specification_dict: dict):
    info = Info(
        'Example API', '1.0.0', 'Service description',
        License('MIT'),
        Contact('manchenkoff', 'artyom@manchenkoff.me')
    )
    servers = (
        Server('https://example.com', 'production'),
        Server('http://stage.example.com', 'staging'),
        Server('http://localhost', 'development'),
    )
    tags = (
        Tag('User', 'User operations'),
    )
    paths = (
        Path('/users', ()),
    )

    expected_specification = Specification(
        '3.0.0',
        info,
        servers,
        tags,
        paths,
    )

    operation_parser = _get_operation_parser_mock()
    specification_parser = SpecificationParser(operation_parser)

    specification = specification_parser.load_specification(specification_dict)

    assert expected_specification == specification
