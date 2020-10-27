from typing import Optional

from ..specification import Contact, Info, License


class InfoBuilder:
    @staticmethod
    def _create_license(license_data: Optional[dict]) -> Optional[License]:
        if license_data is None:
            return None

        data = {
            "name": license_data['name'],
            "url": license_data.get('url'),
        }

        return License(**data)

    @staticmethod
    def _create_contact(contact_data: Optional[dict]) -> Optional[Contact]:
        if contact_data is None:
            return None

        data = {
            "name": contact_data.get('name'),
            "url": contact_data.get('url'),
            "email": contact_data.get('email'),
        }

        return Contact(**data)

    def build(self, info_data: dict) -> Info:
        info_builder_dict = {
            "title": info_data['title'],
            "version": info_data['version'],
            "description": info_data.get('description'),
            "terms_of_service": info_data.get('termsOfService'),
            "license": self._create_license(info_data.get('license')),
            "contact": self._create_contact(info_data.get('contact')),
        }

        return Info(**info_builder_dict)
