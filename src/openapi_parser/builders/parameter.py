"""Parameter builder for path and operation parameters."""

import logging
from typing import Any

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_extension_attributes,
    extract_typed_props,
)
from openapi_parser.builders.content import ContentBuilder
from openapi_parser.builders.schema import SchemaFactory
from openapi_parser.enumeration import (
    CookieParameterStyle,
    HeaderParameterStyle,
    ParameterLocation,
    PathParameterStyle,
    QueryParameterStyle,
)
from openapi_parser.errors import ParserError
from openapi_parser.logging import log_ctx
from openapi_parser.specification import Parameter

logger = logging.getLogger(__name__)

style_to_enum_map = {
    ParameterLocation.HEADER: HeaderParameterStyle,
    ParameterLocation.PATH: PathParameterStyle,
    ParameterLocation.QUERY: QueryParameterStyle,
    ParameterLocation.COOKIE: CookieParameterStyle,
}

default_styles_by_location = {
    ParameterLocation.HEADER: HeaderParameterStyle.SIMPLE,
    ParameterLocation.PATH: PathParameterStyle.SIMPLE,
    ParameterLocation.QUERY: QueryParameterStyle.FORM,
    ParameterLocation.COOKIE: CookieParameterStyle.FORM,
}


class ParameterBuilder:
    """Builds parameter objects from raw specification data."""

    _schema_factory: SchemaFactory
    _content_builder: ContentBuilder

    def __init__(
        self,
        schema_factory: SchemaFactory,
        content_builder: ContentBuilder,
    ) -> None:
        """Initialize parameter builder.

        Args:
            schema_factory: Factory for creating schema objects
            content_builder: Builder for content objects
        """
        self._schema_factory = schema_factory
        self._content_builder = content_builder

    def build_list(
        self,
        parameters: list[dict[str, Any]],
    ) -> list[Parameter]:
        """Build a list of parameters from a list of raw dicts."""
        return [self.build(parameter) for parameter in parameters]

    def build(self, data: dict[str, Any]) -> Parameter:
        """Build a Parameter from a raw dict."""
        with log_ctx("parameters"):
            parameter_name = data.get("name")

            if parameter_name is None:
                raise ParserError(
                    "Parameter is missing required 'name' property",
                )

            with log_ctx(parameter_name):
                logger.debug(f"Parameter parsing [name={parameter_name}]")

                attrs_map = {
                    "name": PropertyMeta(name="name", cast=str),
                    "location": PropertyMeta(name="in", cast=ParameterLocation),
                    "required": PropertyMeta(name="required", cast=bool),
                    "description": PropertyMeta(name="description", cast=str),
                    "example": PropertyMeta(name="example", cast=None),
                    "examples": PropertyMeta(name="examples", cast=dict),
                    "deprecated": PropertyMeta(name="deprecated", cast=bool),
                    "explode": PropertyMeta(name="explode", cast=bool),
                    "allow_reserved": PropertyMeta(name="allowReserved", cast=bool),
                }

                attrs = extract_typed_props(data, attrs_map)

                if data.get("schema") is not None:
                    attrs["schema"] = self._schema_factory.create(data["schema"])

                if data.get("content") is not None:
                    attrs["content"] = self._content_builder.build_list(data["content"])

                if data.get("style"):
                    attrs["style"] = style_to_enum_map[attrs["location"]](data["style"])
                else:
                    attrs["style"] = default_styles_by_location[attrs["location"]]

                if not attrs.get("explode") and attrs["style"].value == "form":
                    attrs["explode"] = True

                attrs["extensions"] = extract_extension_attributes(data)

                if attrs["extensions"]:
                    logger.debug(
                        f"Extracted custom properties [{attrs['extensions'].keys()}]"
                    )

                return Parameter(**attrs)
