from __future__ import annotations

from pathlib import Path

import extraction_steps as steps
import yaml
from schema import SingleArticle


def store_articles_to_yml_file(
    target_folder: Path | None,
    stage_subfolder: str | None,
    file_name: str | None,
    title_to_article: dict[str, SingleArticle],
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
            [title_to_article[article].model_dump() for article in title_to_article], file, allow_unicode=True
            )


def extract_articles_from_mediawiki_xml(
    wiki_xml: str, output_folder: Path | None = None, file_name: str | None = None
) -> dict[str, SingleArticle]:

    pages = steps.extract_text_from_wiki_xml(wiki_xml)
    store_articles_to_yml_file(
        target_folder=output_folder,
        stage_subfolder="1_extracted_pages",
        file_name=file_name,
        title_to_article=pages,
    )

    pages = steps.process_wiki_html(pages)
    store_articles_to_yml_file(
        target_folder=output_folder,
        stage_subfolder="2_processed_html_pages",
        file_name=file_name,
        title_to_article=pages,
    )

    pages = steps.process_wiki_markdown_in_pages(pages)
    store_articles_to_yml_file(
        target_folder=output_folder,
        stage_subfolder="3_processed_markdown_pages",
        file_name=file_name,
        title_to_article=pages,
    )

    articles = steps.split_wiki_page_by_sections(pages)
    store_articles_to_yml_file(
        target_folder=output_folder,
        stage_subfolder="4_split_sections",
        file_name=file_name,
        title_to_article=articles,
    )

    articles = steps.remove_empty_articles(articles)
    store_articles_to_yml_file(
        target_folder=output_folder,
        stage_subfolder="5_remove_empty_articles",
        file_name=file_name,
        title_to_article=articles,
    )
    return articles


def extract_articles_from_file(
    file_path: str, output_folder: Path | None = None
) -> dict[str, SingleArticle]:
    with open(file_path, "r") as file:
        wiki_xml = file.read()
    return extract_articles_from_mediawiki_xml(
        wiki_xml, output_folder=output_folder, file_name=Path(file_path).name
    )
