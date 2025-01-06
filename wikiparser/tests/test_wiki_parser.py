import shutil
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from tempfile import NamedTemporaryFile

import extraction_steps as steps
import wiki_parser
import yaml
from wiki_parser import SingleArticle


class TestWikiParser(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.temp_dir_path = Path(self.temp_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def dump_articles_to_yaml(self, title_to_articles: dict[str, SingleArticle]) -> str:
        buffer = StringIO()
        yaml.dump([article.model_dump() for title, article in title_to_articles.items()], buffer)
        buffer.seek(0)
        return buffer.read()

    def contruct_wiki_xml(self, articles: list[SingleArticle]) -> str:

        page_text = "<mediawiki>\n"
        for article in articles:
            page_text += f"""<page>
                                <title>{article.title}</title>
                                <revision>
                                    <id>53701990</id>
                                    <text bytes="7843">{article.content}</text>
                                </revision>
                            </page>"""

        return page_text + "\n</mediawiki>"

    def test_extract_simple_texts_from_wiki(self):
        wiki_articles_xml = self.contruct_wiki_xml(
            [
                SingleArticle(title="Test", subtitle_to_content="Test text"),
                SingleArticle(title="Test2", subtitle_to_content="Test text 2"),
            ]
        )

        articles = steps.extract_text_from_wiki_xml(wiki_articles_xml)

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles["Test"].title, "Test")
        self.assertEqual(articles["Test"].content, "Test text")
        self.assertEqual(articles["Test2"].title, "Test2")
        self.assertEqual(articles["Test2"].content, "Test text 2")

    def test_extracting_pages_from_file(self):
        wiki_articles_xml = self.contruct_wiki_xml(
            [
                SingleArticle(title="Test", subtitle_to_content="Test text"),
                SingleArticle(title="Test2", subtitle_to_content="Test text 2"),
            ]
        )

        with NamedTemporaryFile() as file:
            file.write(wiki_articles_xml.encode("utf-8"))
            file.seek(0)
            articles = wiki_parser.extract_articles_from_file(file.name)

            self.assertEqual(len(articles), 2)

    def test_storing_extracted_pages_to_file(self):
        articles = {
            "Test": SingleArticle(title="Test", subtitle_to_content="Test text"),
            "Test2": SingleArticle(title="Test2", subtitle_to_content="Test text 2"),
        }

        wiki_parser.store_articles_to_yml_file(
            target_folder=self.temp_dir_path,
            stage_subfolder="test",
            file_name="myfile",
            title_to_article=articles,
        )

        with open(self.temp_dir_path / "test" / "myfile.yaml", "r") as file:
            content = file.read()
            self.assertEqual(content, self.dump_articles_to_yaml(articles))

    def test_process_wiki_html(self):
        articles = {
            "Test": SingleArticle(
                title="Test", subtitle_to_content="Test <div>Test1 text1</div> text"
            ),
            "Test2": SingleArticle(
                title="Test2",
                subtitle_to_content="Test1 <div>Test2 <div>text2</div> 3</div> text 2",
            ),
        }

        processed_articles = steps.process_wiki_html(articles)

        self.assertEqual(len(processed_articles), 2)
        self.assertEqual(processed_articles["Test"].title, "Test")
        self.assertEqual(processed_articles["Test"].content, "Test Test1 text1 text")
        self.assertEqual(processed_articles["Test2"].title, "Test2")
        self.assertEqual(processed_articles["Test2"].content, "Test1 Test2 text2 3 text 2")

    def test_process_wiki_markdown(self):
        articles = {
            "Test": SingleArticle(
                title="Test", subtitle_to_content="Test [[Kategoria:to remove]] text"
            ),
            "Test2": SingleArticle(
                title="Test2",
                subtitle_to_content="Test [[Kategoria:to [[remove]]]]text 2",
            ),
        }

        processed_articles = steps.process_wiki_markdown_in_pages(articles)

        self.assertEqual(len(processed_articles), 2)
        self.assertEqual(processed_articles["Test"].title, "Test")
        self.assertEqual(processed_articles["Test"].content, "Test text")
        self.assertEqual(processed_articles["Test2"].title, "Test2")
        self.assertEqual(processed_articles["Test2"].content, "Test text 2")

    def test_splitting_sections(self):
        articles = {
            "Test": SingleArticle(
                title="Test",
                subtitle_to_content="Test text\n==Section 1==\nSection 1 text\n==Section 2==\nSection 2 text",
            ),
            "Test2": SingleArticle(title="Test2", subtitle_to_content="Test text 2"),
        }

        processed_articles = steps.split_wiki_page_by_sections(articles)

        self.assertEqual(len(processed_articles), 2)
        self.assertEqual(processed_articles["Test"].title, "Test")
        self.assertEqual(len(processed_articles["Test"].subtitle_to_content), 3)
        self.assertEqual(processed_articles["Test"].subtitle_to_content["Main"], "Test text")
        self.assertEqual(
            processed_articles["Test"].subtitle_to_content["Section 1"], "Section 1 text"
        )
        self.assertEqual(
            processed_articles["Test"].subtitle_to_content["Section 2"], "Section 2 text"
        )
        self.assertEqual(processed_articles["Test2"].title, "Test2")
        self.assertEqual(len(processed_articles["Test2"].subtitle_to_content), 1)
        self.assertEqual(
            processed_articles["Test2"].subtitle_to_content["Main"], "Test text 2"
        )

    def test_removal_of_empty_pages(self):
        wiki_articles = {
            "Test": SingleArticle(title="Test", subtitle_to_content=""),
            "Test2": SingleArticle(title="Test2", subtitle_to_content="Test text 2"),
        }

        articles = steps.remove_empty_articles(wiki_articles)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles["Test2"].title, "Test2")
        self.assertEqual(articles["Test2"].content, "Test text 2")

    def test_storing_intermediate_files(self):
        wiki_articles_xml = self.contruct_wiki_xml(
            [
                wiki_parser.SingleArticle(
                    title="Test", subtitle_to_content="Test text"
                ),
                wiki_parser.SingleArticle(
                    title="Test2", subtitle_to_content="Test text 2"
                ),
            ]
        )

        temp_dir = tempfile.mkdtemp()
        temp_dir_path = Path(temp_dir)
        try:
            wiki_parser.extract_articles_from_mediawiki_xml(
                wiki_articles_xml, output_folder=temp_dir_path, file_name="test"
            )
            self.assertTrue(
                (temp_dir_path / "1_extracted_pages" / "test.yaml").exists()
            )
            self.assertTrue(
                (temp_dir_path / "2_processed_html_pages" / "test.yaml").exists()
            )
            self.assertTrue(
                (temp_dir_path / "3_processed_markdown_pages" / "test.yaml").exists()
            )
            self.assertTrue((temp_dir_path / "4_split_sections" / "test.yaml").exists())
        finally:
            shutil.rmtree(temp_dir)
