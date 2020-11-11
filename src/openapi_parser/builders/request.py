from . import ContentBuilder
from .common import PropertyInfoType, extract_attrs_by_map
from ..specification import RequestBody


class RequestBuilder:
    content_builder: ContentBuilder

    def __init__(self, content_builder: ContentBuilder) -> None:
        self.content_builder = content_builder

    def build(self, data: dict) -> RequestBody:
        attrs_map = {
            "content": PropertyInfoType(name="content", type=self.content_builder.build_collection),
            "description": PropertyInfoType(name="description", type=str),
            "required": PropertyInfoType(name="required", type=None),
        }

        attrs = extract_attrs_by_map(data, attrs_map)

        return RequestBody(**attrs)
