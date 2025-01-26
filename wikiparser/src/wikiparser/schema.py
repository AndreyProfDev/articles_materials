from __future__ import annotations

from functools import cached_property

import pandas as pd
import yaml
from pydantic import BaseModel


class SingleSection(BaseModel):
    title: str
    content: str


class MainSection(SingleSection):
    title: str = "Main"


class SingleArticle:
    def __init__(self, title: str, sections: list[SingleSection]) -> None:
        self.title = title
        self.sections = sections

    @property
    def content(self) -> str:
        result = []
        for section in self.sections:
            if section.title == "Main":
                return section.content
            else:
                result.append(f"== {section.title} ==\n{section.content}")
        return "\n".join(result)

    @property
    def sections(self) -> list[SingleSection]:
        return self._sections

    @sections.setter
    def sections(self, sections: list[SingleSection]):
        self._sections = sections

        if hasattr(self, "section_to_content"):
            del self.section_to_content

    @cached_property
    def section_to_content(self) -> dict[str, SingleSection]:
        return {section.title: section for section in self.sections}

    def __getitem__(self, key: str) -> str:
        return self.section_to_content[key].content

    def __setitem__(self, key: str, value: str) -> None:
        self.section_to_content[key].content = value

    def __len__(self) -> int:
        return len(self.sections)

    def contains(self, key: str) -> bool:
        return key in self.section_to_content

    def __str__(self) -> str:
        return f"{self.title}: {self.content}"

    def __repr__(self) -> str:
        return self.__str__()

    def model_dump(self) -> dict[str, str | dict[str, str]]:
        return {self.title: {section.title: section.content for section in self.sections}}

    def model_dump_yaml(self) -> str:
        return yaml.dump(self.model_dump(), allow_unicode=True)


class ArticleBook:
    def __init__(self, articles: list[SingleArticle]) -> None:
        self.articles = articles

    @staticmethod
    def from_dict(article_to_content: dict[str, str | dict[str, str]]) -> ArticleBook:
        articles = []
        for title, content in article_to_content.items():
            sections: list[SingleSection] = []
            if isinstance(content, dict):
                sections = [
                    SingleSection(title=title, content=content)
                    for title, content in content.items()
                ]
            else:
                sections = [MainSection(content=content)]

            articles.append(SingleArticle(title=title, sections=sections))

        return ArticleBook(articles=articles)

    @property
    def articles(self) -> list[SingleArticle]:
        return self._articles

    @articles.setter
    def articles(self, articles: list[SingleArticle]):
        self._articles = articles

        if hasattr(self, "title_to_article"):
            del self.title_to_article

    @cached_property
    def title_to_article(self) -> dict[str, SingleArticle]:
        return {article.title: article for article in self.articles}

    def __getitem__(self, key: str) -> SingleArticle:
        return self.title_to_article[key]

    def __len__(self) -> int:
        return len(self.articles)

    def contains(self, key: str) -> bool:
        return key in self.title_to_article

    def __str__(self) -> str:
        return str(self.title_to_article)

    def __repr__(self) -> str:
        return self.__str__()

    def model_dump(self) -> dict[str, dict[str, str | dict[str, str]]]:
        return {article.title: article.model_dump() for article in self.articles}

    def model_dump_yaml(self) -> str:
        return yaml.dump(self.model_dump(), allow_unicode=True)

    def merge(self, other: ArticleBook) -> ArticleBook:
        return ArticleBook(articles=self.articles + other.articles)

    def as_df(self) -> pd.DataFrame:
        data = []
        for article in self.articles:
            for section in article.sections:
                data.append(
                    {
                        "Article Title": article.title,
                        "Section Title": section.title,
                        "Section Content": section.content,
                    }
                )
        df = pd.DataFrame(data)

        df = df.drop_duplicates(subset=["Article Title", "Section Title", "Section Content"])
        df = df.reset_index(drop=True)

        return df
