from enum import Enum
from sentence_transformers import SentenceTransformer

class HUGGING_FACE_EMBEDDING_MODEL(Enum):
    ST_POLISH_PARAPHRASE_FROM_DISTILROBERTA = "sdadas/st-polish-paraphrase-from-distilroberta"

class HuggingFaceEmbeddingModel:
    def __init__(self, embedding_model_name: HUGGING_FACE_EMBEDDING_MODEL) -> None:
        self.embedding_model = SentenceTransformer(embedding_model_name.value)

    def embed(self, texts_to_embed: list[str]) -> list[list[float]]:
        resp = self.embedding_model.encode(texts_to_embed)

        return resp