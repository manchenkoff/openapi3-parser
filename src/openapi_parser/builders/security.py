from .common import extract_typed_props, PropertyMeta
from .oauth_flow import OAuthFlowBuilder
from ..enumeration import AuthenticationScheme, BaseLocation, SecurityType
from ..specification import Security, SecurityCollection


class SecurityBuilder:
    oauth_flow_builder: OAuthFlowBuilder

    def __init__(self, oauth_flow_builder: OAuthFlowBuilder) -> None:
        self.oauth_flow_builder = oauth_flow_builder

    def build(self, data: dict) -> Security:
        attrs_map = {
            "type": PropertyMeta(name="type", cast=SecurityType),
            "location": PropertyMeta(name="in", cast=BaseLocation),
            "name": PropertyMeta(name="name", cast=None),
            "description": PropertyMeta(name="description", cast=None),
            "scheme": PropertyMeta(name="scheme", cast=AuthenticationScheme),
            "bearer_format": PropertyMeta(name="bearerFormat", cast=None),
            "url": PropertyMeta(name="openIdConnectUrl", cast=None),
            "flows": PropertyMeta(name="flows", cast=self.oauth_flow_builder.build_collection),
        }

        attrs = extract_typed_props(data, attrs_map)

        return Security(**attrs)

    def build_collection(self, data: dict) -> SecurityCollection:
        return {
            oauth_title: self.build(oauth_value)
            for oauth_title, oauth_value
            in data.items()
        }
