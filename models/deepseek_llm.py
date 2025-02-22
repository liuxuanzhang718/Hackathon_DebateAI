import os
from openai import OpenAI
from models.llm_base import LLMClient

class DeepSeekClient(LLMClient):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

    def get_response(self, prompt: str) -> str:
        messages = [
            {"role": "system", "content": "You are an AI assistant that converts sentences into symbolic logic and identifies logical errors."},
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
            max_tokens=200,
            temperature=0.1 # lower temperature for more consistent response
        )
        return response.choices[0].message.content
