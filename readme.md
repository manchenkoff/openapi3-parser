# OpenAPI Parser

A simple package to parse your OpenAPI 3 documents into Python object to work with.

## How to install

To install package run the following command

```
pip install openapi-parser
```

## How to use

Example of parser usage

```
>>> from openapi_parser import parse
>>> content = parse('swagger.yml')
>>> print(content)
```

## Supported specification schemas
- [x] Contact
- [x] License
- [x] Info
- [x] Server
- [x] ExternalDoc
- [x] Tag
- [x] Schema
- [x] Integer schema
- [x] Number schema
- [x] String schema
- [x] Array schema
- [x] Object schema
- [x] Property
- [x] Parameter
- [x] Header
- [x] Content
- [x] RequestBody
- [ ] Response
- [ ] Security
- [ ] ApiKeySecurity
- [ ] HttpSecurity
- [ ] OAuthFlow
- [ ] OAuth2Security
- [ ] OpenIdConnectSecurity
- [ ] Operation
- [ ] PathItem
- [ ] Path
- [ ] Specification

## Features

- [x] OpenAPI's validation with `openapi-spec-validator`
- [x] Parsing all the sections into Python `dataclass`
- [x] Support many `Enum` values to simplify work with `format`, `type`, etc
- [x] Auto-resolve `$ref` links with [Prance](https://pypi.org/project/prance)
- [ ] Support custom `x-*` [attributes](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#specification-extensions)
- [ ] Support automatic merge `allOf` schemas into one while resolving
- [ ] Support `oneOf` schemas
- [ ] Support `anyOf` schemas
- [ ] Support `not` schemas
- [ ] Support `Parameter` [serialization style](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#fixed-fields-10)
- [ ] Support `discriminator` model types
- [ ] Support additional properties in dataclasses (like `example`, `style`, `explode`, etc)