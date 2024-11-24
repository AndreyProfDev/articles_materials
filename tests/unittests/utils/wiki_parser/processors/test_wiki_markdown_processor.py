

import unittest

from utils.wiki_parser.processors import wiki_markdown_processor

class MarkdownProcessorTestCase(unittest.TestCase):

    def testRemoveFileReference(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[Plik:test\ntext]] text")
        self.assertEqual(text, "Test text")

    def testRemoveSeveralFileReferences(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[Plik:test\ntext]]\n[[Plik:test\ntext]] text")
        self.assertEqual(text, "Test \n text")

    def testReplaceSeveralTextReferencesWithText(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[Plik:test\ntext]]\n[[other\ntext]] text")
        self.assertEqual(text, "Test \nother\ntext text")

    def testReplaceTextReferenceWithTextInside(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[other\ntext]] text")
        self.assertEqual(text, "Test other\ntext text")

    def testReplaceTextReferenceWithProperText(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[other|actualtext]] text")

        self.assertEqual(text, "Test actualtext text")

    def testRemoveReferencesToOtherPages(self):
        text = wiki_markdown_processor.process_wiki_markdown(r"Test {{other page}} text")

        self.assertEqual(text, "Test text")

    def testRemoveReferencesToOtherPagesMultiline(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test {{other\npage\n}} text")

        self.assertEqual(text, "Test text")

    def testRemoveReferencesToOtherPagesMultilineInTheBeginning(self):
        text = wiki_markdown_processor.process_wiki_markdown("{{other\npage\n}}\n\nTest text")
        self.assertEqual(text, "Test text")

    def testRemoveReferencesToOtherPagesNested(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test {{other\npage\n{{subpage}}}} text")

        self.assertEqual(text, "Test text")
    def testFinalTextCleaning(self):
        text = wiki_markdown_processor.process_wiki_markdown("\n\nTest     text  ")
        self.assertEqual(text, "Test text")

    def testRemovalOfMultipleNestedReferencesWithFileReferenceOnTopFromText(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[Plik:Test reference\n[[Inner reference]] remaining part of the reference]] text")
        self.assertEqual(text, "Test text")

    def testRemovalOfMultipleNestedReferencesWithFileReferenceOnTopFromText2(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[Plik:Test reference\n[[Inner reference]]]] text")
        self.assertEqual(text, "Test text")

    def testRemovalOfMultipleNestedReferencesWithFileReferenceOnTopFromText3(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[Plik:Test reference\n[[Inner reference|actual text]]]] text")
        self.assertEqual(text, "Test text")

    def testRemovalOfCategories(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[Kategoria:other category]] text")
        self.assertEqual(text, "Test text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [[kategoria:other category]] text")
        self.assertEqual(text, "Test text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [[:kategoria:other category|actual text]] text")
        self.assertEqual(text, "Test actual text text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [[:kategoria:other category]] text")
        self.assertEqual(text, "Test text")

    def testRemovalOfListMarkdown(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test \n* list\n* list text")
        self.assertEqual(text, 'Test \n- list\n- list text')

    def testRemovalBoldTextMarkdown(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test '''bold''' text")
        self.assertEqual(text, "Test bold text")

    def testRemovalOfItalicTextMarkdown(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test ''italic'' text")
        self.assertEqual(text, "Test italic text")

    def testRemovalOfTablesMarkdown(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test {|table beginning\n{|table ending|} remaining part|} text")
        self.assertEqual(text, "Test text")

    def testRemoveHTTPLinks(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [http://www.google.com] text")
        self.assertEqual(text, "Test text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [http://www.google.com google] text")
        self.assertEqual(text, "Test text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [http://www.google.com google] [http://www.google.com google] text")
        self.assertEqual(text, "Test text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [https://www.google.com google] [https://www.google.com google] text")
        self.assertEqual(text, "Test text")

    def testRemovalOfWikiComments(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test <!-- comment --> text")
        self.assertEqual(text, "Test text")

        text = wiki_markdown_processor.process_wiki_markdown("Test <!-- comment \n comment --> text")
        self.assertEqual(text, "Test text")