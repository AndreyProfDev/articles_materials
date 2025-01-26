import pytest

from utils.embedding_models.schema import (
    MODEL_PROVIDER,
    EmbeddingModelInfo,
)
from utils.vector_db.vectordb import VectorIndex


@pytest.fixture
def model_info():
    return EmbeddingModelInfo(
        provider=MODEL_PROVIDER.HUGGING_FACE,
        model_name="test_model",
        dimension=3,
        cost_per_mln_tokens=0.1,
    )


@pytest.fixture
def vector_index(model_info):
    return VectorIndex(model_info=model_info)


def test_insert(vector_index: VectorIndex):
    vector_index.insert_text(text="Test text 1", embedding=[1.0, 2.0, 3.0])
    assert vector_index.size == 1

    vector_index.insert_text("Test text 2", embedding=[2.0, 3.0, 4.0])
    assert vector_index.size == 2


def test_find_text(vector_index: VectorIndex):
    text1 = "Test text 1"
    text2 = "Test text 2"
    vector_index.insert_text(text1, embedding=[1.0, 2.0, 3.0])
    vector_index.insert_text(text2, embedding=[4.0, 5.0, 6.0])

    embedding_to_search = [1.0, 2.0, 4.0]
    assert vector_index.find_text(embedding_to_search, top_k=1) == [text1]
    assert vector_index.find_text(embedding_to_search, top_k=2) == [text1, text2]
    assert vector_index.find_text(embedding_to_search, top_k=3) == [text1, text2]
