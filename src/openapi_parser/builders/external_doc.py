import logging

from .common import extract_extension_attributes
from ..specification import ExternalDoc

logger = logging.getLogger(__name__)


class ExternalDocBuilder:
    @staticmethod
    def build(data: dict) -> ExternalDoc:
        logger.debug(f"External doc parsing: {data['url']}")

        attrs = {
            "url": data['url'],
            "description": data.get('description'),
            "extensions": extract_extension_attributes(data),
        }

        if attrs['extensions']:
            logger.debug(f"Extracted custom properties [{attrs['extensions'].keys()}]")

        return ExternalDoc(**attrs)
