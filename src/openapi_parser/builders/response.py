import logging
from typing import Union

from .common import extract_typed_props, PropertyMeta
from .content import ContentBuilder
from .header import HeaderBuilder
from ..specification import Response

logger = logging.getLogger(__name__)


class ResponseBuilder:
    content_builder: ContentBuilder
    header_builder: HeaderBuilder

    def __init__(self, content_builder: ContentBuilder, header_builder: HeaderBuilder) -> None:
        self.content_builder = content_builder
        self.header_builder = header_builder

    def build(self, code: Union[int, str], data: dict) -> Response:
        logger.debug(f"Response building [code={code}]")

        attrs_map = {
            "description": PropertyMeta(name="description", cast=str),
            "content": PropertyMeta(name="content", cast=self.content_builder.build_list),
            "headers": PropertyMeta(name="headers", cast=self.header_builder.build_list),
        }

        attrs = extract_typed_props(data, attrs_map)

        attrs['is_default'] = code == "default"

        try:
            attrs['code'] = int(code)
        except ValueError:
            logger.debug(f"Response code is not an integer [code={code}]")

        return Response(**attrs)
