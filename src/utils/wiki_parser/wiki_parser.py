

from __future__ import annotations
from bs4 import BeautifulSoup
import re

from utils.wiki_parser.processors.wiki_markdown_processor import process_wiki_markdown
from utils.wiki_parser.schema import SingleArticle
from utils.wiki_parser.processors.wiki_html_processor import process_wiki_html
from utils.wiki_parser import wiki_sections_splitter

def convert_wiki_dump_to_plain_text(text: str) -> str:
    
    new_text = process_wiki_html(text)
    new_text = process_wiki_markdown(new_text)
    new_text = re.sub(r" +", " ", new_text) # replace multiple spaces with single space
    new_text = re.sub(r"\n+", "\n", new_text) # replace multiple new line symbols with single new line symbol

    return new_text.strip()

def extract_articles_from_mediawiki_xml(wiki_xml: str) -> list[SingleArticle]:
    soup = BeautifulSoup(wiki_xml, "xml")
    
    pages = soup.findChildren('page')
    articles = []
    for page in pages:
        title = page.title.text.strip()
        text = page.revision.findChild('text').text.strip()
        text = convert_wiki_dump_to_plain_text(text)
        sections = wiki_sections_splitter.split_wiki_text_by_sections(text)
        if len(sections) > 0:
            articles.append(SingleArticle(title=title, sections=sections))
    return articles

def extract_articles_from_file(file_path: str) -> list[SingleArticle]:
    with open(file_path, "r") as file:
        wiki_xml = file.read()
    return extract_articles_from_mediawiki_xml(wiki_xml)