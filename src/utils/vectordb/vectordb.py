import faiss  # type: ignore
import numpy as np

from utils.embedding_models import tokenizer
from utils.embedding_models.schema import EmbeddingModel


class VectorIndex:

    def __init__(self, embedding_model: EmbeddingModel) -> None:
        self.index = faiss.IndexFlatL2(embedding_model.model_info.dimension)
        self.tokenizer = tokenizer
        self.embedding_model = embedding_model
        self.indexed_texts: dict[int, str] = {}

    def embed_text(self, text: str) -> np.ndarray:
        embedding = self.embedding_model.embed([text])
        embedding_vector = np.array(embedding.embeddings[0]).reshape(1, -1)
        return embedding_vector

    def insert_texts(self, texts: list[str]):
        for text in texts:
            self.insert_text(text)

    def insert_text(self, text: str):
        self.indexed_texts[self.index.ntotal] = text
        self.index.add(self.embed_text(text))  # type: ignore

    def size(self) -> int:
        return self.index.ntotal

    def find_text(self, text: str, top_k: int) -> list[str]:
        text_indices = self.index.search(self.embed_text(text), k=top_k)[1][0]  # type: ignore
        result = [
            self.indexed_texts[int(index)] for index in text_indices if index >= 0
        ]
        return result


class VectorDB:

    def __init__(self) -> None:
        self.indices: dict[str, VectorIndex] = {}

    def add_index(self, index_name: str, embedding_model: EmbeddingModel):
        self.indices[index_name] = VectorIndex(embedding_model)

    def list_indices(self) -> list[str]:
        return list(self.indices.keys())

    def insert_text(self, text: str, index_name: str):
        self.indices[index_name].insert_text(text)

    def insert_texts(self, texts: list[str], index_name: str):
        self.indices[index_name].insert_texts(texts)

    def find_text(self, text: str, top_k: int, index_name: str) -> list[str]:
        return self.indices[index_name].find_text(text, top_k)
