
import shutil
import unittest
import tempfile
from pathlib import Path

from embeddings_comparison.utils.embedding_models.caching import CachedEmbeddingModel
from tests.mocked_objects import MockedEmbeddingModel

class CachedEmbeddingModelTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.temp_dir_path = Path(self.temp_dir)
        self.underlying_model = MockedEmbeddingModel(text_to_embeddings={"test": [1, 2, 3]}, unique_model_name="test_model1")
        self.cached_model = CachedEmbeddingModel(model=self.underlying_model, path_to_cache=self.temp_dir_path)
    
    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_cached_embedding(self):
        
        result = self.underlying_model.embed(["test"])
        self.assertEqual(self.underlying_model.number_of_calls, 1)
        self.assertEqual(result, [[1, 2, 3]])

        result = self.underlying_model.embed(["test"])
        self.assertEqual(self.underlying_model.number_of_calls, 2)
        self.assertEqual(result, [[1, 2, 3]])

        result = self.cached_model.embed(["test"])
        self.assertEqual(self.underlying_model.number_of_calls, 3)
        self.assertEqual(result, [[1, 2, 3]])

        result = self.cached_model.embed(["test"])
        self.assertEqual(self.underlying_model.number_of_calls, 3)
        self.assertEqual(result, [[1, 2, 3]])

    def test_cached_embedding_model_dimension(self):
        self.assertEqual(self.cached_model.get_dimension(), 42)

    def test_caching_of_different_models(self):
        underlying_model_2 = MockedEmbeddingModel(text_to_embeddings={"test": [4, 5, 6]}, unique_model_name="test_model_4")

        model_2 = CachedEmbeddingModel(model=underlying_model_2, path_to_cache=self.temp_dir_path)

        result = self.cached_model.embed(["test"])
        self.assertEqual(self.underlying_model.number_of_calls, 1)
        self.assertEqual(result, [[1, 2, 3]])

        result = model_2.embed(["test"])
        self.assertEqual(underlying_model_2.number_of_calls, 1)
        self.assertEqual(result, [[4, 5, 6]])

        result = self.cached_model.embed(["test"])
        self.assertEqual(self.underlying_model.number_of_calls, 1)
        self.assertEqual(result, [[1, 2, 3]])

        result = model_2.embed(["test"])
        self.assertEqual(underlying_model_2.number_of_calls, 1)
        self.assertEqual(result, [[4, 5, 6]])