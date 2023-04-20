import logging
from typing import List

from . import SchemaFactory
from .common import extract_typed_props, PropertyMeta
from ..enumeration import ParameterLocation, HeaderParameterStyle, PathParameterStyle, QueryParameterStyle, \
    CookieParameterStyle
from ..specification import Parameter

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
    schema_factory: SchemaFactory

    def __init__(self, schema_factory: SchemaFactory) -> None:
        self.schema_factory = schema_factory

    def build_list(self, parameters: List[dict]) -> list[Parameter]:
        return [self.build(parameter) for parameter in parameters]

    def build(self, data: dict) -> Parameter:
        logger.debug(f"Parameter parsing [name={data['name']}]")

        attrs_map = {
            "name": PropertyMeta(name="name", cast=str),
            "location": PropertyMeta(name="in", cast=ParameterLocation),
            "required": PropertyMeta(name="required", cast=None),
            "schema": PropertyMeta(name="schema", cast=self.schema_factory.create),
            "description": PropertyMeta(name="description", cast=str),
            "deprecated": PropertyMeta(name="deprecated", cast=None),
            "explode": PropertyMeta(name="explode", cast=None),
        }

        attrs = extract_typed_props(data, attrs_map)

        if data.get("style"):
            attrs["style"] = style_to_enum_map[attrs["location"]](data["style"])
        else:
            attrs["style"] = default_styles_by_location[attrs["location"]]

        if not attrs.get("explode") and attrs["style"].value == "form":
            attrs["explode"] = True

        return Parameter(**attrs)
