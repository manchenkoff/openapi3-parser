from typing import Any, Dict

from . import ContentBuilder
from ..enumeration import MediaType
from ..specification import RequestBody


class RequestBuilder:
    content_builder: ContentBuilder

    def __init__(self, content_builder: ContentBuilder) -> None:
        self.content_builder = content_builder

    def build(self, data: dict) -> RequestBody:
        attrs: Dict[str, Any]

        attrs = {
            "content": {
                MediaType(key): self.content_builder.build(value)
                for key, value in data["content"].keys()
            }
        }

        if data.get("description") is not None:
            attrs["description"] = data["description"]

        if data.get("required") is not None:
            attrs["required"] = data["required"]

        return RequestBody(**attrs)
