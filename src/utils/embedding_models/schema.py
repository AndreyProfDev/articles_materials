from typing import Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar('T')

class GenericEmbeddingResponse(BaseModel):
    embeddings: list[list[float]]
    promt_tokens: int
    time_to_generate: float

class EmbeddingModelInfo(BaseModel, frozen=True):
    model_name: str
    dimension: int
    cost_per_mln_tokens: float

    @property
    def sanitized_model_name(self) -> str:
        return self.model_name.replace("/", "_") 

class EmbeddingModel(Protocol):
    def embed(self, texts: list[str]) -> GenericEmbeddingResponse: ...

    @property
    def model_info(self) -> EmbeddingModelInfo: ...

