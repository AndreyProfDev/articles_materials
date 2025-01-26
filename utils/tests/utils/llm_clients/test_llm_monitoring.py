import pytest
from pydantic import BaseModel

from utils.llm_clients.cost_monitoring import LLMClientWithCostMonitoring
from utils.llm_clients.schema import ChatMessage, GenericLLMResponse, LLMModelInfo


class MockedResponse(BaseModel, frozen=True):
    response: str


class MockedLLMClient:
    def __init__(
        self, request_to_responce: dict[ChatMessage, GenericLLMResponse[MockedResponse]]
    ) -> None:
        self.request_to_responce = request_to_responce
        self.number_of_calls = 0
        self.model_info = LLMModelInfo(
            model_name="test_model",
            promt_cost_per_mln_tokens=0.1,
            completion_cost_per_mln_tokens=0.1,
        )

    def chat(
        self, messages: list[ChatMessage], _format: type[MockedResponse]
    ) -> GenericLLMResponse[MockedResponse]:
        self.number_of_calls += 1
        response = self.request_to_responce[messages[0]]
        return response

    def get_number_of_calls(self) -> int:
        return self.number_of_calls


@pytest.fixture
def responce() -> GenericLLMResponse[MockedResponse]:
    underlying_responce = MockedResponse(response="responce")
    generic_responce = GenericLLMResponse(
        response=underlying_responce, promt_tokens=2, completion_tokens=3, time_to_generate=0
    )

    return generic_responce


@pytest.fixture
def underlying_client(responce: GenericLLMResponse[MockedResponse]):
    underlying_client = MockedLLMClient(
        request_to_responce={ChatMessage(role="user", content="request"): responce}
    )
    return underlying_client


@pytest.fixture
def client(underlying_client: MockedLLMClient):
    return LLMClientWithCostMonitoring(client=underlying_client)


def test_llm_cost_monitoring(client):
    client.chat([ChatMessage(role="user", content="request")], _format=MockedResponse)
    client.chat([ChatMessage(role="user", content="request")], _format=MockedResponse)

    assert client.promt_tokens == 4
    assert client.completion_tokens == 6
