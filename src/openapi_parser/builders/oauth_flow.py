import logging
from typing import Dict

from .common import extract_typed_props, PropertyMeta
from ..enumeration import OAuthFlowType
from ..specification import OAuthFlow

logger = logging.getLogger(__name__)


class OAuthFlowBuilder:
    @staticmethod
    def build_collection(data: dict) -> Dict[OAuthFlowType, OAuthFlow]:
        logger.debug(f"Parsing OAuth items collection: {data.keys()}")

        attrs_map = {
            "refresh_url": PropertyMeta(name="refreshUrl", cast=None),
            "authorization_url": PropertyMeta(name="authorizationUrl", cast=None),
            "token_url": PropertyMeta(name="tokenUrl", cast=None),
            "scopes": PropertyMeta(name="scopes", cast=None),
        }

        result_oauth_dict = {
            OAuthFlowType(oauth_type): OAuthFlow(
                **extract_typed_props(oauth_value, attrs_map)
            )
            for oauth_type, oauth_value
            in data.items()
        }

        return result_oauth_dict
