from typing import List

from .external_doc import ExternalDocBuilder
from ..specification import Tag


class TagBuilder:
    external_doc_builder: ExternalDocBuilder

    def __init__(self, external_doc_builder: ExternalDocBuilder) -> None:
        self.external_doc_builder = external_doc_builder

    def _build_tag(self, tag_info: dict) -> Tag:
        data = {
            "name": tag_info['name'],
            "description": tag_info.get('description'),
            "external_docs": self.external_doc_builder.build(tag_info.get('externalDocs')),
        }

        return Tag(**data)

    def build_tag_list(self, tag_data_list: list) -> List[Tag]:
        return [self._build_tag(item) for item in tag_data_list]
