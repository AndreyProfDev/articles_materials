from pathlib import Path

import pytest
from pydantic import BaseModel

from utils.llm_clients.cached_client import CachedLLMClient
from utils.llm_clients.schema import ChatMessage, GenericLLMResponse, LLMModelInfo


class MockedResponse(BaseModel, frozen=True):
    responce: str


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
        responce = self.request_to_responce[messages[0]]
        return responce

    def get_number_of_calls(self) -> int:
        return self.number_of_calls


@pytest.fixture
def responce() -> GenericLLMResponse[MockedResponse]:
    underlying_responce = MockedResponse(responce="responce")
    generic_responce = GenericLLMResponse(
        response=underlying_responce, promt_tokens=0, completion_tokens=0, time_to_generate=0
    )

    return generic_responce


@pytest.fixture
def underlying_client(responce: GenericLLMResponse[MockedResponse]):
    underlying_client = MockedLLMClient(
        request_to_responce={ChatMessage(role="user", content="request"): responce}
    )
    return underlying_client


def test_cached_embedding(
    underlying_client: MockedLLMClient, responce: GenericLLMResponse[MockedResponse], tmp_path: Path
):
    result = underlying_client.chat(
        [ChatMessage(role="user", content="request")], _format=MockedResponse
    )
    assert underlying_client.number_of_calls == 1
    assert result == responce

    result = underlying_client.chat(
        [ChatMessage(role="user", content="request")], _format=MockedResponse
    )
    assert underlying_client.number_of_calls == 2
    assert result == responce

    client = CachedLLMClient(client=underlying_client, path_to_cache=tmp_path)

    result = client.chat([ChatMessage(role="user", content="request")], _format=MockedResponse)
    assert underlying_client.number_of_calls == 3
    assert result == responce

    result = client.chat([ChatMessage(role="user", content="request")], _format=MockedResponse)
    assert underlying_client.number_of_calls == 3
    assert result.model_dump_json() == responce.model_dump_json()


if __name__ == "__main__":
    pytest.main()
