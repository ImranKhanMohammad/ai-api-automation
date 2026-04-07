from core.context import Context
from core.resolver import resolve
from client.api_client import call_api


def run_flow(flow, api_store, actions_store):
    context = Context()

    for step in flow["steps"]:
        action_name = step["action"]

        action_def = actions_store[action_name]
        api_name = action_def["steps"][0]["api"]
        api = api_store[api_name]

        input_data = resolve(step.get("input", {}), context.get())

        path_params = {}
        body = {}

        if isinstance(input_data, dict):
            for key, value in input_data.items():
                if key in api["path_params"]:
                    path_params[key] = value
                else:
                    body[key] = value
        else:
            body = input_data

        result = call_api(
            method=api["method"],
            endpoint=api["endpoint"],
            path_params=path_params,
            json=body if body and api["method"] != "GET" else None
        )

        if "save_as" in step:
            context.set(step["save_as"], result.get("data", result))

        print(f"Executed: {action_name}")
        print(f"Result: {result}")

    return context.get()