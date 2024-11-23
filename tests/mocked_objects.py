
class MockedEmbeddingModel:
    def __init__(self, text_to_embeddings: dict[str, list[float]], unique_model_name: str) -> None:
        self.text_to_embeddings = text_to_embeddings
        self.number_of_calls = 0
        self.unique_model_name = unique_model_name

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.number_of_calls += 1
        return [self.text_to_embeddings[text] for text in texts]
    
    def get_dimension(self) -> int:
        return 42
    
    def get_unique_model_name(self) -> str:
        return self.unique_model_name