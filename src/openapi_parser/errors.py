"""Custom exceptions for OpenAPI parsing errors."""

from openapi_parser.logging import _log_ctx_var


class ParserError(Exception):
    """Base parser exception class.

    Throws when any error occurs.
    """

    context: str | None

    def __init__(self, message: str, context: str | None = None) -> None:
        """Initialize the error with an optional parse context path.

        Args:
            message: Error description
            context: Path within the spec where the error occurred (e.g. "paths./users.get")
        """
        super().__init__(message)
        self.context = context if context is not None else (_log_ctx_var.get())

    def __str__(self) -> str:
        """Format error message with optional context prefix."""
        msg = super().__str__()

        if self.context:
            return f"[{self.context}] {msg}"

        return msg
