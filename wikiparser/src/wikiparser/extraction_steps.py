from __future__ import annotations

import copy

from bs4 import BeautifulSoup

import wikiparser.wiki_sections_splitter as splitter

from .processors import (
    wiki_html_processor as html,
    wiki_markdown_processor as markdown,
)
from .schema import ArticleBook, SingleArticle, SingleSection


def extract_text_from_wiki_xml(wiki_xml: str) -> ArticleBook:
    soup = BeautifulSoup(wiki_xml, "lxml")

    pages = soup.findChildren("page")
    extracted_articles = []
    for page in pages:
        title = page.title.text.strip()
        text = page.revision.findChild("text").text.strip()
        sections = SingleSection(title="Main", content=text)
        extracted_articles.append(SingleArticle(title=title, sections=[sections]))

    return ArticleBook(articles=extracted_articles)


def process_wiki_html(book_of_articles: ArticleBook) -> ArticleBook:
    book_of_articles = copy.deepcopy(book_of_articles)

    for article in book_of_articles.articles:
        for section in article.sections:
            section.content = html.process_wiki_html(section.content).strip()

    return book_of_articles


def process_wiki_markdown_in_pages(
    book_of_articles: ArticleBook,
) -> ArticleBook:
    book_of_articles = copy.deepcopy(book_of_articles)

    for article in book_of_articles.articles:
        for section in article.sections:
            section.content = markdown.process_wiki_markdown(section.content).strip()

    return book_of_articles


def split_wiki_page_by_sections(book_of_articles: ArticleBook) -> ArticleBook:
    book_of_articles = copy.deepcopy(book_of_articles)

    for article in book_of_articles.articles:
        splitted_sections: list[SingleSection] = []

        for section in article.sections:
            part = splitter.split_wiki_text_by_sections(section.content)
            splitted_sections.extend(part)

        article.sections = splitted_sections

    return book_of_articles


def remove_empty_articles(book_of_articles: ArticleBook) -> ArticleBook:
    book_of_articles = copy.deepcopy(book_of_articles)

    result: list[SingleArticle] = []
    for article in book_of_articles.articles:
        article.sections = [section for section in article.sections if section.content]
        if article.sections:
            result.append(article)
    return ArticleBook(articles=result)


def remove_irrelevant_sections(
    book_of_articles: ArticleBook, section_titles: list[str]
) -> ArticleBook:
    book_of_articles = copy.deepcopy(book_of_articles)

    for article in book_of_articles.articles:
        article.sections = [
            section for section in article.sections if section.title not in section_titles
        ]
    return book_of_articles
