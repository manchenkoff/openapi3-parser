from .common import PropertyInfoType, extract_attrs_by_map
from ..specification import Contact, Info, License


class InfoBuilder:
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

    def build(self, data: dict) -> Info:
        attrs_map = {
            "title": PropertyInfoType(name="title", type=str),
            "version": PropertyInfoType(name="version", type=str),
            "description": PropertyInfoType(name="description", type=str),
            "terms_of_service": PropertyInfoType(name="termsOfService", type=str),
            "license": PropertyInfoType(name="license", type=self._create_license),
            "contact": PropertyInfoType(name="contact", type=self._create_contact),
        }

        attrs = extract_attrs_by_map(data, attrs_map)

        return Info(**attrs)
