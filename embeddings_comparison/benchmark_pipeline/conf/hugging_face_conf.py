from dataclasses import dataclass

from hydra.core.config_store import ConfigStore

from utils.embedding_models.schema import MODEL_PROVIDER, EmbeddingModelInfo


def sanitize_model_name(model_name: str) -> str:
    return model_name.replace("/", "_")


@dataclass
class ST_POLISH_PARAPHRASE_FROM_DISTILROBERTA(EmbeddingModelInfo):
    provider: MODEL_PROVIDER = MODEL_PROVIDER.HUGGING_FACE
    model_name: str = "sdadas/st-polish-paraphrase-from-distilroberta"
    dimension: int = 768
    cost_per_mln_tokens: float = 0.0


@dataclass
class ST_POLISH_PARAPHRASE_FROM_MPNET(EmbeddingModelInfo):
    provider: MODEL_PROVIDER = MODEL_PROVIDER.HUGGING_FACE
    model_name: str = "sdadas/st-polish-paraphrase-from-mpnet"
    dimension: int = 768
    cost_per_mln_tokens: float = 0.0


@dataclass
class ORB_ST_POLISH_KARTONBERTA_BASE_ALPHA_V1(EmbeddingModelInfo):
    provider: MODEL_PROVIDER = MODEL_PROVIDER.HUGGING_FACE
    model_name: str = "OrlikB/st-polish-kartonberta-base-alpha-v1"
    dimension: int = 768
    cost_per_mln_tokens: float = 0.0


@dataclass
class ORB_KARTONBERT_USE(EmbeddingModelInfo):
    provider: MODEL_PROVIDER = MODEL_PROVIDER.HUGGING_FACE
    model_name: str = "OrlikB/KartonBERT-USE-base-v1"
    dimension: int = 768
    cost_per_mln_tokens: float = 0.0


def register_models_in_config_store():
    cs = ConfigStore.instance()
    cs.store(
        name=sanitize_model_name(ST_POLISH_PARAPHRASE_FROM_DISTILROBERTA.model_name),
        group="embedding_model",
        node=ST_POLISH_PARAPHRASE_FROM_DISTILROBERTA,
    )
    cs.store(
        name=sanitize_model_name(ST_POLISH_PARAPHRASE_FROM_MPNET.model_name),
        group="embedding_model",
        node=ST_POLISH_PARAPHRASE_FROM_MPNET,
    )
    cs.store(
        name=sanitize_model_name(ORB_ST_POLISH_KARTONBERTA_BASE_ALPHA_V1.model_name),
        group="embedding_model",
        node=ORB_ST_POLISH_KARTONBERTA_BASE_ALPHA_V1,
    )
    cs.store(
        name=sanitize_model_name(ORB_KARTONBERT_USE.model_name),
        group="embedding_model",
        node=ORB_KARTONBERT_USE,
    )
