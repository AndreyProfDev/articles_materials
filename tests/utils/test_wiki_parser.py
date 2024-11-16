from tempfile import NamedTemporaryFile
import unittest

from embeddings_comparison.utils import wiki_parser

class TestWikiMarkdownParsing(unittest.TestCase):

    def testRemoveFileReference(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test [[Plik:test\ntext]] text")
        self.assertEqual(text, "Test text")

    def testRemoveSeveralFileReferences(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test [[Plik:test\ntext]]\n[[Plik:test\ntext]] text")
        self.assertEqual(text, "Test \n text")

    def testReplaceSeveralTextReferencesWithText(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test [[Plik:test\ntext]]\n[[other\ntext]] text")
        self.assertEqual(text, "Test \nother\ntext text")

    def testReplaceTextReferenceWithTextInside(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test [[other\ntext]] text")
        self.assertEqual(text, "Test other\ntext text")

    def testReplaceTextReferenceWithProperText(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test [[other|actualtext]] text")

        self.assertEqual(text, "Test actualtext text")

    def testRemoveReferencesToOtherPages(self):
        text = wiki_parser.convert_wiki_markdown_to_text(r"Test {{other page}} text")

        self.assertEqual(text, "Test text")

    def testRemoveReferencesToOtherPagesMultiline(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test {{other\npage\n}} text")

        self.assertEqual(text, "Test text")

    def testRemoveReferencesToOtherPagesMultilineInTheBeginning(self):
        text = wiki_parser.convert_wiki_markdown_to_text("{{other\npage\n}}\n\nTest text")
        self.assertEqual(text, "Test text")

    def testFinalTextCleaning(self):
        text = wiki_parser.convert_wiki_markdown_to_text("\n\nTest     text  ")
        self.assertEqual(text, "Test text")

    def testRemovalOfMultipleNestedReferencesWithFileReferenceOnTopFromText(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test [[Plik:Test reference\n[[Inner reference]] remaining part of the reference]] text")
        self.assertEqual(text, "Test text")

    def testRemovalOfMultipleNestedReferencesWithFileReferenceOnTopFromText2(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test [[Plik:Test reference\n[[Inner reference]]]] text")
        self.assertEqual(text, "Test text")

    def testRemovalOfMultipleNestedReferencesWithFileReferenceOnTopFromText3(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test [[Plik:Test reference\n[[Inner reference|actual text]]]] text")
        self.assertEqual(text, "Test text")

    def testRemovalOfCategories(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test [[Kategoria:other category]] text")
        self.assertEqual(text, "Test text")

    def testRemovalOfListMarkdown(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test \n* list\n* list text")
        self.assertEqual(text, "Test \n list\n list text")

    def testRemovalBoldTextMarkdown(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test '''bold''' text")
        self.assertEqual(text, "Test bold text")

    def testRemovalOfItalicTextMarkdown(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test ''italic'' text")
        self.assertEqual(text, "Test italic text")

    def testRemovalOfTablesMarkdown(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test {|table beginning\n{|table ending|} remaining part|} text")
        self.assertEqual(text, "Test text")

    def testRemovalOfHTMLReferences(self):
        text = wiki_parser.convert_wiki_markdown_to_text("Test <ref>other reference</ref> text")
        self.assertEqual(text, "Test text")

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

        articles = wiki_parser.extract_pages_from_mediawiki_xml(wiki_articles_xml)

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
            articles = wiki_parser.extract_pages_from_file(file.name)

            self.assertEqual(len(articles), 2)

    def test_removal_of_empty_pages(self):
        wiki_articles_xml = self.contruct_wiki_xml([wiki_parser.SingleArticle(title="Test", sections=""), 
                                                    wiki_parser.SingleArticle(title="Test2", sections="Test text 2")])

        articles = wiki_parser.extract_pages_from_mediawiki_xml(wiki_articles_xml)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test2")
        self.assertEqual(articles[0].content, "Test text 2")

    def test_split_wiki_text_by_sections(self):
        text = """== Section 1 ==
        Section 1 text
        == Section 2 ==
        Section 2 text
        """
        sections = list(wiki_parser.split_wiki_text_by_sections(text))

        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].title, 'Section 1')
        self.assertEqual(sections[0].content, "Section 1 text")

        self.assertEqual(sections[1].title, 'Section 2')
        self.assertEqual(sections[1].content, "Section 2 text")

    def test_split_wiki_text_by_sections_without_sections(self):
        text = """Section 1 text\nstill text
        """
        sections = list(wiki_parser.split_wiki_text_by_sections(text))

        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].title, 'Main')
        self.assertEqual(sections[0].content, "Section 1 text\nstill text")

    def test_split_wiki_text_by_sections_without_first_section(self):
        text = """Section 1 text
        == Section 2 ==
        Section 2 text
        """
        sections = list(wiki_parser.split_wiki_text_by_sections(text))

        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].title, 'Main')
        self.assertEqual(sections[0].content, "Section 1 text")

        self.assertEqual(sections[1].title, 'Section 2')
        self.assertEqual(sections[1].content, "Section 2 text")

    def test_removal_of_empty_sections(self):
        text = """== Section 1 ==
        Section 1 text
        == Section 2 ==
        """
        sections = list(wiki_parser.split_wiki_text_by_sections(text))

        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].title, 'Section 1')
        self.assertEqual(sections[0].content, "Section 1 text")