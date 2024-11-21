from enum import Enum
from sentence_transformers import SentenceTransformer

class HF_EMBEDDING_MODEL_NAME(Enum):
    ST_POLISH_PARAPHRASE_FROM_DISTILROBERTA = "sdadas/st-polish-paraphrase-from-distilroberta"

HF_EMBEDDING_LENGTH: dict[HF_EMBEDDING_MODEL_NAME, int] = {
    HF_EMBEDDING_MODEL_NAME.ST_POLISH_PARAPHRASE_FROM_DISTILROBERTA: 768,
}

class HFEmbeddingModel:
    def __init__(self, model_name: HF_EMBEDDING_MODEL_NAME) -> None:
        self.embedding_model_name = model_name
        self.embedding_model = SentenceTransformer(model_name.value)

    def embed(self, texts: list[str]) -> list[list[float]]:
        resp = self.embedding_model.encode(texts)

        return resp.tolist()
    
    def get_dimension(self) -> int:
        return HF_EMBEDDING_LENGTH[self.embedding_model_name]
    
    def get_unique_model_name(self) -> str:
        return self.embedding_model_name.value.replace("/", "_")