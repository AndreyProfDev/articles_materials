import unittest

from src.utils.storage import ArticleStorage
from utils.wiki_parser.wiki_parser import SingleArticle
import pandas as pd

class ArticleStorageTestCase(unittest.TestCase):

    def test_storage(self):
        storage = ArticleStorage()
        articles = [SingleArticle(title="Test", sections="Test content"), 
                    SingleArticle(title="Test2", sections="Test content 2")]
        storage.save_articles(articles)

        self.assertEqual(len(storage), 2)

    def test_load_table(self):
        storage = ArticleStorage()
        articles = [SingleArticle(title="Test", sections="Test content"), 
                    SingleArticle(title="Test2", sections="Test content 2")]
        storage.save_articles(articles)
        actual_df = storage.load_all()

        expected_df = pd.DataFrame({'Article Title': ['Test', 'Test2'],
                                    'Section Title': ['Main', 'Main'],
                                    'Section Content': ['Test content', 'Test content 2']})

        self.assertTrue(actual_df.equals(expected_df))