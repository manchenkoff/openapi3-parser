# Swagger Parser

A simple package to parse your Swagger API documents into Python object to work with.

## How to install

To install package run the following command

```
pip install swagger-parser
```

## How to use

Example of parser usage

```
>>> from swagger_parser import parse
>>> content = parse('swagger.yml')
>>> print(content)
```

## Parsers
- [x] Info (including Contact, License)
- [x] Server
- [x] ExternalDoc
- [x] Tag
- [ ] Schema
- [ ] Integer
- [ ] Number
- [ ] String
- [ ] Array
- [ ] Object
- [ ] Property
- [ ] Parameter
- [ ] Content
- [ ] RequestBody
- [ ] Header
- [ ] Response
- [ ] Security
- [ ] OAuthFlow
- [ ] Operation
- [ ] PathItem
- [ ] Path
- [ ] Specification

## Features

- [x] Swagger validation with `openapi-spec-validator`
- [x] Parsing all the sections into Python `dataclass`
- [x] Support many `Enum` values to simplify work with `format`, `type`, etc
- [x] Auto-resolve `$ref` links
- [ ] Use own parsing method instead of [Prance](https://pypi.org/project/prance) package to resolve `$ref` items' names
- [ ] Support custom `x-*` [attributes](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#specification-extensions)
- [ ] Support merge `allOf` schemas into one
- [ ] Support `oneOf` schemas
- [ ] Support `anyOf` schemas
- [ ] Support `not` schemas
- [ ] Support `Parameter` [serialization style](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#fixed-fields-10)
- [ ] Support `discriminator` model types
- [ ] Support additional properties in dataclasses (like `example`, `style`, `explode`, etc)