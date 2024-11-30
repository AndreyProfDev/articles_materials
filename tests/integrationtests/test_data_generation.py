import unittest

from dotenv import load_dotenv

from src.utils.llm_clients.cached_client import CachedLLMClient
from src.utils.llm_clients.open_ai_client import OPEN_AI_MODEL_NAME, OpenAIClient
from src.utils.question_generation import BASE_PROMT_PL, GeneratedQuestions, generate_question_for_text
import os

class QuestionGenerationTestCase(unittest.TestCase):

    def setUp(self) -> None:
        load_dotenv()

    @unittest.skip("Integration test for OpenAI Completion API")
    def test_generate_question_for_extract(self):

        api_key = os.environ.get('OPEN_AI_KEY')
        self.assertIsNotNone(api_key)

        llm_client = CachedLLMClient[GeneratedQuestions](client=OpenAIClient(api_key=str(api_key), model_name=OPEN_AI_MODEL_NAME.GPT_4O))
        
        extracted = 'The quick brown fox jumps over the lazy dog'
        questions = generate_question_for_text(llm_client, extracted, BASE_PROMT_PL)

        self.assertEqual(len(questions.questions), 5)
