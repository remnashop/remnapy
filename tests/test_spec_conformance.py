"""Check the SDK against the Remnawave 3.2.1 OpenAPI spec.

These tests are offline: no live panel is needed, only shape is compared.
"""

import re

import pytest

from remnapy import models
from remnapy.enums.error_code import ErrorCode
from tests import spec_utils
from tests.spec_utils import (
    load_spec,
    model_fields,
    normalize_path,
    request_schema,
    response_schema,
    schema_fields,
    sdk_endpoints,
    spec_endpoints,
    spec_path_params,
    spec_query_params,
)

# Divergences accepted as intentional. Every entry must carry a reason.
ALLOWED_FIELD_DIFFS: dict[tuple[str, str], str] = {}

HOST_MODELS: tuple[str, ...] = (
    "CreateHostRequestDto",
    "UpdateHostRequestDto",
    "UpdateManyHostsRequestDto",
    "CreateHostResponseDto",
    "UpdateHostResponseDto",
    "GetAllHostsResponseDto",
    "GetOneHostResponseDto",
)

# Top-level fields the SDK models for panels newer than the target version,
# keyed by (model, field): (version that added it, reason). Not in the target
# spec, so not "extra"; test_spec_compat checks them against the specs that
# have them.
NEWER_PANEL_FIELDS: dict[tuple[str, str], tuple[tuple[int, ...], str]] = {
    **{
        (model, "internalSquads"): ((3, 4, 0), "host squad mode, replaces excludedInternalSquads")
        for model in HOST_MODELS
    },
    **{(model, "mapper"): ((3, 3, 0), "host config rewrites per client") for model in HOST_MODELS},
}

# Known query-parameter divergences left unresolved. Keyed by (METHOD,
# normalized path). Every entry must carry a reason.
ALLOWED_QUERY_PARAM_DIFFS: dict[tuple[str, str], str] = {}


def _spec_by_shape() -> dict[tuple[str, str], tuple[str, dict]]:
    """Spec endpoints keyed by normalized path."""
    return {
        (method, normalize_path(path)): (path, operation)
        for (method, path), operation in spec_endpoints().items()
    }


def _sdk_by_shape() -> dict[tuple[str, str], spec_utils.SdkEndpoint]:
    return {
        (endpoint.method, normalize_path(endpoint.path)): endpoint
        for endpoint in sdk_endpoints().values()
    }


def test_no_missing_endpoints():
    """Every endpoint in the spec is declared in an SDK controller."""
    missing = sorted(set(_spec_by_shape()) - set(_sdk_by_shape()))
    assert not missing, "Missing from the SDK:\n" + "\n".join(f"  {m} {p}" for m, p in missing)


def test_no_stale_endpoints():
    """The SDK controllers declare no endpoint the spec does not have."""
    sdk = _sdk_by_shape()
    stale = sorted(set(sdk) - set(_spec_by_shape()))
    assert not stale, "Not in the spec:\n" + "\n".join(
        f"  {m} {p} ({sdk[(m, p)].file}::{sdk[(m, p)].func})" for m, p in stale
    )


def test_path_params_match():
    """Path-parameter names match the spec."""
    spec_shapes = _spec_by_shape()
    mismatches = []
    for shape, endpoint in _sdk_by_shape().items():
        if shape not in spec_shapes:
            continue
        spec_path, _ = spec_shapes[shape]
        expected = spec_path_params(spec_path)
        actual = spec_path_params(endpoint.path)
        if expected != actual:
            mismatches.append(f"  {endpoint.file}::{endpoint.func}: {endpoint.path} -> expected {spec_path}")
    assert not mismatches, "Path parameters diverge:\n" + "\n".join(mismatches)


def test_query_params_match():
    """Query-parameter names match the spec (alias-aware)."""
    spec_shapes = _spec_by_shape()
    mismatches = []
    for shape, endpoint in sorted(_sdk_by_shape().items()):
        if shape not in spec_shapes:
            continue
        if shape in ALLOWED_QUERY_PARAM_DIFFS:
            continue
        _, operation = spec_shapes[shape]
        expected = spec_query_params(operation)
        actual = endpoint.query_params
        missing, extra = expected - actual, actual - expected
        if missing or extra:
            lines = [f"  {shape[0]} {shape[1]} ({endpoint.file}::{endpoint.func})"]
            lines += [f"    + missing from the SDK: {name}" for name in sorted(missing)]
            lines += [f"    - extra in the SDK: {name}" for name in sorted(extra)]
            mismatches.append("\n".join(lines))
    assert not mismatches, "Query parameters diverge:\n" + "\n".join(mismatches)


def _field_diff(
    model_name: str, schema: dict | None, spec: dict, *, strip_response: bool
) -> tuple[set[str], set[str]]:
    """(spec fields missing from the model; model fields missing from the spec).

    `strip_response` must be True only for response schemas and models: a
    request body is never wrapped in a `response` envelope, so a field by that
    name there is genuine (see `VerifyPasskeyRegistrationBodyDto`).
    """
    model = getattr(models, model_name, None)
    if model is None or not hasattr(model, "model_fields"):
        return set(), set()
    expected = schema_fields(schema, spec, strip_response=strip_response)
    actual = model_fields(model, strip_response=strip_response)
    return expected - actual, actual - expected


def _top_level(field: str) -> str:
    return re.split(r"\.|\[\]", field.removeprefix("[]"), maxsplit=1)[0]


@pytest.mark.parametrize("kind", ["request", "response"])
def test_models_match_spec(kind):
    """Request/response model fields match the spec schemas."""
    spec = load_spec()
    spec_shapes = _spec_by_shape()
    problems = []

    for shape, endpoint in sorted(_sdk_by_shape().items()):
        if shape not in spec_shapes:
            continue
        _, operation = spec_shapes[shape]

        if kind == "response":
            model_name, schema = endpoint.response_model, response_schema(operation)
        else:
            model_name, schema = endpoint.body_model, request_schema(operation)

        if model_name is None or schema is None:
            continue
        if (model_name, kind) in ALLOWED_FIELD_DIFFS:
            continue

        missing, extra = _field_diff(model_name, schema, spec, strip_response=(kind == "response"))
        extra = {field for field in extra if (model_name, _top_level(field)) not in NEWER_PANEL_FIELDS}
        if missing or extra:
            lines = [f"  {shape[0]} {shape[1]} — {model_name} ({endpoint.file}::{endpoint.func})"]
            lines += [f"    + missing from the SDK: {field}" for field in sorted(missing)]
            lines += [f"    - extra in the SDK: {field}" for field in sorted(extra)]
            problems.append("\n".join(lines))

    assert not problems, f"{kind} models diverge from the spec:\n" + "\n".join(problems)


def test_error_codes_complete():
    """ErrorCode covers every error code in the spec.

    The check is one-directional: the SDK also carries panel runtime codes
    (AUTH*, BL*, N* and others) that the spec never documents, and those must
    survive.
    """
    import json

    spec_codes = set(re.findall(r'"([A-Z]\d{3})"', json.dumps(load_spec())))
    sdk_codes = {member.value for member in ErrorCode}
    missing = sorted(spec_codes - sdk_codes)
    assert not missing, f"Missing from ErrorCode: {missing}"


WEBHOOK_SCHEMAS = {
    "RemnawaveWebhookUserEventsDto": "UserEventDto",
    "RemnawaveWebhookUserHwidDevicesEventsDto": "UserHwidDeviceEventDto",
    "RemnawaveWebhookNodeEventsDto": "NodeEventDto",
    "RemnawaveWebhookServiceEventsDto": "ServiceEventDto",
    "RemnawaveWebhookErrorsEventsDto": "CustomErrorEventDto",
    "RemnawaveWebhookCrmEventsDto": "CrmEventDto",
    "RemnawaveWebhookTorrentBlockerEventsDto": "TorrentBlockerEventDto",
}


def test_webhook_models_match():
    """Webhook models match the RemnawaveWebhook*EventsDto schemas."""
    from remnapy.models import webhook as webhook_models

    spec = load_spec()
    problems = []
    for schema_name, model_name in WEBHOOK_SCHEMAS.items():
        schema = spec["components"]["schemas"][schema_name]
        model = getattr(webhook_models, model_name)
        expected = schema_fields(schema, spec)
        actual = model_fields(model)
        missing, extra = expected - actual, actual - expected
        if missing or extra:
            lines = [f"  {schema_name} — {model_name}"]
            lines += [f"    + missing from the SDK: {field}" for field in sorted(missing)]
            lines += [f"    - extra in the SDK: {field}" for field in sorted(extra)]
            problems.append("\n".join(lines))

    assert not problems, "Webhook models diverge from the spec:\n" + "\n".join(problems)


@pytest.mark.parametrize("nullable_as_null", [False, True], ids=["populated", "nullable=null"])
def test_webhook_models_accept_spec_payloads(nullable_as_null):
    """Webhook models parse a payload built from the spec.

    Field-name comparison (`test_webhook_models_match`) sees neither types nor
    optionality. Webhooks are pushed by the panel rather than requested, so
    there is no other way to exercise their parsing — hence building the
    payload from the schema.
    """
    from remnapy.models import webhook as webhook_models

    spec = load_spec()
    problems = []
    for schema_name, model_name in WEBHOOK_SCHEMAS.items():
        schema = spec["components"]["schemas"][schema_name]
        payload = spec_utils.sample_payload(schema, spec, nullable_as_null=nullable_as_null)
        try:
            getattr(webhook_models, model_name).model_validate(payload)
        except Exception as exc:  # noqa: BLE001
            problems.append(f"  {model_name}: {str(exc).splitlines()[0]}")

    assert not problems, "Webhook models fail to parse a spec-shaped payload:\n" + "\n".join(problems)
