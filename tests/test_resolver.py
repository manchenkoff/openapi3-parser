from unittest import mock

import prance
import pytest

from openapi_parser.errors import ParserError
from openapi_parser.resolver import (
    OpenAPIResolver,
    _default_recursion_limit_handler,
)


@mock.patch("openapi_parser.resolver.prance.ResolvingParser")
def test_resolve_validation_error(mock_resolving_parser: mock.MagicMock) -> None:
    mock_instance = mock_resolving_parser.return_value
    mock_instance.parse.side_effect = prance.ValidationError("invalid spec")

    resolver = OpenAPIResolver("fake.yaml")

    with pytest.raises(ParserError, match="OpenAPI validation error"):
        resolver.resolve()


@mock.patch("openapi_parser.resolver.prance.ResolvingParser")
def test_resolve_generic_error(mock_resolving_parser: mock.MagicMock) -> None:
    mock_instance = mock_resolving_parser.return_value
    mock_instance.parse.side_effect = RuntimeError("connection failed")

    resolver = OpenAPIResolver("fake.yaml")

    with pytest.raises(ParserError, match="OpenAPI file parsing error"):
        resolver.resolve()


@mock.patch("openapi_parser.resolver.prance.ResolvingParser")
def test_custom_recursion_limit(
    mock_resolving_parser: mock.MagicMock,
) -> None:
    OpenAPIResolver("fake.yaml", recursion_limit=10)

    mock_resolving_parser.assert_called_once_with(
        "fake.yaml",
        spec_string=None,
        backend=mock.ANY,
        strict=False,
        lazy=True,
        recursion_limit=10,
        recursion_limit_handler=_default_recursion_limit_handler,
    )


def test_default_recursion_limit_handler_returns_placeholder() -> None:
    result = _default_recursion_limit_handler(1, "http://example.com#/test")
    assert result == {"type": "object"}
