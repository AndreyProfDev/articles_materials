
from pydantic import BaseModel
from bs4 import BeautifulSoup
import re

class SingleArticle(BaseModel):
    title: str
    text: str

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

def cleanText(text: str) -> str:
    
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

def extractPagesFromString(wiki_xml: str) -> list[SingleArticle]:
    soup = BeautifulSoup(wiki_xml, "xml")
    
    pages = soup.findChildren('page')
    articles = []
    for page in pages:
        title = page.title.text.strip()
        text = page.revision.findChild('text').text.strip()
        text = cleanText(text)
        
        if len(text) > 0:
            articles.append(SingleArticle(title=title, text=text))
    return articles

def extractPagesFromFile(file_path: str) -> list[SingleArticle]:
    with open(file_path, "r") as file:
        wiki_xml = file.read()
    return extractPagesFromString(wiki_xml)