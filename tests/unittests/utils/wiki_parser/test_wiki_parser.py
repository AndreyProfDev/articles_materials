from tempfile import NamedTemporaryFile
import unittest

from utils.wiki_parser import wiki_parser


class TestWikiParser(unittest.TestCase):

    def contruct_wiki_xml(self, articles: list[wiki_parser.SingleArticle]) -> str:

        page_text = "<mediawiki>\n"
        for article in articles:
            page_text += f"""<page>
                                <title>{article.title}</title>
                                <revision>
                                    <id>53701990</id>
                                    <text bytes="7843">{article.content}</text>
                                </revision>
                            </page>"""
            
        return page_text + "\n</mediawiki>"
 
    def test_extract_simple_texts_from_wiki(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", sections="Test text"), 
                                                    wiki_parser.SingleArticle(title="Test2", sections="Test text 2")])

        articles = wiki_parser.extract_articles_from_mediawiki_xml(wiki_articles_xml)

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].content, "Test text")
        self.assertEqual(articles[1].title, "Test2")
        self.assertEqual(articles[1].content, "Test text 2")

    def test_extracting_pages_from_file(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", sections="Test text"), 
                                                    wiki_parser.SingleArticle(title="Test2", sections="Test text 2")])

        with NamedTemporaryFile() as file:
            file.write(wiki_articles_xml.encode('utf-8'))
            file.seek(0)
            articles = wiki_parser.extract_articles_from_file(file.name)

            self.assertEqual(len(articles), 2)

    def test_removal_of_empty_pages(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", sections=""), 
                                                    wiki_parser.SingleArticle(title="Test2", sections="Test text 2")])

        articles = wiki_parser.extract_articles_from_mediawiki_xml(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test2")
        self.assertEqual(articles[0].content, "Test text 2")

