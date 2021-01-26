import prance

from .errors import ParserError

OPENAPI_SPEC_VALIDATOR = 'openapi-spec-validator'


class OpenAPIResolver:
    _resolver: prance.ResolvingParser

    def __init__(self, uri: str) -> None:
        self._resolver = prance.ResolvingParser(
            uri,
            backend=OPENAPI_SPEC_VALIDATOR,
            strict=False,
            lazy=True
        )

    def resolve(self) -> dict:
        try:
            self._resolver.parse()

            return self._resolver.specification
        except prance.ValidationError as error:
            raise ParserError(f"OpenAPI validation error: {error}")
        except prance.util.formats.ParseError as error:
            raise ParserError(f"OpenAPI file parsing error: {error}")
