

from pathlib import Path

from openai import BaseModel

from src.utils.caching import FileBasedTextCache

from typing import Generic, TypeVar

class MonitoringEvent(BaseModel):
    id: str
    cost: int

T = TypeVar('T', bound='MonitoringEvent')

class EmbeddingCreatedEvent(MonitoringEvent):
    model_name: str
    text: str
    embedding: list[float]

class TextCompletionEvent(MonitoringEvent):
    model_name: str
    text: str

class EventRegistry(Generic[T]):

    def __init__(self, prefix: str, event_format: type[T], cache_path: Path = Path('~/.cache/monitoring_service_cache').expanduser()) -> None:
        self.cache = FileBasedTextCache(prefix=prefix, path_to_cache=cache_path)
        self._events: dict[str, T] = {}
        self.cached_cost = 0
        self.new_cost = 0
        self.event_format = event_format
        self.warmap_cache()

    def warmap_cache(self) -> None:
        cached_elements_dict = self.cache.retrieve_all()
        for key, value in cached_elements_dict.items():
            embedding_info = self.event_format.model_validate_json(value)
            self._events[key] = embedding_info
            self.cached_cost += embedding_info.cost

    def is_empty(self) -> bool:
        return len(self._events) == 0
    
    def register_event(self, event: T) -> None:
        self._events[event.id] = event
        self.new_cost += event.cost
        self.cache.store(event.id, event.model_dump_json())

    def get_event(self, id: str) -> T:
        if id not in self._events:
            raise ValueError(f'No embedding info for id: {id}')
        
        return self._events[id]
    
    def get_total_cost(self) -> int:
        return self.cached_cost + self.new_cost

class EmbeddingEventRegistry(EventRegistry[EmbeddingCreatedEvent]):
    
    def __init__(self, cache_path: Path = Path('~/.cache/monitoring_service_cache').expanduser()) -> None:
        prefix = 'embeddings_monitoring'
        super().__init__(prefix, EmbeddingCreatedEvent, cache_path)


class CompletionEventRegistry(EventRegistry[TextCompletionEvent]):
    
    def __init__(self, cache_path: Path = Path('~/.cache/monitoring_service_cache').expanduser()) -> None:
        prefix = 'text_completion_monitoring'
        super().__init__(prefix, TextCompletionEvent, cache_path)