from openai import OpenAI
from enum import Enum

class OPENAI_EMBEDDING_MODEL_NAME(str, Enum):
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"
    

OPENAI_EMBEDDING_LENGTH: dict[OPENAI_EMBEDDING_MODEL_NAME, int] = {
    OPENAI_EMBEDDING_MODEL_NAME.TEXT_EMBEDDING_3_SMALL: 1536,
    OPENAI_EMBEDDING_MODEL_NAME.TEXT_EMBEDDING_ADA_002: 1536,
    OPENAI_EMBEDDING_MODEL_NAME.TEXT_EMBEDDING_3_LARGE: 3072,
}
class OpenAIEmbeddingModel:
    def __init__(self, api_key: str, model: OPENAI_EMBEDDING_MODEL_NAME) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def get_dimension(self) -> int:
        return OPENAI_EMBEDDING_LENGTH[self.model]

    def embed(self, texts: list[str]) -> list[list[float]]:
        resp = self.client.embeddings.create(
            input=texts,
            model=self.model.value
        )

        return [d.embedding for d in resp.data]
    
    def get_unique_model_name(self) -> str:
        return self.model.value