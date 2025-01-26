import os

import pytest

from utils.llm_clients.cached_client import CachedLLMClient
from utils.llm_clients.cost_monitoring import LLMClientWithCostMonitoring
from utils.llm_clients.providers import supported_models
from utils.llm_clients.providers.open_ai_client import OpenAIClient
from utils.question_generation import BASE_PROMT_PL, GeneratedQuestions, generate_question_for_text


@pytest.fixture
def open_ai_client() -> OpenAIClient:
    api_key = os.environ.get("OPEN_AI_KEY")
    assert api_key is not None

    return OpenAIClient(api_key=str(api_key), model_info=supported_models.GPT_4O)


@pytest.fixture
def cached_llm_client(open_ai_client) -> CachedLLMClient[GeneratedQuestions]:
    return CachedLLMClient(client=open_ai_client)


@pytest.fixture
def monitored_llm_client(cached_llm_client) -> LLMClientWithCostMonitoring:
    return LLMClientWithCostMonitoring(client=cached_llm_client)


@pytest.mark.skip(reason="Integration test for OpenAI Completion API")
def test_generate_question_for_extract(monitored_llm_client):
    extracted = "The quick brown fox jumps over the lazy dog"
    questions = generate_question_for_text(monitored_llm_client, extracted, BASE_PROMT_PL)

    assert len(questions.questions) == 5
    assert monitored_llm_client.promt_tokens > 0
    assert monitored_llm_client.completion_tokens > 0
