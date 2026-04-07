import requests
from config import OLLAMA_URL, OLLAMA_MODEL


class LLMClient:

    def __init__(self):
        self.base_url = OLLAMA_URL
        self.model = OLLAMA_MODEL

    def generate(self, prompt: str) -> str:
        """
        Public method used by the system.
        """
        return self._call_llm(prompt)

    def _call_llm(self, prompt: str) -> str:
        """
        Internal method to call Ollama API.
        """
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response", "")