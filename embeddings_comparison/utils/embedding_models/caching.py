
from pathlib import Path

from embeddings_comparison.utils.caching import FileBasedTextCache
from embeddings_comparison.utils.embedding_models.schema import EmbeddingModel

def embeddding_to_string(embedding: list[float]) -> str:
    return ",".join(str(x) for x in embedding)

def string_to_embedding(string: str | None) -> list[float] | None:
    if string is None:
        return None
    
    return [float(x) for x in string.split(",")]

class CachedEmbeddingModel:

    def __init__(self, model: EmbeddingModel, path_to_cache: Path = Path("~/.cache/embeddings_cache")) -> None:
        self.cache = FileBasedTextCache(prefix=model.get_unique_model_name(), path_to_cache=path_to_cache)
        self.model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = []

        for text in texts:
            cached = self.cache.retrieve(text)
            embedding = string_to_embedding(cached)

            if embedding is None:
                embedding = self.model.embed([text])[0]
                self.cache.store(text, embeddding_to_string(embedding))

            embeddings.append(embedding)
        return embeddings
    
    def get_dimension(self) -> int:
        return self.model.get_dimension()
    
    def get_unique_model_name(self) -> str:
        return self.model.get_unique_model_name()