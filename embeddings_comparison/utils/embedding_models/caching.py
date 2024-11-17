
from pathlib import Path
import hashlib

from embeddings_comparison.utils.embedding_models.schema import EmbeddingModel

class CachedEmbeddingModel:

    def __init__(self, model: EmbeddingModel, path_to_cache: Path = Path("~/.cache/embeddings_cache")) -> None:
        self.model = model
        self.path_to_cache = path_to_cache

    def _get_embedding_cache_file_path(self, text: str) -> Path:
        cache_file_name = hashlib.md5(text.encode("utf-8")).hexdigest()
        cache_path = self.path_to_cache / cache_file_name
        return cache_path
    
    def _read_embedding_from_cache(self, text: str) -> list[float] | None:
        cache_path = self._get_embedding_cache_file_path(text)
        if cache_path.exists():
            with open(cache_path, "r") as f:
                return [float(x) for x in f.read().split(",")]
        return None
    
    def _write_embedding_to_cache(self, text: str, embedding: list[float]) -> None:
        cache_path = self._get_embedding_cache_file_path(text)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w") as f:
            f.write(",".join(str(x) for x in embedding))

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = []

        for text in texts:
            embedding = self._read_embedding_from_cache(text)

            if embedding is None:
                embedding = self.model.embed([text])[0]
                self._write_embedding_to_cache(text, embedding)

            embeddings.append(embedding)
        return embeddings
    
    def get_dimension(self) -> int:
        return self.model.get_dimension()