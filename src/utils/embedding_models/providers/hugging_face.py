from sentence_transformers import SentenceTransformer
from utils.embedding_models.caching import CachedEmbeddingModel
from utils.embedding_models.cost_monitoring import EmbeddingModelWithCostMonitoring
from utils.embedding_models.schema import EmbeddingModelInfo, GenericEmbeddingResponse
import time

class HFEmbeddingModel:
    def __init__(self, model_info: EmbeddingModelInfo) -> None:
        self.model_info = model_info
        self.embedding_model = SentenceTransformer(model_info.model_name)

    def embed(self, texts: list[str]) -> GenericEmbeddingResponse:
        start_time = time.perf_counter()
        resp = self.embedding_model.encode(texts, show_progress_bar = False)
        duration = time.perf_counter() - start_time
        embeddings = resp.tolist()
        return GenericEmbeddingResponse(promt_tokens=0, embeddings=embeddings, time_to_generate=duration)
    
def init_model( model_info: EmbeddingModelInfo) -> EmbeddingModelWithCostMonitoring:
    model = HFEmbeddingModel(model_info=model_info)
    model = CachedEmbeddingModel(model=model)
    model = EmbeddingModelWithCostMonitoring(model=model)
    return model