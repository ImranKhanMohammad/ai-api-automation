from api_store.schema_utils import simplify_schema


def build_api_store(swagger):
    api_store = {}
    for path, methods in swagger.get("paths", {}).items():
        for method, details in methods.items():

            action_name = (
                f"{method}_{path.strip('/')}".replace("/", "_")
                .replace("{", "")
                .replace("}", "")
            )
            if not action_name.strip("_"):  # skip if path part is empty
                continue

            request_schema = extract_request(details, swagger)
            response_schema = extract_response(details, swagger)
            path_params = extract_path_params(details)
            query_params = extract_query_params(details)

            api_store[action_name] = {
                "method": method.upper(),
                "endpoint": path,
                "path_params": path_params,
                "query_params": query_params,
                "request_schema": request_schema,
                "response_schema": response_schema,
            }
    return api_store


def extract_request(details, swagger):
    rb = details.get("requestBody", {})
    content = rb.get("content", {})
    schema = content.get("application/json", {}).get("schema", {})
    return simplify_schema(schema, swagger)


def extract_response(details, swagger):
    responses = details.get("responses", {})
    for code in ["200", "201"]:
        if code in responses:
            schema = (
                responses[code]
                .get("content", {})
                .get("application/json", {})
                .get("schema", {})
            )
            return simplify_schema(schema, swagger)
    return {}


def extract_path_params(details):
    params = details.get("parameters", [])
    result = {}

    for p in params:
        if p.get("in") == "path":
            result[p["name"]] = p.get("schema", {}).get("type", "string")

    return result

def extract_query_params(details):
    params = details.get("parameters", [])
    result = {}

    for p in params:
        if p.get("in") == "query":
            result[p["name"]] = p.get("schema", {}).get("type", "string")

    return result