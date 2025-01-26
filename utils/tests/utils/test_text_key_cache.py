from collections.abc import Callable
from pathlib import Path

import pytest

from utils.caching import FileBasedTextCache


@pytest.fixture
def temp_dir_path(tmp_path: Path):
    return tmp_path


@pytest.fixture
def cache_factory(temp_dir_path: Path):
    def create_cache(prefix: str):
        return FileBasedTextCache(prefix=prefix, path_to_cache=temp_dir_path)

    return create_cache


@pytest.fixture
def cache(cache_factory: Callable[[str], FileBasedTextCache]):
    return cache_factory("test")


def test_store_cached_text(cache: FileBasedTextCache):
    cache.store("key", "value")

    files_stored = list(cache.path_to_cache.glob("*"))
    assert len(list(files_stored)) == 1

    assert files_stored[0].name.startswith("test_")


def test_cached_text_exists(cache: FileBasedTextCache):
    assert not cache.exists("key")

    cache.store("key", "value")
    assert cache.exists("key")

    assert not cache.exists("other key")


def test_retrieve_existing_cached_test(cache: FileBasedTextCache):
    cache.store("key", "value")

    assert cache.retrieve("key") == "value"


def test_retrieve_non_existing_cached_test(cache: FileBasedTextCache):
    assert cache.retrieve("key") is None


def test_retrieve_all_cached_texts(
    cache: FileBasedTextCache, cache_factory: Callable[[str], FileBasedTextCache]
):
    cache.store("key", "value")
    cache.store("key2", "value")

    cache2 = cache_factory("test")

    assert cache2.retrieve_all() == {"key": "value", "key2": "value"}

    cache3 = cache_factory("other")
    assert cache3.retrieve_all() == {}
