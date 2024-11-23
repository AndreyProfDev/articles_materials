import unittest

from src.utils.embedding_models import tokenizer
from src.utils.embedding_models.tokenizer import ENCODING_MODEL_NAME

class TextTokenizerTestCase(unittest.TestCase):

    def test_tokenizing(self):
        text = "This is a test"

        result = tokenizer.tokenize_text(text, ENCODING_MODEL_NAME.TEXT_EMBEDDING_3_SMALL)
        self.assertEqual(result, [2028, 374, 264, 1296])

        result = tokenizer.tokenize_text(text, ENCODING_MODEL_NAME.TEXT_EMBEDDING_3_LARGE)
        self.assertEqual(result, [2028, 374, 264, 1296])

        result = tokenizer.tokenize_text(text, ENCODING_MODEL_NAME.TEXT_EMBEDDING_ADA_002)
        self.assertEqual(result, [2028, 374, 264, 1296])
        
        number_of_tokens = tokenizer.calculate_number_of_tokens(text, ENCODING_MODEL_NAME.TEXT_EMBEDDING_3_LARGE)
        self.assertEqual(number_of_tokens, 4)

