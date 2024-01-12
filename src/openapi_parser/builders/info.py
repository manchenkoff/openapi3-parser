import logging

from .common import extract_typed_props, PropertyMeta, extract_extension_attributes
from ..specification import Contact, Info, License

logger = logging.getLogger(__name__)


class InfoBuilder:
    def build(self, data: dict) -> Info:
        logger.debug(f"Info section parsing [title={data['title']}]")

        attrs_map = {
            "title": PropertyMeta(name="title", cast=str),
            "version": PropertyMeta(name="version", cast=str),
            "description": PropertyMeta(name="description", cast=str),
            "terms_of_service": PropertyMeta(name="termsOfService", cast=str),
            "license": PropertyMeta(name="license", cast=self._create_license),
            "contact": PropertyMeta(name="contact", cast=self._create_contact),
        }

        attrs = extract_typed_props(data, attrs_map)
        attrs["extensions"] = extract_extension_attributes(data)

        if attrs['extensions']:
            logger.debug(f"Extracted custom properties [{attrs['extensions'].keys()}]")

        return Info(**attrs)

    @staticmethod
    def _create_license(data: dict) -> License:
        attrs = {
            "name": data['name'],
            "url": data.get('url'),
        }

        return License(**attrs)

    @staticmethod
    def _create_contact(data: dict) -> Contact:
        attrs = {
            "name": data.get('name'),
            "url": data.get('url'),
            "email": data.get('email'),
        }

        return Contact(**attrs)
