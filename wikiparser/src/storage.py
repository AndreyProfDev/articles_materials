import pandas as pd
from wiki_parser import SingleArticle


class ArticleStorage:

    def __init__(self):
        self.records = []

    def save_articles(self, articles: list[SingleArticle]):
        for article in articles:
            for subtitle, content in article.subtitle_to_content.items():
                record = {}
                record["Article Title"] = article.title
                record["Section Title"] = subtitle
                record["Section Content"] = content

                self.records.append(record)

    def load_all(self) -> pd.DataFrame:
        return pd.DataFrame(self.records)

    def __len__(self):
        return len(self.records)
