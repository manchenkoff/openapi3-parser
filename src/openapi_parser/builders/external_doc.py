import logging

from ..specification import ExternalDoc

logger = logging.getLogger(__name__)


class ExternalDocBuilder:
    @staticmethod
    def build(data: dict) -> ExternalDoc:
        logger.debug(f"External doc parsing: {data['url']}")

        attrs = {
            "url": data['url'],
            "description": data.get('description')
        }

        return ExternalDoc(**attrs)
