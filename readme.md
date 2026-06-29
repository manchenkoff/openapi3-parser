# OpenAPI Parser

[![PyPI - Version](https://img.shields.io/pypi/v/openapi3-parser)](https://pypi.org/project/openapi3-parser/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/openapi3-parser)](https://clickpy.clickhouse.com/dashboard/openapi3-parser)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openapi3-parser)](https://pypi.org/project/openapi3-parser/)
[![PyPI - Format](https://img.shields.io/pypi/format/openapi3-parser)](https://pypi.org/project/openapi3-parser/)

Parse OpenAPI 3 documents into fully typed Python dataclass objects.
Navigate your API specification programmatically — servers, paths,
operations, parameters, schemas, security schemes, and more.

| Version | Status         |
| ------- | -------------- |
| 2.0     | Deprecated     |
| 3.0     | **Supported**  |
| 3.1     | In development |

## Installation

```bash
pip install openapi3-parser
```

## Quick Start

```python
from openapi_parser import parse

specification = parse("swagger.yml")
print(specification.info.title)  # e.g. "User example service"
```

## Use Cases

### Parse from different sources

```python
# From file path
spec = parse("specs/openapi.yml")

# From URL
spec = parse("https://example.com/openapi.json")

# From raw string
spec = parse(spec_string="""
openapi: "3.0.0"
info:
  title: My API
  version: "1.0.0"
paths: {}
""")
```

### Navigate servers, paths, and operations

```python
specification = parse("swagger.yml")

# List all servers
for server in specification.servers:
    print(f"{server.description} - {server.url}")

# List all paths and their HTTP methods
for path in specification.paths:
    methods = ", ".join(op.method.value for op in path.operations)
    print(f"{path.url}: [{methods}]")

# Inspect operation details
for path in specification.paths:
    for op in path.operations:
        print(f"[{op.method.value}] {path.url}: {op.summary}")
        if op.deprecated:
            print("  (deprecated)")
        if op.operation_id:
            print(f"  operationId: {op.operation_id}")
```

### Enum strictness

By default, content types, string formats, and other enum fields are validated
against predefined enums. For specs that use custom values, pass
`strict_enum=False`:

```python
# Accepts non-standard content types like "application/vnd.api+json"
spec = parse("swagger.yml", strict_enum=False)
```

When strict mode is off, unrecognized values are wrapped in a `LooseEnum`
object instead of raising an error.

### Error Handling

```python
from openapi_parser.errors import ParserError

try:
    spec = parse("invalid.yml")
except ParserError as e:
    print(f"Parsing failed: {e}")
```

## Data Model

Parsed documents return a `Specification` object composed of fully typed
dataclasses:

| Model           | Description |
| --------------- | ----------- |
| `Specification` | Root document — version, info, servers, paths, schemas, security |
| `Info`          | API metadata — title, version, description, contact, license |
| `Server`        | Server definition — url, description, variables |
| `Path`          | URL path — operations, parameters |
| `Operation`     | HTTP method — responses, parameters, request body, security |
| `Parameter`     | Path/query/header/cookie param — schema, style, required |
| `Response`      | Status code, description, content, headers |
| `RequestBody`   | Content, description, required |
| `Content`       | Media type, schema, example |
| `Schema`        | Base type — Integer, Number, String, Boolean, Array, Object, Null |
| `Property`      | Object property — name, schema |
| `OneOf`/`AnyOf` | Composition schemas with discriminator support |
| `Security`      | Security scheme — apiKey, http, oauth2, openIdConnect |
| `OAuthFlow`     | OAuth flow — authorization, token, scopes |
| `Header`        | Response header — name, schema, description |
| `Tag`           | Tag with optional external docs |
| `ExternalDoc`   | External documentation reference |
| `Discriminator` | Polymorphism discriminator — property name, mapping |

See the [specification module](src/openapi_parser/specification.py) for
all available fields and types.

## Development

```bash
# Install with dev dependencies
uv sync --dev

# Lint
uv run ruff check .
uv run mypy .
uv run ty check .

# Test
uv run pytest

# Format
uv run ruff format .
```
