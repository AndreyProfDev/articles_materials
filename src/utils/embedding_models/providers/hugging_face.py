from sentence_transformers import SentenceTransformer
from utils.embedding_models.caching import CachedEmbeddingModel
from utils.embedding_models.cost_monitoring import EmbeddingModelWithCostMonitoring
from utils.embedding_models.schema import EmbeddingModelInfo, GenericEmbeddingResponse

class HFEmbeddingModel:
    def __init__(self, model_info: EmbeddingModelInfo) -> None:
        self.model_info = model_info
        self.embedding_model = SentenceTransformer(model_info.model_name)

    def embed(self, texts: list[str]) -> GenericEmbeddingResponse:
        resp = self.embedding_model.encode(texts)
        embeddings = resp.tolist()
        return GenericEmbeddingResponse(promt_tokens=0, embeddings=embeddings)
    
def init_model( model_info: EmbeddingModelInfo) -> EmbeddingModelWithCostMonitoring:
    model = HFEmbeddingModel(model_info=model_info)
    model = CachedEmbeddingModel(model=model)
    model = EmbeddingModelWithCostMonitoring(model=model)
    return model