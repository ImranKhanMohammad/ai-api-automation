import json


def build_actions_store(api_store):
    actions_store = {}

    for api_name, api in api_store.items():
        # skip GET APIs
        if api["method"] == "GET":
            continue

        actions_store[api_name] = {
            "steps": [
                {
                    "api": api_name
                }
            ],
            "inputs": {
                "path_params": api.get("path_params", {}),
                "query_params": api.get("query_params", {}),
                "body": api.get("request_schema", {})
            }
        }

    return actions_store


if __name__ == "__main__":
    with open("input/api_store.json") as f:
        api_store = json.load(f)

    actions_store = build_actions_store(api_store)

    with open("input/actions_store.json", "w") as f:
        json.dump(actions_store, f, indent=2)

    print("actions_store.json created")