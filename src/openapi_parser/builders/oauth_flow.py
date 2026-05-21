"""OAuth flow builder for security schemes."""

import logging
from typing import Any, cast

from openapi_parser.builders.common import (
    PropertyMeta,
    extract_extension_attributes,
    extract_typed_props,
)
from openapi_parser.enumeration import OAuthFlowType
from openapi_parser.specification import OAuthFlow

logger = logging.getLogger(__name__)


class OAuthFlowBuilder:
    """Builds OAuth flow collections from raw specification data."""

    @staticmethod
    def build_collection(data: dict[str, Any]) -> dict[OAuthFlowType, OAuthFlow]:
        """Build a dict of OAuthFlow objects from a raw dict."""
        logger.debug(f"Parsing OAuth items collection: {data.keys()}")

        attrs_map = {
            "refresh_url": PropertyMeta(name="refreshUrl", cast=str),
            "authorization_url": PropertyMeta(name="authorizationUrl", cast=str),
            "token_url": PropertyMeta(name="tokenUrl", cast=str),
            "scopes": PropertyMeta(name="scopes", cast=dict),
        }

        result_oauth_dict = {
            OAuthFlowType(oauth_type): OAuthFlow(
                extensions=extract_extension_attributes(oauth_value),
                **extract_typed_props(oauth_value, attrs_map),
            )
            for oauth_type, oauth_value in data.items()
            if not oauth_type.startswith("x-")
        }

        extensions = extract_extension_attributes(data)

        if extensions:
            logger.debug(f"Extracted custom properties [{extensions.keys()}]")

            for extension in extensions:
                result_oauth_dict[cast(OAuthFlowType, extension)] = cast(
                    OAuthFlow, extensions[extension]
                )

        return result_oauth_dict
