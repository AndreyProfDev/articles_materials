from enum import Enum
from openai import OpenAI
from pydantic import BaseModel

from embeddings_comparison.utils.llm_clients.schema import ChatMessage

class OPEN_AI_MODEL_NAME(str, Enum):
    GPT_4O = 'gpt-4o'

class OpenAIClient:
    def __init__(self, api_key:str, model_name:OPEN_AI_MODEL_NAME):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name.value

    def chat(self, messages: list[ChatMessage], _format: type[BaseModel]) -> BaseModel:

        completion = self.client.beta.chat.completions.parse(
                    model=self.model_name,
                    messages=[message.model_dump() for message in messages], # type: ignore
                    response_format=_format
        )

        return completion
