import pytest

from utils.embedding_models.caching import CachedEmbeddingModel
from utils.embedding_models.monitoring import EmbeddingModelWithMonitoring
from utils.providers import supported_models
from utils.providers.hugging_face import HFEmbeddingModel
from utils.vector_db.vectordb import VectorIndex


@pytest.fixture
def model_info():
    return supported_models.ST_POLISH_PARAPHRASE_FROM_DISTILROBERTA


@pytest.fixture
def hf_embedding_model(model_info):
    return HFEmbeddingModel(model_info=model_info)


@pytest.fixture
def cached_hf_embedding_model(hf_embedding_model):
    return CachedEmbeddingModel(model=hf_embedding_model)


@pytest.fixture
def monitored_hf_embedding_model(cached_hf_embedding_model):
    return EmbeddingModelWithMonitoring(model=cached_hf_embedding_model)


@pytest.fixture
def vector_index(model_info):
    return VectorIndex(model_info=model_info)


@pytest.mark.skip(reason="Integration test for Hugging Face Embeddings API")
def test_populate_database_with_hugging_face_embeddings(
    vector_index: VectorIndex, monitored_hf_embedding_model: EmbeddingModelWithMonitoring
):
    first_text = "To jest pierwszy tekst testowy"
    first_text_embedding = monitored_hf_embedding_model.embed([first_text]).embeddings[0]
    vector_index.insert_text(text=first_text, embedding=first_text_embedding)
    assert vector_index.size == 1

    second_text = "To jest drugi tekst testowy"
    second_text_embedding = monitored_hf_embedding_model.embed([second_text]).embeddings[0]
    vector_index.insert_text(text=second_text, embedding=second_text_embedding)
    assert vector_index.size == 2

    found = vector_index.find_text(first_text_embedding, top_k=1)
    found = [first_text]

    third_text = "To jest pierwszy tekst"
    third_text_embedding = monitored_hf_embedding_model.embed([third_text]).embeddings[0]
    found = vector_index.find_text(third_text_embedding, top_k=1)
    assert found == [first_text]


if __name__ == "__main__":
    pytest.main()
