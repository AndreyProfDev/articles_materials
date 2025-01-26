from wikiparser.schema import ArticleBook, SingleArticle


class ArticleBookWithTracking(ArticleBook):
    def __init__(self, articles: list[SingleArticle], run_id: int) -> None:
        self.run_id = run_id
        super().__init__(articles=articles)


class ArticleWithTracking(SingleArticle):
    pass
