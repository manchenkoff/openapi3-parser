# OpenAPI Parser

![PyPI - Version](https://img.shields.io/pypi/v/openapi3-parser)
![PyPI - Downloads](https://img.shields.io/pypi/dm/openapi3-parser)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openapi3-parser)
![PyPI - Format](https://img.shields.io/pypi/format/openapi3-parser)
![PyPI - License](https://img.shields.io/pypi/l/openapi3-parser)

A simple package to parse your OpenAPI 3 documents into Python object to work with.

Supported versions:

| Version | Status         |
| ------- | -------------- |
| 2.0     | Deprecated     |
| 3.0     | **Supported**  |
| 3.1     | In development |

## How to install

To install package run the following command

```
pip install openapi3-parser
```

## How to use

Example of parser usage

```
>>> from openapi_parser import parse
>>> content = parse('swagger.yml')
>>> print(content)
```

Get application servers

```python
from openapi_parser import parse

specification = parse('data/swagger.yml')

print("Application servers")

for server in specification.servers:
    print(f"{server.description} - {server.url}")

# Output
#
# >> Application servers
# >> production - https://users.app
# >> staging - http://stage.users.app
# >> development - http://users.local
```

Get list of application URLs

```python
from openapi_parser import parse

specification = parse('tests/data/swagger.yml')

urls = [x.url for x in specification.paths]

print(urls)

# Output
#
# >> ['/users', '/users/{uuid}']
```

Get operation with supported HTTP methods

```python
from openapi_parser import parse

specification = parse('tests/data/swagger.yml')

for path in specification.paths:
    supported_methods = ','.join([x.method.value for x in path.operations])

    print(f"Operation: {path.url}, methods: {supported_methods}")

# Output
#
# >> Operation: /users, methods: get,post
# >> Operation: /users/{uuid}, methods: get,put
```
