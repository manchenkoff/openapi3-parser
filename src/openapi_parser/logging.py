"""Logging utilities for automatic context prefixing."""

from __future__ import annotations

import contextvars
import logging

_log_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "openapi_log_ctx",
    default="",
)

_original_factory = logging.getLogRecordFactory()


def _context_record_factory(
    name: str,
    level: int,
    pathname: str,
    lineno: int,
    msg: str,
    args: tuple[object, ...],
    exc_info: object,
    func: str | None = None,
    sinfo: str | None = None,
    **kwargs: object,
) -> logging.LogRecord:
    record = _original_factory(
        name,
        level,
        pathname,
        lineno,
        msg,
        args,
        exc_info,
        func,
        sinfo,
        **kwargs,
    )

    ctx = _log_ctx_var.get()

    if ctx:
        record.msg = f"[{ctx}] {record.msg}"

    return record


logging.setLogRecordFactory(_context_record_factory)


class log_ctx:
    """Context manager that appends segments to the current parse context.

    Usage:
        with log_ctx("paths", url):
            ...
            with log_ctx("get"):
                ...
    """

    def __init__(self, *segments: str | None) -> None:
        """Initialize context manager with path segments to append."""
        self.segments = [s for s in segments if s is not None]

    def __enter__(self) -> log_ctx:
        """Enter context block, appending segments to the current context."""
        current = _log_ctx_var.get()

        parts = [current] if current else []
        parts.extend(self.segments)

        self._token = _log_ctx_var.set(".".join(parts))

        return self

    def __exit__(self, *_args: object) -> None:
        """Exit context block, restoring the previous context."""
        _log_ctx_var.reset(self._token)
