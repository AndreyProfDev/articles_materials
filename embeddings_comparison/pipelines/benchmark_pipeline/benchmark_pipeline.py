# import os
# import time
# from collections import deque

import os
import time

from metaflow import Config
from metaflow.client.core import Flow
from metaflow.decorators import step
from metaflow.flowspec import FlowSpec

from utils.embedding_models.monitoring import EmbeddingModelWithMonitoring
from utils.embedding_models.schema import MODEL_PROVIDER, EmbeddingModelInfo
from utils.providers import hugging_face, open_ai

# from utils.vectordb.vectordb import VectorIndex


def get_model_provider(
    provider: MODEL_PROVIDER, config: EmbeddingModelInfo, open_ai_key: str
) -> EmbeddingModelWithMonitoring:
    if provider == MODEL_PROVIDER.HUGGING_FACE:
        return hugging_face.init_model(model_info=config)
    elif provider == MODEL_PROVIDER.OPEN_AI:
        return open_ai.init_model(
            api_key=open_ai_key,
            model_info=config,
            #    path_to_cache=path_to_cache
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")


class WikiArticlesDataFlow(FlowSpec):
    config = Config("config", default_value="")

    # sourceFolder = Parameter(
    #     "sourceFolder",
    #     help="Local source folder with raw files",
    #     default="data/0_raw files",
    # )
    # targetFolder = Parameter(
    #     "targetFolder",
    #     help="Local target folder with processed files",
    #     default="data/6_processed_articles",
    # )

    @step
    def start(self):
        # Load data
        self.data = Flow("WikiArticlesFeatureFlow").latest_run.data.final_dataframe
        records = self.data.to_dict(orient="records")

        self.chunks = [records]
        if "batch_size" in self.config:
            batch_size: int = self.config["batch_size"]  # type: ignore
            self.chunks = [records[i : i + batch_size] for i in range(0, len(records), batch_size)]

        self.next(self.embed_articles, foreach="chunks")

    @step
    def embed_articles(self):
        config = EmbeddingModelInfo(**self.config["embedding_model"])  # type: ignore

        open_ai_key = os.environ["OPEN_AI_KEY"]

        t = time.process_time()
        self.model = get_model_provider(config.provider, config, open_ai_key)
        self.model_initialisation_time = time.process_time() - t

        t = time.process_time()
        for record in self.input:
            record["embeddings"] = self.model.embed([record["Section With Context"]])
            record["question_embeddings"] = []
            for question in record["questions"]:
                record["question_embeddings"].append(self.model.embed([question]))
        self.embedding_time = time.process_time() - t

        self.records = self.input

        self.next(self.join)

    # @step
    # def perform_test(self, inputs):
    #     config = EmbeddingModelInfo(**self.config["embedding_model"])  # type: ignore

    #     average_model_initialisation_time = 0
    #     total_embedding_time = 0

    #     vector_index = VectorIndex(config)
    #     records = deque()

    #     for input in inputs:
    #         average_model_initialisation_time += input.model_initialisation_time
    #         total_embedding_time += input.embedding_time

    #         for record in input.records:
    #             records.append(record)
    #             vector_index.insert_text(record["text"], record["embeddings"])

    #     for record in records:
    #         record["answers"] = []
    #         for question_embedding in record["question_embeddings"]:
    #             record["answers"].append(vector_index.find_text(question_embedding, 1))

    #     self.records = records

    #     self.average_model_initialisation_time = average_model_initialisation_time
    #     self.total_embedding_time = total_embedding_time

    #     self.next(self.end)

    @step
    def join(self, inputs):
        self.next(self.end)

    @step
    def end(self):
        # Evaluation
        pass


if __name__ == "__main__":
    WikiArticlesDataFlow()
