import unittest

from utils.embedding_models.monitoring import EmbeddingModelWithMonitoring
from utils.embedding_models.schema import EmbeddingModelInfo, GenericEmbeddingResponse


class MockedEmbeddingModel:
    def __init__(
        self, text_to_embeddings: dict[str, list[float]], unique_model_name: str
    ) -> None:
        self.text_to_embeddings = text_to_embeddings
        self.number_of_calls = 0
        self.unique_model_name = unique_model_name

    def embed(self, texts: list[str]) -> GenericEmbeddingResponse:
        self.number_of_calls += 1
        embeddings = [self.text_to_embeddings[text] for text in texts]
        return GenericEmbeddingResponse(
            embeddings=embeddings, promt_tokens=6, time_to_generate=2
        )

    @property
    def model_info(self) -> EmbeddingModelInfo:
        return EmbeddingModelInfo(
            model_name="test_model", dimension=42, cost_per_mln_tokens=0.1
        )


class EmbeddingMonitoringTestCase(unittest.TestCase):

    def test_cost_monitoring(self):

        underlying_model = MockedEmbeddingModel(
            text_to_embeddings={"test": [1, 2, 3]}, unique_model_name="test_model1"
        )
        client = EmbeddingModelWithMonitoring(model=underlying_model)

        client.embed(["test"])
        client.embed(["test"])

        self.assertEqual(client.promt_tokens, 12)

    def test_time_monitoring(self):

        underlying_model = MockedEmbeddingModel(
            text_to_embeddings={"test": [1, 2, 3]}, unique_model_name="test_model1"
        )
        client = EmbeddingModelWithMonitoring(model=underlying_model)

        client.embed(["test"])
        client.embed(["test"])

        self.assertEqual(client.time_to_generate, 4)
