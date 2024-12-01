
from pydantic import BaseModel

from utils.llm_clients.schema import ChatMessage, GenericLLMResponse, LLMCLient

from typing import TypeVar, Generic

ResponseFormat = TypeVar('ResponseFormat', bound=BaseModel)

class LLMClientWithCostMonitoring(Generic[ResponseFormat]):

    def __init__(self, client: LLMCLient[ResponseFormat]) -> None:
        self.client = client
        self.completion_tokens = 0
        self.promt_tokens = 0
        self.model_info = self.client.model_info

    def chat(self, messages: list[ChatMessage], _format: type[ResponseFormat]) -> GenericLLMResponse[ResponseFormat]:
        response = self.client.chat(messages, _format)
        self.completion_tokens += response.completion_tokens
        self.promt_tokens += response.promt_tokens

        return response
    
    def get_total_promt_cost(self) -> float:
        return self.promt_tokens * self.client.model_info.promt_cost_per_mln_tokens / 1_000_000
    
    def get_total_completion_cost(self) -> float:
        return self.completion_tokens * self.client.model_info.completion_cost_per_mln_tokens / 1_000_000