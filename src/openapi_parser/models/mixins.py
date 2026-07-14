"""Deduplication, cache, and extension mixins for OpenAPI models."""

from typing import Any

from pydantic import BaseModel, Field, ValidationInfo, model_validator

_CACHE_ATTRIBUTE = "_ref_cache"


class ExtensionsMixin(BaseModel):
    """Mixin that provides an ``extensions`` dict with automatic ``x-*`` extraction."""

    extensions: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def _extract_extensions(cls, data: Any) -> Any:
        """Move ``x-*`` keys into the extensions dict before model validation."""
        if not isinstance(data, dict):
            return data

        extensions = data.get("extensions", {})

        if not isinstance(extensions, dict):
            extensions = {}

        original_keys = list(data.keys())

        for key in original_keys:
            if isinstance(key, str) and key.startswith("x-"):
                extensions[key] = data.pop(key)

        if extensions:
            data["extensions"] = extensions

        return data


class RefCacheMixin(BaseModel):
    """Mixin for models that can be $ref targets.

    Stores a per-class cache keyed by ref_name. When model_validate
    encounters the same ref_name twice, it returns the cached object,
    ensuring single Python object identity for each $ref.

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
        """Get or create the per-class ref cache dictionary."""
        cache: dict[str, Any] | None = getattr(cls, _CACHE_ATTRIBUTE, None)

        if cache is None:
            cache = {}
            setattr(cls, _CACHE_ATTRIBUTE, cache)

        return cache

    @classmethod
    def clear_ref_cache(cls) -> None:
        """Clear the ref cache for this class and all subclasses."""
        cls._get_cache().clear()

        for subclass in cls.__subclasses__():
            subclass.clear_ref_cache()
