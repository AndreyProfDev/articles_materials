from utils.embedding_models.schema import EmbeddingModelInfo

# Hugging Face models
ST_POLISH_PARAPHRASE_FROM_DISTILROBERTA = EmbeddingModelInfo(
    model_name="sdadas/st-polish-paraphrase-from-distilroberta",
    dimension=768,
    cost_per_mln_tokens=0.0,
)

ST_POLISH_PARAPHRASE_FROM_MPNET = EmbeddingModelInfo(
    model_name="sdadas/st-polish-paraphrase-from-mpnet",
    dimension=768,
    cost_per_mln_tokens=0.0,
)

ORB_ST_POLISH_KARTONBERTA_BASE_ALPHA_V1 = EmbeddingModelInfo(
    model_name="OrlikB/st-polish-kartonberta-base-alpha-v1",
    dimension=768,
    cost_per_mln_tokens=0.0,
)

ORB_KARTONBERT_USE = EmbeddingModelInfo(
    model_name="OrlikB/KartonBERT-USE-base-v1",
    dimension=768,
    cost_per_mln_tokens=0.0,
)

# OpenAI models
TEXT_EMBEDDING_3_SMALL = EmbeddingModelInfo(
    model_name="text-embedding-3-small", dimension=1536, cost_per_mln_tokens=0.020
)
TEXT_EMBEDDING_3_LARGE = EmbeddingModelInfo(
    model_name="text-embedding-3-large", dimension=3072, cost_per_mln_tokens=0.130
)
TEXT_EMBEDDING_ADA_002 = EmbeddingModelInfo(
    model_name="text-embedding-ada-002", dimension=1536, cost_per_mln_tokens=0.100
)
