import wikiparser.extraction_steps as steps
from wikiparser import wiki_parser
from wikiparser.schema import ArticleBook


def contruct_wiki_xml(book_of_articles: ArticleBook) -> str:
    page_text = "<mediawiki>\n"
    for article in book_of_articles.articles:
        page_text += f"""<page>
                            <title>{article.title}</title>
                            <revision>
                                <id>53701990</id>
                                <text bytes="7843">{article.content}</text>
                            </revision>
                        </page>"""
    return page_text + "\n</mediawiki>"


def test_extract_simple_texts_from_wiki():
    wiki_articles_xml = contruct_wiki_xml(
        book_of_articles=ArticleBook.from_dict({"Test": "Test text", "Test2": "Test text 2"})
    )

    book_of_articles = steps.extract_text_from_wiki_xml(wiki_articles_xml)

    assert len(book_of_articles) == 2
    assert book_of_articles["Test"]["Main"] == "Test text"
    assert book_of_articles["Test2"]["Main"] == "Test text 2"


def test_storing_extracted_pages_to_file(tmp_path):
    book_of_articles = ArticleBook.from_dict({"Test": "Test text", "Test2": "Test text 2"})

    wiki_parser.store_articles_to_yml_file(
        target_folder=tmp_path,
        stage_subfolder="test",
        file_name="myfile",
        book_of_articles=book_of_articles,
    )

    with open(tmp_path / "test" / "myfile.yaml") as file:
        content = file.read()
        assert content == book_of_articles.model_dump_yaml(), (
            "Content of stored article is not equal to the original one"
        )


def test_extracting_pages_from_file(tmp_path):
    wiki_articles_xml = contruct_wiki_xml(
        book_of_articles=ArticleBook.from_dict({"Test": "Test text", "Test2": "Test text 2"})
    )

    with open(tmp_path / "test.xml", "w") as file:
        file.write(wiki_articles_xml)
        file.seek(0)
        articles = wiki_parser.extract_articles_from_file(file.name)

        assert len(articles) == 2


def test_process_wiki_html():
    articles = ArticleBook.from_dict(
        {
            "Test": "Test <div>Test1 text1</div> text",
            "Test2": "Test1 <div>Test2 <div>text2</div> 3</div> text 2",
        }
    )

    processed_articles = steps.process_wiki_html(articles)

    assert len(processed_articles) == 2
    assert processed_articles["Test"]["Main"] == "Test Test1 text1 text"
    assert processed_articles["Test2"]["Main"] == "Test1 Test2 text2 3 text 2"


def test_process_wiki_markdown():
    articles = ArticleBook.from_dict(
        {
            "Test": "Test [[Kategoria:to remove]] text",
            "Test2": "Test [[Kategoria:to [[remove]]]]text 2",
        }
    )

    processed_articles = steps.process_wiki_markdown_in_pages(articles)

    assert len(processed_articles) == 2
    assert processed_articles["Test"]["Main"] == "Test text"
    assert processed_articles["Test2"]["Main"] == "Test text 2"


def test_splitting_sections():
    articles = ArticleBook.from_dict(
        {
            "Test": "Test text\n==Section 1==\nSection 1 text\n==Section 2==\nSection 2 text",
            "Test2": "Test text 2",
        }
    )

    processed_articles = steps.split_wiki_page_by_sections(articles)

    assert len(processed_articles) == 2
    assert len(processed_articles["Test"]) == 3

    assert processed_articles["Test"]["Main"] == "Test text"
    assert processed_articles["Test"]["Section 1"] == "Section 1 text"
    assert processed_articles["Test"]["Section 2"] == "Section 2 text"

    assert len(processed_articles["Test2"]) == 1
    assert processed_articles["Test2"]["Main"] == "Test text 2"


def test_removal_of_empty_pages():
    wiki_articles = ArticleBook.from_dict({"Test": "", "Test2": "Test text 2"})

    book_of_articles = steps.remove_empty_articles(wiki_articles)

    assert len(book_of_articles) == 1
    assert book_of_articles["Test2"]["Main"] == "Test text 2"


def test_storing_intermediate_files(tmp_path):
    wiki_articles_xml = contruct_wiki_xml(
        book_of_articles=ArticleBook.from_dict({"Test": "Test text", "Test2": "Test text 2"})
    )

    wiki_parser.extract_articles_from_mediawiki_xml(
        wiki_articles_xml, output_folder=tmp_path, file_name="test"
    )
    assert (tmp_path / "1_extracted_pages" / "test.yaml").exists()
    assert (tmp_path / "2_processed_html_pages" / "test.yaml").exists()
    assert (tmp_path / "3_processed_markdown_pages" / "test.yaml").exists()
    assert (tmp_path / "4_split_sections" / "test.yaml").exists()
