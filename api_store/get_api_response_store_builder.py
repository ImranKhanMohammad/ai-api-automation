import json
import os
from pathlib import Path

from client.api_client import call_api
from datamodel_code_generator import InputFileType, generate


def call_get_api(endpoint, path_params=None):
    response = call_api(
        method="GET",
        endpoint=endpoint,
        path_params=path_params
    )
    return response.get("data")


def has_unresolved_path_params(path_params: dict) -> bool:
    type_hints = {"integer", "string", "number", "boolean"}
    return any(str(v) in type_hints for v in path_params.values())


def build_get_api_response_store(api_store: dict) -> dict:
    os.makedirs("models", exist_ok=True)
    store = {}

    for name, api in api_store.items():
        if api["method"] != "GET":
            continue

        path_params = api.get("path_params", {})

        if has_unresolved_path_params(path_params):
            print(f"[SKIP] {name} — path params need real values: {path_params}")
            continue

        print(f"[PROCESSING] {name}")

        data = call_get_api(api["endpoint"], path_params or None)

        if data is None:
            print(f"[SKIP] No data returned for {name}")
            continue

        if isinstance(data, dict) and "detail" in data:
            print(f"[SKIP] Error response for {name}")
            continue

        if isinstance(data, list):
            data = data[0] if data else None
            if data is None:
                print(f"[SKIP] Empty list for {name}")
                continue

        # write full JSON response (no sampling)
        json_path = Path(f"models/{name}.json")
        model_path = Path(f"models/{name}.py")

        json_path.write_text(json.dumps(data, indent=2))

        # generate directly from JSON
        try:
            generate(
                input_=json_path,
                input_file_type=InputFileType.Json,
                output=model_path,
            )

            json_path.unlink()
        except Exception as e:
            print(f"[ERROR] Model generation failed for {name}: {e}")
            json_path.unlink()
            continue

        print(f"[SAVED] {model_path}")

        store[name] = {
            "endpoint": api["endpoint"],
            "model_file": str(model_path)
        }

    return store


if __name__ == "__main__":
    with open("input/api_store.json") as f:
        api_store = json.load(f)

    store = build_get_api_response_store(api_store)

    with open("input/get_api_response_store.json", "w") as f:
        json.dump(store, f, indent=2)

    print("[DONE]")