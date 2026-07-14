"""OpenAPI 3.0 specification models."""

from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from openapi_parser.enumeration import (
    ApiKeyLocation,
    CookieParameterStyle,
    DataType,
    HeaderParameterStyle,
    OAuthFlowType,
    ParameterLocation,
    PathParameterStyle,
    QueryParameterStyle,
    SecurityType,
)
from openapi_parser.models.base import (
    Discriminator,
    ExternalDoc,
    Info,
    Link,
    OAuthFlow,
    Server,
    _ModelBase,
    _MutableModelBase,
)
from openapi_parser.models.mixins import ExtensionsMixin, RefCacheMixin


class Schema(ExtensionsMixin, RefCacheMixin, _MutableModelBase):
    """Schema object for data definition.

    Not frozen to allow in-place update of placeholders during
    circular $ref resolution. Object identity is preserved via
    RefCacheMixin's dedup cache.
    """

    type: DataType | None = None
    title: str | None = None
    description: str | None = None
    enum: list[Any] | None = None
    example: Any | None = None
    default: Any | None = None
    nullable: bool | None = None
    read_only: bool | None = Field(default=None, alias="readOnly")
    write_only: bool | None = Field(default=None, alias="writeOnly")
    deprecated: bool = False

    # Numeric
    multiple_of: int | float | None = Field(default=None, alias="multipleOf")
    maximum: int | float | None = None
    exclusive_maximum: int | float | None = Field(
        default=None, alias="exclusiveMaximum"
    )
    minimum: int | float | None = None
    exclusive_minimum: int | float | None = Field(
        default=None,
        alias="exclusiveMinimum",
    )

    # String
    max_length: int | None = Field(default=None, alias="maxLength")
    min_length: int | None = Field(default=None, alias="minLength")
    pattern: str | None = None

    # Array
    max_items: int | None = Field(default=None, alias="maxItems")
    min_items: int | None = Field(default=None, alias="minItems")
    unique_items: bool | None = Field(default=None, alias="uniqueItems")
    items: Schema | None = None

    # Object
    properties: dict[str, Schema] | None = None
    additional_properties: bool | Schema | None = Field(
        default=None,
        alias="additionalProperties",
    )
    required: list[str] = Field(default_factory=list)
    max_properties: int | None = Field(default=None, alias="maxProperties")
    min_properties: int | None = Field(default=None, alias="minProperties")

    # Composition
    all_of: list[Schema] | None = Field(default=None, alias="allOf")
    one_of: list[Schema] | None = Field(default=None, alias="oneOf")
    any_of: list[Schema] | None = Field(default=None, alias="anyOf")
    not_schema: Schema | None = Field(default=None, alias="not")

    # Meta
    format: str | None = None
    discriminator: Discriminator | None = None
    xml: dict[str, Any] | None = None
    external_docs: ExternalDoc | None = Field(default=None, alias="externalDocs")


class Header(ExtensionsMixin, RefCacheMixin, _ModelBase):
    """Header object definition."""

    schema: Schema | None = Field(default=None)  # type: ignore[assignment]  # shadows BaseModel.schema()
    description: str | None = None
    required: bool | None = None
    deprecated: bool = False


class Encoding(ExtensionsMixin, _ModelBase):
    """Encoding object definition."""

    content_type: str | None = Field(default=None, alias="contentType")
    headers: dict[str, Header] | None = None
    style: (
        PathParameterStyle
        | QueryParameterStyle
        | HeaderParameterStyle
        | CookieParameterStyle
        | None
    ) = None
    explode: bool | None = None
    allow_reserved: bool | None = Field(default=None, alias="allowReserved")


class Example(ExtensionsMixin, RefCacheMixin, _ModelBase):
    """Example object definition."""

    summary: str | None = None
    description: str | None = None
    value: Any | None = None
    external_value: str | None = Field(default=None, alias="externalValue")


class MediaType(ExtensionsMixin, _ModelBase):
    """Media Type object definition."""

    schema: Schema | None = Field(default=None)  # type: ignore[assignment]  # shadows BaseModel.schema()
    example: Any | None = None
    examples: dict[str, Example] | None = None
    encoding: dict[str, Encoding] | None = None


class Parameter(ExtensionsMixin, RefCacheMixin, _ModelBase):
    """Parameter object definition."""

    name: str
    location: ParameterLocation = Field(alias="in")
    description: str | None = None
    required: bool | None = None
    deprecated: bool = False
    allow_empty_value: bool | None = Field(default=None, alias="allowEmptyValue")
    style: (
        PathParameterStyle
        | QueryParameterStyle
        | HeaderParameterStyle
        | CookieParameterStyle
        | None
    ) = None
    explode: bool | None = None
    allow_reserved: bool | None = Field(default=None, alias="allowReserved")
    schema: Schema | None = Field(default=None)  # type: ignore[assignment]  # shadows BaseModel.schema()
    example: Any | None = None
    examples: dict[str, Example] | None = None
    content: dict[str, MediaType] | None = None


class RequestBody(ExtensionsMixin, RefCacheMixin, _ModelBase):
    """Request Body object definition."""

    description: str | None = None
    content: dict[str, MediaType]
    required: bool | None = None


class Response(ExtensionsMixin, RefCacheMixin, _ModelBase):
    """Response object definition."""

    description: str
    headers: dict[str, Header] | None = None
    content: dict[str, MediaType] | None = None
    links: dict[str, Link] | None = None


class Callback(ExtensionsMixin, _ModelBase):
    """A map of expressions to PathItem objects."""

    expressions: dict[str, PathItem]

    @model_validator(mode="before")
    @classmethod
    def _parse_callback(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "expressions" in data:
                return data

            expressions = {}
            rest: dict[str, Any] = {}

            for k, v in data.items():
                if k.startswith("x-"):
                    rest[k] = v
                else:
                    expressions[k] = v

            return {"expressions": expressions, **rest}

        return data


class Operation(ExtensionsMixin, _ModelBase):
    """Operation object definition."""

    summary: str | None = None
    description: str | None = None
    operation_id: str | None = Field(default=None, alias="operationId")
    parameters: list[Parameter] | None = None
    request_body: RequestBody | None = Field(default=None, alias="requestBody")
    responses: dict[str, Response]
    callbacks: dict[str, Callback] | None = None
    deprecated: bool = False
    security: list[dict[str, list[str]]] | None = None
    servers: list[Server] | None = None
    tags: list[str] | None = None
    external_docs: ExternalDoc | None = Field(default=None, alias="externalDocs")

    @model_validator(mode="before")
    @classmethod
    def _coerce_response_keys(cls, data: Any) -> Any:
        if (
            isinstance(data, dict)
            and "responses" in data
            and isinstance(data["responses"], dict)
        ):
            data["responses"] = {str(k): v for k, v in data["responses"].items()}

        return data


class PathItem(ExtensionsMixin, RefCacheMixin, _ModelBase):
    """Path Item object definition."""

    summary: str | None = None
    description: str | None = None
    get: Operation | None = None
    put: Operation | None = None
    post: Operation | None = None
    delete: Operation | None = None
    options: Operation | None = None
    head: Operation | None = None
    patch: Operation | None = None
    trace: Operation | None = None
    parameters: list[Parameter] | None = None


class SecurityScheme(ExtensionsMixin, RefCacheMixin, _ModelBase):
    """Security Scheme object definition."""

    type: SecurityType
    description: str | None = None
    name: str | None = None
    location: ApiKeyLocation | None = Field(default=None, alias="in")
    scheme: str | None = None
    bearer_format: str | None = Field(default=None, alias="bearerFormat")
    flows: dict[OAuthFlowType, OAuthFlow] | None = None
    open_id_connect_url: str | None = Field(default=None, alias="openIdConnectUrl")


class Tag(ExtensionsMixin, _ModelBase):
    """Tag object definition."""

    name: str
    description: str | None = None
    external_docs: ExternalDoc | None = Field(default=None, alias="externalDocs")


class Components(ExtensionsMixin, _ModelBase):
    """Components object definition."""

    schemas: dict[str, Schema] | None = None
    responses: dict[str, Response] | None = None
    parameters: dict[str, Parameter] | None = None
    examples: dict[str, Example] | None = None
    request_bodies: dict[str, RequestBody] | None = Field(
        default=None,
        alias="requestBodies",
    )
    headers: dict[str, Header] | None = None
    security_schemes: dict[str, SecurityScheme] | None = Field(
        default=None,
        alias="securitySchemes",
    )
    links: dict[str, Link] | None = None
    callbacks: dict[str, Callback] | None = None
    path_items: dict[str, PathItem] | None = Field(default=None, alias="pathItems")


class Specification(ExtensionsMixin, _ModelBase):
    """OpenAPI 3.0 specification root object."""

    openapi: str = "3.0.0"
    info: Info
    servers: list[Server] = []
    paths: dict[str, PathItem]
    components: Components | None = None
    security: list[dict[str, list[str]]] | None = None
    tags: list[Tag] | None = None
    external_docs: ExternalDoc | None = Field(default=None, alias="externalDocs")
