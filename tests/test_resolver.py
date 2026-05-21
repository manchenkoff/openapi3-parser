from unittest import mock

import prance
import pytest

from openapi_parser.errors import ParserError
from openapi_parser.resolver import OpenAPIResolver


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
