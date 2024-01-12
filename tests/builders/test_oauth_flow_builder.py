from typing import Dict

import pytest

from openapi_parser.builders import OAuthFlowBuilder
from openapi_parser.enumeration import OAuthFlowType
from openapi_parser.specification import OAuthFlow

data_provider = (
    (
        {
            "clientCredentials": {
                "authorizationUrl": "https://example.com/api/oauth/dialog",
                "refreshUrl": "https://example.com/api/oauth/dialog",
                "tokenUrl": "https://example.com/api/oauth/dialog",
                "x-state": "some data to be passed to oath server",
            },
        },
        {
            OAuthFlowType.CLIENT_CREDENTIALS: OAuthFlow(
                authorization_url="https://example.com/api/oauth/dialog",
                refresh_url="https://example.com/api/oauth/dialog",
                token_url="https://example.com/api/oauth/dialog",
                extensions={"state": "some data to be passed to oath server"}
            ),
        },
    ),
    (
        {
            "implicit": {
                "authorizationUrl": "https://example.com/api/oauth/dialog",
                "scopes": {
                    "write:pets": "modify pets in your account",
                    "read:pets": "read your pets"
                }
            },
            "authorizationCode": {
                "authorizationUrl": "https://example.com/api/oauth/dialog",
                "tokenUrl": "https://example.com/api/oauth/token",
                "scopes": {
                    "write:pets": "modify pets in your account",
                    "read:pets": "read your pets"
                }
            },
            "x-customFlow": {
                "custom_attribute": "custom value"
            }
        },
        {
            OAuthFlowType.IMPLICIT: OAuthFlow(
                authorization_url="https://example.com/api/oauth/dialog",
                scopes={
                    "write:pets": "modify pets in your account",
                    "read:pets": "read your pets"
                }
            ),
            OAuthFlowType.AUTHORIZATION_CODE: OAuthFlow(
                authorization_url="https://example.com/api/oauth/dialog",
                token_url="https://example.com/api/oauth/token",
                scopes={
                    "write:pets": "modify pets in your account",
                    "read:pets": "read your pets"
                }
            ),
            "customFlow": {
                "custom_attribute": "custom value"
            }
        },
    ),
)


@pytest.mark.parametrize(['data', 'expected'], data_provider)
def test_oauth_flow_builder(data: dict, expected: Dict[OAuthFlowType, OAuthFlow]):
    builder = OAuthFlowBuilder()

    assert builder.build_collection(data) == expected
