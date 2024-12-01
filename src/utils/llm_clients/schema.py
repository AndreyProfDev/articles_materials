
from typing import Generic, Literal, Protocol

from pydantic import BaseModel

from typing import TypeVar

T = TypeVar('T')

class LLMModelInfo(BaseModel, frozen=True):
    model_name: str
    completion_cost_per_mln_tokens: float
    promt_cost_per_mln_tokens: float

    @property
    def sanitized_model_name(self) -> str:
        return self.model_name.replace("/", "_")

class ChatMessage(BaseModel, frozen=True):
    role: Literal['system', 'user', 'assystant']
    content: str

class GenericLLMResponse(Generic[T], BaseModel):
    response: T
    promt_tokens: int
    completion_tokens: int

class LLMCLient(Protocol[T]):
    def chat(self, messages: list[ChatMessage], _format: type[T]) -> GenericLLMResponse[T]:
        ...

    @property
    def model_info(self) -> LLMModelInfo:
        ...

