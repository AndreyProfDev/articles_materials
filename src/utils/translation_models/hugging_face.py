from enum import Enum
from transformers import pipeline


class HUGGING_FACE_TRANSLATOR_MODEL(Enum):
    HUGGING_FACE_TRANSLATOR = "Helsinki-NLP/opus-mt-pl-en"

class Device(Enum):
    CPU = "cpu"
    GPU = "cuda"

class TranslatorEnglishToPolish:
    def __init__(self, translation_model_name: HUGGING_FACE_TRANSLATOR_MODEL, device: Device=Device.CPU) -> None:
        self.translation_pipeline = pipeline("translation", model=translation_model_name.value, device=device.value)

    def translate(self, text: str, max_completion_length=512) -> str:
        resp = self.translation_pipeline(text, max_completion_length)

        return resp