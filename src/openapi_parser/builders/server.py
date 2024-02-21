import logging

from .common import extract_typed_props, PropertyMeta, extract_extension_attributes
from ..specification import Server

logger = logging.getLogger(__name__)


class ServerBuilder:
    def build_list(self, data_list: list) -> list[Server]:
        return [self._build_server(item) for item in data_list]

    @staticmethod
    def _build_server(data: dict) -> Server:
        logger.debug(f"Server item parsing [{data['url']}]")

        attrs_map = {
            "url": PropertyMeta(name="url", cast=str),
            "description": PropertyMeta(name="description", cast=str),
            "variables": PropertyMeta(name="variables", cast=None),
        }

        attrs = extract_typed_props(data, attrs_map)
        attrs['extensions'] = extract_extension_attributes(data)

        if attrs['extensions']:
            logger.debug(f"Extracted custom properties [{attrs['extensions'].keys()}]")

        return Server(**attrs)
