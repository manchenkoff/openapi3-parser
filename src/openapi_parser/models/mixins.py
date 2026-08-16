"""Deduplication, cache, and extension mixins for OpenAPI models."""

import threading
from typing import Any

from pydantic import BaseModel, Field, ValidationInfo, model_validator

_CACHE_ATTRIBUTE = "_ref_cache"

_thread_cache = threading.local()


class ExtensionsMixin(BaseModel):
    """Mixin that provides an ``extensions`` dict with automatic ``x-*`` extraction."""

    extensions: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def _extract_extensions(cls, data: Any) -> Any:
        """Move ``x-*`` keys into the extensions dict before model validation."""
        if not isinstance(data, dict):
            return data

        raw_extensions = data.get("extensions")
        extensions = dict(raw_extensions) if isinstance(raw_extensions, dict) else {}

        result = {}

        for key, value in data.items():
            if isinstance(key, str) and key.startswith("x-"):
                extensions[key] = value
            else:
                result[key] = value

        if extensions:
            result["extensions"] = extensions

        return result


class RefCacheMixin(BaseModel):
    """Mixin for models that can be $ref targets.

    Stores a per-class cache keyed by ref_name. When model_validate
    encounters the same ref_name twice, it returns the cached object,
    ensuring single Python object identity for each $ref.

    The cache lives in a ``threading.local`` so concurrent ``parse()``
    calls in different threads never share state.

    Circular refs are already broken by the resolver before Pydantic
    validation, so no cycle-handling logic is needed here.
    """

    ref_name: str | None = None

    @model_validator(mode="wrap")
    @classmethod
    def _deduplicate_refs(cls, value: Any, handler: Any, _info: ValidationInfo) -> Any:
        """Return the cached object for a ref_name already seen, otherwise validate and cache.

        Called by Pydantic automatically on models with this mixin.
        """
        if not cls._should_cache(value):
            return handler(value)

        ref_name: str = value["ref_name"]
        cache = cls._get_cache()

        if ref_name in cache:
            return cache[ref_name]

        result = handler(value)
        cache[ref_name] = result

        return result

    @classmethod
    def _should_cache(cls, value: Any) -> bool:
        """Check whether *value* has a ref_name that should be cached."""
        return (
            isinstance(value, dict)
            and "ref_name" in value
            and isinstance(value["ref_name"], str)
        )

    @classmethod
    def _get_cache(cls) -> dict[str, Any]:
        """Get or create the per-class ref cache for the current thread."""
        caches: dict[type, dict[str, Any]] | None = getattr(
            _thread_cache, _CACHE_ATTRIBUTE, None
        )

        if caches is None:
            caches = {}
            setattr(_thread_cache, _CACHE_ATTRIBUTE, caches)

        cache = caches.get(cls)

        if cache is None:
            cache = {}
            caches[cls] = cache

        return cache

    @classmethod
    def clear_ref_cache(cls) -> None:
        """Clear the ref cache for the current thread."""
        caches: dict[type, dict[str, Any]] | None = getattr(
            _thread_cache, _CACHE_ATTRIBUTE, None
        )

        if caches is not None:
            for cache in caches.values():
                cache.clear()
