from . import ContentBuilder, HeaderBuilder
from .common import extract_attrs_by_map, PropertyInfoType
from ..specification import Response


class ResponseBuilder:
    content_builder: ContentBuilder
    header_builder: HeaderBuilder

    def __init__(self, content_builder: ContentBuilder, header_builder: HeaderBuilder) -> None:
        self.content_builder = content_builder
        self.header_builder = header_builder

    def build(self, data: dict) -> Response:
        attrs_map = {
            "description": PropertyInfoType(name="description", type=str),
            "content": PropertyInfoType(name="content", type=self.content_builder.build_collection),
            "headers": PropertyInfoType(name="headers", type=self.header_builder.build_collection),
        }

        attrs = extract_attrs_by_map(data, attrs_map)

        return Response(**attrs)
