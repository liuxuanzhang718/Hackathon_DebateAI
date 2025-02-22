import os
from dotenv import load_dotenv

from models.openai_llm import OpenAIClient
from models.deepseek_llm import DeepSeekClient
# from models.claude_llm import ClaudeClient
# from models.gemini_llm import GeminiClient

load_dotenv()

def get_llm_client(model_name: str):
    if model_name == "openai":
        return OpenAIClient()
    elif model_name == "deepseek":
        return DeepSeekClient()
    # elif model_name == "claude":
    #     return ClaudeClient()
    # elif model_name == "gemini":
    #     return GeminiClient()
    else:
        raise ValueError(f"Unknown model: {model_name}")

