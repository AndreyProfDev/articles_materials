from typing import Generic, TypeVar
from openai import OpenAI
from pydantic import BaseModel

from utils.llm_clients.schema import ChatMessage, GenericLLMResponse, LLMModelInfo

ResponseFormat = TypeVar('ResponseFormat', bound=BaseModel)

class OpenAIClient(Generic[ResponseFormat]):
    def __init__(self, api_key:str, model_info: LLMModelInfo):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.model_info = model_info

    def chat(self, messages: list[ChatMessage], _format: type[ResponseFormat]) -> GenericLLMResponse[ResponseFormat]:

        completion = self.client.beta.chat.completions.parse(
                    model=self.model_info.model_name,
                    messages=[message.model_dump() for message in messages], # type: ignore
                    response_format=_format
        )

        content = completion.choices[0].message.content

        if not content:
            raise ValueError("Empty response from the model")

        if completion.usage is None:
            raise ValueError("Usage information is not available in the response")

        completion_tokens=completion.usage.completion_tokens
        promt_tokens=completion.usage.prompt_tokens
        response = _format.model_validate_json(content)
        return GenericLLMResponse[_format](response=response, promt_tokens=promt_tokens, completion_tokens=completion_tokens)