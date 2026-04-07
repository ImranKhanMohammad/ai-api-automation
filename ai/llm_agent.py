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

Example output:
["post_employees", "get_employees"]
"""

        raw = self.llm_client.generate(prompt)
        cleaned = self._clean_output(raw)

        try:
            return json.loads(cleaned)
        except Exception:
            print("[ERROR] Failed to parse actions:", raw)
            return []

    def _clean_output(self, text: str) -> str:
        if not text:
            return ""

        if "```" in text:
            text = text.replace("```json", "").replace("```", "")

        return text.strip()