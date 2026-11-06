import json
from ai.llm_client import LLMClient


class LLMAgent:

    def __init__(self):
        self.llm_client = LLMClient()

    def decide_actions(self, user_intent: str, available_actions: list) -> list:
        actions_list = "\n".join(f"- {a}" for a in available_actions)

        prompt = f"""
You are an automation agent.

Return ONLY a valid JSON array of action names.
No explanation. No text. No markdown.

User intent:
{user_intent}

Available actions:
{actions_list}

Rules:
- post_ creates a new record. put_ updates an existing one.
- If the intent says create, add, or new, include the post_ action. Do not use put_ to create.
- Include later actions the intent also asks for, such as terminate.

Example output:
["post_employees", "put_employees_emp_id_terminate"]
"""

        raw = self.llm_client.generate(prompt)
        cleaned = self._clean_output(raw)

        try:
            parsed = json.loads(cleaned)
        except Exception:
            print("[ERROR] Failed to parse actions:", raw)
            return []

        if isinstance(parsed, list):
            return [a for a in parsed if isinstance(a, str)]

        if isinstance(parsed, dict):
            for value in parsed.values():
                if isinstance(value, list):
                    return [a for a in value if isinstance(a, str)]

        print("[ERROR] Actions were not a list:", raw)
        return []

    def resolve_path_params(self, path_params: dict, context: dict) -> dict:
        """
        Given path params needed and available context from previous steps,
        ask LLM to resolve the values.
        """
        if not path_params or not context:
            return {}

        prompt = f"""
You are resolving path parameters for an API call.

Path parameters needed (name: type):
{json.dumps(path_params, indent=2)}

Available context from previous API responses:
{json.dumps(context, indent=2)}

Rules:
- Return ONLY a valid JSON object with resolved values
- Match each path param to the correct value from context
- No explanation, no markdown, no extra text

Example output:
{{"emp_id": 3}}
"""

        raw = self.llm_client.generate(prompt)
        cleaned = self._clean_output(raw)

        try:
            return json.loads(cleaned)
        except Exception:
            print("[ERROR] Failed to resolve path params:", raw)
            return {}

    def _clean_output(self, text: str) -> str:
        if not text:
            return ""

        if "```" in text:
            text = text.replace("```json", "").replace("```", "")

        return text.strip()