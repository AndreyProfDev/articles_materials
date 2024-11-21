
from typing import Literal, Protocol

from pydantic import BaseModel

from typing import TypeVar

T = TypeVar('T')

class ChatMessage(BaseModel, frozen=True):
    role: Literal['system', 'user', 'assystant']
    content: str

class LLMCLient(Protocol[T]):
    def chat(self, messages: list[ChatMessage], _format: type[T]) -> T:
        ...

    def get_unique_model_name(self) -> str:
        ...