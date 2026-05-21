"""OpenAPI specification resolver using prance."""

import logging
from typing import Any, cast

import prance

from openapi_parser.errors import ParserError

OPENAPI_SPEC_VALIDATOR = "openapi-spec-validator"

logger = logging.getLogger(__name__)


class OpenAPIResolver:
    """Resolves and validates OpenAPI specs using prance."""

    _resolver: prance.ResolvingParser

    def __init__(self, uri: str | None, spec_string: str | None = None) -> None:
        """Initialize resolver.

        Args:
            uri: Path or URL to the spec file
            spec_string: Raw spec string as alternative to uri
        """
        self._resolver = prance.ResolvingParser(
            uri,
            spec_string=spec_string,
            backend=OPENAPI_SPEC_VALIDATOR,
            strict=False,
            lazy=True,
        )

    def resolve(self) -> dict[str, Any]:
        """Resolve OpenAPI specification with Prance parser.

        Returns:
            dict: Normalized and parsed specification as a dictionary

        Raises:
            ParserError: If some validation or parsing error occurred
        """
        try:
            logger.debug("Resolving specification file")

            self._resolver.parse()

            return cast(dict[str, Any], self._resolver.specification)
        except prance.ValidationError as error:
            raise ParserError(f"OpenAPI validation error: {error}") from error
        except Exception as error:
            raise ParserError(f"OpenAPI file parsing error: {error}") from error
