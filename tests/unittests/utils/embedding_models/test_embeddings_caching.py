import shutil
import tempfile
import unittest
from pathlib import Path

from utils.embedding_models.caching import CachedEmbeddingModel
from utils.embedding_models.schema import EmbeddingModelInfo, GenericEmbeddingResponse


class MockedEmbeddingModel:
    def __init__(
        self, text_to_embeddings: dict[str, list[float]], unique_model_name: str
    ) -> None:
        self.text_to_embeddings = text_to_embeddings
        self.number_of_calls = 0
        self.unique_model_name = unique_model_name
        self.model_info = EmbeddingModelInfo(
            model_name=unique_model_name, dimension=42, cost_per_mln_tokens=0.1
        )

    def embed(self, texts: list[str]) -> GenericEmbeddingResponse:
        self.number_of_calls += 1
        embeddings = [self.text_to_embeddings[text] for text in texts]
        return GenericEmbeddingResponse(
            embeddings=embeddings, promt_tokens=0, time_to_generate=0
        )


class CachedEmbeddingModelTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.temp_dir_path = Path(self.temp_dir)
        self.underlying_model = MockedEmbeddingModel(
            text_to_embeddings={"test": [1, 2, 3]}, unique_model_name="test_model1"
        )
        self.cached_model = CachedEmbeddingModel(
            model=self.underlying_model, path_to_cache=self.temp_dir_path
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_cached_embedding(self):

        result = self.underlying_model.embed(["test"])
        self.assertEqual(self.underlying_model.number_of_calls, 1)
        self.assertEqual(result.embeddings, [[1, 2, 3]])

        result = self.underlying_model.embed(["test"])
        self.assertEqual(self.underlying_model.number_of_calls, 2)
        self.assertEqual(result.embeddings, [[1, 2, 3]])

        result = self.cached_model.embed(["test"])
        self.assertEqual(self.underlying_model.number_of_calls, 3)
        self.assertEqual(result.embeddings, [[1, 2, 3]])

        result = self.cached_model.embed(["test"])
        self.assertEqual(self.underlying_model.number_of_calls, 3)
        self.assertEqual(result.embeddings, [[1, 2, 3]])

    def test_cached_embedding_model_dimension(self):
        self.assertEqual(self.cached_model.model_info.dimension, 42)

    def test_caching_of_different_models(self):
        underlying_model_2 = MockedEmbeddingModel(
            text_to_embeddings={"test": [4, 5, 6]}, unique_model_name="test_model_4"
        )

        model_2 = CachedEmbeddingModel(
            model=underlying_model_2, path_to_cache=self.temp_dir_path
        )

        result = self.cached_model.embed(["test"])
        self.assertEqual(self.underlying_model.number_of_calls, 1)
        self.assertEqual(result.embeddings, [[1, 2, 3]])

        result = model_2.embed(["test"])
        self.assertEqual(underlying_model_2.number_of_calls, 1)
        self.assertEqual(result.embeddings, [[4, 5, 6]])

        result = self.cached_model.embed(["test"])
        self.assertEqual(self.underlying_model.number_of_calls, 1)
        self.assertEqual(result.embeddings, [[1, 2, 3]])

        result = model_2.embed(["test"])
        self.assertEqual(underlying_model_2.number_of_calls, 1)
        self.assertEqual(result.embeddings, [[4, 5, 6]])
