from dataclasses import dataclass, field
from typing import Any, Optional

from .enumeration import *


@dataclass
class Contact:
    name: Optional[str] = None
    url: Optional[str] = None
    email: Optional[str] = None


@dataclass
class License:
    name: str
    url: Optional[str] = None


@dataclass
class Info:
    title: str
    version: str
    description: Optional[str] = None
    terms_of_service: Optional[str] = None
    contact: Optional[Contact] = None
    license: Optional[License] = None


@dataclass
class Server:
    url: str
    description: Optional[str] = None
    variables: Optional[dict] = field(default_factory=dict)


@dataclass
class ExternalDoc:
    url: str
    description: Optional[str] = None


@dataclass
class Schema:
    type: DataType
    title: Optional[str] = None
    enum: Optional[list[Any]] = None
    example: Optional[Any] = None
    description: Optional[str] = None
    default: Optional[Any] = None
    nullable: Optional[bool] = None
    read_only: Optional[bool] = None
    write_only: Optional[bool] = None
    deprecated: Optional[bool] = None
    extensions: Optional[dict] = field(default_factory=dict)

    # all_of: Any  # TODO
    # one_of: Any  # TODO
    # any_of: Any  # TODO
    # not: Any  # TODO

    def __post_init__(self) -> None:
        # normalize default values if None passed in __init__
        if self.enum is None:
            self.enum = []
        if self.nullable is None:
            self.nullable = False
        if self.read_only is None:
            self.read_only = False
        if self.write_only is None:
            self.write_only = False
        if self.deprecated is None:
            self.deprecated = False


@dataclass
class Integer(Schema):
    multiple_of: Optional[int] = None
    maximum: Optional[int] = None
    exclusive_maximum: Optional[int] = None
    minimum: Optional[int] = None
    exclusive_minimum: Optional[int] = None
    format: Optional[IntegerFormat] = None


@dataclass
class Number(Schema):
    multiple_of: Optional[float] = None
    maximum: Optional[float] = None
    exclusive_maximum: Optional[float] = None
    minimum: Optional[float] = None
    exclusive_minimum: Optional[float] = None
    format: Optional[NumberFormat] = None


@dataclass
class String(Schema):
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    pattern: Optional[str] = None
    format: Optional[StringFormat] = None


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
    schema: Schema
    required: Optional[bool] = field(default=False)
    description: Optional[str] = None
    # example: Optional[Any]  # TODO
    # examples: list[Any] = field(default_factory=list)  # TODO
    deprecated: Optional[bool] = field(default=False)
    # style: str  # TODO
    # explode: bool  # TODO
    # allow_reserved: bool  # TODO


@dataclass
class Content:
    type: ContentType
    schema: Schema
    # example: Optional[Any]  # TODO
    # examples: list[Any] = field(default_factory=list)  # TODO
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
    # callbacks: dict[str, Callback] = field(default_factory=dict)  # TODO


@dataclass
class Path:
    url: str
    summary: Optional[str] = None
    description: Optional[str] = None
    operations: list[Operation] = field(default_factory=list)
    parameters: list[Parameter] = field(default_factory=list)


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
