from api_store.ref_resolver import resolve_ref

def simplify_schema(schema, swagger):
    if not schema:
        return {}

    if "$ref" in schema:
        resolved = resolve_ref(schema["$ref"], swagger)
        return simplify_schema(resolved, swagger)

    if "allOf" in schema:
        merged = {}
        for sub in schema["allOf"]:
            merged.update(simplify_schema(sub, swagger))
        return merged

    if schema.get("type") == "object":
        return {
            k: simplify_schema(v, swagger)
            for k, v in schema.get("properties", {}).items()
        }

    if schema.get("type") == "array":
        return [simplify_schema(schema.get("items", {}), swagger)]

    return schema.get("type", "string")