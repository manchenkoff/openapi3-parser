from typing import Any, Dict

from . import ContentBuilder, HeaderBuilder
from ..specification import Response


class ResponseBuilder:
    content_builder: ContentBuilder
    header_builder: HeaderBuilder

    def __init__(self, content_builder: ContentBuilder, header_builder: HeaderBuilder) -> None:
        self.content_builder = content_builder
        self.header_builder = header_builder

    def build(self, data: dict) -> Response:
        attrs: Dict[str, Any]

        attrs = {
            "description": data["description"],
            "content": self.content_builder.build_collection(data["content"]),
        }

        if data.get("headers") is not None:
            attrs["headers"] = self.header_builder.build_collection(data["headers"])

        return Response(**attrs)
