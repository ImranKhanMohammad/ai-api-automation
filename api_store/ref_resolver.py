def resolve_ref(ref: str, swagger: dict):
    parts = ref.lstrip("#/").split("/")
    result = swagger
    for part in parts:
        result = result.get(part, {})
    return result