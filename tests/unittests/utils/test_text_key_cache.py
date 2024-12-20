import shutil
import tempfile
import unittest
from pathlib import Path

from utils.caching import FileBasedTextCache


class TextKeyCacheTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.temp_dir_path = Path(self.temp_dir)
        self.cache = FileBasedTextCache(prefix="test", path_to_cache=self.temp_dir_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_store_cached_text(self):
        self.cache.store("key", "value")

        files_stored = list(self.temp_dir_path.glob("*"))
        self.assertEqual(len(list(files_stored)), 1)

        self.assertTrue(files_stored[0].name.startswith("test_"))

    def test_cached_text_exists(self):

        self.assertFalse(self.cache.exists("key"))

        self.cache.store("key", "value")
        self.assertTrue(self.cache.exists("key"))

        self.assertFalse(self.cache.exists("other key"))

    def test_retrieve_existing_cached_test(self):

        self.cache.store("key", "value")

        self.assertEqual(self.cache.retrieve("key"), "value")

    def test_retrieve_non_existing_cached_test(self):

        self.assertEqual(self.cache.retrieve("key"), None)

    def test_retrieve_all_cached_texts(self):

        self.cache.store("key", "value")
        self.cache.store("key2", "value")

        cache2 = FileBasedTextCache(prefix="test", path_to_cache=self.temp_dir_path)

        self.assertEqual(cache2.retrieve_all(), {"key": "value", "key2": "value"})

        cache3 = FileBasedTextCache(prefix="other", path_to_cache=self.temp_dir_path)
        self.assertEqual(cache3.retrieve_all(), {})
