
import unittest

from utils.wiki_parser.processors import wiki_html_processor

class WikiHTMLProcessorTestCase(unittest.TestCase):

    def test_removal_of_nbsp(self):
        text = wiki_html_processor.process_wiki_html("Test &nbsp; text")
        self.assertEqual(text, "Test text")

    def test_unescape_html(self):
        text = wiki_html_processor.process_wiki_html('Test &lt;div&gt;other reference&lt;/div&gt; text')
        self.assertEqual(text, "Test other reference text")

    def test_removal_of_div(self):
        text = wiki_html_processor.process_wiki_html("Test <div>other reference</div> text")
        self.assertEqual(text, "Test other reference text")

        text = wiki_html_processor.process_wiki_html("Test <div style=x>other reference</div> text")
        self.assertEqual(text, "Test other reference text")

        text = wiki_html_processor.process_wiki_html("Test <div style=x/> text")
        self.assertEqual(text, "Test text")

        text = wiki_html_processor.process_wiki_html("Test <div>other reference <div>another reference</div></div> text")
        self.assertEqual(text, "Test other reference another reference text")

        text = wiki_html_processor.process_wiki_html("Test <div>other reference <div>another reference</div></div> test <br /> text")
        self.assertEqual(text, "Test other reference another reference test \n text")

    def test_removal_of_h2(self):
        text = wiki_html_processor.process_wiki_html("Test <h2>other reference</h2> text")
        self.assertEqual(text, "Test other reference text")

        text = wiki_html_processor.process_wiki_html("Test <h2 style=x/> text")
        self.assertEqual(text, "Test text")

    def test_removal_of_span(self):
        text = wiki_html_processor.process_wiki_html("Test <span>other reference</span> text")
        self.assertEqual(text, "Test other reference text")

    def test_removal_of_html_references(self):
        text = wiki_html_processor.process_wiki_html("Test <ref>other reference</ref> text")
        self.assertEqual(text, "Test other reference text")

        text = wiki_html_processor.process_wiki_html("Test <ref name=2>other reference</ref> text")
        self.assertEqual(text, "Test other reference text")

        text = wiki_html_processor.process_wiki_html("Test <ref name=2/> text")
        self.assertEqual(text, "Test text")

    def test_removal_of_galleries(self):
        text = wiki_html_processor.process_wiki_html("Test <gallery>other reference</gallery> text")
        self.assertEqual(text, "Test text")

        text = wiki_html_processor.process_wiki_html("Test <gallery name=2>other reference</gallery> text")
        self.assertEqual(text, "Test text")

        text = wiki_html_processor.process_wiki_html("Test <gallery name=2/> text")
        self.assertEqual(text, "Test text")