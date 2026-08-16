"""Main entry point for the OpenAPI parser."""

import os
import types
from typing import Any, TypeAlias, cast

from pydantic import ValidationError
from yaml import YAMLError
from yaml import safe_load as safe_load_yaml

from openapi_parser import models
from openapi_parser.errors import ParserError
from openapi_parser.models.mixins import RefCacheMixin
from openapi_parser.models.v2_0 import normalize_swagger_v2
from openapi_parser.models.v3_0 import Specification as SpecificationV3_0
from openapi_parser.models.v3_1 import Specification as SpecificationV3_1
from openapi_parser.resolver import _read_uri, resolve

Specification: TypeAlias = SpecificationV3_0 | SpecificationV3_1

_VERSION_SPEC_MAP = {
    "2.0": models.v3_0,
    "3.0": models.v3_0,
    "3.1": models.v3_1,
    "3.2": models.v3_1,
}


def _detect_version(raw: dict[str, Any]) -> str:
    """Determine the OpenAPI/Swagger version from the raw spec dict."""
    if "swagger" in raw:
        return "2.0"

    # extract major.minor version from the string
    version_parts = raw.get("openapi", "").split(".")[:2]

    return ".".join(version_parts)


def _load_raw(uri: str | None, spec_string: str | None) -> dict[str, Any]:
    """Load and parse YAML/JSON from *uri* or *spec_string*."""
    try:
        if uri:
            raw = safe_load_yaml(_read_uri(uri))
        elif spec_string:
            raw = safe_load_yaml(spec_string)
        else:
            raise ParserError("Either uri or spec_string must be provided")
    except (OSError, YAMLError) as e:
        raise ParserError(f"Failed to load spec: {e}") from e

    if not isinstance(raw, dict):
        raise ParserError("OpenAPI spec must be a dictionary")

    return raw


def _validate_model(
    spec_module: types.ModuleType,
    resolved: dict[str, Any],
    version_key: str,
) -> Specification:
    """Validate the resolved spec against a version-specific module."""
    try:
        return cast(Specification, spec_module.Specification.model_validate(resolved))
    except ValidationError as e:
        raise ParserError(f"Validation failed for OpenAPI {version_key}: {e}") from e


def parse(
    uri: str | os.PathLike[str] | None = None,
    spec_string: str | None = None,
    base_uri: str | os.PathLike[str] | None = None,
) -> Specification:
    """Parse an OpenAPI/Swagger spec into fully typed Pydantic models.

    Parameters
    ----------
    uri : str, optional
        Location of the spec file. Accepts a local paths and URIs.
    spec_string : str, optional
        Raw spec YAML/JSON string (alternative to *uri*).
    base_uri : str, optional
        Location used to resolve external ``$ref`` targets when parsing
        a *spec_string* (e.g. ``"file:///path/to/specs/main.yaml"``).
        Ignored when *uri* is provided.

    Returns:
    -------
    Specification
        Version-specific typed specification model.

    Raises:
    ------
    ParserError
        On parse failures, wrapping the original exception.
    """
    RefCacheMixin.clear_ref_cache()

    if uri is not None:
        uri = os.fspath(uri)

    if base_uri is not None:
        base_uri = os.fspath(base_uri)

    raw = _load_raw(uri, spec_string)

    version = _detect_version(raw)
    if version == "2.0":
        raw = normalize_swagger_v2(raw)

    spec_module = _VERSION_SPEC_MAP.get(version)
    if spec_module is None:
        raise ParserError(f"Unsupported OpenAPI version: {version}")

    try:
        resolved = resolve(raw, base_uri if uri is None else uri, version)
    except Exception as e:
        raise ParserError(f"Failed to resolve references: {e}") from e

    return _validate_model(spec_module, resolved, version)
