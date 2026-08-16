"""Tests for parse() input type handling.

Covers local files (YAML/JSON), `file://` URIs,
and `http://`/`https://` URLs.
"""

import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any
from unittest.mock import patch

import pytest
import yaml

from openapi_parser.errors import ParserError
from openapi_parser.models.v3_0 import Specification
from openapi_parser.parser import parse

MINIMAL_SPEC = {
    "openapi": "3.0.0",
    "info": {"title": "Test", "version": "1.0.0"},
    "paths": {},
}


def _write_minimal(path: str) -> str:
    """Write a minimal valid spec to *path* and return its absolute path."""
    with open(path, "w") as f:
        if path.endswith(".json"):
            json.dump(MINIMAL_SPEC, f)
        else:
            yaml.dump(MINIMAL_SPEC, f)
    return os.path.abspath(path)


# ---------------------------------------------------------------------------
# Local file (YAML)
# ---------------------------------------------------------------------------


def test_parse_local_yaml(tmp_path: object) -> None:
    p = os.path.join(str(tmp_path), "spec.yaml")
    path = _write_minimal(p)
    spec = parse(uri=path)
    assert isinstance(spec, Specification)
    assert spec.openapi == "3.0.0"
    assert spec.info.title == "Test"


# ---------------------------------------------------------------------------
# Local file (JSON)
# ---------------------------------------------------------------------------


def test_parse_local_json(tmp_path: object) -> None:
    p = os.path.join(str(tmp_path), "spec.json")
    path = _write_minimal(p)
    spec = parse(uri=path)
    assert isinstance(spec, Specification)
    assert spec.info.version == "1.0.0"


# ---------------------------------------------------------------------------
# file:// URI
# ---------------------------------------------------------------------------


def test_parse_file_uri(tmp_path: object) -> None:
    p = os.path.join(str(tmp_path), "spec.yaml")
    path = _write_minimal(p)
    file_uri = "file://" + path
    spec = parse(uri=file_uri)
    assert isinstance(spec, Specification)
    assert spec.info.title == "Test"


def test_parse_file_uri_json(tmp_path: object) -> None:
    p = os.path.join(str(tmp_path), "spec.json")
    path = _write_minimal(p)
    file_uri = "file://" + path
    spec = parse(uri=file_uri)
    assert isinstance(spec, Specification)
    assert spec.info.version == "1.0.0"


# ---------------------------------------------------------------------------
# HTTP / HTTPS URL (mocked)
# ---------------------------------------------------------------------------


def _mock_urlopen(spec_dict: dict[str, Any]) -> Any:
    """Return a mock for `urlopen` in parser that returns *spec_dict*."""
    raw_bytes = yaml.dump(spec_dict).encode("utf-8")

    class _Response:
        def __enter__(self) -> "_Response":
            return self

        def __exit__(self, *args: Any) -> None:
            pass

        def read(self) -> bytes:
            return raw_bytes

    return patch(
        "openapi_parser.resolver.urlopen",
        return_value=_Response(),
    )


def test_parse_http_url() -> None:
    with _mock_urlopen(MINIMAL_SPEC):
        spec = parse(uri="http://example.com/spec.yaml")
    assert isinstance(spec, Specification)
    assert spec.info.title == "Test"


def test_parse_https_url() -> None:
    with _mock_urlopen(MINIMAL_SPEC):
        spec = parse(uri="https://example.com/spec.yaml")
    assert isinstance(spec, Specification)
    assert spec.info.version == "1.0.0"


def test_parse_https_url_json() -> None:
    raw_bytes = json.dumps(MINIMAL_SPEC).encode("utf-8")

    class _Response:
        def __enter__(self) -> "_Response":
            return self

        def __exit__(self, *args: Any) -> None:
            pass

        def read(self) -> bytes:
            return raw_bytes

    with patch(
        "openapi_parser.resolver.urlopen",
        return_value=_Response(),
    ):
        spec = parse(uri="https://api.example.org/v3/spec.json")
    assert isinstance(spec, Specification)
    assert spec.openapi == "3.0.0"


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------


def test_no_args_raises() -> None:
    with pytest.raises(ParserError, match="Either uri or spec_string"):
        parse()


def test_nonexistent_file_raises() -> None:
    with pytest.raises(ParserError, match="Failed to load spec"):
        parse(uri="/nonexistent/path/spec.yaml")


def test_nonexistent_file_uri_raises() -> None:
    with pytest.raises(ParserError, match="Failed to load spec"):
        parse(uri="file:///nonexistent/spec.yaml")


def test_http_url_open_failure() -> None:
    """Simulate a network error when fetching a URL."""

    def _fail(*args: Any, **kwargs: Any) -> None:
        raise OSError("Connection refused")

    with (
        patch(
            "openapi_parser.resolver.urlopen",
            _fail,
        ),
        pytest.raises(ParserError, match="Failed to load spec"),
    ):
        parse(uri="http://unknown.example.com/spec.yaml")


def test_callback_shorthand_preserves_extensions() -> None:
    """Callback shorthand (without ``expressions`` key) must keep ``x-*`` keys
    so that ExtensionsMixin._extract_extensions can move them to the
    extensions field."""
    raw = {
        "openapi": "3.0.0",
        "info": {"title": "Test", "version": "1.0.0"},
        "paths": {
            "/test": {
                "get": {
                    "responses": {"200": {"description": "OK"}},
                    "callbacks": {
                        "onData": {
                            "{$request.body#/id}": {
                                "post": {
                                    "responses": {"200": {"description": "Callback OK"}}
                                }
                            },
                            "x-custom": "works",
                        }
                    },
                }
            }
        },
    }
    spec = parse(spec_string=yaml.dump(raw))
    operation = spec.paths["/test"].get
    assert operation is not None
    assert operation.callbacks is not None
    cb = operation.callbacks["onData"]
    assert cb.extensions == {"x-custom": "works"}


# ---------------------------------------------------------------------------
# Reuse a real fixture via file:// (verifies full parse, not just minimal)
# ---------------------------------------------------------------------------


def test_parse_full_via_file_uri() -> None:
    """Parse the openapi_3.0.yaml fixture via a file:// URI."""
    path = os.path.join(os.path.dirname(__file__), "data", "openapi_3.0.yaml")
    file_uri = "file://" + os.path.abspath(path)
    spec = parse(uri=file_uri)
    assert isinstance(spec, Specification)
    assert spec.info.title == "User example service"


def test_ref_cache_isolation_between_parses() -> None:
    """RefCacheMixin caches must not leak between consecutive parse() calls
    when specs share ``$ref`` names. Each call should produce independent
    Python objects."""
    spec_a = """
openapi: "3.0.0"
info:
  title: "A"
  version: "1.0.0"
paths:
  /items:
    get:
      responses:
        "200":
          description: "Success"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Foo"
components:
  schemas:
    Foo:
      type: object
"""

    spec_b = """
openapi: "3.0.0"
info:
  title: "B"
  version: "1.0.0"
paths:
  /items:
    get:
      responses:
        "200":
          description: "Success"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Foo"
components:
  schemas:
    Foo:
      type: string
"""

    parsed_a = parse(spec_string=spec_a)
    parsed_b = parse(spec_string=spec_b)

    assert parsed_a.components is not None
    assert parsed_a.components.schemas is not None
    assert parsed_b.components is not None
    assert parsed_b.components.schemas is not None
    foo_a = parsed_a.components.schemas["Foo"]
    foo_b = parsed_b.components.schemas["Foo"]

    assert foo_a is not foo_b, "Each parse() must produce independent Schema objects"
    assert foo_a.type is not None and foo_a.type.value == "object"
    assert foo_b.type is not None and foo_b.type.value == "string"


# ---------------------------------------------------------------------------
# Nested relative reference resolution
# ---------------------------------------------------------------------------


def test_parse_nested_relative_references(tmp_path: object) -> None:
    """Test resolution of nested relative file references."""
    from openapi_parser.enumeration import DataType
    from openapi_parser.models.v3_0 import Specification

    # Create directory structure
    base_dir = str(tmp_path)
    nested_dir = os.path.join(base_dir, "nested")
    os.makedirs(nested_dir, exist_ok=True)

    main_spec = """
openapi: "3.0.0"
info:
  title: "Main API"
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
                $ref: "nested/first.yaml"
"""

    first_spec = """
type: object
properties:
  value:
    $ref: "second.yaml"
"""

    second_spec = """
type: string
"""

    main_path = os.path.join(base_dir, "main.yaml")
    first_path = os.path.join(nested_dir, "first.yaml")
    second_path = os.path.join(nested_dir, "second.yaml")

    with open(main_path, "w") as f:
        f.write(main_spec)
    with open(first_path, "w") as f:
        f.write(first_spec)
    with open(second_path, "w") as f:
        f.write(second_spec)

    spec = parse(uri=main_path)
    assert isinstance(spec, Specification)

    # Verify resolution
    get_op = spec.paths["/users"].get
    assert get_op is not None
    assert get_op.responses["200"].content is not None
    schema = get_op.responses["200"].content["application/json"].schema_object
    assert schema is not None
    assert schema.properties is not None
    second_prop = schema.properties["value"]
    assert second_prop.type == DataType.STRING


# ---------------------------------------------------------------------------
# pathlib.Path and Extra Fields support
# ---------------------------------------------------------------------------


def test_parse_file_ref_chain(tmp_path: object) -> None:
    """Test resolution when a file ref resolves to content that is itself a $ref.

    main.yaml -> nested/alias.yaml -> nested/target.yaml
    This exercises the recursive resolution inside _resolve_ref_node.
    """
    base_dir = str(tmp_path)
    nested_dir = os.path.join(base_dir, "nested")
    os.makedirs(nested_dir, exist_ok=True)

    main_spec = """
openapi: "3.0.0"
info:
  title: "Main API"
  version: "1.0.0"
paths:
  /items:
    get:
      responses:
        "200":
          description: "Success"
          content:
            application/json:
              schema:
                $ref: "nested/alias.yaml"
"""

    alias_spec = """
$ref: "target.yaml"
"""

    target_spec = """
type: string
"""

    def _write(path: str, content: str) -> None:
        with open(path, "w") as f:
            f.write(content)

    _write(os.path.join(base_dir, "main.yaml"), main_spec)
    _write(os.path.join(nested_dir, "alias.yaml"), alias_spec)
    _write(os.path.join(nested_dir, "target.yaml"), target_spec)

    from openapi_parser.enumeration import DataType

    spec = parse(uri=os.path.join(base_dir, "main.yaml"))
    get_op = spec.paths["/items"].get
    assert get_op is not None
    media_type = get_op.responses["200"].content
    assert media_type is not None
    schema = media_type["application/json"].schema_object
    assert schema is not None
    assert schema.type == DataType.STRING


def test_parse_path_object(tmp_path: object) -> None:
    """Test parsing using a pathlib.Path object instead of a string."""
    from pathlib import Path

    p = Path(str(tmp_path)) / "spec.yaml"
    path = _write_minimal(str(p))
    spec = parse(uri=Path(path))
    assert isinstance(spec, Specification)
    assert spec.info.title == "Test"


def test_schema_allows_extra_fields() -> None:
    """Test that extra fields on Schema (e.g. const) are preserved."""
    spec_yaml = """
openapi: "3.0.0"
info:
  title: "Extra Fields Test"
  version: "1.0.0"
paths:
  /test:
    get:
      responses:
        "200":
          description: "Success"
          content:
            application/json:
              schema:
                type: string
                const: "expected_value"
                prefixItems:
                  - type: integer
"""
    spec = parse(spec_string=spec_yaml)
    get_op = spec.paths["/test"].get
    assert get_op is not None
    assert get_op.responses["200"].content is not None
    schema = get_op.responses["200"].content["application/json"].schema_object
    assert schema is not None
    # Verify extra fields are preserved in model_extra
    assert schema.model_extra is not None
    assert schema.model_extra.get("const") == "expected_value"
    assert schema.model_extra.get("prefixItems") == [{"type": "integer"}]


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_parse_isolated_across_threads() -> None:
    """Concurrent parse() calls in different threads must not share ref caches."""
    spec_a = """
openapi: "3.0.0"
info:
  title: "A"
  version: "1.0.0"
paths:
  /items:
    get:
      responses:
        "200":
          description: "Success"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Foo"
components:
  schemas:
    Foo:
      type: object
"""

    spec_b = """
openapi: "3.0.0"
info:
  title: "B"
  version: "1.0.0"
paths:
  /items:
    get:
      responses:
        "200":
          description: "Success"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Foo"
components:
  schemas:
    Foo:
      type: string
"""

    barrier = threading.Barrier(2)
    results: dict[str, Specification] = {}

    def run(key: str, text: str) -> None:
        barrier.wait()
        results[key] = parse(spec_string=text)

    with ThreadPoolExecutor(max_workers=2) as pool:
        pool.submit(run, "a", spec_a)
        pool.submit(run, "b", spec_b)

    components_a = results["a"].components
    components_b = results["b"].components
    assert components_a is not None and components_a.schemas is not None
    assert components_b is not None and components_b.schemas is not None
    foo_a = components_a.schemas["Foo"]
    foo_b = components_b.schemas["Foo"]

    assert foo_a is not foo_b
    assert foo_a.type is not None and foo_a.type.value == "object"
    assert foo_b.type is not None and foo_b.type.value == "string"


# ---------------------------------------------------------------------------
# spec_string + base_uri (external refs)
# ---------------------------------------------------------------------------


def test_parse_spec_string_with_base_uri(tmp_path: object) -> None:
    """External $refs resolve when parsing spec_string with a base_uri."""
    refs_dir = os.path.join(str(tmp_path), "refs")
    os.makedirs(refs_dir, exist_ok=True)

    ref_path = os.path.join(refs_dir, "user.yaml")
    with open(ref_path, "w") as f:
        f.write("type: string\n")

    spec_text = """
openapi: "3.0.0"
info:
  title: "Base URI API"
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
                $ref: "user.yaml"
"""
    base = os.path.join(refs_dir, "main.yaml")

    spec = parse(spec_string=spec_text, base_uri=base)
    get_op = spec.paths["/users"].get
    assert get_op is not None
    media_type = get_op.responses["200"].content
    assert media_type is not None
    schema = media_type["application/json"].schema_object
    assert schema is not None
    assert schema.type is not None and schema.type.value == "string"


# ---------------------------------------------------------------------------
# Callback serialization
# ---------------------------------------------------------------------------


def test_callback_roundtrip_dump() -> None:
    """Callback.model_dump() must produce the spec-compliant flat map."""
    spec_yaml = """
openapi: "3.0.0"
info:
  title: "Callback Test"
  version: "1.0.0"
paths:
  /test:
    get:
      responses:
        "200":
          description: "OK"
      callbacks:
        onData:
          "{$request.body#/id}":
            post:
              responses:
                "200":
                  description: "Callback OK"
          x-custom: "works"
"""
    spec = parse(spec_string=spec_yaml)
    get_op = spec.paths["/test"].get
    assert get_op is not None
    callbacks = get_op.callbacks
    assert callbacks is not None
    callback = callbacks["onData"]

    dumped = callback.model_dump()
    assert "{$request.body#/id}" in dumped
    assert (
        dumped["{$request.body#/id}"]["post"]["responses"]["200"]["description"]
        == "Callback OK"
    )
    assert dumped["x-custom"] == "works"
    assert "expressions" not in dumped


# ---------------------------------------------------------------------------
# PathItem servers + mutualTLS security scheme
# ---------------------------------------------------------------------------


def test_path_item_servers() -> None:
    """PathItem must support the spec-compliant servers field."""
    spec_yaml = """
openapi: "3.0.0"
info:
  title: "Servers on Path"
  version: "1.0.0"
paths:
  /test:
    servers:
      - url: "https://staging.example.com"
    get:
      responses:
        "200":
          description: "OK"
"""
    spec = parse(spec_string=spec_yaml)
    path_item = spec.paths["/test"]
    assert path_item.servers is not None
    assert path_item.servers[0].url == "https://staging.example.com"


def test_mutual_tls_security_scheme() -> None:
    """OpenAPI 3.1 mutualTLS security scheme type must parse."""
    from openapi_parser.enumeration import SecurityType

    spec_yaml = """
openapi: "3.1.0"
info:
  title: "mutualTLS Test"
  version: "1.0.0"
paths: {}
components:
  securitySchemes:
    mTLS:
      type: mutualTLS
"""
    spec = parse(spec_string=spec_yaml)
    assert spec.components is not None
    assert spec.components.security_schemes is not None
    assert spec.components.security_schemes["mTLS"].type == SecurityType.MUTUAL_TLS


# ---------------------------------------------------------------------------
# Enumeration export & Component sections resolution
# ---------------------------------------------------------------------------


def test_enumeration_export() -> None:
    """Ensure that the enumeration module is exported at the top-level package."""
    import openapi_parser

    assert hasattr(openapi_parser, "enumeration")
    from openapi_parser.enumeration import DataType

    assert openapi_parser.enumeration.DataType is DataType


def test_path_items_resolver_annotation() -> None:
    """Ensure pathItems components are correctly resolved and annotated with ref_name in v3.1."""
    spec_yaml = """
openapi: "3.1.0"
info:
  title: "pathItems component test"
  version: "1.0.0"
paths:
  /users:
    $ref: "#/components/pathItems/UserPath"
components:
  pathItems:
    UserPath:
      get:
        responses:
          "200":
            description: "OK"
"""
    spec = parse(spec_string=spec_yaml)
    assert "/users" in spec.paths
    path_item = spec.paths["/users"]
    assert path_item.ref_name == "#/components/pathItems/UserPath"
    assert path_item.get is not None
