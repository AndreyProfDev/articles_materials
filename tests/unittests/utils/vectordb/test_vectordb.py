import unittest

from utils.embedding_models.schema import EmbeddingModelInfo, GenericEmbeddingResponse

from utils.vectordb.vectordb import VectorDB, VectorIndex

class MockedEmbeddingModel:
    def __init__(self, text_to_embedding: dict[str, list[float]], dimension: int) -> None:
        self.text_to_embedding = text_to_embedding
        self.dimension = dimension
        self.model_info = EmbeddingModelInfo(model_name="test_model", dimension=dimension, cost_per_mln_tokens=0.1)

    def embed(self, texts: list[str]) -> GenericEmbeddingResponse:

        embeddings = [self.text_to_embedding[text] for text in texts if text in self.text_to_embedding]
        return GenericEmbeddingResponse(embeddings=embeddings, promt_tokens=0, time_to_generate=0)


class VectorDBTestCase(unittest.TestCase):
    def setUp(self):
        embedding_model = MockedEmbeddingModel(
            text_to_embedding = {
                'Test text 1': [1.0, 2.0, 3.0],
                'Test text 2': [4.0, 5.0, 6.0],
                'Test text 3': [1.0, 2.0, 4.0],
            },
            dimension = 3
        )
        self.db = VectorIndex(embedding_model=embedding_model)

    def test_insert(self):
        self.db.insert_text('Test text 1')
        self.assertEqual(self.db.size(), 1)

        self.db.insert_text('Test text 2')
        self.assertEqual(self.db.size(), 2)
        
    def test_find_text(self):
        text = 'Test text 1'
        text2 = 'Test text 2'
        self.db.insert_text(text)
        self.db.insert_text(text2)
        
        self.assertEqual(self.db.find_text('Test text 3', top_k = 1), [text])
        self.assertEqual(self.db.find_text('Test text 3', top_k = 2), [text, text2])
        self.assertEqual(self.db.find_text('Test text 3', top_k = 3), [text, text2])

    def test_initalize_vector_db(self):

        vector_db = VectorDB()
        vector_db.add_index('test_index', self.db.embedding_model)
        vector_db.insert_texts(['Test text 1', 'Test text 2'], 'test_index')
        self.assertEqual(vector_db.find_text('Test text 3', top_k = 1, index_name = 'test_index'), ['Test text 1'])

    def test_initalize_vector_db_with_many_indices(self):

        vector_db = VectorDB()
        vector_db.add_index('test_index', self.db.embedding_model)
        vector_db.insert_texts(['Test text 1', 'Test text 2'], 'test_index')

        other_embedding_model = MockedEmbeddingModel(
            text_to_embedding = {
                'Test text 3': [1.0, 2.0, 4.0],
            },
            dimension = 3
        )
        vector_db.add_index('test_index2', other_embedding_model)
        vector_db.insert_texts(['Test text 3'], 'test_index2')
        self.assertNotEqual(vector_db.find_text('Test text 3', top_k = 1, index_name = 'test_index'), ['Test text 3'])
        self.assertEqual(vector_db.find_text('Test text 3', top_k = 1, index_name = 'test_index2'), ['Test text 3'])

    def test_vector_db_list_indices(self):
        vector_db = VectorDB()
        vector_db.add_index('test_index', self.db.embedding_model)
        vector_db.add_index('test_index2', self.db.embedding_model)
        self.assertEqual(vector_db.list_indices(), ['test_index', 'test_index2'])