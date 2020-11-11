from . import ContentBuilder
from .common import PropertyMeta, extract_typed_props
from ..specification import RequestBody


class RequestBuilder:
    content_builder: ContentBuilder

    def __init__(self, content_builder: ContentBuilder) -> None:
        self.content_builder = content_builder

    def build(self, data: dict) -> RequestBody:
        attrs_map = {
            "content": PropertyMeta(name="content", cast=self.content_builder.build_collection),
            "description": PropertyMeta(name="description", cast=str),
            "required": PropertyMeta(name="required", cast=None),
        }

        attrs = extract_typed_props(data, attrs_map)

        return RequestBody(**attrs)
