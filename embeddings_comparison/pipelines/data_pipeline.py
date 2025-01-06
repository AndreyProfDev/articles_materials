import os
import pathlib

import extraction_steps as steps
from metaflow.metaflow_current import current
from metaflow.decorators import step
from metaflow.flowspec import FlowSpec
from metaflow.parameters import Parameter
from metaflow import card
from metaflow.cards import Markdown

class WikiArticlesDataFlow(FlowSpec):

    sourceFolder = Parameter(
        "sourceFolder",
        help="Local source folder with raw files",
        default="data/0_raw files",
    )

    @card
    @step
    def start(self):
        sourceFolder = pathlib.Path(str(self.sourceFolder))

        self.data_files = [
            str(sourceFolder / filename)
            for filename in os.listdir(sourceFolder)
            if filename.endswith(".xml")
        ]

        self.next(self.extract_articles, foreach="data_files")

    @card
    @step
    def extract_articles(self):
        with open(str(self.input), "r") as file:
            wiki_xml = file.read()
            self.extracted_articles = steps.extract_text_from_wiki_xml(wiki_xml)

            for title, article in self.extracted_articles.items():
                article.run_id = current.run_id
        self.next(self.process_wiki_html)

    @card
    @step
    def process_wiki_html(self):
        self.processed_articles = steps.process_wiki_html(self.extracted_articles)
        self.next(self.process_wiki_markdown_in_pages)

    @card
    @step
    def process_wiki_markdown_in_pages(self):
        self.processed_articles = steps.process_wiki_markdown_in_pages(
            self.extracted_articles
        )
        self.next(self.split_wiki_page_by_sections)

    @card
    @step
    def split_wiki_page_by_sections(self):
        self.processed_articles = steps.split_wiki_page_by_sections(
            self.extracted_articles
        )
        self.next(self.remove_empty_articles)

    @card
    @step
    def remove_empty_articles(self):
        self.processed_articles = steps.remove_empty_articles(self.extracted_articles)
        self.next(self.join)

    @card
    @step
    def join(self, inputs):
        self.next(self.end)

    @card
    @step
    def end(self):
        pass


if __name__ == "__main__":
    WikiArticlesDataFlow()
