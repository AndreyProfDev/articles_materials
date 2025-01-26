from wikiparser import wiki_sections_splitter


def test_split_wiki_text_by_sections():
    text = """== Section 1 ==
    Section 1 text
    == Section 2 ==
    Section 2 text
    """
    sections = wiki_sections_splitter.split_wiki_text_by_sections(text)

    assert len(sections) == 2
    assert sections[0].title == "Section 1"
    assert sections[0].content == "Section 1 text"

    assert sections[1].title == "Section 2"
    assert sections[1].content == "Section 2 text"


def test_split_wiki_text_by_sections_without_sections():
    text = """Section 1 text\nstill text
    """
    sections = wiki_sections_splitter.split_wiki_text_by_sections(text)

    assert len(sections) == 1
    assert sections[0].title == "Main"
    assert sections[0].content == "Section 1 text\nstill text"


def test_split_wiki_text_by_sections_without_first_section():
    text = """Section 1 text
    == Section 2 ==
    Section 2 text
    """
    sections = wiki_sections_splitter.split_wiki_text_by_sections(text)

    assert len(sections) == 2
    assert sections[0].title == "Main"
    assert sections[0].content == "Section 1 text"
