from abc import ABC, abstractmethod

class LLMClient(ABC):
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        pass
