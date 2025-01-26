from typing import Protocol, TypeVar

from pydantic import BaseModel
from dataclasses import dataclass
from enum import StrEnum

T = TypeVar("T")

def sanitized_model_name(model_name: str) -> str:
    return model_name.replace("/", "_")

class GenericEmbeddingResponse(BaseModel):
    embeddings: list[list[float]]
    promt_tokens: int
    time_to_generate: float


class MODEL_PROVIDER(StrEnum):
    HUGGING_FACE = "hugging_face"
    OPEN_AI = "open_ai"

@dataclass
class EmbeddingModelInfo:
    provider: MODEL_PROVIDER
    model_name: str
    dimension: int
    cost_per_mln_tokens: float


class EmbeddingModel(Protocol):
    def embed(self, texts: list[str]) -> GenericEmbeddingResponse: ...

    @property
    def model_info(self) -> EmbeddingModelInfo: ...
