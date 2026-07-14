"""OpenAPI specification resolver using the referencing library."""

from collections.abc import Callable
from os.path import abspath, dirname, isabs, join
from typing import Any, TypeVar, cast
from urllib.parse import urljoin, urlparse
from urllib.request import url2pathname, urlopen

from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
from yaml import safe_load

from openapi_parser.models.v3_0 import Components


def _read_uri(uri: str) -> str:
    """Read the full contents of a URI into a string."""
    parsed = urlparse(uri)

    if parsed.scheme in ("http", "https"):
        with urlopen(uri, timeout=10) as response:
            body: str = response.read().decode("utf-8")
            return body

    if parsed.scheme == "file":
        with open(url2pathname(parsed.path)) as f:
            return f.read()

    with open(uri) as f:
        return f.read()


def _make_retriever(base_uri: str) -> Callable[[str], Resource[Any]]:
    """Build a retriever callable for the ``referencing`` library.

    Handles both local files and HTTP(S) external ``$ref`` targets
    using the shared :func:`_read_uri` helper.
    """
    parsed = urlparse(base_uri)
    is_http = parsed.scheme in ("http", "https")

    if not is_http:
        resolved = url2pathname(parsed.path) if parsed.scheme == "file" else base_uri
        base_dir = dirname(abspath(resolved))

    def _retrieve(u: str) -> Resource[Any]:
        if is_http:
            ref_url = urljoin(base_uri, u)
            raw: Any = safe_load(_read_uri(ref_url))
        else:
            path = join(base_dir, u) if not isabs(u) else u
            raw = safe_load(_read_uri(path))

        return Resource.from_contents(raw, default_specification=DRAFT202012)

    return _retrieve


_COMPONENT_SECTIONS = frozenset(
    field.alias or name
    for name, field in Components.model_fields.items()
    if name != "extensions"
)


def _traverse(
    node: Any,
    process_dict: Callable[[dict[str, Any]], Any] | None = None,
    *,
    _tracking: set[int],
) -> Any:
    """Walk a JSON-like tree with ``id()``-based cycle tracking.

    For every dict encountered, *process_dict* is called first.
    If it returns a value other than ``None``, that value replaces the
    dict and recursion is skipped (used for ``$ref`` resolution and
    cycle-breaking placeholders).
    """
    if isinstance(node, dict):
        if process_dict is not None:
            replacement = process_dict(node)

            if replacement is not None:
                return replacement

        nid = id(node)

        _tracking.add(nid)

        try:
            for k, v in list(node.items()):
                node[k] = _traverse(v, process_dict, _tracking=_tracking)

            return node
        finally:
            _tracking.discard(nid)

    if isinstance(node, list):
        for i, v in enumerate(node):
            node[i] = _traverse(v, process_dict, _tracking=_tracking)

        return node

    return node


def _annotate_component_refs(data: dict[str, Any]) -> None:
    """Add ref_name to every component entry so RefCacheMixin can track them."""
    components = data.get("components")

    if not isinstance(components, dict):
        return

    for section in _COMPONENT_SECTIONS:
        entries = components.get(section)

        if not isinstance(entries, dict):
            continue

        for name, entry in entries.items():
            if isinstance(entry, dict) and "ref_name" not in entry:
                entry["ref_name"] = f"#/components/{section}/{name}"


T = TypeVar("T")


def _resolve_ref_node(
    node: dict[str, Any],
    resolver: Any,
    resolved_cache: dict[str, dict[str, Any]],
    _walking: set[int],
) -> Any:
    """Resolve a single $ref node and return the referenced content."""
    ref = node["$ref"]

    if ref in resolved_cache:
        cached: Any = resolved_cache[ref]

        if isinstance(cached, dict) and id(cached) in _walking:
            return {"ref_name": ref}

        return cached

    result = resolver.lookup(ref)
    contents = result.contents
    evolved_resolver = result.resolver

    if isinstance(contents, dict):
        resolved_cache[ref] = contents
        contents_id = id(contents)

        if contents_id in _walking:
            return {"ref_name": ref}

        if "$ref" in contents and isinstance(contents["$ref"], str):
            resolved = _resolve_ref_node(
                contents, evolved_resolver, resolved_cache, _walking
            )
            resolved_cache[ref] = resolved
            return resolved

        _walking.add(contents_id)

        try:
            for k, v in list(contents.items()):
                contents[k] = _walk(v, evolved_resolver, resolved_cache, _walking)
        finally:
            _walking.discard(contents_id)

        contents["ref_name"] = ref

        return contents

    return _walk(contents, evolved_resolver, resolved_cache, _walking)


def _walk(
    node: T,
    resolver: Any,
    resolved_cache: dict[str, dict[str, Any]] | None = None,
    _walking: set[int] | None = None,
) -> T:
    """Recursively walk and resolve all $ref nodes in the spec tree."""
    if resolved_cache is None:
        resolved_cache = {}

    if _walking is None:
        _walking = set()

    def _dict_fn(d: dict[str, Any]) -> Any:
        if "$ref" in d and isinstance(d["$ref"], str):
            return _resolve_ref_node(d, resolver, resolved_cache, _walking)

        return None

    return cast(T, _traverse(node, _dict_fn, _tracking=_walking))


def _build_registry(raw: dict[str, Any], uri: str | None = None) -> Registry[Any]:
    """Build a ``referencing`` Registry with the root spec loaded."""
    retrieval: Callable[[str], Resource[Any]] | None = (
        _make_retriever(uri) if uri else None
    )
    registry = (
        Registry(retrieve=retrieval) if retrieval else Registry()  # type: ignore[call-arg]  # referencing stubs missing ``retrieve``
    )

    return cast(
        "Registry[Any]",
        registry.with_resource(
            "urn:root",
            Resource.from_contents(raw, default_specification=DRAFT202012),
        ),
    )


def resolve(raw: dict[str, Any], uri: str | None = None) -> dict[str, Any]:
    """Resolve all ``$ref`` entries in *raw*, annotating each with *ref_name*.

    Every ``$ref`` is replaced with the resolved content plus a
    ``{"ref_name": "<ref path>"}`` marker. Python object cycles
    (self-referencing / bidirectional refs) are broken by replacing
    the nested occurrence with ``{"ref_name": "<path>"}``.
    """
    registry = _build_registry(raw, uri)
    resolver_obj = registry.resolver(base_uri="urn:root")
    result = _walk(raw, resolver_obj)
    _annotate_component_refs(result)

    return result
