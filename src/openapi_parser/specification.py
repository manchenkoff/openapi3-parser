from dataclasses import dataclass, field
from typing import Any, Optional, Union

from .enumeration import *
from .loose_types import (
    LooseContentType,
    LooseIntegerFormat,
    LooseNumberFormat,
    LooseStringFormat,
)


@dataclass
class Contact:
    name: Optional[str] = None
    url: Optional[str] = None
    email: Optional[str] = None


@dataclass
class License:
    name: str
    url: Optional[str] = None
    extensions: Optional[dict] = field(default_factory=dict)


@dataclass
class Info:
    title: str
    version: str
    description: Optional[str] = None
    terms_of_service: Optional[str] = None
    contact: Optional[Contact] = None
    license: Optional[License] = None
    extensions: Optional[dict] = field(default_factory=dict)


@dataclass
class Server:
    url: str
    description: Optional[str] = None
    variables: Optional[dict] = field(default_factory=dict)
    extensions: Optional[dict] = field(default_factory=dict)


@dataclass
class ExternalDoc:
    url: str
    description: Optional[str] = None
    extensions: Optional[dict] = field(default_factory=dict)


@dataclass
class Schema:
    type: DataType
    title: Optional[str] = None
    enum: Optional[list[Any]] = field(default_factory=list)
    example: Optional[Any] = None
    description: Optional[str] = None
    default: Optional[Any] = None
    nullable: Optional[bool] = field(default=False)
    read_only: Optional[bool] = field(default=False)
    write_only: Optional[bool] = field(default=False)
    deprecated: Optional[bool] = field(default=False)
    extensions: Optional[dict] = field(default_factory=dict)

    # all_of: Any  # TODO
    # one_of: Any  # TODO
    # any_of: Any  # TODO
    # not: Any  # TODO


@dataclass
class Integer(Schema):
    multiple_of: Optional[int] = None
    maximum: Optional[int] = None
    exclusive_maximum: Optional[int] = None
    minimum: Optional[int] = None
    exclusive_minimum: Optional[int] = None
    format: Optional[Union[IntegerFormat, LooseIntegerFormat]] = None


@dataclass
class Number(Schema):
    multiple_of: Optional[float] = None
    maximum: Optional[float] = None
    exclusive_maximum: Optional[float] = None
    minimum: Optional[float] = None
    exclusive_minimum: Optional[float] = None
    format: Optional[Union[NumberFormat, LooseNumberFormat]] = None


@dataclass
class String(Schema):
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    pattern: Optional[str] = None
    format: Optional[Union[StringFormat, LooseStringFormat]] = None


@dataclass
class Null(Schema):
    pass


@dataclass
class Boolean(Schema):
    pass


@dataclass
class Array(Schema):
    max_items: Optional[int] = None
    min_items: Optional[int] = None
    unique_items: Optional[bool] = None
    items: Schema = None  # type: ignore


@dataclass
class Discriminator:
    property_name: str
    mapping: Optional[dict] = field(default_factory=dict)


@dataclass
class OneOf(Schema):
    schemas: list[Schema] = field(default_factory=list)
    discriminator: Optional[Discriminator] = None


@dataclass
class AnyOf(Schema):
    schemas: list[Schema] = field(default_factory=list)


@dataclass
class Property:
    name: str
    schema: Schema


@dataclass
class Object(Schema):
    max_properties: Optional[int] = None
    min_properties: Optional[int] = None
    required: list[str] = field(default_factory=list)
    properties: list[Property] = field(default_factory=list)
    # additional_properties: Optional[Union[bool, Schema]] = field(default=True)  # TODO


@dataclass
class Parameter:
    name: str
    location: ParameterLocation
    schema: Optional[Schema] = None
    content: Optional[list['Content']] = None
    required: Optional[bool] = field(default=False)
    description: Optional[str] = None
    # example: Optional[Any]  # TODO
    # examples: list[Any] = field(default_factory=list)  # TODO
    # allow_reserved: bool  # TODO
    deprecated: Optional[bool] = field(default=False)
    style: Optional[str] = None
    explode: Optional[bool] = field(default=False)
    extensions: Optional[dict] = field(default_factory=dict)


@dataclass
class Content:
    type: Union[ContentType, LooseContentType]
    schema: Schema
    example: Optional[Any] = None
    examples: dict[str, Any] = field(default_factory=dict)
    # encoding: dict[str, Encoding]  # TODO


@dataclass
class RequestBody:
    content: list[Content]
    description: Optional[str] = None
    required: Optional[bool] = field(default=False)


@dataclass
class Header:
    name: str
    schema: Schema
    description: Optional[str] = None
    required: Optional[bool] = field(default=False)
    deprecated: Optional[bool] = field(default=False)
    extensions: Optional[dict] = field(default_factory=dict)


@dataclass
class Response:
    is_default: bool
    description: str
    code: Optional[int] = None
    content: Optional[list[Content]] = None
    headers: list[Header] = field(default_factory=list)
    # links: dict[str, Link]  # TODO


@dataclass
class OAuthFlow:
    refresh_url: Optional[str] = None
    authorization_url: Optional[str] = None
    token_url: Optional[str] = None
    scopes: dict[str, str] = field(default_factory=dict)
    extensions: Optional[dict] = field(default_factory=dict)


@dataclass
class Security:
    type: SecurityType
    location: Optional[BaseLocation] = None
    description: Optional[str] = None
    name: Optional[str] = None
    scheme: Optional[AuthenticationScheme] = None
    bearer_format: Optional[str] = None
    flows: dict[OAuthFlowType, OAuthFlow] = field(default_factory=dict)
    url: Optional[str] = None
    extensions: Optional[dict] = field(default_factory=dict)


@dataclass
class Operation:
    method: OperationMethod
    responses: list[Response]
    summary: Optional[str] = None
    description: Optional[str] = None
    operation_id: Optional[str] = None
    external_docs: Optional[ExternalDoc] = None
    request_body: Optional[RequestBody] = None
    deprecated: Optional[bool] = field(default=False)
    parameters: list[Parameter] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    security: list[dict[str, Any]] = field(default_factory=list)
    extensions: Optional[dict] = field(default_factory=dict)
    # callbacks: dict[str, Callback] = field(default_factory=dict)  # TODO


@dataclass
class Path:
    url: str
    summary: Optional[str] = None
    description: Optional[str] = None
    operations: list[Operation] = field(default_factory=list)
    parameters: list[Parameter] = field(default_factory=list)
    extensions: Optional[dict] = field(default_factory=dict)


@dataclass
class Tag:
    name: str
    description: Optional[str] = None
    external_docs: Optional[ExternalDoc] = None


@dataclass
class Specification:
    version: str
    info: Info
    servers: list[Server] = field(default_factory=list)
    tags: list[Tag] = field(default_factory=list)
    security_schemas: dict[str, Security] = field(default_factory=dict)
    security: list[dict[str, Any]] = field(default_factory=list)
    schemas: dict[str, Schema] = field(default_factory=dict)
    external_docs: Optional[ExternalDoc] = None
    paths: list[Path] = field(default_factory=list)
    extensions: Optional[dict] = field(default_factory=dict)
