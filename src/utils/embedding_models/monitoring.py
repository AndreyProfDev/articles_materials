from utils.embedding_models.schema import EmbeddingModel, GenericEmbeddingResponse


class EmbeddingModelWithMonitoring:

    def __init__(self, model: EmbeddingModel) -> None:
        self.model = model
        self.promt_tokens = 0
        self.time_to_generate = 0
        self.model_info = self.model.model_info

    def embed(self, texts: list[str]) -> GenericEmbeddingResponse:
        resp = self.model.embed(texts)
        self.promt_tokens += resp.promt_tokens
        self.time_to_generate += resp.time_to_generate
        return resp

    def get_total_cost(self) -> float:
        return self.promt_tokens * self.model.model_info.cost_per_mln_tokens / 1_000_000

    def get_total_time(self) -> float:
        return self.time_to_generate
