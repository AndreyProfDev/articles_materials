
from pathlib import Path

from pydantic import BaseModel

from embeddings_comparison.utils.caching import FileBasedTextCache
from embeddings_comparison.utils.llm_clients.schema import ChatMessage, LLMCLient

from typing import TypeVar, Generic

ResponseFormat = TypeVar('ResponseFormat', bound=BaseModel)

class CachedLLMClient(Generic[ResponseFormat]):

    def __init__(self, client: LLMCLient[ResponseFormat], path_to_cache: Path) -> None:
        self.client = client
        self.cache = FileBasedTextCache(prefix=client.get_unique_model_name(), path_to_cache=path_to_cache)

    def chat_messages_to_string(self, messages: list[ChatMessage]) -> str:
        return "\n".join([message.model_dump_json() for message in messages])
    
    def response_from_string(self, string: str) -> list[ChatMessage]:
        return [ChatMessage.model_validate_json(message) for message in string.split("\n")]

    def chat(self, messages: list[ChatMessage], _format: type[ResponseFormat]) -> ResponseFormat:

        promt = self.chat_messages_to_string(messages)

        if self.cache.exists(promt):
            return _format.model_validate_json(str(self.cache.retrieve(promt)))
        
        response = self.client.chat(messages, _format)

        self.cache.store(promt, response.model_dump_json())

        return response