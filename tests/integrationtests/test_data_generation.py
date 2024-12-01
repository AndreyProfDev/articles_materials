import unittest

from dotenv import load_dotenv
from utils.llm_clients.cached_client import CachedLLMClient
from utils.llm_clients.cost_monitoring import LLMClientWithCostMonitoring

from utils.llm_clients.providers import supported_models
from utils.llm_clients.providers.open_ai_client import OpenAIClient
from utils.question_generation import BASE_PROMT_PL, GeneratedQuestions, generate_question_for_text
import os

class QuestionGenerationTestCase(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()

    @unittest.skip("Integration test for OpenAI Completion API")
    def test_generate_question_for_extract(self):

        api_key = os.environ.get('OPEN_AI_KEY')
        self.assertIsNotNone(api_key)

        llm_client = OpenAIClient(api_key=str(api_key), model_info=supported_models.GPT_4O)
        llm_client = CachedLLMClient[GeneratedQuestions](client=llm_client)
        llm_client = LLMClientWithCostMonitoring(client=llm_client)
        
        extracted = 'The quick brown fox jumps over the lazy dog'
        questions = generate_question_for_text(llm_client, extracted, BASE_PROMT_PL)

        self.assertEqual(len(questions.questions), 5)
        self.assertTrue(llm_client.promt_tokens > 0)
        self.assertTrue(llm_client.completion_tokens > 0)
