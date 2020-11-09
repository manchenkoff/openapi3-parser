from openapi_parser.specification import Contact, Info, License


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
        license_data = data.get('license')
        contact_data = data.get('contact')

        attrs = {
            "title": data['title'],
            "version": data['version'],
            "description": data.get('description'),
            "terms_of_service": data.get('termsOfService'),
            "license": self._create_license(license_data) if license_data is not None else None,
            "contact": self._create_contact(contact_data) if contact_data is not None else None,
        }

        return Info(**attrs)
