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
                                    <id>53701990</id>
                                    <text bytes="7843">{article.text}</text>
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

    def testRemoveFileReference(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test [[Plik:test\ntext]] text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test text")

    def testRemoveSeveralFileReferences(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test [[Plik:test\ntext]]\n[[Plik:test\ntext]] text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test \n text")

    def testReplaceSeveralTextReferencesWithText(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test [[Plik:test\ntext]]\n[[other\ntext]] text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test \nother\ntext text")

    def testReplaceTextReferenceWithTextInside(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test [[other\ntext]] text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test other\ntext text")

    def testReplaceTextReferenceWithProperText(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test [[other|actualtext]] text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test actualtext text")

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
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text=r"Test {{other page}} text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test text")

    def testRemoveReferencesToOtherPagesMultiline(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test {{other\npage\n}} text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test text")

    def testRemoveReferencesToOtherPagesMultilineInTheBeginning(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="{{other\npage\n}}\n\nTest text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test text")

    def testFinalTextCleaning(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="\n\nTest     text  ")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test text")

    def testRemovalOfMultipleNestedReferencesWithFileReferenceOnTopFromText(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test [[Plik:Test reference\n[[Inner reference]] remaining part of the reference]] text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test text")

    def testRemovalOfMultipleNestedReferencesWithFileReferenceOnTopFromText2(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test [[Plik:Test reference\n[[Inner reference]]]] text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test text")

    def testRemovalOfHTMLReferences(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test <ref>other reference</ref> text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test other reference text")

    def testRemovalOfCategories(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test [[Kategoria:other category]] text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test text")

    def testRemovalOfListMarkdown(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test \n* list\n* list text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test \n list\n list text")

    def testRemovalOfEmptyPages(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text=""), wiki_parser.SingleArticle(title="Test2", text="Test text 2")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test2")
        self.assertEqual(articles[0].text, "Test text 2")

    def testRemovalBoldTextMarkdown(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test '''bold''' text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test bold text")

    def testRemovalOfItalicTextMarkdown(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test ''italic'' text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test italic text")

    def testRemovalOfTablesMarkdown(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", text="Test {|table beginning\n{|table ending|} remaining part|} text")])

        articles = wiki_parser.extractPagesFromString(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test")
        self.assertEqual(articles[0].text, "Test text")