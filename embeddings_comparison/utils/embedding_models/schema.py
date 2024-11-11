from typing import Protocol

class EmbeddingModel(Protocol):
    def embed(self, embeddings: list[str]) -> list[list[float]]: ...