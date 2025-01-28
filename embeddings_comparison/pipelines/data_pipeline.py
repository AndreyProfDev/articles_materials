import os
import pathlib

from metaflow import card, current
from metaflow.decorators import step
from metaflow.flowspec import FlowSpec
from metaflow.parameters import Parameter
from metaflow.plugins.cards.card_modules.components import Markdown

import wikiparser.extraction_steps as steps
from wikiparser.schema import ArticleBook


class WikiArticlesDataFlow(FlowSpec):
    sourceFolder = Parameter(
        "sourceFolder",
        help="Local source folder with raw files",
        default="data/0_raw files",
    )
    targetFolder = Parameter(
        "targetFolder",
        help="Local target folder with processed files",
        default="data/6_processed_articles",
    )

    @step
    def start(self):
        sourceFolder = pathlib.Path(str(self.sourceFolder))

        self.data_files = [
            str(sourceFolder / filename)
            for filename in os.listdir(sourceFolder)
            if filename.endswith(".xml")
        ]

        self.next(self.extract_articles, foreach="data_files")

    @step
    def extract_articles(self):
        with open(str(self.input)) as file:
            wiki_xml = file.read()
            self.articles_book = steps.extract_text_from_wiki_xml(wiki_xml)

        self.article_to_pathspec = {
            article.title: str(current.pathspec) for article in self.articles_book.articles
        }
        self.next(self.process_wiki_html)

    @step
    def process_wiki_html(self):
        self.articles_book = steps.process_wiki_html(self.articles_book)
        self.next(self.process_wiki_markdown_in_pages)

    @step
    def process_wiki_markdown_in_pages(self):
        self.articles_book = steps.process_wiki_markdown_in_pages(self.articles_book)
        self.next(self.split_wiki_page_by_sections)

    @step
    def split_wiki_page_by_sections(self):
        self.articles_book = steps.split_wiki_page_by_sections(self.articles_book)
        self.next(self.remove_empty_articles)

    @step
    def remove_empty_articles(self):
        self.articles_book = steps.remove_empty_articles(self.articles_book)
        self.next(self.remove_irrelevant_sections)

    @step
    def remove_irrelevant_sections(self):
        self.articles_book = steps.remove_irrelevant_sections(
            self.articles_book,
            ["Linki zewnętrzne", "Zobacz też", "Bibliografia", "Przypisy"],
        )

        self.next(self.join_to_dataframe)

    @step
    def join_to_dataframe(self, inputs):
        main_book: ArticleBook = inputs[0].articles_book
        for i in inputs[1:]:
            main_book = main_book.merge(i.articles_book)

        self.final_book = main_book

        self.next(self.add_context_column)

    @card(type="blank")
    @step
    def add_context_column(self):
        final_df = self.final_book.as_df()

        final_df["Section With Context"] = (
            final_df["Article Title"]
            + "\n"
            + final_df["Section Title"]
            + "\n"
            + final_df["Section Content"]
        )
        final_df.loc[final_df["Section Title"] == "Main", "Section With Context"] = (
            final_df["Article Title"] + "\n" + final_df["Section Content"]
        )

        self.final_df = final_df

        current.card.append(Markdown("# Dataset statistics:"))
        current.card.append(Markdown(f"Number of articles: {final_df['Article Title'].nunique()}"))
        current.card.append(Markdown(f"Number of sections: {final_df.shape[0]}"))
        current.card.append(
            Markdown(f"Longest section: {final_df['Section Content'].str.len().max()} characters")
        )
        current.card.append(
            Markdown(f"Shortest section: {final_df['Section Content'].str.len().min()} characters")
        )
        current.card.append(
            Markdown(
                f"Mean section length: {int(final_df['Section Content'].str.len().mean())} characters"
            )
        )
        current.card.append(
            Markdown(
                f"Std section length: {int(final_df['Section Content'].str.len().std())} characters"
            )
        )

        # self.final_df = final_df
        self.next(self.end)

    @step
    def end(self):
        self.final_df.to_parquet(pathlib.Path(str(self.targetFolder)) / "articles.parquet")


def main():
    WikiArticlesDataFlow()


if __name__ == "__main__":
    main()
