"""Swagger 2.0 to OpenAPI 3.0 normalization helper."""

from collections.abc import Iterator
from typing import Any


def _iter_path_entries(
    data: dict[str, Any],
) -> Iterator[tuple[str, str, dict[str, Any]]]:
    """Yield ``(path, key, value)`` for every dict entry in every path item."""
    paths = data.get("paths", {})

    if not isinstance(paths, dict):
        return

    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue

        for key, value in path_item.items():
            if isinstance(value, dict):
                yield path, key, value


def normalize_swagger_v2(data: dict[str, Any]) -> dict[str, Any]:
    """Transform Swagger 2.0 dict to OpenAPI 3.0-compatible shape."""
    data["openapi"] = "3.0.0"

    # host + basePath + schemes → servers
    if "host" in data or "basePath" in data or "schemes" in data:
        host = data.pop("host", "localhost")
        base_path = data.pop("basePath", "")
        schemes = data.pop("schemes", ["https"])
        data["servers"] = [
            {"url": f"{scheme}://{host}{base_path}"} for scheme in schemes
        ]

    # definitions → components.schemas
    if "definitions" in data:
        data.setdefault("components", {})["schemas"] = data.pop("definitions")

    # securityDefinitions → components.securitySchemes
    if "securityDefinitions" in data:
        data.setdefault("components", {})["securitySchemes"] = data.pop(
            "securityDefinitions"
        )

    # parameters -> components.parameters
    if "parameters" in data:
        data.setdefault("components", {})["parameters"] = data.pop("parameters")

    # responses -> components.responses
    if "responses" in data:
        data.setdefault("components", {})["responses"] = data.pop("responses")

    # Rewrite $ref strings
    data = _rewrite_refs(data)

    # consumes/produces → per-operation defaults & inject
    _inject_content_defaults(data)

    # in: formData parameters → requestBody
    _convert_formdata_to_request_body(data)

    # in: body parameters → requestBody
    _convert_body_parameters(data)

    # convert response schemas
    _convert_responses(data)

    return data


def _rewrite_refs(node: Any) -> Any:
    """Rewrite Swagger 2.0 $ref paths to OpenAPI 3.0 equivalents."""
    if isinstance(node, dict):
        if "$ref" in node and isinstance(node["$ref"], str):
            ref = node["$ref"]

            if ref.startswith("#/definitions/"):
                node["$ref"] = ref.replace(
                    "#/definitions/",
                    "#/components/schemas/",
                )
            elif ref.startswith("#/securityDefinitions/"):
                node["$ref"] = ref.replace(
                    "#/securityDefinitions/",
                    "#/components/securitySchemes/",
                )
            elif ref.startswith("#/parameters/"):
                node["$ref"] = ref.replace(
                    "#/parameters/",
                    "#/components/parameters/",
                )
            elif ref.startswith("#/responses/"):
                node["$ref"] = ref.replace(
                    "#/responses/",
                    "#/components/responses/",
                )

        return {k: _rewrite_refs(v) for k, v in node.items()}

    if isinstance(node, list):
        return [_rewrite_refs(v) for v in node]

    return node


def _inject_content_defaults(data: dict[str, Any]) -> None:
    """Migrate global consumes/produces into each operation."""
    global_consumes = data.pop("consumes", ["application/json"])
    global_produces = data.pop("produces", ["application/json"])

    for _, _, operation in _iter_path_entries(data):
        if "consumes" in operation:
            operation["consumes"] = list(operation["consumes"])
        else:
            operation["consumes"] = list(global_consumes)

        if "produces" in operation:
            operation["produces"] = list(operation["produces"])
        else:
            operation["produces"] = list(global_produces)


def _build_formdata_schema(form_params: list[dict[str, Any]]) -> dict[str, Any]:
    """Build an object schema from formData parameter definitions."""
    properties: dict[str, Any] = {}
    required: list[str] = []

    for param in form_params:
        name = param.get("name")

        if not name:
            continue

        prop_schema: dict[str, Any] = {}

        for field in ("type", "description", "default", "enum", "format", "items"):
            if field in param:
                prop_schema[field] = param[field]

        properties[name] = prop_schema

        if param.get("required"):
            required.append(name)

    schema: dict[str, Any] = {"type": "object", "properties": properties}

    if required:
        schema["required"] = required

    return schema


def _convert_formdata_to_request_body(data: dict[str, Any]) -> None:
    """Merge formData parameters into a single requestBody per operation."""
    for _, _, operation in _iter_path_entries(data):
        parameters = operation.get("parameters", [])

        if not isinstance(parameters, list):
            continue

        form_params = []
        new_parameters = []

        for param in parameters:
            if isinstance(param, dict) and param.get("in") == "formData":
                form_params.append(param)
            else:
                new_parameters.append(param)

        operation["parameters"] = new_parameters

        if form_params:
            schema = _build_formdata_schema(form_params)

            consumes = operation.pop("consumes", ["application/x-www-form-urlencoded"])
            if not consumes:
                consumes = ["application/x-www-form-urlencoded"]

            content = {}
            for mime in consumes:
                content[mime] = {"schema": schema}

            operation["requestBody"] = {"required": True, "content": content}


def _convert_body_parameters(data: dict[str, Any]) -> None:
    """Convert body parameters into a requestBody object per operation."""
    for _, _, operation in _iter_path_entries(data):
        parameters = operation.get("parameters", [])

        if not isinstance(parameters, list):
            continue

        body_param = None
        new_parameters = []

        for param in parameters:
            if isinstance(param, dict) and param.get("in") == "body":
                body_param = param
            else:
                new_parameters.append(param)

        operation["parameters"] = new_parameters

        if body_param:
            consumes = operation.pop("consumes", ["application/json"])
            content = {}
            schema = body_param.get("schema", {})

            for mime in consumes:
                content[mime] = {"schema": schema}

            operation["requestBody"] = {
                "required": body_param.get("required", False),
                "description": body_param.get("description"),
                "content": content,
            }


def _convert_responses(data: dict[str, Any]) -> None:
    """Wrap response schemas into content/media-type structure."""
    for _, _, operation in _iter_path_entries(data):
        produces = operation.pop("produces", ["application/json"])
        responses = operation.get("responses", {})

        if not isinstance(responses, dict):
            continue

        for _code, response in responses.items():
            if not isinstance(response, dict):
                continue

            if "schema" in response:
                schema = response.pop("schema")
                content = {}

                for mime in produces:
                    content[mime] = {"schema": schema}

                response["content"] = content
