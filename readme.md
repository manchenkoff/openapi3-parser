# OpenAPI Parser

A simple package to parse your OpenAPI 3 documents into Python object to work with.

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

urls = [x.pattern for x in specification.paths]

print(urls)

# Output
#
# >> ['/users', '/users/{uuid}']
```

Get operation with supported HTTP methods

```python
from openapi_parser import parse

specification = parse('tests/data/swagger.yml')

for operation in specification.paths:
    pattern = operation.pattern
    supported_methods = ','.join([x.name for x in operation.item.operations])
    
    print(f"Operation: {pattern}, methods: {supported_methods}")

# Output
#
# >> Operation: /users, methods: GET,POST
# >> Operation: /users/{uuid}, methods: GET,PUT
```