from typing import Optional

from .external_doc import ExternalDocBuilder
from ..specification import Tag, TagList


class TagBuilder:
    external_doc_builder: ExternalDocBuilder

    def __init__(self, external_doc_builder: ExternalDocBuilder) -> None:
        self.external_doc_builder = external_doc_builder

    def _build_tag(self, data: dict) -> Tag:
        attrs = {
            "name": data['name'],
            "description": data.get('description'),
            "external_docs": self.external_doc_builder.build(data.get('externalDocs')),
        }

        return Tag(**attrs)

    def build_list(self, data_list: Optional[list]) -> TagList:
        if data_list is None:
            return []

        return [self._build_tag(item) for item in data_list]
