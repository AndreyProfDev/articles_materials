from enum import Enum
import tiktoken

class ENCODING_MODEL_NAME(Enum):
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"


def tokenize_text(text: str, encoding_model_name: ENCODING_MODEL_NAME) -> list[int]:
    tokenizer = tiktoken.encoding_for_model(encoding_model_name.value)
    return tokenizer.encode(text)

def calculate_number_of_tokens(text: str, encoding_model_name: ENCODING_MODEL_NAME) -> int:
    return len(tokenize_text(text, encoding_model_name))