
from utils.wiki_parser.wiki_parser import SingleArticle
import pandas as pd

class ArticleStorage:

    def __init__(self):
        self.records = []
    
    def save_articles(self, articles: list[SingleArticle]):
        for article in articles:
            for section in article.sections:
                record = {}
                record['Article Title'] = article.title
                record['Section Title'] = section.title
                record['Section Content'] = section.content

                self.records.append(record)
    
    def load_all(self) -> pd.DataFrame:
        return pd.DataFrame(self.records)

    def __len__(self):
        return len(self.records)