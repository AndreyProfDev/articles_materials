from wikiparser.extraction_steps import remove_irrelevant_sections
from wikiparser.schema import ArticleBook


def test_removal_of_irrelevant_sections():
    book_of_articles = ArticleBook.from_dict(
        {
            "Article 1": {"Section 1": "Content 1", "Section 2": "Content 2"},
            "Article 2": {"Section 1": "Content 1", "Section 3": "Content 2"},
        }
    )

    result = remove_irrelevant_sections(book_of_articles, ["Section 1", "Section 2"])

    assert len(result) == 2
    assert len(result["Article 1"]) == 0
    assert len(result["Article 2"]) == 1
    assert result["Article 2"]["Section 3"] == "Content 2"
