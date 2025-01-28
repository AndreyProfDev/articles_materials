import os
import pathlib
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv
from metaflow.decorators import step
from metaflow.flowspec import FlowSpec
from metaflow.parameters import Parameter
from tqdm.auto import tqdm

from utils.llm_clients.cached_client import CachedLLMClient
from utils.llm_clients.providers import supported_models
from utils.llm_clients.providers.open_ai_client import OpenAIClient
from utils.question_generation import BASE_PROMT_PL, generate_question_for_text


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i : i + n])

    return result


class WikiArticlesFeatureFlow(FlowSpec):
    sourceFolder = Parameter(
        "sourceFolder",
        help="Local source folder with parket files with articles",
        default="data/6_processed_articles",
    )

    cachePath = Parameter(
        "cachePath", help="Local folder for cache", default="cache/completion_cache"
    )

    questionGenerationPromt = Parameter(
        "questionGenerationPromt", help="Promt for question generation", default=BASE_PROMT_PL
    )

    targetFolder = Parameter(
        "targetFolder",
        help="Local target folder with processed files",
        default="data/7_enriched_articles",
    )

    batchSize = Parameter(
        "batchSize", help="Number of records to process in one batch", default=100
    )

    @step
    def start(self):
        sourceFolder = pathlib.Path(str(self.sourceFolder))

        articles = pd.read_parquet(sourceFolder / "articles.parquet")
        self.article_records = chunks(articles.to_dict(orient="records"), self.batchSize)

        self.next(self.add_questions, foreach="article_records")

    @step
    def add_questions(self):
        self.records: Iterable[dict[str, Any]] = self.input  # type: ignore

        cachePath = Path(str(self.cachePath))
        open_ai_key = os.environ["OPEN_AI_KEY"]

        openai_client = OpenAIClient(api_key=open_ai_key, model_info=supported_models.GPT_4O)
        openai_client = CachedLLMClient(client=openai_client, path_to_cache=cachePath)

        for record in tqdm(self.records):
            record["questions"] = generate_question_for_text(
                openai_client, record["Section With Context"], BASE_PROMT_PL
            ).questions

        self.next(self.join_to_dataframe)

    @step
    def join_to_dataframe(self, inputs):
        records = []
        for i in inputs:
            records.extend(i.records)
        self.final_dataframe = pd.DataFrame(records)
        self.final_dataframe.to_parquet(pathlib.Path(str(self.targetFolder)) / "articles.parquet")
        self.next(self.end)

    @step
    def end(self):
        self.final_dataframe = self.final_dataframe


def main():
    WikiArticlesFeatureFlow()


if __name__ == "__main__":
    load_dotenv()
    main()
