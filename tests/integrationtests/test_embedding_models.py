import unittest
import os

from dotenv import load_dotenv
from utils.embedding_models.cost_monitoring import EmbeddingModelWithCostMonitoring

from utils.embedding_models.caching import CachedEmbeddingModel
from utils.embedding_models.providers.hugging_face import HFEmbeddingModel
from utils.embedding_models.providers.open_ai import OpenAIEmbeddingModel
from utils.vectordb.vectordb import VectorIndex
from utils.embedding_models.providers import supported_models

class CalculatingAndStoringEmbeddingsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
    
    @unittest.skip("Integration test for OpenAI Embeddings API")
    def test_populate_database_with_openai_embeddings(self):

        api_key = os.environ.get('OPEN_AI_KEY')
        self.assertIsNotNone(api_key)

        embedding_model = OpenAIEmbeddingModel(api_key=str(api_key), model_info=supported_models.TEXT_EMBEDDING_3_SMALL)
        embedding_model = CachedEmbeddingModel(model=embedding_model)
        embedding_model = EmbeddingModelWithCostMonitoring(model=embedding_model)
        vector_db = VectorIndex(embedding_model=embedding_model)

        vector_db.insert_text('This is a first test text')
        self.assertEqual(vector_db.size(), 1)

        vector_db.insert_text('This is a second test text')
        self.assertEqual(vector_db.size(), 2)

        found = vector_db.find_text('This is a first test text', top_k=1)
        self.assertEqual(found, ['This is a first test text'])

        found = vector_db.find_text('This is a first text', top_k=1)
        self.assertEqual(found, ['This is a first test text'])

        self.assertTrue(embedding_model.promt_tokens > 0)

    @unittest.skip("Integration test for Hugging Face Embeddings API")
    def test_populate_database_with_hugging_face_embeddings(self):

        embedding_model = HFEmbeddingModel(supported_models.ST_POLISH_PARAPHRASE_FROM_DISTILROBERTA)
        cached_model = CachedEmbeddingModel(model=embedding_model)
        vector_db = VectorIndex(embedding_model=cached_model)

        vector_db.insert_text('To jest pierwszy tekst testowy')
        self.assertEqual(vector_db.size(), 1)

        vector_db.insert_text('To jest drugi tekst testowy')
        self.assertEqual(vector_db.size(), 2)

        found = vector_db.find_text('To jest pierwszy tekst testowy', top_k=1)
        self.assertEqual(found, ['To jest pierwszy tekst testowy'])

        found = vector_db.find_text('To jest pierwszy tekst', top_k=1)
        self.assertEqual(found, ['To jest pierwszy tekst testowy'])
