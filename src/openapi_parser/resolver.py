import logging
from typing import Optional

import prance

from .errors import ParserError

OPENAPI_SPEC_VALIDATOR = 'openapi-spec-validator'

logger = logging.getLogger(__name__)


class OpenAPIResolver:
    _resolver: prance.ResolvingParser

    def __init__(self, uri: Optional[str], spec_string: Optional[str] = None) -> None:
        self._resolver = prance.ResolvingParser(
            uri,
            spec_string=spec_string,
            backend=OPENAPI_SPEC_VALIDATOR,
            strict=False,
            lazy=True
        )

    def resolve(self) -> dict:
        """Resolve OpenAPI specification with Prance parser

        Returns:
            dict: Normalized and parsed specification as a dictionary

        Raises:
            ParserError: If some validation or parsing error occurred
        """
        try:
            logger.debug(f"Resolving specification file")
            self._resolver.parse()
            return self._resolver.specification
        except prance.ValidationError as error:
            raise ParserError(f"OpenAPI validation error: {error}")
        except Exception as error:
            raise ParserError(f"OpenAPI file parsing error: {error}")
