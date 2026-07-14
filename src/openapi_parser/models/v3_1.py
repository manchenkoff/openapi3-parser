"""OpenAPI 3.1/3.2 specification models."""

from __future__ import annotations

from pydantic import Field

from openapi_parser.enumeration import DataType
from openapi_parser.models import v3_0
from openapi_parser.models.base import ExternalDoc, _ModelBase
from openapi_parser.models.mixins import ExtensionsMixin


class Schema(v3_0.Schema):
    """Schema object for data definition in OpenAPI 3.1+."""

    type: DataType | list[DataType] | None = None  # type: ignore[assignment]  # 3.1 allows type as array
    items: Schema | None = None
    properties: dict[str, Schema] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Schema
    additional_properties: bool | Schema | None = Field(
        default=None,
        alias="additionalProperties",
    )
    all_of: list[Schema] | None = Field(default=None, alias="allOf")  # type: ignore[assignment]  # narrowed to v3_1.Schema
    one_of: list[Schema] | None = Field(default=None, alias="oneOf")  # type: ignore[assignment]  # narrowed to v3_1.Schema
    any_of: list[Schema] | None = Field(default=None, alias="anyOf")  # type: ignore[assignment]  # narrowed to v3_1.Schema
    not_schema: Schema | None = Field(default=None, alias="not")


class Header(v3_0.Header):
    """Header object definition in OpenAPI 3.1+."""

    schema: Schema | None = Field(default=None)


class Encoding(v3_0.Encoding):
    """Encoding object definition in OpenAPI 3.1+."""

    headers: dict[str, Header] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Header


class MediaType(v3_0.MediaType):
    """Media Type object definition in OpenAPI 3.1+."""

    schema: Schema | None = Field(default=None)
    encoding: dict[str, Encoding] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Encoding


class Parameter(v3_0.Parameter):
    """Parameter object definition in OpenAPI 3.1+."""

    schema: Schema | None = Field(default=None)
    content: dict[str, MediaType] | None = None  # type: ignore[assignment]  # narrowed to v3_1.MediaType


class RequestBody(v3_0.RequestBody):
    """Request Body object definition in OpenAPI 3.1+."""

    content: dict[str, MediaType]  # type: ignore[assignment]  # narrowed to v3_1.MediaType


class Response(v3_0.Response):
    """Response object definition in OpenAPI 3.1+."""

    headers: dict[str, Header] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Header
    content: dict[str, MediaType] | None = None  # type: ignore[assignment]  # narrowed to v3_1.MediaType


class Callback(v3_0.Callback):
    """A map of expressions to PathItem objects (v3.1+)."""

    expressions: dict[str, PathItem]  # type: ignore[assignment]  # narrowed to v3_1.PathItem


class Operation(v3_0.Operation):
    """Operation object definition in OpenAPI 3.1+."""

    parameters: list[Parameter] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Parameter
    request_body: RequestBody | None = Field(default=None, alias="requestBody")
    responses: dict[str, Response]  # type: ignore[assignment]  # narrowed to v3_1.Response
    callbacks: dict[str, Callback] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Callback


class PathItem(v3_0.PathItem):
    """Path Item object definition in OpenAPI 3.1+."""

    get: Operation | None = None
    put: Operation | None = None
    post: Operation | None = None
    delete: Operation | None = None
    options: Operation | None = None
    head: Operation | None = None
    patch: Operation | None = None
    trace: Operation | None = None
    parameters: list[Parameter] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Parameter
    additional_operations: dict[str, Operation] | None = Field(
        default=None,
        alias="additionalOperations",
    )


class Tag(ExtensionsMixin, _ModelBase):
    """Structured Tag object definition for OpenAPI 3.2."""

    name: str
    summary: str | None = None
    description: str | None = None
    parent: str | None = None
    kind: str | None = None
    external_docs: ExternalDoc | None = Field(default=None, alias="externalDocs")


class Components(v3_0.Components):
    """Components object definition in OpenAPI 3.1+."""

    schemas: dict[str, Schema] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Schema
    responses: dict[str, Response] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Response
    parameters: dict[str, Parameter] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Parameter
    request_bodies: dict[str, RequestBody] | None = Field(  # type: ignore[assignment]  # narrowed to v3_1.RequestBody
        default=None,
        alias="requestBodies",
    )
    headers: dict[str, Header] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Header
    callbacks: dict[str, Callback] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Callback
    path_items: dict[str, PathItem] | None = Field(default=None, alias="pathItems")  # type: ignore[assignment]  # narrowed to v3_1.PathItem


class Specification(v3_0.Specification):
    """OpenAPI 3.1+ specification root object."""

    openapi: str = "3.1.0"
    paths: dict[str, PathItem]  # type: ignore[assignment]  # narrowed to v3_1.PathItem
    components: Components | None = None
    tags: list[Tag] | None = None  # type: ignore[assignment]  # narrowed to v3_1.Tag
    webhooks: dict[str, PathItem] | None = None
    json_schema_dialect: str | None = Field(default=None, alias="jsonSchemaDialect")
