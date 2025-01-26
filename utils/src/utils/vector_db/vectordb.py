import faiss
import numpy as np  # type: ignore

from utils.embedding_models import tokenizer
from utils.embedding_models.schema import EmbeddingModelInfo


class VectorIndex:
    def __init__(self, model_info: EmbeddingModelInfo) -> None:
        self.index = faiss.IndexFlatL2(model_info.dimension)
        self.tokenizer = tokenizer
        self.indexed_texts: dict[int, str] = {}

    def insert_texts(self, texts: list[str], embeddings: list[list[float]]):
        for text, embedding in zip(texts, embeddings, strict=False):
            self.insert_text(text, embedding)

    def insert_text(self, text: str, embedding: list[float]):
        self.indexed_texts[self.index.ntotal] = text

        arr = np.array(embedding, dtype=np.float32).reshape((1, -1))
        self.index.add(arr)  # type: ignore

    @property
    def size(self) -> int:
        return self.index.ntotal

    def find_text(self, embedding: list[float], top_k: int) -> list[str]:
        arr = np.array(embedding, dtype=np.float32).reshape((1, -1))
        text_indices = self.index.search(arr, k=top_k)[1][0]  # type: ignore
        result = [self.indexed_texts[int(index)] for index in text_indices if index >= 0]
        return result
