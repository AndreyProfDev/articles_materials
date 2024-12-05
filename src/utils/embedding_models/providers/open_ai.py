from openai import OpenAI
from utils.embedding_models.caching import CachedEmbeddingModel
from utils.embedding_models.cost_monitoring import EmbeddingModelWithCostMonitoring
from utils.embedding_models.schema import EmbeddingModelInfo, GenericEmbeddingResponse
import time

class OpenAIEmbeddingModel:
    def __init__(self, api_key: str, model_info: EmbeddingModelInfo) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model_info = model_info

    def embed(self, texts: list[str]) -> GenericEmbeddingResponse:
        start_time = time.perf_counter()
        resp = self.client.embeddings.create(
            input=texts,
            model=self.model_info.model_name,
        )
        duration = time.perf_counter() - start_time

        promt_tokens = resp.usage.prompt_tokens
        embeddings = [d.embedding for d in resp.data]

        return GenericEmbeddingResponse(embeddings=embeddings, promt_tokens=promt_tokens, time_to_generate=duration)
    
def init_model(api_key: str, model_info: EmbeddingModelInfo) -> EmbeddingModelWithCostMonitoring:
    model = OpenAIEmbeddingModel(api_key=api_key, model_info=model_info)
    model = CachedEmbeddingModel(model=model)
    model = EmbeddingModelWithCostMonitoring(model=model)
    return model