from dataclasses import dataclass

from hydra.core.config_store import ConfigStore

from utils.embedding_models.schema import MODEL_PROVIDER, EmbeddingModelInfo


@dataclass
class TEXT_EMBEDDING_3_SMALL(EmbeddingModelInfo):
    provider: MODEL_PROVIDER = MODEL_PROVIDER.OPEN_AI
    model_name: str = "text-embedding-3-small"
    dimension: int = 1536
    cost_per_mln_tokens: float = 0.020


@dataclass
class TEXT_EMBEDDING_3_LARGE(EmbeddingModelInfo):
    provider: MODEL_PROVIDER = MODEL_PROVIDER.OPEN_AI
    model_name: str = "text-embedding-3-large"
    dimension: int = 3072
    cost_per_mln_tokens: float = 0.130


@dataclass
class TEXT_EMBEDDING_ADA_002(EmbeddingModelInfo):
    provider: MODEL_PROVIDER = MODEL_PROVIDER.OPEN_AI
    model_name: str = "text-embedding-ada-002"
    dimension: int = 1536
    cost_per_mln_tokens: float = 0.100


def register_models_in_config_store():
    cs = ConfigStore.instance()
    cs.store(
        name=TEXT_EMBEDDING_3_SMALL.model_name, group="embedding_model", node=TEXT_EMBEDDING_3_SMALL
    )
    cs.store(
        name=TEXT_EMBEDDING_3_LARGE.model_name, group="embedding_model", node=TEXT_EMBEDDING_3_LARGE
    )
    cs.store(
        name=TEXT_EMBEDDING_ADA_002.model_name, group="embedding_model", node=TEXT_EMBEDDING_ADA_002
    )
