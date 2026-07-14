"""Tests for parser error handling."""

import pytest
from pydantic import ValidationError

from openapi_parser.errors import ParserError
from openapi_parser.parser import parse


def test_missing_required_fields() -> None:
    """Test validation errors for missing required fields (like info)."""
    spec_yaml = """
openapi: "3.0.0"
paths: {}
"""
    with pytest.raises(ParserError) as exc_info:
        parse(spec_string=spec_yaml)

    err = exc_info.value
    assert isinstance(err.__cause__, ValidationError)
    errors = err.errors()
    assert len(errors) > 0

    # Ensure details about the missing field are present
    missing_fields = [e["loc"] for e in errors]
    assert ("info",) in missing_fields


def test_invalid_types() -> None:
    """Test validation errors for invalid data types (e.g. non-string title)."""
    spec_yaml = """
openapi: "3.0.0"
info:
  title: 123
  version: "1.0.0"
paths: {}
"""
    with pytest.raises(ParserError) as exc_info:
        parse(spec_string=spec_yaml)

    err = exc_info.value
    assert isinstance(err.__cause__, ValidationError)
    assert err.errors()


def test_broken_ref() -> None:
    """Test error raised when a reference cannot be resolved."""
    spec_yaml = """
openapi: "3.0.0"
info:
  title: "Broken Ref API"
  version: "1.0.0"
paths:
  /users:
    get:
      responses:
        "200":
          description: "Success"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/NonExistent"
"""
    with pytest.raises(ParserError, match="Failed to resolve references"):
        parse(spec_string=spec_yaml)
