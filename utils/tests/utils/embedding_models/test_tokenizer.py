import pytest
from pytest import param

from utils.embedding_models import tokenizer
from utils.embedding_models.tokenizer import ENCODING_MODEL_NAME


@pytest.mark.parametrize(
    ("model"),
    [
        param(
            ENCODING_MODEL_NAME.TEXT_EMBEDDING_3_SMALL,
            id="Testing tokenizer for Open AI small embedding model",
        ),
        param(
            ENCODING_MODEL_NAME.TEXT_EMBEDDING_3_LARGE,
            id="Testing tokenizer for Open AI large embedding model",
        ),
        param(
            ENCODING_MODEL_NAME.TEXT_EMBEDDING_ADA_002,
            id="Testing tokenizer for Open AI Ada 002 embedding model",
        ),
    ],
)
def test_tokenizing(model: ENCODING_MODEL_NAME):
    text = "This is a test"
    expected_tokens = [2028, 374, 264, 1296]

    result = tokenizer.tokenize_text(text, model)
    assert result == expected_tokens

    number_of_tokens = tokenizer.calculate_number_of_tokens(
        text, ENCODING_MODEL_NAME.TEXT_EMBEDDING_3_LARGE
    )
    assert number_of_tokens == 4
