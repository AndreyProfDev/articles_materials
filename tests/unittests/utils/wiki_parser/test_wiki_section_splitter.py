

import unittest

from utils.wiki_parser import wiki_sections_splitter

class WikiSectionSplitterTestCase(unittest.TestCase):

    def test_split_wiki_text_by_sections(self):
        text = """== Section 1 ==
        Section 1 text
        == Section 2 ==
        Section 2 text
        """
        sections = list(wiki_sections_splitter.split_wiki_text_by_sections(text))

        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].title, 'Section 1')
        self.assertEqual(sections[0].content, "Section 1 text")

        self.assertEqual(sections[1].title, 'Section 2')
        self.assertEqual(sections[1].content, "Section 2 text")

    def test_split_wiki_text_by_sections_without_sections(self):
        text = """Section 1 text\nstill text
        """
        sections = list(wiki_sections_splitter.split_wiki_text_by_sections(text))

        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].title, 'Main')
        self.assertEqual(sections[0].content, "Section 1 text\nstill text")

    def test_split_wiki_text_by_sections_without_first_section(self):
        text = """Section 1 text
        == Section 2 ==
        Section 2 text
        """
        sections = list(wiki_sections_splitter.split_wiki_text_by_sections(text))

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
        sections = list(wiki_sections_splitter.split_wiki_text_by_sections(text))

        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].title, 'Section 1')
        self.assertEqual(sections[0].content, "Section 1 text")