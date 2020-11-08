from typing import Optional

from ..specification import Contact, Info, License


class InfoBuilder:
    @staticmethod
    def _create_license(data: Optional[dict]) -> Optional[License]:
        if data is None:
            return None

        attrs = {
            "name": data['name'],
            "url": data.get('url'),
        }

        return License(**attrs)

    @staticmethod
    def _create_contact(data: Optional[dict]) -> Optional[Contact]:
        if data is None:
            return None

        attrs = {
            "name": data.get('name'),
            "url": data.get('url'),
            "email": data.get('email'),
        }

        return Contact(**attrs)

    def build(self, data: dict) -> Info:
        attrs = {
            "title": data['title'],
            "version": data['version'],
            "description": data.get('description'),
            "terms_of_service": data.get('termsOfService'),
            "license": self._create_license(data.get('license')),
            "contact": self._create_contact(data.get('contact')),
        }

        return Info(**attrs)
