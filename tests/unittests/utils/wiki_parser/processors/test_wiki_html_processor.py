
import unittest

from utils.wiki_parser.processors import wiki_html_processor

class WikiHTMLProcessorTestCase(unittest.TestCase):

    def test_removal_of_nbsp(self):
        text = wiki_html_processor.process_wiki_html("Test &nbsp; text")
        self.assertEqual(text, "Test text")

    def testUnescapeHTML(self):
        text = wiki_html_processor.process_wiki_html('Test &lt;div&gt;other reference&lt;/div&gt; text')
        self.assertEqual(text, "Test text")

    def testRemovalOfDiv(self):
        text = wiki_html_processor.process_wiki_html("Test <div>other reference</div> text")
        self.assertEqual(text, "Test text")

        text = wiki_html_processor.process_wiki_html("Test <div style=x>other reference</div> text")
        self.assertEqual(text, "Test text")

        text = wiki_html_processor.process_wiki_html("Test <div style=x/> text")
        self.assertEqual(text, "Test text")

        text = wiki_html_processor.process_wiki_html("Test <div>other reference<div>another reference</div></div> text")
        self.assertEqual(text, "Test text")

        text = wiki_html_processor.process_wiki_html("Test <div>other reference<div>another reference</div></div> test <br /> text")
        self.assertEqual(text, "Test test \n text")

    def testRemovalOfHTMLReferences(self):
        text = wiki_html_processor.process_wiki_html("Test <ref>other reference</ref> text")
        self.assertEqual(text, "Test text")

        text = wiki_html_processor.process_wiki_html("Test <ref name=2>other reference</ref> text")
        self.assertEqual(text, "Test text")

        text = wiki_html_processor.process_wiki_html("Test <ref name=2/> text")
        self.assertEqual(text, "Test text")