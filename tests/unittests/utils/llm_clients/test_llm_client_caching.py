from pathlib import Path
import shutil
import tempfile
import unittest

from pydantic import BaseModel
from utils.llm_clients.cached_client import CachedLLMClient

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
        return GenericLLMResponse(response=response, promt_tokens=0, completion_tokens=0, time_to_generate=0)

    def get_number_of_calls(self) -> int:
        return self.number_of_calls
    
    
class CachedLLMClientTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.temp_dir_path = Path(self.temp_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)
    
    def test_cached_embedding(self):
        underlying_response = MockedResponse(response="response")
        response = GenericLLMResponse[MockedResponse](response=underlying_response, promt_tokens=0, completion_tokens=0, time_to_generate=0)
        underlying_client = MockedLLMClient(request_to_responce={ChatMessage(role="user", content="request"): underlying_response})

        result = underlying_client.chat([ChatMessage(role="user", content="request")], _format=MockedResponse)
        self.assertEqual(underlying_client.number_of_calls, 1)
        self.assertEqual(result, response)

        result = underlying_client.chat([ChatMessage(role="user", content="request")], _format=MockedResponse)
        self.assertEqual(underlying_client.number_of_calls, 2)
        self.assertEqual(result, response)

        client = CachedLLMClient(client=underlying_client, path_to_cache=self.temp_dir_path)

        result = client.chat([ChatMessage(role="user", content="request")], _format=MockedResponse)
        self.assertEqual(underlying_client.number_of_calls, 3)
        self.assertEqual(result, response)

        result = client.chat([ChatMessage(role="user", content="request")], _format=MockedResponse)
        self.assertEqual(underlying_client.number_of_calls, 3)
        self.assertEqual(result.model_dump_json(), response.model_dump_json())