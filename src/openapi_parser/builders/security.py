"""Security scheme builder."""

import logging
from typing import Any

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_extension_attributes,
    extract_typed_props,
)
from openapi_parser.builders.oauth_flow import OAuthFlowBuilder
from openapi_parser.enumeration import AuthenticationScheme, BaseLocation, SecurityType
from openapi_parser.logging import log_ctx
from openapi_parser.specification import Security

logger = logging.getLogger(__name__)


class SecurityBuilder:
    """Builds security scheme objects from raw specification data."""

    _oauth_flow_builder: OAuthFlowBuilder

    def __init__(self, oauth_flow_builder: OAuthFlowBuilder) -> None:
        """Initialize security builder.

        Args:
            oauth_flow_builder: Builder for OAuth flow objects
        """
        self._oauth_flow_builder = oauth_flow_builder

    def build(self, data: dict[str, Any]) -> Security:
        """Build a Security object from a raw dict."""
        logger.debug("Security item parsing")

        attrs_map = {
            "type": PropertyMeta(name="type", cast=SecurityType),
            "location": PropertyMeta(name="in", cast=BaseLocation),
            "name": PropertyMeta(name="name", cast=str),
            "description": PropertyMeta(name="description", cast=str),
            "scheme": PropertyMeta(name="scheme", cast=AuthenticationScheme),
            "bearer_format": PropertyMeta(name="bearerFormat", cast=str),
            "url": PropertyMeta(name="openIdConnectUrl", cast=str),
            "flows": PropertyMeta(
                name="flows",
                cast=self._oauth_flow_builder.build_collection,
            ),
        }

        attrs = extract_typed_props(data, attrs_map)
        attrs["extensions"] = extract_extension_attributes(data)

        if attrs["extensions"]:
            logger.debug(
                f"Extracted custom properties [{attrs['extensions'].keys()}]",
            )

        return Security(**attrs)

    def build_collection(
        self,
        data: dict[str, Any],
    ) -> dict[str, Security]:
        """Build a dict of named Security objects."""
        result: dict[str, Security] = {}

        for scheme_name, scheme_data in data.items():
            with log_ctx("securitySchemes", scheme_name):
                result[scheme_name] = self.build(scheme_data)

        return result
