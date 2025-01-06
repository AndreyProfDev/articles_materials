from __future__ import annotations

import copy

import wiki_sections_splitter as splitter
from bs4 import BeautifulSoup
from processors import wiki_html_processor as html
from processors import wiki_markdown_processor as markdown
from schema import SingleArticle


def extract_text_from_wiki_xml(wiki_xml: str) -> dict[str, SingleArticle]:
    soup = BeautifulSoup(wiki_xml, "lxml")

    pages = soup.findChildren("page")
    extracted_articles = {}
    for page in pages:
        title = page.title.text.strip()
        text = page.revision.findChild("text").text.strip()
        sections = {"Main": text}
        extracted_articles[title] = SingleArticle(
            title=title, subtitle_to_content=sections
        )

    return extracted_articles


def process_wiki_html(
    title_to_article: dict[str, SingleArticle]
) -> dict[str, SingleArticle]:
    title_to_article = copy.deepcopy(title_to_article)

    for article in title_to_article.values():
        article.subtitle_to_content = {
            subtitle: html.process_wiki_html(content).strip()
            for subtitle, content in article.subtitle_to_content.items()
        }
    return title_to_article


def process_wiki_markdown_in_pages(
    title_to_article: dict[str, SingleArticle],
) -> dict[str, SingleArticle]:
    title_to_article = copy.deepcopy(title_to_article)

    for article in title_to_article.values():
        article.subtitle_to_content = {
            subtitle: markdown.process_wiki_markdown(content).strip()
            for subtitle, content in article.subtitle_to_content.items()
        }
    return title_to_article


def split_wiki_page_by_sections(
    title_to_article: dict[str, SingleArticle]
) -> dict[str, SingleArticle]:
    title_to_article = copy.deepcopy(title_to_article)

    for article in title_to_article.values():
        splitted_sections = {}
        for content in article.subtitle_to_content.values():
            part = splitter.split_wiki_text_by_sections(content)
            splitted_sections.update(part)
        article.subtitle_to_content = splitted_sections

    return title_to_article


def remove_empty_articles(title_to_article: dict[str, SingleArticle]) -> dict[str, SingleArticle]:
    result = {}
    for title, article in title_to_article.items():
        article.subtitle_to_content = {
            subtitle: content
            for subtitle, content in article.subtitle_to_content.items()
            if content
        }
        if article.subtitle_to_content:
            result[title] = article
    return result
