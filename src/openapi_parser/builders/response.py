from . import ContentBuilder, HeaderBuilder
from .common import extract_typed_props, PropertyMeta
from ..specification import Response


class ResponseBuilder:
    content_builder: ContentBuilder
    header_builder: HeaderBuilder

    def __init__(self, content_builder: ContentBuilder, header_builder: HeaderBuilder) -> None:
        self.content_builder = content_builder
        self.header_builder = header_builder

    def build(self, data: dict) -> Response:
        attrs_map = {
            "description": PropertyMeta(name="description", cast=str),
            "content": PropertyMeta(name="content", cast=self.content_builder.build_collection),
            "headers": PropertyMeta(name="headers", cast=self.header_builder.build_collection),
        }

        attrs = extract_typed_props(data, attrs_map)

        return Response(**attrs)
