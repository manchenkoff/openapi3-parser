OPENAPI_SPEC_VALIDATOR = 'openapi-spec-validator'


class ResolverError(Exception):
    """
    Base resolver error class.
    Throws when any error occurs.
    """
    pass


class SwaggerResolver:
    uri: str

    def __init__(self, uri: str) -> None:
        self.uri = uri
