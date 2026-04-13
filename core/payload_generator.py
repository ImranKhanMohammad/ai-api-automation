import re
import json

from client.api_client import call_api
from ai.llm_client import LLMClient

TYPE_DEFAULTS = {
    "string": "",
    "integer": 0,
    "number": 0.0,
    "boolean": False,
    "array": [],
    "object": {},
}


def _base_resource(endpoint: str) -> str:
    """
    Extract base resource from endpoint.
    /employees                    -> /employees
    /employees/{emp_id}           -> /employees
    /employees/{emp_id}/terminate -> /employees
    """
    match = re.match(r"^(/[^{]*)", endpoint)
    if match:
        return match.group(1).rstrip("/") or "/"
    return "/"


def _find_get_api(base_resource: str, api_store: dict) -> dict | None:
    """
    Find GET API matching base resource.
    Prefer GET without path params (list endpoint).
    """
    candidates = []

    for name, api in api_store.items():
        if api["method"] != "GET":
            continue
        api_base = _base_resource(api["endpoint"])
        if api_base == base_resource:
            candidates.append(api)

    if not candidates:
        return None

    no_params = [c for c in candidates if not c.get("path_params")]
    return no_params[0] if no_params else candidates[0]


def _call_get_api(api: dict) -> dict | None:
    """
    Call GET API and return first item if list, or dict directly.
    """
    result = call_api(
        method="GET",
        endpoint=api["endpoint"],
        path_params=None
    )
    data = result.get("data")

    if isinstance(data, list):
        return data[0] if data else None

    if isinstance(data, dict):
        return data

    return None


def _type_fallback(schema: dict) -> dict:
    """
    Last resort — generate payload from pure type defaults only.
    """
    if not schema or not isinstance(schema, dict):
        return {}

    payload = {}
    for field, field_type in schema.items():
        if isinstance(field_type, dict):
            payload[field] = _type_fallback(field_type)
        elif isinstance(field_type, list):
            payload[field] = []
        else:
            payload[field] = TYPE_DEFAULTS.get(str(field_type), "")
    return payload


def _ask_llm(schema: dict, sample_data: dict) -> dict | None:
    """
    Ask LLM to generate a valid payload using schema + real system data.
    """
    prompt = f"""You are an API test data generator.

Generate a valid JSON payload for a POST/PUT request.

Request schema (field: type):
{json.dumps(schema, indent=2)}

Real data already in the system (use as reference for realistic values):
{json.dumps(sample_data, indent=2)}

Rules:
- Return ONLY a valid JSON object
- No explanation, no markdown, no extra text
- Values must be realistic based on the sample data
- Do not copy the id field
"""
    client = LLMClient()
    raw = client.generate(prompt)

    cleaned = raw.strip()
    if "```" in cleaned:
        cleaned = re.sub(r"```(?:json)?", "", cleaned).replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except Exception:
        print(f"[WARN] LLM payload parse failed: {raw}")
        return None


def generate_payload(action_name: str, api: dict, api_store: dict) -> dict:
    """
    Main entry point.
    1. Find GET API on same base resource
    2. Call it -> get real sample data [0]
    3. Ask LLM to generate payload using schema + sample
    4. Fallback to type defaults if LLM fails
    """
    schema = api.get("request_schema", {})

    if not schema:
        return {}

    base = _base_resource(api["endpoint"])
    get_api = _find_get_api(base, api_store)

    if get_api:
        sample_data = _call_get_api(get_api)
        if sample_data:
            payload = _ask_llm(schema, sample_data)
            if payload:
                return payload
            print(f"[WARN] LLM failed for {action_name}, using type fallback")
        else:
            print(f"[WARN] GET returned no data for {action_name}, using type fallback")
    else:
        print(f"[WARN] No GET API found for {action_name}, using type fallback")

    return _type_fallback(schema)


def merge_payload(base: dict, overrides: dict) -> dict:
    """
    Deep merge TC overrides on top of base payload.
    TC values always win.
    """
    if not overrides:
        return base

    result = base.copy()
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_payload(result[key], value)
        else:
            result[key] = value
    return result