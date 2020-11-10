from ..specification import ExternalDoc


class ExternalDocBuilder:
    @staticmethod
    def build(data: dict) -> ExternalDoc:
        attrs = {
            "url": data['url'],
            "description": data.get('description')
        }

        return ExternalDoc(**attrs)
