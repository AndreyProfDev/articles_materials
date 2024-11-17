import unittest

from embeddings_comparison.utils.vectordb.vectordb import VectorDB

class MockedEmbeddingModel:
    def __init__(self, text_to_embedding: dict[str, list[float]], dimension: int) -> None:
        self.text_to_embedding = text_to_embedding
        self.dimension = dimension

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self.text_to_embedding[text] for text in texts]
    
    def get_dimension(self) -> int:
        return self.dimension


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
        self.db = VectorDB(embedding_model=embedding_model)

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