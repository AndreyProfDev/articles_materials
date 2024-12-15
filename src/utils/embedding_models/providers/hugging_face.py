import time
from typing import Literal

from sentence_transformers import SentenceTransformer

from utils.embedding_models.caching import CachedEmbeddingModel
from utils.embedding_models.monitoring import EmbeddingModelWithMonitoring
from utils.embedding_models.schema import EmbeddingModelInfo, GenericEmbeddingResponse


class HFEmbeddingModel:
    def __init__(
        self,
        model_info: EmbeddingModelInfo,
        device: Literal["cpu", "cuda"] = "cuda",
    ) -> None:
        self.model_info = model_info
        self.embedding_model = SentenceTransformer(model_info.model_name, device=device)

    def embed(self, texts: list[str]) -> GenericEmbeddingResponse:
        start_time = time.perf_counter()
        resp = self.embedding_model.encode(texts, show_progress_bar=False)
        duration = time.perf_counter() - start_time
        embeddings = resp.tolist()
        return GenericEmbeddingResponse(
            promt_tokens=0, embeddings=embeddings, time_to_generate=duration
        )


def init_model(model_info: EmbeddingModelInfo) -> EmbeddingModelWithMonitoring:
    model = HFEmbeddingModel(model_info=model_info)
    model = CachedEmbeddingModel(model=model)
    model = EmbeddingModelWithMonitoring(model=model)
    return model
