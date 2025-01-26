import pytest
from pytest import param

from wikiparser.processors import wiki_html_processor


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        param("Test &nbsp; text", "Test text", id="Test nbsp removal"),
        param(
            "Test &lt;div&gt;other reference&lt;/div&gt; text",
            "Test other reference text",
            id="Test text unescaping",
        ),
        param(
            "Test <div>other reference</div> text",
            "Test other reference text",
            id="Test div removal",
        ),
        param(
            "Test <div style=x>other reference</div> text",
            "Test other reference text",
            id="Test div removal with style",
        ),
        param(
            "Test <div style=x/> text",
            "Test text",
            id="Test div self-closing",
        ),
        param(
            "Test <div>other reference <div>another reference</div></div> text",
            "Test other reference another reference text",
            id="Test nested div removal",
        ),
        param(
            "Test <div>other reference <div>another reference</div></div> test <br /> text",
            "Test other reference another reference test \n text",
            id="Test nested div removal with br",
        ),
        param(
            "Test <h2>other reference</h2> text",
            "Test other reference text",
            id="Test h2 removal",
        ),
        param("Test <h2 style=x/> text", "Test text", id="Test h2 self-closing"),
        param(
            "Test <span>other reference</span> text",
            "Test other reference text",
            id="Test span removal",
        ),
        param(
            "Test <ref>other reference</ref> text",
            "Test other reference text",
            id="Test ref removal",
        ),
        param(
            "Test <ref name=2>other reference</ref> text",
            "Test other reference text",
            id="Test ref removal with name",
        ),
        param("Test <ref name=2/> text", "Test text", id="Test ref self-closing"),
        param(
            "Test <gallery>other reference</gallery> text",
            "Test text",
            id="Test gallery removal",
        ),
        param(
            "Test <gallery name=2>other reference</gallery> text",
            "Test text",
            id="Test gallery removal with name",
        ),
        param(
            "Test <gallery name=2/> text",
            "Test text",
            id="Test gallery self-closing",
        ),
    ],
)
def test_wiki_html_processor(test_input: str, expected: str):
    text = wiki_html_processor.process_wiki_html(test_input)
    assert text == expected
