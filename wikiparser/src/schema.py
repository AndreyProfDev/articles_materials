
from pydantic import BaseModel


class ArticleSection(BaseModel):
    title: str
    content: str

class SingleArticle(BaseModel):
    title: str
    sections: list[ArticleSection]
    
    def __init__(self, title: str, sections: str | list[ArticleSection]):
        if isinstance(sections, str):
            sections = [ArticleSection(title="Main", content=sections)]
        super().__init__(title=title, sections=sections)

    @property
    def content(self) -> str:

        result = []
        for section in self.sections:
            if section.title == "Main":
                return section.content
            else:
                result.append(f"== {section.title} ==\n{section.content}")
        return "\n".join(result)