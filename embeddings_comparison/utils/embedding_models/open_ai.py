from openai import OpenAI
from enum import Enum

class OPEN_AI_EMBEDDING_MODEL(Enum):
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_MEDIUM = "text-embedding-3-medium"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"


class OpenAIEmbeddingModel:
    def __init__(self, api_key: str, model: OPEN_AI_EMBEDDING_MODEL) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        resp = self.client.embeddings.create(
            input=texts,
            model=self.model.value
        )

        return [d.embedding for d in resp.data]