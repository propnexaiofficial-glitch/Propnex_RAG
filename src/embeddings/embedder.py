from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_model()
    return model.encode(texts, show_progress_bar=True, normalize_embeddings=True).tolist()


def embed_query(query: str) -> list[float]:
    model = get_model()
    return model.encode(query, normalize_embeddings=True).tolist()