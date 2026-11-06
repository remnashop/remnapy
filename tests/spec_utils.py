"""Helpers for checking the SDK against the Remnawave OpenAPI spec."""

from __future__ import annotations

import ast
import json
import re
import typing
from dataclasses import dataclass
from functools import cache, lru_cache
from pathlib import Path
from typing import Any

from pydantic import BaseModel

SPEC_DIR = Path(__file__).parent / "spec"
# The version the SDK mirrors: checked field for field (test_spec_conformance).
SPEC_PATH = SPEC_DIR / "remnawave-3.4.8.json"
CONTROLLERS_DIR = Path(__file__).parent.parent / "remnapy" / "controllers"

HTTP_METHODS = ("get", "post", "put", "patch", "delete")

# How deep nested structures are expanded. Must match between schemas and
# models, otherwise deep trees produce phantom divergences.
MAX_DEPTH = 16


@dataclass(frozen=True)
class SdkEndpoint:
    """An endpoint declared by a decorator in an SDK controller."""

    method: str
    path: str
    response_model: str | None
    body_model: str | None
    func: str
    file: str
    query_params: frozenset[str] = frozenset()


@cache
def load_spec(path: Path = SPEC_PATH) -> dict[str, Any]:
    """Load an OpenAPI spec, the target version's by default."""
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def compat_specs() -> list[Path]:
    """Specs of every panel version the SDK must keep working with, oldest first."""
    return sorted(SPEC_DIR.glob("remnawave-*.json"), key=lambda path: spec_version(path))


def spec_version(path: Path) -> tuple[int, ...]:
    """`remnawave-3.4.8.json` -> (3, 4, 8)."""
    return tuple(int(part) for part in path.stem.removeprefix("remnawave-").split("."))


def normalize_path(path: str) -> str:
    """Replace path-parameter names with placeholders: /users/{userId} -> /users/{}."""
    return re.sub(r"\{[^}]+\}", "{}", path)


@cache
def spec_endpoints(path: Path = SPEC_PATH) -> dict[tuple[str, str], dict[str, Any]]:
    """Endpoints from the spec, keyed by (METHOD, path without the /api prefix)."""
    spec = load_spec(path)
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for route, operations in spec["paths"].items():
        sdk_path = route.removeprefix("/api")
        for method, operation in operations.items():
            if method in HTTP_METHODS:
                result[(method.upper(), sdk_path)] = operation
    return result


@lru_cache(maxsize=1)
def sdk_endpoints() -> dict[tuple[str, str], SdkEndpoint]:
    """Endpoints declared across the SDK controllers."""
    result: dict[tuple[str, str], SdkEndpoint] = {}
    for source in sorted(CONTROLLERS_DIR.glob("*.py")):
        tree = ast.parse(source.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
                continue
            for decorator in node.decorator_list:
                endpoint = _parse_decorator(decorator, node, source.name)
                if endpoint is not None:
                    result[(endpoint.method, endpoint.path)] = endpoint
    return result


def _parse_decorator(
    decorator: ast.expr, func: ast.AsyncFunctionDef | ast.FunctionDef, filename: str
) -> SdkEndpoint | None:
    if not isinstance(decorator, ast.Call) or not isinstance(decorator.func, ast.Name):
        return None
    if decorator.func.id not in HTTP_METHODS:
        return None
    if not decorator.args or not isinstance(decorator.args[0], ast.Constant):
        return None

    response_model = None
    for keyword in decorator.keywords:
        if keyword.arg == "response_class" and isinstance(keyword.value, ast.Name):
            response_model = keyword.value.id

    body_model = None
    query_params: set[str] = set()
    for arg in func.args.args:
        if arg.annotation is None:
            continue
        annotation_src = ast.unparse(arg.annotation)
        if arg.arg == "body":
            match = re.search(r"Annotated\[\s*([A-Za-z_0-9]+)", annotation_src)
            if match:
                body_model = match.group(1)
        if "Query(" in annotation_src:
            alias_match = re.search(r"alias=['\"]([^'\"]+)['\"]", annotation_src)
            query_params.add(alias_match.group(1) if alias_match else arg.arg)

    return SdkEndpoint(
        method=decorator.func.id.upper(),
        path=decorator.args[0].value,
        response_model=response_model,
        body_model=body_model,
        func=func.name,
        file=filename,
        query_params=frozenset(query_params),
    )


def schema_fields(
    schema: dict[str, Any] | None, spec: dict[str, Any], *, strip_response: bool = True
) -> set[str]:
    """Flatten a JSON schema into a set of field paths.

    Arrays are marked with a `[]` suffix and nesting with a dot:
    `users[]activeInternalSquads[]uuid`. The `response` envelope is stripped
    when `strip_response=True` (the default; turn it off for request-body
    schemas, where a `response` field is a real field rather than an envelope).

    When there is nothing to strip — the whole schema is the envelope itself
    with no nested property, e.g. `{"response": {}}` — the field keeps the
    envelope's name instead of collapsing to an empty string. An empty string
    would drop the endpoint from the report rather than naming it
    (see `_strip_envelope`).
    """
    fields = _walk_schema(schema, spec, seen=frozenset(), depth=0)
    return {_strip_envelope(field, strip_response=strip_response) for field in fields}


def _walk_schema(
    node: dict[str, Any] | None,
    spec: dict[str, Any],
    seen: frozenset[str],
    depth: int,
) -> set[str]:
    if node is None or depth > MAX_DEPTH:
        return set()

    if "$ref" in node:
        name = node["$ref"].rsplit("/", 1)[-1]
        if name in seen:
            return set()
        target = spec["components"]["schemas"].get(name, {})
        return _walk_schema(target, spec, seen | {name}, depth + 1)

    for combinator in ("allOf", "oneOf", "anyOf"):
        if combinator in node:
            combined: set[str] = set()
            for sub in node[combinator]:
                combined |= _walk_schema(sub, spec, seen, depth + 1)
            return combined

    if node.get("type") == "array":
        return {f"[]{field}" for field in _walk_schema(node.get("items"), spec, seen, depth + 1)}

    if "properties" in node:
        fields: set[str] = set()
        for name, sub in node["properties"].items():
            children = _walk_schema(sub, spec, seen, depth + 1)
            if children:
                fields |= {f"{name}{'' if child.startswith('[]') else '.'}{child}" for child in children}
            else:
                fields.add(name)
        return fields

    return set()


def model_fields(model: type, *, strip_response: bool = True) -> set[str]:
    """Flatten a pydantic model into a set of field paths.

    Paths use the same format as `schema_fields`. The `RootModel` wrapper is
    always unwrapped; `strip_response` controls the `response` envelope (see
    `_strip_envelope`) and must be off for request bodies.

    As in `schema_fields`, a field with nothing to strip beyond the envelope
    keeps the envelope's name rather than collapsing to an empty string.
    """
    fields = _walk_model(model, seen=frozenset(), depth=0)
    return {_strip_envelope(field, strip_response=strip_response) for field in fields}


def _walk_model(model: type, seen: frozenset[type], depth: int) -> set[str]:
    if depth > MAX_DEPTH or model in seen or not hasattr(model, "model_fields"):
        return set()

    fields: set[str] = set()
    for name, field in model.model_fields.items():
        alias = field.alias or field.serialization_alias or field.validation_alias or name
        if not isinstance(alias, str):
            alias = name

        children = _annotation_fields(field.annotation, seen | {model}, depth + 1)
        if children:
            fields |= {f"{alias}{'' if child.startswith('[]') else '.'}{child}" for child in children}
        else:
            fields.add(alias)
    return fields


def _annotation_fields(annotation: Any, seen: frozenset[type], depth: int) -> set[str]:
    """Fields of a nested model inside an annotation (Optional, Union, list, ...)."""
    result: set[str] = set()
    for candidate in _unwrap_annotation(annotation):
        if isinstance(candidate, type) and issubclass(candidate, BaseModel):
            result |= _walk_model(candidate, seen, depth)
            continue
        origin = typing.get_origin(candidate)
        if origin in (list, set, tuple):
            args = typing.get_args(candidate)
            if args:
                nested = _annotation_fields(args[0], seen, depth)
                result |= {f"[]{field}" for field in nested}
    return result


def _unwrap_annotation(annotation: Any) -> list[Any]:
    """Unwrap Optional/Union/Annotated into a list of candidate types."""
    origin = typing.get_origin(annotation)
    if origin is typing.Union or getattr(origin, "__name__", None) == "UnionType":
        return [arg for arg in typing.get_args(annotation) if arg is not type(None)]
    if origin is typing.Annotated or getattr(annotation, "__metadata__", None) is not None:
        args = typing.get_args(annotation)
        if args:
            return _unwrap_annotation(args[0])
    return [annotation]


def _strip_envelope(field: str, *, strip_response: bool = True) -> str:
    """Strip the outer `response.` (spec) or `root.` (RootModel) envelope.

    The `response` envelope exists only on response schemas — the panel never
    wraps a request body in one — so on request schemas and models a `response`
    field is genuine and must survive (`strip_response=False`). The `root`
    envelope is pydantic's `RootModel` unwrapping, a separate mechanism, and is
    always stripped.

    When the field *is* the envelope and there is nothing beneath it (e.g. a
    response schema of `{"response": {}}` with no nested property, or a model
    with no fields), the name is not cut down to an empty string: an empty
    string is not a field name, it is the endpoint vanishing from the report.
    The envelope's own name (`response`/`root`) is returned instead, so the
    endpoint stays visible under a readable name.
    """
    envelopes = ("response", "root") if strip_response else ("root",)
    for envelope in envelopes:
        if field == envelope:
            return field
        if field.startswith(f"{envelope}."):
            return field[len(envelope) + 1 :]
        if field.startswith(f"{envelope}[]"):
            return field[len(envelope) :]
    return field


def response_schema(operation: dict[str, Any]) -> dict[str, Any] | None:
    """Schema of an operation's successful response (200 or 201)."""
    for code in ("200", "201"):
        response = operation.get("responses", {}).get(code)
        if response is None:
            continue
        return response.get("content", {}).get("application/json", {}).get("schema")
    return None


def request_schema(operation: dict[str, Any]) -> dict[str, Any] | None:
    """Schema of an operation's request body."""
    body = operation.get("requestBody", {})
    return body.get("content", {}).get("application/json", {}).get("schema")


def spec_path_params(path: str) -> list[str]:
    """Path-parameter names, in order of appearance."""
    return re.findall(r"\{([^}]+)\}", path)


def spec_query_params(operation: dict[str, Any]) -> set[str]:
    """Query-parameter names of a spec operation."""
    return {
        param["name"]
        for param in operation.get("parameters", [])
        if param.get("in") == "query"
    }


def sample_payload(
    schema: dict[str, Any] | None,
    spec: dict[str, Any],
    nullable_as_null: bool = False,
    depth: int = 0,
    required_only: bool = False,
) -> Any:
    """Build a value that satisfies the schema.

    Needed to check models against data rather than field names alone: name
    comparison sees neither types nor optionality, and that is exactly where
    part of this migration's defects hid.

    ``nullable_as_null`` substitutes ``None`` everywhere the spec marks a field
    ``nullable``, which checks that the model survives empty values.
    ``required_only`` leaves out every property the spec does not require,
    which checks that the model demands nothing the panel may omit.
    """
    if depth > 12 or schema is None:
        return None

    if "$ref" in schema:
        target = spec["components"]["schemas"].get(schema["$ref"].rsplit("/", 1)[-1], {})
        return sample_payload(target, spec, nullable_as_null, depth + 1, required_only)

    if "allOf" in schema:
        # an intersection: every part contributes properties
        merged: dict[str, Any] = {}
        for part in schema["allOf"]:
            value = sample_payload(part, spec, nullable_as_null, depth + 1, required_only)
            if isinstance(value, dict):
                merged.update(value)
        return merged
    for combinator in ("oneOf", "anyOf"):
        if combinator in schema:
            return sample_payload(schema[combinator][0], spec, nullable_as_null, depth + 1, required_only)

    if schema.get("nullable") and nullable_as_null:
        return None
    if not schema:
        # `{}` is the spec's "any": the panel sends an object there (configs, WebAuthn options)
        return {}
    if "enum" in schema:
        return schema["enum"][0]

    kind = schema.get("type")
    if kind == "object" and "properties" not in schema:
        return {}
    if kind == "object" or "properties" in schema:
        required = set(schema.get("required", []))
        return {
            name: sample_payload(sub, spec, nullable_as_null, depth + 1, required_only)
            for name, sub in schema.get("properties", {}).items()
            if not required_only or name in required
        }
    if kind == "array":
        return [sample_payload(schema.get("items"), spec, nullable_as_null, depth + 1, required_only)]
    if kind == "string":
        return _sample_string(schema)
    if kind in ("number", "integer"):
        return 1
    if kind == "boolean":
        return True
    return None


def _sample_string(schema: dict[str, Any]) -> str:
    fmt = schema.get("format")
    if fmt == "date-time":
        return "2026-01-01T00:00:00.000Z"
    if fmt == "date":
        return "2026-01-01"
    if fmt == "uuid":
        return "0199aa11-0000-4000-8000-000000000000"
    if fmt == "email":
        return "user@example.com"
    if fmt in ("uri", "url"):
        return "https://example.com/x"
    if fmt == "ipv4":
        return "127.0.0.1"
    if fmt == "ipv6":
        return "::1"

    pattern = schema.get("pattern", "")
    # zod's ISO datetime regex; some panel builds drop `format: date-time`
    if "[2468][048]" in pattern:
        return "2026-01-01T00:00:00.000Z"
    if pattern == "^[A-Z0-9_:]+$":
        return "TAG"
    if "0-9a-fA-F" in pattern:
        return "0199aa11-0000-4000-8000-000000000000"
    return "sample"
