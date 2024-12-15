from __future__ import annotations

import copy
from pathlib import Path

import yaml
from bs4 import BeautifulSoup

from utils.wiki_parser import wiki_sections_splitter
from utils.wiki_parser.processors import wiki_html_processor, wiki_markdown_processor
from utils.wiki_parser.schema import ArticleSection, SingleArticle


def extract_text_from_wiki_xml(wiki_xml: str) -> list[SingleArticle]:
    soup = BeautifulSoup(wiki_xml, "xml")

    pages = soup.findChildren("page")
    extracted_articles = []
    for page in pages:
        title = page.title.text.strip()
        text = page.revision.findChild("text").text.strip()
        sections = [ArticleSection(title="Main", content=text)]
        extracted_articles.append(SingleArticle(title=title, sections=sections))

    return extracted_articles


def store_articles_to_yml_file(
    target_folder: Path | None,
    stage_subfolder: str | None,
    file_name: str | None,
    content: list[SingleArticle],
) -> None:
    if (
        target_folder is not None
        and stage_subfolder is not None
        and file_name is not None
    ):
        target_folder = target_folder / stage_subfolder
        file_name = f"{Path(file_name).stem}.yaml"
        target_folder.mkdir(parents=True, exist_ok=True)
        with open(target_folder / file_name, "w") as file:
            yaml.dump(
                [article.model_dump() for article in content], file, allow_unicode=True
            )


def process_wiki_html(articles: list[SingleArticle]) -> list[SingleArticle]:
    articles = copy.deepcopy(articles)

    for article in articles:
        for section in article.sections:
            section.content = wiki_html_processor.process_wiki_html(section.content)
            section.content = section.content.strip()
    return articles


def process_wiki_markdown_in_pages(
    articles: list[SingleArticle],
) -> list[SingleArticle]:
    articles = copy.deepcopy(articles)

    for article in articles:
        for section in article.sections:
            section.content = wiki_markdown_processor.process_wiki_markdown(
                section.content
            )
            section.content = section.content.strip()
    return articles


def split_wiki_page_by_sections(articles: list[SingleArticle]) -> list[SingleArticle]:
    articles = copy.deepcopy(articles)

    for article in articles:
        splitted_sections = []
        for section in article.sections:
            splitted_sections.extend(
                wiki_sections_splitter.split_wiki_text_by_sections(section.content)
            )
        article.sections = splitted_sections

    return articles


def remove_empty_articles(articles: list[SingleArticle]) -> list[SingleArticle]:
    result = []
    for article in articles:
        article.sections = [section for section in article.sections if section.content]
        if article.sections:
            result.append(article)
    return result


def extract_articles_from_mediawiki_xml(
    wiki_xml: str, output_folder: Path | None = None, file_name: str | None = None
) -> list[SingleArticle]:

    pages = extract_text_from_wiki_xml(wiki_xml)
    store_articles_to_yml_file(
        target_folder=output_folder,
        stage_subfolder="1_extracted_pages",
        file_name=file_name,
        content=pages,
    )

    pages = process_wiki_html(pages)
    store_articles_to_yml_file(
        target_folder=output_folder,
        stage_subfolder="2_processed_html_pages",
        file_name=file_name,
        content=pages,
    )

    pages = process_wiki_markdown_in_pages(pages)
    store_articles_to_yml_file(
        target_folder=output_folder,
        stage_subfolder="3_processed_markdown_pages",
        file_name=file_name,
        content=pages,
    )

    articles = split_wiki_page_by_sections(pages)
    store_articles_to_yml_file(
        target_folder=output_folder,
        stage_subfolder="4_split_sections",
        file_name=file_name,
        content=articles,
    )

    articles = remove_empty_articles(articles)
    store_articles_to_yml_file(
        target_folder=output_folder,
        stage_subfolder="5_remove_empty_articles",
        file_name=file_name,
        content=articles,
    )
    return articles


def extract_articles_from_file(
    file_path: str, output_folder: Path | None = None
) -> list[SingleArticle]:
    with open(file_path, "r") as file:
        wiki_xml = file.read()
    return extract_articles_from_mediawiki_xml(
        wiki_xml, output_folder=output_folder, file_name=Path(file_path).name
    )
