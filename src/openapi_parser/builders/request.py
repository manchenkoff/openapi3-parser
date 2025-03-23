import logging

from .common import extract_typed_props, PropertyMeta
from .content import ContentBuilder
from ..specification import RequestBody

logger = logging.getLogger(__name__)


class RequestBuilder:
    content_builder: ContentBuilder

    def __init__(self, content_builder: ContentBuilder) -> None:
        self.content_builder = content_builder

    def build(self, data: dict) -> RequestBody:
        logger.debug(f"Request building")

        attrs_map = {
            "content": PropertyMeta(name="content", cast=self.content_builder.build_list),
            "description": PropertyMeta(name="description", cast=str),
            "required": PropertyMeta(name="required", cast=None),
        }

        attrs = extract_typed_props(data, attrs_map)

        return RequestBody(**attrs)
