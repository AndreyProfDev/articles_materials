import os

import pytest

from utils.embedding_models.caching import CachedEmbeddingModel
from utils.embedding_models.monitoring import EmbeddingModelWithMonitoring
from utils.providers import supported_models
from utils.providers.open_ai import OpenAIEmbeddingModel
from utils.vector_db.vectordb import VectorIndex


@pytest.fixture
def model_info():
    return supported_models.TEXT_EMBEDDING_3_SMALL


@pytest.fixture
def openai_embedding_model(model_info):
    api_key = os.environ["OPEN_AI_KEY"]
    return OpenAIEmbeddingModel(api_key=api_key, model_info=model_info)


@pytest.fixture
def cached_openai_embedding_model(openai_embedding_model):
    return CachedEmbeddingModel(model=openai_embedding_model)


@pytest.fixture
def monitored_openai_embedding_model(cached_openai_embedding_model):
    return EmbeddingModelWithMonitoring(model=cached_openai_embedding_model)


@pytest.fixture
def vector_index(model_info):
    return VectorIndex(model_info=model_info)


@pytest.mark.skip(reason="Integration test for OpenAI Embeddings API")
def test_populate_database_with_openai_embeddings(
    vector_index: VectorIndex, monitored_openai_embedding_model: EmbeddingModelWithMonitoring
):
    embedding_model = monitored_openai_embedding_model

    first_text = "This is a first test text"
    first_text_embedding = embedding_model.embed([first_text]).embeddings[0]
    vector_index.insert_text(first_text, first_text_embedding)
    assert vector_index.size == 1

    second_text = "This is a second test text"
    second_text_embedding = embedding_model.embed([second_text]).embeddings[0]
    vector_index.insert_text(second_text, second_text_embedding)
    assert vector_index.size == 2

    found = vector_index.find_text(embedding=first_text_embedding, top_k=1)
    assert found == ["This is a first test text"]

    third_text = "This is a first text"
    third_text_embedding = embedding_model.embed([third_text]).embeddings[0]
    found = vector_index.find_text(embedding=third_text_embedding, top_k=1)
    assert found == [first_text]

    assert embedding_model.time_to_generate > 0


if __name__ == "__main__":
    pytest.main()
