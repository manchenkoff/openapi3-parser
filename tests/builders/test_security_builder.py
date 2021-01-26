from unittest import mock

import pytest

from openapi_parser.builders import OAuthFlowBuilder
from openapi_parser.builders.security import SecurityBuilder
from openapi_parser.enumeration import AuthenticationScheme, BaseLocation, OAuthFlowType, SecurityType
from openapi_parser.specification import OAuthFlow, Security


def _get_oauth_flow_builder_mock(expected) -> OAuthFlowBuilder:
    mock_object = mock.MagicMock()
    mock_object.build_collection.return_value = expected

    return mock_object


flows_mock = {
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
}

data_provider = (
    (
        {
            "type": "http",
            "scheme": "basic"
        },
        Security(
            type=SecurityType.HTTP,
            scheme=AuthenticationScheme.BASIC
        ),
        _get_oauth_flow_builder_mock(None),
    ),
    (
        {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
        Security(
            type=SecurityType.HTTP,
            scheme=AuthenticationScheme.BEARER,
            bearer_format="JWT"
        ),
        _get_oauth_flow_builder_mock(None),
    ),
    (
        {
            "type": "openIdConnect",
            "openIdConnectUrl": "https://example.com/api/openid",
        },
        Security(
            type=SecurityType.OPEN_ID_CONNECT,
            url="https://example.com/api/openid"
        ),
        _get_oauth_flow_builder_mock(None),
    ),
    (
        {
            "type": "apiKey",
            "in": "header",
        },
        Security(
            type=SecurityType.API_KEY,
            location=BaseLocation.HEADER,
        ),
        _get_oauth_flow_builder_mock(None),
    ),
    (
        {
            "type": "apiKey",
            "name": "api_key",
            "in": "header",
            "description": "authorization key to communicate with API"
        },
        Security(
            type=SecurityType.API_KEY,
            location=BaseLocation.HEADER,
            name="api_key",
            description="authorization key to communicate with API"
        ),
        _get_oauth_flow_builder_mock(None),
    ),
    (
        {
            "type": "oauth2",
            "flows": {
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
                }
            }
        },
        Security(
            type=SecurityType.OAUTH2,
            flows=flows_mock
        ),
        _get_oauth_flow_builder_mock(flows_mock),
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'oauth_flow_builder'], data_provider)
def test_build(data: dict, expected: Security, oauth_flow_builder: OAuthFlowBuilder):
    builder = SecurityBuilder(oauth_flow_builder)

    assert builder.build(data) == expected


collection_data_provider = (
    (
        {
            "Basic": {
                "type": "http",
                "scheme": "basic"
            },
        },
        {
            "Basic": Security(
                type=SecurityType.HTTP,
                scheme=AuthenticationScheme.BASIC
            ),
        },
        _get_oauth_flow_builder_mock(None),
    ),
)


@pytest.mark.parametrize(['data', 'expected', 'oauth_flow_builder'], collection_data_provider)
def test_build_collection(data: dict, expected: dict, oauth_flow_builder: OAuthFlowBuilder):
    builder = SecurityBuilder(oauth_flow_builder)

    assert builder.build_collection(data) == expected
