
from pathlib import Path

from utils.caching import FileBasedTextCache
from utils.embedding_models.schema import EmbeddingModel, EmbeddingModelInfo, GenericEmbeddingResponse

class CachedEmbeddingModel:

    def __init__(self, model: EmbeddingModel, path_to_cache: Path = Path("~/.cache/embeddings_cache").expanduser()) -> None:
        model_name = model.model_info.sanitized_model_name
        self.cache = FileBasedTextCache(prefix=model_name, path_to_cache=path_to_cache)
        self.model = model

    def embed(self, texts: list[str]) -> GenericEmbeddingResponse:
    
        embeddings = []
        total_promt_tokes = 0
        time_to_generate = 0

        for text in texts:
            cached = self.cache.retrieve(text)
            
            if cached is not None:
                embedding = GenericEmbeddingResponse.model_validate_json(cached)
            else:
                embedding = self.model.embed([text])
                self.cache.store(text, embedding.model_dump_json())

            embeddings.append(embedding.embeddings[0])
            total_promt_tokes += embedding.promt_tokens
            time_to_generate += embedding.time_to_generate
        return GenericEmbeddingResponse(embeddings=embeddings, promt_tokens=total_promt_tokes, time_to_generate=time_to_generate)
    
    @property
    def model_info(self) -> EmbeddingModelInfo:
        return self.model.model_info