from core.context import Context
from core.payload_generator import generate_payload, merge_payload
from client.api_client import call_api
from ai.llm_agent import LLMAgent


def run_flow(flow, api_store, actions_store):
    context = Context()
    agent = LLMAgent()

    for step in flow["steps"]:
        action_name = step["action"]

        action_def = actions_store[action_name]
        api_name = action_def["steps"][0]["api"]
        api = api_store[api_name]

        # Resolve path params — LLM picks correct values from context
        path_params = {}
        if api.get("path_params"):
            path_params = agent.resolve_path_params(
                api["path_params"],
                context.get() or {}
            )
            print(f"[PATH PARAMS] {path_params}")

        # TC overrides for body — from step definition
        body_overrides = step.get("input", {})

        # Generate payload: GET real data -> LLM -> fallback to type defaults
        base_payload = generate_payload(action_name, api, api_store)
        body = merge_payload(base_payload, body_overrides)

        result = call_api(
            method=api["method"],
            endpoint=api["endpoint"],
            path_params=path_params,
            json=body if body and api["method"] != "GET" else None
        )

        # Auto-save every response to context under action name
        response_data = result.get("data", result)
        context.set(action_name, response_data)
        print(f"[CONTEXT] saved '{action_name}'")

        print(f"Executed: {action_name}")
        print(f"Result: {result}")

    return context.get()