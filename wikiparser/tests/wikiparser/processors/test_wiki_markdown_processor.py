# import unittest

# from wikiparser.processors import wiki_markdown_processor

import pytest
from pytest import param

from wikiparser.processors import wiki_markdown_processor


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        param("Test [[Plik:test\ntext]] text", "Test text", id="Test file reference removal"),
        param(
            "Test [[Plik:test\ntext]]\n[[Plik:test\ntext]] text",
            "Test \n text",
            id="Test several file references removal",
        ),
        param(
            "Test [[Plik:test\ntext]]\n[[other\ntext]] text",
            "Test \nother\ntext text",
            id="Test several text references removal",
        ),
        param(
            "Test [[other\ntext]] text", "Test other\ntext text", id="Test text reference removal"
        ),
        param(
            "Test [[other|actualtext]] text",
            "Test actualtext text",
            id="Test text reference with text inside",
        ),
        param(r"Test {{other page}} text", "Test text", id="Test other page removal"),
        param("Test {{other\npage\n}} text", "Test text", id="Test other page removal"),
        param("{{other\npage\n}}\n\nTest text", "Test text", id="Test other page removal"),
        param(
            "Test {{other\npage\n{{subpage}}}} text",
            "Test text",
            id="Test nested other page removal",
        ),
        param("\n\nTest     text  ", "Test text", id="Test final text cleaning"),
        param(
            "Test [[Plik:Test reference\n[[Inner reference]] remaining part of the reference]] text",
            "Test text",
            id="Test removal of multiple nested references with file reference on top",
        ),
        param(
            "Test [[Plik:Test reference\n[[Inner reference]]]] text",
            "Test text",
            id="Test removal of multiple nested references with file reference on top",
        ),
        param(
            "Test [[Plik:Test reference\n[[Inner reference|actual text]]]] text",
            "Test text",
            id="Test removal of multiple nested references with file reference on top",
        ),
        param("Test [[Kategoria:other category]] text", "Test text", id="Test category removal"),
        param(
            "Test [[:kategoria:other category|actual text]] text",
            "Test actual text text",
            id="Test category removal with text inside",
        ),
        param(
            "Test [[:kategoria:other category]] text",
            "Test text",
            id="Test category removal without text inside",
        ),
        param(
            "Test \n* list\n* list text",
            "Test \n- list\n- list text",
            id="Test list markdown replacement",
        ),
        param(
            "Test \n* list\n** list text",
            "Test \n- list\n-- list text",
            id="Test list/sublist markdown replacement",
        ),
        param(
            "Test \n** list\n*** list text",
            "Test \n-- list\n--- list text",
            id="Test list/sublist/sublist markdown replacement",
        ),
        param("Test '''bold''' text", "Test bold text", id="Test bold text markdown removal"),
        param("Test ''italic'' text", "Test italic text", id="Test italic text markdown removal"),
        param(
            "Test {|table beginning\n{|table ending|} remaining part|} text",
            "Test text",
            id="Test table removal",
        ),
        param("Test [http://www.google.com] text", "Test text", id="Test http link removal"),
        param(
            "Test [http://www.google.com google] text",
            "Test google text",
            id="Test http link with text removal",
        ),
        param(
            "Test [http://www.google.com google] [http://www.google.com google] text",
            "Test google google text",
            id="Test http link with text removal",
        ),
        param(
            "Test [https://www.google.com google] [https://www.google.com google] text",
            "Test google google text",
            id="Test http link with text removal",
        ),
        param("Test <!-- comment --> text", "Test text", id="Test comment removal"),
        param("Test <!-- comment \n comment --> text", "Test text", id="Test comment removal"),
        param(
            "[[File:Przyszloscludzkosci.png|thumb|język = en}}]] test", "test", id="Test file link"
        ),
        param(
            "Test <blockquote>text</blockquote> text", "Test \ntext\n text", id="Test blockquote"
        ),
        param("__NOTOC__ test text", "test text", id="Test __NOTOC__ removal"),
        param("__NOEDITSECTION__ test text", "test text", id="Test __NOEDITSECTION__ removal"),
        param(
            "__NOTOC____NOEDITSECTION__ test text",
            "test text",
            id="Test __NOTOC__ and __NOEDITSECTION__ removal",
        ),
    ],
)
def test_markdown_processor(test_input: str, expected: str):
    actual = wiki_markdown_processor.process_wiki_markdown(test_input)
    assert actual == expected
