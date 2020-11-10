from ..builders.external_doc import ExternalDocBuilder
from ..specification import Tag, TagList


class TagBuilder:
    _external_doc_builder: ExternalDocBuilder

    def __init__(self, external_doc_builder: ExternalDocBuilder) -> None:
        self._external_doc_builder = external_doc_builder

    def _build_tag(self, data: dict) -> Tag:
        attrs = {
            "name": data['name'],
            "description": data.get('description'),
        }

        if data.get('externalDocs') is not None:
            attrs['external_docs'] = self._external_doc_builder.build(data['externalDocs'])

        return Tag(**attrs)

    def build_list(self, data_list: list) -> TagList:
        return [self._build_tag(item) for item in data_list]
