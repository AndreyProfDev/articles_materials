

from __future__ import annotations
from pydantic import BaseModel
from bs4 import BeautifulSoup
import re


class ArticleSection(BaseModel):
    title: str
    content: str

class SingleArticle(BaseModel):
    title: str
    sections: list[ArticleSection]
    
    def __init__(self, title: str, sections: str | list[ArticleSection]):
        if isinstance(sections, str):
            sections = [ArticleSection(title="Main", content=sections)]
        super().__init__(title=title, sections=sections)

    @property
    def content(self) -> str:

        result = []
        for section in self.sections:
            if section.title == "Main":
                return section.content
            else:
                result.append(f"== {section.title} ==\n{section.content}")
        return "\n".join(result)

def _extract_simple_wikilink_content(text: str) -> str:
        pattern = r"""
            \[\[                  # Match opening [[
            (?!                   # Negative lookahead
                (Plik|Kategoria): # Don't match if starts with Plik: or Kategoria:
            )
            (?P<content>[^\[]*?)  # Named capture group for the content
            \]\]                  # Match closing ]]
        """

        return re.sub(pattern, r"\g<content>", text, flags=re.S | re.VERBOSE)

def _extract_display_text_from_piped_wikilinks(text: str) -> str:
    pattern = r"""
        \[\[            # Match opening [[
        [^\[][^\[]*     # Match any chars except [ until
        \|              # the pipe separator |
        (?P<display>    # Named capture group for display text
            [^\[][^\[]*?  # Match any chars except [ (non-greedy)
        )
        \]\]            # Match closing ]]
    """

    return re.sub(pattern, r"\g<display>", text, flags=re.S | re.VERBOSE)

def _remove_file_and_category_links(text: str) -> str:
    pattern = r"""
        \[\[                    # Match opening [[
        (Plik|Kategoria):      # Match either Plik: or Kategoria:
        (?:                     # Start non-capturing group
            (?!\[\[)           # Negative lookahead - don't match if next chars are [[
            .                  # Match any character
        )*?                     # Repeat non-greedily
        \]\]                    # Match closing ]]
    """
    return re.sub(pattern, "", text, flags=re.S | re.VERBOSE)

def _remove_simple_tables(text: str) -> str:
    pattern = r"""
        \{\|          # Match opening {|
        [^\{]*?      # Match any chars except { (non-greedy)
        \|\}         # Match closing |}
    """
    return re.sub(pattern, "", text, flags=re.S | re.VERBOSE)

def _remove_wiki_templates(text: str) -> str:
    pattern = r"""
        \{\{        # Match opening {{
        .*?         # Match any chars (non-greedy)
        \}\}        # Match closing }}
    """
    return re.sub(pattern, "", text, flags=re.S | re.VERBOSE)

def convert_wiki_markdown_to_text(text: str) -> str:
    
    while True:
        new_text = _remove_file_and_category_links(text)
        new_text = _extract_display_text_from_piped_wikilinks(new_text)
        new_text = _extract_simple_wikilink_content(new_text)
        new_text = _remove_wiki_templates(new_text)
        new_text = re.sub(r"<ref>.*?</ref>", "", new_text, flags=re.S) # remove references to other pages
        new_text = _remove_simple_tables(new_text)
        new_text = re.sub(r" +", " ", new_text) # replace multiple spaces with single space
        new_text = re.sub(r"\n+", "\n", new_text) # replace multiple new line symbols with single new line symbol
        new_text = re.sub(r"\n\*", "\n", new_text, flags=re.S) # remove bullet points
        new_text = re.sub(r"\'\'\'", "", new_text) # remove bold text markdown
        new_text = re.sub(r"\'\'", "", new_text) # remove italic text markdown

        if new_text == text:
            text = new_text
            break
        text = new_text

    return text.strip()

def split_wiki_text_by_sections(text: str) -> list[ArticleSection]:
    pattern = r"""
        ==+         # Match opening equals signs
        \s*         # Optional whitespace
        ([^=]+?)    # Section title (capture group 1)
        \s*         # Optional whitespace
        ==+        # Match closing equals signs
        \s*        # Optional whitespace
        ((?:(?!==+)[\s\S])*) # Section content (capture group 2)
    """
    
    # Find all explicit sections
    matches = list(re.finditer(pattern, text, flags=re.VERBOSE))
    sections = []
    
    # Check for content before first section
    if matches and matches[0].start() > 0:
        main_content = text[:matches[0].start()].strip()
        if main_content:
            sections.append(ArticleSection(title="Main", content=main_content))
    
    # Add remaining sections
    for match in matches:
        title = match.group(1).strip()
        content = match.group(2).strip()
        if content:
            sections.append(ArticleSection(title=title, content=content))
    
    # If no sections found at all, treat entire text as main section
    if not sections and text.strip():
        sections.append(ArticleSection(title="Main", content=text.strip()))
        
    return sections

def extract_pages_from_mediawiki_xml(wiki_xml: str) -> list[SingleArticle]:
    soup = BeautifulSoup(wiki_xml, "xml")
    
    pages = soup.findChildren('page')
    articles = []
    for page in pages:
        title = page.title.text.strip()
        text = page.revision.findChild('text').text.strip()
        text = convert_wiki_markdown_to_text(text)
        sections = split_wiki_text_by_sections(text)
        
        if len(text) > 0:
            articles.append(SingleArticle(title=title, sections=sections))
    return articles

def extract_pages_from_file(file_path: str) -> list[SingleArticle]:
    with open(file_path, "r") as file:
        wiki_xml = file.read()
    return extract_pages_from_mediawiki_xml(wiki_xml)