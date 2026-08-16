# OpenAPI Parser

[![PyPI - Version](https://img.shields.io/pypi/v/openapi3-parser)](https://pypi.org/project/openapi3-parser/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/openapi3-parser)](https://clickpy.clickhouse.com/dashboard/openapi3-parser)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openapi3-parser)](https://pypi.org/project/openapi3-parser/)
[![PyPI - Format](https://img.shields.io/pypi/format/openapi3-parser)](https://pypi.org/project/openapi3-parser/)

Parse OpenAPI and Swagger documents into fully typed Pydantic models.
Navigate your API specification programmatically — servers, paths,
operations, parameters, schemas, security schemes, and more.

| Version | Status         |
| ------- | -------------- |
| 2.0     | Supported*     |
| 3.0     | Supported      |
| 3.1     | Supported      |
| 3.2     | Supported      |

\* Swagger 2.0 documents are normalized to OpenAPI 3.0.

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

# From raw string with external $refs (resolved relative to base_uri)
spec = parse(
    spec_string=open("specs/openapi.yml").read(),
    base_uri="file:///abs/path/specs/openapi.yml",
)
```

### Navigate servers, paths, and operations

```python
specification = parse("swagger.yml")

# List all servers
for server in specification.servers:
    print(f"{server.description} - {server.url}")

# Iterate paths and their HTTP methods
for path, path_item in specification.paths.items():
    methods = ", ".join(
        method for method in ("get", "put", "post", "delete", "patch")
        if getattr(path_item, method) is not None
    )
    print(f"{path}: [{methods}]")

# Inspect operation details
for path_item in specification.paths.values():
    get_op = path_item.get
    if get_op is None:
        continue
    print(f"[GET] {path}: {get_op.summary}")
    if get_op.deprecated:
        print("  (deprecated)")
    if get_op.operation_id:
        print(f"  operationId: {get_op.operation_id}")
```

### Follow `$ref` references

`$ref` entries are resolved in place and annotated with a `ref_name`
pointing back to their canonical location:

```python
schema = specification.components.schemas["Pet"]
print(schema.ref_name)  # "#/components/schemas/Pet"
```

### Error Handling

```python
from openapi_parser.errors import ParserError

try:
    spec = parse("invalid.yml")
except ParserError as e:
    print(f"Parsing failed: {e}")
    for detail in e.errors():
        print(detail["loc"], detail["msg"])
```

## Data Model

Parsed documents return a `Specification` object composed of fully typed
Pydantic models:

| Model            | Description |
| ---------------- | ----------- |
| `Specification`  | Root document — openapi, info, servers, paths, components, security |
| `Info`           | API metadata — title, version, description, contact, license |
| `Server`         | Server definition — url, description, variables |
| `PathItem`       | URL path — get/post/put/delete/patch, parameters, servers |
| `Operation`      | HTTP method — responses, parameters, request body, security |
| `Parameter`      | Path/query/header/cookie param — schema, style, required |
| `Response`       | Status code, description, content, headers |
| `RequestBody`    | Content, description, required |
| `MediaType`      | Media type — schema, example, encoding |
| `Schema`         | Data definition — type, properties, items, composition |
| `Components`     | Reusable schemas, responses, parameters, examples, headers, ... |
| `SecurityScheme` | Security scheme — apiKey, http, oauth2, openIdConnect, mutualTLS |
| `OAuthFlow`      | OAuth flow — authorization, token, scopes |
| `Header`         | Response header — name, schema, description |
| `Link`           | Link definition — operation, parameters, request body |
| `Example`        | Example — value, summary, externalValue |
| `Tag`            | Tag with optional external docs |
| `ExternalDoc`    | External documentation reference |
| `Discriminator`  | Polymorphism discriminator — property name, mapping |

See the [models](src/openapi_parser/models/) package for all available
fields and types.

## Development

```bash
# Install with dev dependencies
uv sync --dev

# Lint
uv run ruff check src/ tests/
uv run mypy src/ tests/
uv run ty check

# Test
uv run pytest

# Format
uv run ruff format src/ tests/
```
