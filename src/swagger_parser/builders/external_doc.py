from typing import Optional

from ..specification import ExternalDoc


class ExternalDocBuilder:
    @staticmethod
    def build(data: dict) -> Optional[ExternalDoc]:
        if data is None:
            return None

        attrs = {
            "url": data['url'],
            "description": data.get('description')
        }

        return ExternalDoc(**attrs)
