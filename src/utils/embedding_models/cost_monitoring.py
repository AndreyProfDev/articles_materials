
from utils.embedding_models.schema import EmbeddingModel, GenericEmbeddingResponse


class EmbeddingModelWithCostMonitoring:

    def __init__(self, model: EmbeddingModel) -> None:
        self.model = model
        self.promt_tokens = 0
        self.model_info = self.model.model_info

    def embed(self, texts: list[str]) -> GenericEmbeddingResponse:
        resp = self.model.embed(texts)
        self.promt_tokens += resp.promt_tokens
        return resp
    
    def get_total_cost(self) -> float:
        return self.promt_tokens * self.model.model_info.cost_per_mln_tokens / 1_000_000