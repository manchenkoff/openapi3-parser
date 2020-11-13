from .common import extract_typed_props, PropertyMeta
from ..builders.external_doc import ExternalDocBuilder
from ..specification import Tag, TagList


class TagBuilder:
    _external_doc_builder: ExternalDocBuilder

    def __init__(self, external_doc_builder: ExternalDocBuilder) -> None:
        self._external_doc_builder = external_doc_builder

    def build_list(self, data_list: list) -> TagList:
        return [self._build_tag(item) for item in data_list]

    def _build_tag(self, data: dict) -> Tag:
        attrs_map = {
            "name": PropertyMeta(name="name", cast=str),
            "description": PropertyMeta(name="description", cast=str),
            "external_docs": PropertyMeta(name="externalDocs", cast=self._external_doc_builder.build),
        }

        attrs = extract_typed_props(data, attrs_map)

        return Tag(**attrs)
