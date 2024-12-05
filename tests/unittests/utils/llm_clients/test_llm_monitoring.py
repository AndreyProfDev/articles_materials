

import unittest

from pydantic import BaseModel
from utils.llm_clients.cost_monitoring import LLMClientWithCostMonitoring
from utils.llm_clients.schema import ChatMessage, GenericLLMResponse, LLMModelInfo

class MockedResponse(BaseModel, frozen=True):
    response: str

class MockedLLMClient:
    def __init__(self, request_to_responce: dict[ChatMessage, MockedResponse]) -> None:
        self.request_to_responce = request_to_responce
        self.number_of_calls = 0
        self.model_info = LLMModelInfo(model_name="test_model", promt_cost_per_mln_tokens=0.1, completion_cost_per_mln_tokens=0.1)

    def chat(self, messages: list[ChatMessage], _format: type[MockedResponse]) -> GenericLLMResponse[MockedResponse]:
        self.number_of_calls += 1
        response = self.request_to_responce[messages[0]]
        return GenericLLMResponse(response=response, promt_tokens=2, completion_tokens=3, time_to_generate=0)

    def get_number_of_calls(self) -> int:
        return self.number_of_calls
    
class LLMCostMonitoringTestCase(unittest.TestCase):

    def test_llm_cost_monitoring(self):
        underlying_response = MockedResponse(response="response")
        client = MockedLLMClient(request_to_responce={ChatMessage(role="user", content="request"): underlying_response})
        client = LLMClientWithCostMonitoring(client=client)


        client.chat([ChatMessage(role="user", content="request")], _format=MockedResponse)
        client.chat([ChatMessage(role="user", content="request")], _format=MockedResponse)

        self.assertEqual(client.promt_tokens, 4)
        self.assertEqual(client.completion_tokens, 6)