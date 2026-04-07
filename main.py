import json
import os

from api_store.swagger_loader import load_swagger
from api_store.api_store_builder import build_api_store
from api_store.actions_store_builder import build_actions_store
from api_store.get_api_response_store_builder import build_get_api_response_store
from core.executor import run_flow
from ai.llm_agent import LLMAgent
from config import SWAGGER_URL


def load_nl():
    with open("input/nl.txt") as f:
        return f.read().strip()


if __name__ == "__main__":

    # STEP 1: Load swagger + build stores
    swagger = load_swagger(SWAGGER_URL)
    api_store = build_api_store(swagger)

    os.makedirs("input", exist_ok=True)

    with open("input/swagger.json", "w") as f:
        json.dump(swagger, f, indent=2)

    with open("input/api_store.json", "w") as f:
        json.dump(api_store, f, indent=2)

    actions_store = build_actions_store(api_store)

    with open("input/actions_store.json", "w") as f:
        json.dump(actions_store, f, indent=2)

    get_api_response_store = build_get_api_response_store(api_store)

    with open("input/get_api_response_store.json", "w") as f:
        json.dump(get_api_response_store, f, indent=2)

    # STEP 2: Read NL
    nl = load_nl()
    print("\n[INTENT]")
    print(nl)

    # STEP 3: Decide actions using LLM
    llm_agent = LLMAgent()
    available_actions = list(actions_store.keys())
    actions = llm_agent.decide_actions(nl, available_actions)

    print("\n[ACTIONS]")
    print(actions)

    # STEP 4: Build flow
    flow = {
        "steps": [{"action": a} for a in actions]
    }

    # STEP 5: Execute flow
    result = run_flow(flow, api_store, actions_store)

    print("\n[RESULT]")
    print(result)