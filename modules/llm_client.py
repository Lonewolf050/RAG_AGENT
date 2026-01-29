import ollama
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import settings


class LLMClient:
    def __init__(self):
        self.model = settings.OLLAMA_MODEL
        print(f"[LLM] Using model: {self.model}")
    
    def generate_summary(self, context: str, query: str) -> str:
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {query}

Provide a clear and concise summary."""

        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            return response["response"].strip()
        except Exception as e:
            return f"Error: {str(e)}"


_client = None

def get_llm_client():
    global _client
    if _client is None:
        _client = LLMClient()
    return _client
