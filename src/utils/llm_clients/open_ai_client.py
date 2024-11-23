from enum import Enum
from typing import Generic, TypeVar
from openai import OpenAI
from pydantic import BaseModel

from src.utils.llm_clients.schema import ChatMessage

class OPEN_AI_MODEL_NAME(str, Enum):
    GPT_4O = 'gpt-4o'

ResponseFormat = TypeVar('ResponseFormat', bound=BaseModel)

class OpenAIClient(Generic[ResponseFormat]):
    def __init__(self, api_key:str, model_name:OPEN_AI_MODEL_NAME):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name.value

    def chat(self, messages: list[ChatMessage], _format: type[ResponseFormat]) -> ResponseFormat:

        completion = self.client.beta.chat.completions.parse(
                    model=self.model_name,
                    messages=[message.model_dump() for message in messages], # type: ignore
                    response_format=_format
        )

        content = completion.choices[0].message.content

        if not content:
            raise ValueError("Empty response from the model")

        return _format.model_validate_json(content)
    
    def get_unique_model_name(self) -> str:
        return self.model_name
