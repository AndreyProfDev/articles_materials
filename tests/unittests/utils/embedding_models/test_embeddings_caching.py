
import unittest
import tempfile
from pathlib import Path

from embeddings_comparison.utils.embedding_models.caching import CachedEmbeddingModel

class MockedEmbeddingModel:
    def __init__(self, text_to_embeddings: dict[str, list[float]]) -> None:
        self.text_to_embeddings = text_to_embeddings
        self.number_of_calls = 0

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.number_of_calls += 1
        return [self.text_to_embeddings[text] for text in texts]
    
    def get_dimension(self) -> int:
        return 42

class CachedEmbeddingModelTestCase(unittest.TestCase):


    def test_cached_embedding(self):
        underlying_model = MockedEmbeddingModel(text_to_embeddings={"test": [1, 2, 3]})

        result = underlying_model.embed(["test"])
        self.assertEqual(underlying_model.number_of_calls, 1)
        self.assertEqual(result, [[1, 2, 3]])

        result = underlying_model.embed(["test"])
        self.assertEqual(underlying_model.number_of_calls, 2)
        self.assertEqual(result, [[1, 2, 3]])

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_dir_path = Path(tmp_dir)
            model = CachedEmbeddingModel(model=underlying_model, path_to_cache=temp_dir_path)

            result = model.embed(["test"])
            self.assertEqual(underlying_model.number_of_calls, 3)
            self.assertEqual(result, [[1, 2, 3]])

            result = model.embed(["test"])
            self.assertEqual(underlying_model.number_of_calls, 3)
            self.assertEqual(result, [[1, 2, 3]])

    def test_cached_embedding_model_dimension(self):
        underlying_model = MockedEmbeddingModel(text_to_embeddings={"test": [1, 2, 3]})

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_dir_path = Path(tmp_dir)
            model = CachedEmbeddingModel(model=underlying_model, path_to_cache=temp_dir_path)

            self.assertEqual(model.get_dimension(), 42)