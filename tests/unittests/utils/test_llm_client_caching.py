from pathlib import Path
import shutil
import tempfile
import unittest

from pydantic import BaseModel

from src.utils.llm_clients.cached_client import CachedLLMClient
from src.utils.llm_clients.schema import ChatMessage

class MockedResponse(BaseModel, frozen=True):
    response: str

class MockedLLMClient:
    def __init__(self, request_to_responce: dict[ChatMessage, MockedResponse]) -> None:
        self.request_to_responce = request_to_responce
        self.number_of_calls = 0

    def chat(self, messages: list[ChatMessage], _format: type[MockedResponse]) -> MockedResponse:
        self.number_of_calls += 1
        return self.request_to_responce[messages[0]]

    def get_number_of_calls(self) -> int:
        return self.number_of_calls
    
    def get_unique_model_name(self) -> str:
        return "mocked"

class CachedLLMClientTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.temp_dir_path = Path(self.temp_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)
    
    def test_cached_embedding(self):
        response = MockedResponse(response="response")
        underlying_client = MockedLLMClient(request_to_responce={ChatMessage(role="user", content="request"): response})

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
        self.assertEqual(result, response)