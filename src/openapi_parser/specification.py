"""OpenAPI specification data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from openapi_parser.enumeration import (
    AuthenticationScheme,
    BaseLocation,
    ContentType,
    CookieParameterStyle,
    DataType,
    HeaderParameterStyle,
    IntegerFormat,
    NumberFormat,
    OAuthFlowType,
    OperationMethod,
    ParameterLocation,
    PathParameterStyle,
    QueryParameterStyle,
    SecurityType,
    StringFormat,
)
from openapi_parser.loose_types import (
    LooseContentType,
    LooseIntegerFormat,
    LooseNumberFormat,
    LooseStringFormat,
)


@dataclass
class Contact:
    """API contact information."""

    name: str | None = None
    url: str | None = None
    email: str | None = None


@dataclass
class License:
    """API license information."""

    name: str
    url: str | None = None
    extensions: dict[str, Any] | None = field(default_factory=dict)


@dataclass
class Info:
    """API metadata information."""

    title: str
    version: str
    description: str | None = None
    terms_of_service: str | None = None
    contact: Contact | None = None
    license: License | None = None
    extensions: dict[str, Any] | None = field(default_factory=dict)


@dataclass
class Server:
    """API server definition."""

    url: str
    description: str | None = None
    variables: dict[str, Any] | None = field(default_factory=dict)
    extensions: dict[str, Any] | None = field(default_factory=dict)


@dataclass
class ExternalDoc:
    """External documentation reference."""

    url: str
    description: str | None = None
    extensions: dict[str, Any] | None = field(default_factory=dict)


@dataclass
class Schema:
    """Base schema model."""

    type: DataType
    title: str | None = None
    enum: list[Any] | None = field(default_factory=list)
    example: Any | None = None
    description: str | None = None
    default: Any | None = None
    nullable: bool | None = field(default=False)
    read_only: bool | None = field(default=False)
    write_only: bool | None = field(default=False)
    deprecated: bool | None = field(default=False)
    extensions: dict[str, Any] | None = field(default_factory=dict)

    # all_of: Any  # TODO
    # one_of: Any  # TODO
    # any_of: Any  # TODO
    # not: Any  # TODO


@dataclass
class Integer(Schema):
    """Integer type schema."""

    multiple_of: int | None = None
    maximum: int | None = None
    exclusive_maximum: int | None = None
    minimum: int | None = None
    exclusive_minimum: int | None = None
    format: IntegerFormat | LooseIntegerFormat | None = None


@dataclass
class Number(Schema):
    """Number type schema."""

    multiple_of: float | None = None
    maximum: float | None = None
    exclusive_maximum: float | None = None
    minimum: float | None = None
    exclusive_minimum: float | None = None
    format: NumberFormat | LooseNumberFormat | None = None


@dataclass
class String(Schema):
    """String type schema."""

    max_length: int | None = None
    min_length: int | None = None
    pattern: str | None = None
    format: StringFormat | LooseStringFormat | None = None


@dataclass
class Null(Schema):
    """Null type schema."""

    pass


@dataclass
class Boolean(Schema):
    """Boolean type schema."""

    pass


@dataclass
class Array(Schema):
    """Array type schema."""

    max_items: int | None = None
    min_items: int | None = None
    unique_items: bool | None = None
    items: Schema | None = None


@dataclass
class Discriminator:
    """Polymorphism discriminator."""

    property_name: str
    mapping: dict[str, Any] | None = field(default_factory=dict)


@dataclass
class OneOf(Schema):
    """OneOf composition schema."""

    schemas: list[Schema] = field(default_factory=list)
    discriminator: Discriminator | None = None


@dataclass
class AnyOf(Schema):
    """AnyOf composition schema."""

    schemas: list[Schema] = field(default_factory=list)


@dataclass
class Property:
    """Schema property definition."""

    name: str
    schema: Schema


@dataclass
class Object(Schema):
    """Object type schema."""

    max_properties: int | None = None
    min_properties: int | None = None
    required: list[str] = field(default_factory=list)
    properties: list[Property] = field(default_factory=list)
    # additional_properties: Optional[Union[bool, Schema]] = field(default=True)  # TODO


@dataclass
class Parameter:
    """API parameter definition."""

    name: str
    location: ParameterLocation
    schema: Schema | None = None
    content: list[Content] | None = None
    required: bool | None = field(default=False)
    description: str | None = None
    example: Any | None = None
    examples: dict[str, Any] = field(default_factory=dict)
    # allow_reserved: bool  # TODO
    deprecated: bool | None = field(default=False)
    style: (
        str
        | PathParameterStyle
        | QueryParameterStyle
        | HeaderParameterStyle
        | CookieParameterStyle
        | None
    ) = None
    explode: bool | None = field(default=False)
    extensions: dict[str, Any] | None = field(default_factory=dict)


@dataclass
class Content:
    """Request/response content definition."""

    type: ContentType | LooseContentType
    schema: Schema
    example: Any | None = None
    examples: dict[str, Any] = field(default_factory=dict)
    # encoding: dict[str, Encoding]  # TODO


@dataclass
class RequestBody:
    """Request body definition."""

    content: list[Content]
    description: str | None = None
    required: bool | None = field(default=False)


@dataclass
class Header:
    """Response header definition."""

    name: str
    schema: Schema
    description: str | None = None
    required: bool | None = field(default=False)
    deprecated: bool | None = field(default=False)
    extensions: dict[str, Any] | None = field(default_factory=dict)


@dataclass
class Response:
    """API response definition."""

    is_default: bool
    description: str
    code: int | None = None
    content: list[Content] | None = None
    headers: list[Header] = field(default_factory=list)


@dataclass
class OAuthFlow:
    """OAuth flow definition."""

    refresh_url: str | None = None
    authorization_url: str | None = None
    token_url: str | None = None
    scopes: dict[str, str] = field(default_factory=dict)
    extensions: dict[str, Any] | None = field(default_factory=dict)


@dataclass
class Security:
    """Security scheme definition."""

    type: SecurityType
    location: BaseLocation | None = None
    description: str | None = None
    name: str | None = None
    scheme: AuthenticationScheme | None = None
    bearer_format: str | None = None
    flows: dict[OAuthFlowType, OAuthFlow] = field(default_factory=dict)
    url: str | None = None
    extensions: dict[str, Any] | None = field(default_factory=dict)


@dataclass
class Operation:
    """API operation definition."""

    method: OperationMethod
    responses: list[Response]
    summary: str | None = None
    description: str | None = None
    operation_id: str | None = None
    external_docs: ExternalDoc | None = None
    request_body: RequestBody | None = None
    deprecated: bool | None = field(default=False)
    parameters: list[Parameter] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    security: list[dict[str, Any]] = field(default_factory=list)
    extensions: dict[str, Any] | None = field(default_factory=dict)
    # callbacks: dict[str, Callback] = field(default_factory=dict)  # TODO


@dataclass
class Path:
    """API path definition."""

    url: str
    summary: str | None = None
    description: str | None = None
    operations: list[Operation] = field(default_factory=list)
    parameters: list[Parameter] = field(default_factory=list)
    extensions: dict[str, Any] | None = field(default_factory=dict)


@dataclass
class Tag:
    """API tag definition."""

    name: str
    description: str | None = None
    external_docs: ExternalDoc | None = None


@dataclass
class Specification:
    """Root OpenAPI specification object."""

    version: str
    info: Info
    servers: list[Server] = field(default_factory=list)
    tags: list[Tag] = field(default_factory=list)
    security_schemas: dict[str, Security] = field(default_factory=dict)
    security: list[dict[str, Any]] = field(default_factory=list)
    schemas: dict[str, Schema] = field(default_factory=dict)
    external_docs: ExternalDoc | None = None
    paths: list[Path] = field(default_factory=list)
    extensions: dict[str, Any] | None = field(default_factory=dict)
