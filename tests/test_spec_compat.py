"""Check the SDK against every supported panel version (tests/spec/remnawave-*.json).

test_spec_conformance holds the SDK to its target version field for field.
This one only looks for what breaks a call on an older or newer panel: an SDK
endpoint the panel lacks, a request missing a field the panel requires, a
response or webhook the models cannot parse. A field a newer panel adds is not
a break — the models drop unknown keys.
"""

import re
from pathlib import Path

import httpx
import pytest
from pydantic import ValidationError

from remnapy import models
from remnapy.models import webhook as webhook_models
from remnapy.rapid.client import BaseController
from tests import spec_utils
from tests.spec_utils import (
    compat_specs,
    load_spec,
    model_fields,
    normalize_path,
    request_schema,
    response_schema,
    sample_payload,
    schema_fields,
    sdk_endpoints,
    spec_endpoints,
    spec_version,
)
from tests.test_spec_conformance import NEWER_PANEL_FIELDS, WEBHOOK_SCHEMAS, _top_level

# SDK endpoints a panel gained after 3.0.0, by the version that added them.
ENDPOINT_SINCE: dict[tuple[str, str], tuple[int, ...]] = {
    ("GET", "/system/configuration"): (3, 2, 0),
}

# Fields the spec types looser than the panel fills them, so a sample built from
# the spec is not something the panel sends. Keyed by (model, error location
# with list indexes as `*`). Every entry must carry a reason.
SPEC_UNDERSTATES: dict[tuple[str, str], str] = {
    ("GetNodesStatisticsResponseDto", "lastSevenDays.*.date"): (
        "spec: plain string; the panel sends DATE_TRUNC(...)::date, an ISO date"
    ),
    **{
        (
            model,
            f"oauth2Settings.{provider}",
        ): "zod .default(): optional in the spec, always filled"
        for model in (
            "GetRemnawaveSettingsResponseDto",
            "UpdateRemnawaveSettingsResponseDto",
        )
        for provider in ("keycloak", "generic", "telegram")
    },
}

SAMPLE_MODES = {
    "populated": {},
    "nullable=null": {"nullable_as_null": True},
    "required-only": {"required_only": True},
}

SPECS = compat_specs()


def _version_id(path: Path) -> str:
    return ".".join(map(str, spec_version(path)))


@pytest.fixture(params=SPECS, ids=_version_id)
def spec_path(request) -> Path:
    return request.param


def _loc(loc: tuple) -> str:
    return re.sub(r"\.\d+(?=\.|$)", ".*", ".".join(map(str, loc)))


def _shared_endpoints(path: Path):
    """(SDK endpoint, spec operation) for every SDK endpoint the panel has."""
    spec_by_shape = {
        (method, normalize_path(route)): operation
        for (method, route), operation in spec_endpoints(path).items()
    }
    for endpoint in sorted(sdk_endpoints().values(), key=lambda e: (e.path, e.method)):
        operation = spec_by_shape.get((endpoint.method, normalize_path(endpoint.path)))
        if operation is not None:
            yield endpoint, operation


def test_spec_versions_present():
    """The target version and both ends of the supported range are checked."""
    versions = [spec_version(path) for path in SPECS]
    assert spec_version(spec_utils.SPEC_PATH) in versions
    assert versions[0] == (3, 0, 0)


def test_sdk_endpoints_exist(spec_path):
    """Every SDK endpoint is served by the panel, unless it came later."""
    version = spec_version(spec_path)
    spec_shapes = {(m, normalize_path(p)) for m, p in spec_endpoints(spec_path)}
    missing = sorted(
        f"  {e.method} {e.path} ({e.file}::{e.func})"
        for e in sdk_endpoints().values()
        if (e.method, normalize_path(e.path)) not in spec_shapes
        and version >= ENDPOINT_SINCE.get((e.method, e.path), (0,))
    )
    assert not missing, f"Not served by panel {_version_id(spec_path)}:\n" + "\n".join(
        missing
    )


def test_requests_carry_required_fields(spec_path):
    """Request models can send every top-level field the panel requires."""
    spec = load_spec(spec_path)
    problems = []
    for endpoint, operation in _shared_endpoints(spec_path):
        schema = request_schema(operation)
        model = getattr(models, endpoint.body_model or "", None)
        if schema is None or model is None:
            continue
        while "$ref" in schema:
            schema = spec["components"]["schemas"][schema["$ref"].rsplit("/", 1)[-1]]
        required = set(schema.get("required", []))
        known = {
            field.split(".")[0].split("[]")[0]
            for field in model_fields(model, strip_response=False)
        }
        if missing := sorted(required - known):
            problems.append(
                f"  {endpoint.method} {endpoint.path} — {model.__name__}: {missing}"
            )
    assert not problems, (
        f"Requests lack fields panel {_version_id(spec_path)} requires:\n"
        + "\n".join(problems)
    )


@pytest.mark.parametrize("mode", SAMPLE_MODES)
def test_responses_parse(spec_path, mode):
    """Response models parse what the panel sends, through the SDK's own parser."""
    spec = load_spec(spec_path)
    problems = []
    for endpoint, operation in _shared_endpoints(spec_path):
        schema = response_schema(operation)
        response_class = getattr(models, endpoint.response_model or "", None)
        if schema is None or response_class is None:
            continue
        payload = sample_payload(schema, spec, **SAMPLE_MODES[mode])
        response = httpx.Response(
            200, json=payload, request=httpx.Request(endpoint.method, "http://panel")
        )
        try:
            BaseController._handle_response(None, response, response_class)  # type: ignore[arg-type]
        except ValidationError as exc:
            errors = [
                f"{_loc(error['loc'])}: {error['msg']}"
                for error in exc.errors()
                if (response_class.__name__, _loc(error["loc"])) not in SPEC_UNDERSTATES
            ]
            if errors:
                problems.append(
                    f"  {endpoint.method} {endpoint.path} — {response_class.__name__}: {'; '.join(errors)}"
                )
    assert not problems, (
        f"Responses of panel {_version_id(spec_path)} fail to parse:\n"
        + "\n".join(problems)
    )


@pytest.mark.parametrize("mode", SAMPLE_MODES)
def test_webhooks_parse(spec_path, mode):
    """Webhook models parse the panel's webhook payloads."""
    spec = load_spec(spec_path)
    problems = []
    for schema_name, model_name in WEBHOOK_SCHEMAS.items():
        schema = spec["components"]["schemas"].get(schema_name)
        if schema is None:
            continue
        payload = sample_payload(schema, spec, **SAMPLE_MODES[mode])
        try:
            getattr(webhook_models, model_name).model_validate(payload)
        except ValidationError as exc:
            errors = [f"{_loc(error['loc'])}: {error['msg']}" for error in exc.errors()]
            problems.append(f"  {model_name}: {'; '.join(errors)}")
    assert not problems, (
        f"Webhooks of panel {_version_id(spec_path)} fail to parse:\n"
        + "\n".join(problems)
    )


def test_newer_panel_fields_match(spec_path):
    """Fields modeled ahead of the target version match the panels that have them."""
    version = spec_version(spec_path)
    spec = load_spec(spec_path)
    problems = []
    for endpoint, operation in _shared_endpoints(spec_path):
        for name, schema, strip in (
            (endpoint.body_model, request_schema(operation), False),
            (endpoint.response_model, response_schema(operation), True),
        ):
            model = getattr(models, name or "", None)
            if model is None or schema is None:
                continue
            for (model_name, top), (since, _) in NEWER_PANEL_FIELDS.items():
                if model_name != model.__name__ or version < since:
                    continue
                ours = {
                    f
                    for f in model_fields(model, strip_response=strip)
                    if _top_level(f) == top
                }
                if not ours:
                    continue
                theirs = {
                    f
                    for f in schema_fields(schema, spec, strip_response=strip)
                    if _top_level(f) == top
                }
                if ours != theirs:
                    problems.append(
                        f"  {endpoint.method} {endpoint.path} — {model.__name__}.{top}: "
                        f"missing {sorted(theirs - ours)}, extra {sorted(ours - theirs)}"
                    )
    assert not problems, (
        f"Fields diverge from panel {_version_id(spec_path)}:\n" + "\n".join(problems)
    )
