from typing import Optional

from ..specification import ExternalDoc


class ExternalDocBuilder:
    @staticmethod
    def build(external_doc_info: dict) -> Optional[ExternalDoc]:
        if external_doc_info is None:
            return None

        data = {
            "url": external_doc_info['url'],
            "description": external_doc_info.get('description')
        }

        return ExternalDoc(**data)
