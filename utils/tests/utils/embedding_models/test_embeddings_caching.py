import pytest

from utils.embedding_models.caching import CachedEmbeddingModel
from utils.embedding_models.schema import (
    MODEL_PROVIDER,
    EmbeddingModelInfo,
    GenericEmbeddingResponse,
)


class MockedEmbeddingModel:
    def __init__(self, text_to_embeddings: dict[str, list[float]], unique_model_name: str) -> None:
        self.text_to_embeddings = text_to_embeddings
        self.number_of_calls = 0
        self.unique_model_name = unique_model_name
        self.model_info = EmbeddingModelInfo(
            provider=MODEL_PROVIDER.HUGGING_FACE,
            model_name=unique_model_name,
            dimension=42,
            cost_per_mln_tokens=0.1,
        )

    def embed(self, texts: list[str]) -> GenericEmbeddingResponse:
        self.number_of_calls += 1
        embeddings = [self.text_to_embeddings[text] for text in texts]
        return GenericEmbeddingResponse(embeddings=embeddings, promt_tokens=0, time_to_generate=0)


@pytest.fixture
def underlying_model() -> MockedEmbeddingModel:
    return MockedEmbeddingModel(
        text_to_embeddings={"test": [1, 2, 3]}, unique_model_name="test_model1"
    )


@pytest.fixture
def cached_model(underlying_model, tmp_path) -> CachedEmbeddingModel:
    return CachedEmbeddingModel(model=underlying_model, path_to_cache=tmp_path)


def test_cached_embedding(underlying_model, cached_model):
    result = underlying_model.embed(["test"])
    assert underlying_model.number_of_calls == 1
    assert result.embeddings == [[1, 2, 3]]

    result = underlying_model.embed(["test"])
    assert underlying_model.number_of_calls == 2
    assert result.embeddings == [[1, 2, 3]]

    result = cached_model.embed(["test"])
    assert underlying_model.number_of_calls == 3
    assert result.embeddings == [[1, 2, 3]]

    result = cached_model.embed(["test"])
    assert underlying_model.number_of_calls == 3
    assert result.embeddings == [[1, 2, 3]]
