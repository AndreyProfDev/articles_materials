import unittest

from utils.wiki_parser.schema import ArticleSection

from src.utils.storage import ArticleStorage
from utils.wiki_parser.wiki_parser import SingleArticle
import pandas as pd

class ArticleStorageTestCase(unittest.TestCase):

    def test_storing_simple_articles(self):
        storage = ArticleStorage()
        articles = [SingleArticle(title="Test", sections="Test content"), 
                    SingleArticle(title="Test2", sections="Test content 2")]
        storage.save_articles(articles)

        self.assertEqual(len(storage), 2)

    def test_storing_multisection_arcticles(self):
        storage = ArticleStorage()
        articles = [SingleArticle(title="Test", sections=[ArticleSection(title="Section 1", content="Test content"),
                                                          ArticleSection(title="Section 2", content="Test content 2")]), 
                    SingleArticle(title="Test2", sections="Test content 2")]
        storage.save_articles(articles)

        actual_df = storage.load_all()
        assert actual_df.equals(pd.DataFrame({'Article Title': ['Test', 'Test', 'Test2'],
                                              'Section Title': ['Section 1', 'Section 2', 'Main'],
                                              'Section Content': ['Test content', 'Test content 2', 'Test content 2']}))

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