import os
from openai import OpenAI
from models.llm_base import LLMClient

class OpenAIClient(LLMClient):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_response(self, prompt: str) -> str:
        messages = [
            {"role": "system", "content": "You are an AI assistant that converts sentences into symbolic logic and identifies logical errors."},
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=200,
            temperature=0.1
        )
        return response.choices[0].message.content
