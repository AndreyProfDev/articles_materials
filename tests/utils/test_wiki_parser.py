from tempfile import NamedTemporaryFile
import unittest

from embeddings_comparison.utils import wiki_parser


class TestWikiParser(unittest.TestCase):

    def contruct_wiki_xml(self, articles: list[wiki_parser.SingleArticle]) -> str:

        page_text = "<mediawiki>\n"
        for article in articles:
            page_text += f"""<page>
                                <title>{article.title}</title>
                                <revision>
                                    <text>{article.text}</text>
                                </revision>
                            </page>"""
            
        return page_text + "\n</mediawiki>"
 
    def testExtractSimpleTextsFromWiki(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test text"), 
                                                    wiki_parser.SingleArticle(title="Test2", text="Test text 2")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test text")
        self.assertEqual(articles[1].title, "Test2")
        self.assertEqual(articles[1].text, "Test text 2")

    def testRemoveFileReferences(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test [[Plik:test text]] text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test text")

    def testReplaceTextReferencesWithText(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test [[other text]] text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test other text text")

    def testExtractingPagesFromFile(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test text"), 
                                                    wiki_parser.SingleArticle(title="Test2", text="Test text 2")])

        with NamedTemporaryFile() as file:
            file.write(wiki_articles_xml.encode('utf-8'))
            file.seek(0)
            articles = wiki_parser.extractPagesFromFile(file.name)

            self.assertEqual(len(articles), 2)
            self.assertEqual(articles[0].title, "Test")
            self.assertEqual(articles[0].text, "Test text")
            self.assertEqual(articles[1].title, "Test2")
            self.assertEqual(articles[1].text, "Test text 2")

    def testRemoveReferencesToOtherPages(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test {{other page}} text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test text")