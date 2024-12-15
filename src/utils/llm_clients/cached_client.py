from pathlib import Path
from typing import Generic, TypeVar

from pydantic import BaseModel

from utils.caching import FileBasedTextCache
from utils.llm_clients.schema import (
    ChatMessage,
    GenericLLMResponse,
    LLMCLient,
    LLMModelInfo,
)

ResponseFormat = TypeVar("ResponseFormat", bound=BaseModel)


class CachedLLMClient(Generic[ResponseFormat]):

    def __init__(
        self,
        client: LLMCLient[ResponseFormat],
        path_to_cache: Path = Path("~/.cache/completion_cache").expanduser(),
    ) -> None:
        self.client = client
        model_name = client.model_info.sanitized_model_name
        self.cache = FileBasedTextCache(prefix=model_name, path_to_cache=path_to_cache)

    def chat_messages_to_string(self, messages: list[ChatMessage]) -> str:
        return "\n".join([message.model_dump_json() for message in messages])

    def response_from_string(self, string: str) -> list[ChatMessage]:
        return [
            ChatMessage.model_validate_json(message) for message in string.split("\n")
        ]

    def chat(
        self, messages: list[ChatMessage], _format: type[ResponseFormat]
    ) -> GenericLLMResponse[ResponseFormat]:

        promt = self.chat_messages_to_string(messages)

        if self.cache.exists(promt):
            retrieved = str(self.cache.retrieve(promt))
            response = GenericLLMResponse[_format].model_validate_json(retrieved)
            response.response = _format.model_validate(response.response)
            return response

        self.cache.exists(promt)
        response = self.client.chat(messages, _format)
        self.cache.exists(promt)

        self.cache.store(promt, response.model_dump_json())

        return response

    @property
    def model_info(self) -> LLMModelInfo:
        return self.client.model_info
