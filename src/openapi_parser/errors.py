"""Custom exceptions for OpenAPI parsing errors."""

from pydantic import ValidationError
from pydantic_core import ErrorDetails


class ParserError(Exception):
    """Wraps all parsing/validation errors with context."""

    def errors(self) -> list[ErrorDetails]:
        """Return validation errors if available.

        Returns an empty list otherwise.
        """
        if isinstance(self.__cause__, ValidationError):
            return self.__cause__.errors()

        return []
