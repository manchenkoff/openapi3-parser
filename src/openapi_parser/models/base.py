"""Shared OpenAPI base models."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from openapi_parser.models.mixins import ExtensionsMixin, RefCacheMixin


class _ModelBase(BaseModel):
    """Base for frozen models."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)


class _MutableModelBase(BaseModel):
    """Base for mutable models (e.g. Schema with circular ref placeholders)."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Contact(ExtensionsMixin, _ModelBase):
    """Contact information for the exposed API."""

    name: str | None = None
    url: str | None = None
    email: str | None = None


class License(ExtensionsMixin, _ModelBase):
    """License information for the exposed API."""

    name: str
    url: str | None = None


class Info(ExtensionsMixin, _ModelBase):
    """Metadata about the API."""

    title: str
    version: str
    description: str | None = None
    terms_of_service: str | None = Field(default=None, alias="termsOfService")
    contact: Contact | None = None
    license: License | None = None


class ServerVariable(ExtensionsMixin, _ModelBase):
    """An object representing a Server Variable for server URL template substitution."""

    default: str
    enum: list[str] | None = None
    description: str | None = None


class Server(ExtensionsMixin, _ModelBase):
    """An object representing a Server."""

    url: str
    description: str | None = None
    variables: dict[str, ServerVariable] | None = None


class ExternalDoc(ExtensionsMixin, _ModelBase):
    """Information about external documentation."""

    url: str
    description: str | None = None


class Discriminator(_ModelBase):
    """Discriminator object for inheritance mapping."""

    property_name: str = Field(alias="propertyName")
    mapping: dict[str, str] | None = None


class OAuthFlow(ExtensionsMixin, _ModelBase):
    """Configuration details for a supported OAuth Flow."""

    authorization_url: str | None = Field(default=None, alias="authorizationUrl")
    token_url: str | None = Field(default=None, alias="tokenUrl")
    refresh_url: str | None = Field(default=None, alias="refreshUrl")
    scopes: dict[str, str] = Field(default_factory=dict)


class Link(ExtensionsMixin, RefCacheMixin, _ModelBase):
    """Link definition for response links."""

    operation_ref: str | None = Field(default=None, alias="operationRef")
    operation_id: str | None = Field(default=None, alias="operationId")
    parameters: dict[str, Any] | None = None
    request_body: Any | None = Field(default=None, alias="requestBody")
    description: str | None = None
    server: Server | None = None
