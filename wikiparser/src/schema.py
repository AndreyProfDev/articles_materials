from pydantic import BaseModel


class SingleArticle(BaseModel):
    title: str
    subtitle_to_content: dict[str, str]
    run_id: str | None = None

    def __init__(
        self,
        title: str,
        subtitle_to_content: str | dict[str, str],
        run_id: str | None = None,
    ):
        if isinstance(subtitle_to_content, str):
            subtitle_to_content = {"Main": subtitle_to_content}

        super().__init__(
            title=title, subtitle_to_content=subtitle_to_content, run_id=run_id
        )

    @property
    def content(self) -> str:

        result = []
        for subtitle, content in self.subtitle_to_content.items():
            if subtitle == "Main":
                return content
            else:
                result.append(f"== {subtitle} ==\n{content}")
        return "\n".join(result)
