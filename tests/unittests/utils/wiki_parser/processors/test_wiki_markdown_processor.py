

import unittest

from utils.wiki_parser.processors import wiki_markdown_processor

class MarkdownProcessorTestCase(unittest.TestCase):

    def test_remove_file_reference(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[Plik:test\ntext]] text")
        self.assertEqual(text, "Test text")

    def test_remove_several_file_references(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[Plik:test\ntext]]\n[[Plik:test\ntext]] text")
        self.assertEqual(text, "Test \n text")

    def test_replace_several_text_references_with_text(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[Plik:test\ntext]]\n[[other\ntext]] text")
        self.assertEqual(text, "Test \nother\ntext text")

    def test_replace_text_reference_with_text_inside(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[other\ntext]] text")
        self.assertEqual(text, "Test other\ntext text")

    def test_replace_text_reference_with_proper_text(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[other|actualtext]] text")

        self.assertEqual(text, "Test actualtext text")

    def test_remove_references_to_other_pages(self):
        text = wiki_markdown_processor.process_wiki_markdown(r"Test {{other page}} text")

        self.assertEqual(text, "Test text")

    def test_remove_references_to_other_pages_multiline(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test {{other\npage\n}} text")

        self.assertEqual(text, "Test text")

    def test_remove_references_to_other_pages_multiline_in_the_beginning(self):
        text = wiki_markdown_processor.process_wiki_markdown("{{other\npage\n}}\n\nTest text")
        self.assertEqual(text, "Test text")

    def test_remove_references_to_other_pages_nested(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test {{other\npage\n{{subpage}}}} text")

        self.assertEqual(text, "Test text")

    def test_final_text_cleaning(self):
        text = wiki_markdown_processor.process_wiki_markdown("\n\nTest     text  ")
        self.assertEqual(text, "Test text")

    def test_removal_of_multiple_nested_references_with_file_reference_on_top_from_text(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[Plik:Test reference\n[[Inner reference]] remaining part of the reference]] text")
        self.assertEqual(text, "Test text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [[Plik:Test reference\n[[Inner reference]]]] text")
        self.assertEqual(text, "Test text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [[Plik:Test reference\n[[Inner reference|actual text]]]] text")
        self.assertEqual(text, "Test text")

    def test_removal_of_categories(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [[Kategoria:other category]] text")
        self.assertEqual(text, "Test text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [[kategoria:other category]] text")
        self.assertEqual(text, "Test text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [[:kategoria:other category|actual text]] text")
        self.assertEqual(text, "Test actual text text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [[:kategoria:other category]] text")
        self.assertEqual(text, "Test text")

    def test_removal_of_list_markdown(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test \n* list\n* list text")
        self.assertEqual(text, 'Test \n- list\n- list text')

        text = wiki_markdown_processor.process_wiki_markdown("Test \n* list\n** list text")
        self.assertEqual(text, 'Test \n- list\n-- list text')

        text = wiki_markdown_processor.process_wiki_markdown("Test \n** list\n*** list text")
        self.assertEqual(text, 'Test \n-- list\n--- list text')

    def test_removal_bold_text_markdown(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test '''bold''' text")
        self.assertEqual(text, "Test bold text")

    def test_removal_of_italic_text_markdown(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test ''italic'' text")
        self.assertEqual(text, "Test italic text")

    def test_removal_of_tables_markdown(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test {|table beginning\n{|table ending|} remaining part|} text")
        self.assertEqual(text, "Test text")

    def test_remove_http_links(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test [http://www.google.com] text")
        self.assertEqual(text, "Test text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [http://www.google.com google] text")
        self.assertEqual(text, "Test google text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [http://www.google.com google] [http://www.google.com google] text")
        self.assertEqual(text, "Test google google text")

        text = wiki_markdown_processor.process_wiki_markdown("Test [https://www.google.com google] [https://www.google.com google] text")
        self.assertEqual(text, "Test google google text")

    def test_removal_of_wiki_comments(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test <!-- comment --> text")
        self.assertEqual(text, "Test text")

        text = wiki_markdown_processor.process_wiki_markdown("Test <!-- comment \n comment --> text")
        self.assertEqual(text, "Test text")

    def test_removal_of_file_link(self):
        text = wiki_markdown_processor.process_wiki_markdown("[[File:Przyszloscludzkosci.png|thumb|język = en}}]] test")
        
        self.assertEqual(text, "test")

    def test_removal_of_blockquote(self):
        text = wiki_markdown_processor.process_wiki_markdown("Test <blockquote>text</blockquote> text")
        self.assertEqual(text, "Test \ntext\n text")

    def test_removal_of_wiki_specific_prefixes(self):
        text = wiki_markdown_processor.process_wiki_markdown("__NOTOC__ test text")
        self.assertEqual(text, "test text")

        text = wiki_markdown_processor.process_wiki_markdown("__NOEDITSECTION__ test text")
        self.assertEqual(text, "test text")

        text = wiki_markdown_processor.process_wiki_markdown("__NOTOC____NOEDITSECTION__ test text")
        self.assertEqual(text, "test text")