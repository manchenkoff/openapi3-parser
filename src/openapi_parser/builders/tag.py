from .common import extract_attrs_by_map, PropertyInfoType
from ..builders.external_doc import ExternalDocBuilder
from ..specification import Tag, TagList


class TagBuilder:
    _external_doc_builder: ExternalDocBuilder

    def __init__(self, external_doc_builder: ExternalDocBuilder) -> None:
        self._external_doc_builder = external_doc_builder

    def _build_tag(self, data: dict) -> Tag:
        attrs_map = {
            "name": PropertyInfoType(name="name", type=str),
            "description": PropertyInfoType(name="description", type=str),
            "external_docs": PropertyInfoType(name="externalDocs", type=self._external_doc_builder.build),
        }

        attrs = extract_attrs_by_map(data, attrs_map)

        return Tag(**attrs)

    def build_list(self, data_list: list) -> TagList:
        return [self._build_tag(item) for item in data_list]
