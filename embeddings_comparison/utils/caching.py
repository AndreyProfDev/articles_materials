

import hashlib
from pathlib import Path
from typing import Annotated

from pydantic import constr


class FileBasedTextCache:
    def __init__(self, prefix: Annotated[str, constr(min_length=1)], path_to_cache: Path) -> None:
        self.prefix = prefix
        self.path_to_cache = path_to_cache

    def _get_cache_file_path(self, text: str) -> Path:
        cache_file_name = hashlib.md5(text.encode("utf-8")).hexdigest()
        cache_path = self.path_to_cache / f"{self.prefix}_{cache_file_name}"
        return cache_path

    def store(self, key: str, value: str) -> None:
        cache_path = self._get_cache_file_path(key)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "wb") as f:
            f.write(value.encode("utf-8"))

    def exists(self, key: str) -> bool:
        cache_path = self._get_cache_file_path(key)
        return cache_path.exists()
    
    def retrieve(self, key: str) -> str | None:
        if not self.exists(key):
            return None

        cache_path = self._get_cache_file_path(key)
        with open(cache_path, "rb") as f:
            return f.read().decode("utf-8")