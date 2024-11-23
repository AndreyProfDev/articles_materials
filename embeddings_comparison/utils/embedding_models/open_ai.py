from openai import OpenAI
from enum import Enum

from openai.types.create_embedding_response import CreateEmbeddingResponse

from embeddings_comparison.utils.monitoring.monitoring_service import EmbeddingCreatedEvent, EmbeddingEventRegistry

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
    def __init__(self, api_key: str, model: OPENAI_EMBEDDING_MODEL_NAME, event_registry: EmbeddingEventRegistry | None = None) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.event_registry = event_registry

    def get_dimension(self) -> int:
        return OPENAI_EMBEDDING_LENGTH[self.model]
    
    def _register_event(self, texts: list[str], response: CreateEmbeddingResponse) -> None:
        if self.event_registry:
            
            if len(response.data) != 1:
                raise ValueError(f"""Registering embedding creation event is 
                                 supported only for case when there is one embedding on response
                                 (otherwise usage cannot be splitted between separate embeddings)
                                 
                                 Provided # of texts: {len(texts)}""")
            
            event = EmbeddingCreatedEvent(id=texts[0],
                                            text=texts[0],
                                            embedding=response.data[0].embedding,
                                            cost=response.usage.prompt_tokens,
                                            model_name=self.model.value)
            self.event_registry.register_event(event)

    def embed(self, texts: list[str]) -> list[list[float]]:
        resp = self.client.embeddings.create(
            input=texts,
            model=self.model.value
        )

        self._register_event(texts=texts, response=resp)

        return [d.embedding for d in resp.data]
    
    def get_unique_model_name(self) -> str:
        return self.model.value