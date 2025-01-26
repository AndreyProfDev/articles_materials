import pytest

from utils.embedding_models.monitoring import EmbeddingModelWithMonitoring
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

    def embed(self, texts: list[str]) -> GenericEmbeddingResponse:
        self.number_of_calls += 1
        embeddings = [self.text_to_embeddings[text] for text in texts]
        return GenericEmbeddingResponse(embeddings=embeddings, promt_tokens=6, time_to_generate=2)

    @property
    def model_info(self) -> EmbeddingModelInfo:
        return EmbeddingModelInfo(
            provider=MODEL_PROVIDER.HUGGING_FACE,
            model_name="test_model",
            dimension=42,
            cost_per_mln_tokens=0.1,
        )


@pytest.fixture
def underlying_model() -> MockedEmbeddingModel:
    return MockedEmbeddingModel(
        text_to_embeddings={"test": [1, 2, 3]}, unique_model_name="test_model1"
    )


def monitored_model(underlying_model) -> EmbeddingModelWithMonitoring:
    return EmbeddingModelWithMonitoring(model=underlying_model)


def test_time_cost_monitoring(underlying_model):
    client = EmbeddingModelWithMonitoring(model=underlying_model)

    client.embed(["test"])
    client.embed(["test"])

    assert client.time_to_generate == 4
    assert client.promt_tokens == 12
