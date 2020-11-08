import prance

OPENAPI_SPEC_VALIDATOR = 'openapi-spec-validator'


class ResolverError(Exception):
    """
    Base resolver error class.
    Throws when any error occurs.
    """
    pass


class OpenAPIResolver(prance.ResolvingParser):
    def __init__(self, uri: str) -> None:
        super().__init__(
            uri,
            backend='openapi-spec-validator',
            strict=False,
            lazy=True
        )
