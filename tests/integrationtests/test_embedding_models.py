import unittest
import os

from dotenv import load_dotenv

from embeddings_comparison.utils.embedding_models.caching import CachedEmbeddingModel
from embeddings_comparison.utils.embedding_models.hugging_face import HF_EMBEDDING_MODEL_NAME, HFEmbeddingModel
from embeddings_comparison.utils.embedding_models.open_ai import OPENAI_EMBEDDING_MODEL_NAME, OpenAIEmbeddingModel
from embeddings_comparison.utils.monitoring.monitoring_service import EmbeddingEventRegistry
from embeddings_comparison.utils.vectordb.vectordb import VectorIndex

class CalculatingAndStoringEmbeddingsTestCase(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()
    
    def test_populate_database_with_openai_embeddings(self):

        api_key = os.environ.get('OPEN_AI_KEY')
        self.assertIsNotNone(api_key)

        event_registry = EmbeddingEventRegistry()
        embedding_model = OpenAIEmbeddingModel(api_key=str(api_key), model=OPENAI_EMBEDDING_MODEL_NAME.TEXT_EMBEDDING_3_SMALL, event_registry=event_registry)
        cached_model = CachedEmbeddingModel(model=embedding_model)
        vector_db = VectorIndex(embedding_model=cached_model)

        vector_db.insert_text('This is a first test text')
        self.assertEqual(vector_db.size(), 1)

        vector_db.insert_text('This is a second test text')
        self.assertEqual(vector_db.size(), 2)

        found = vector_db.find_text('This is a first test text', top_k=1)
        self.assertEqual(found, ['This is a first test text'])

        found = vector_db.find_text('This is a first text', top_k=1)
        self.assertEqual(found, ['This is a first test text'])

        self.assertEqual(event_registry.get_total_cost(), 17)

    def test_populate_database_with_hugging_face_embeddings(self):

        embedding_model = HFEmbeddingModel(HF_EMBEDDING_MODEL_NAME.ST_POLISH_PARAPHRASE_FROM_DISTILROBERTA)
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
