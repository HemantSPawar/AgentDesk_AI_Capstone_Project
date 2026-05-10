import json
import math

from openai import OpenAI

from agentdesk_ai.config import settings

_kb_vector_cache = None


def load_knowledge_base() -> list[dict]:
    with open(settings.kb_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _embed_texts(texts: list[str]) -> list[list[float]]:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set for embedding retrieval.")
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.embeddings.create(model=settings.embedding_model, input=texts)
    return [item.embedding for item in response.data]


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def _load_kb_vectors(docs: list[dict]) -> list[tuple[dict, list[float]]]:
    global _kb_vector_cache
    if _kb_vector_cache is not None and len(_kb_vector_cache) == len(docs):
        return _kb_vector_cache
    corpus = [f"{doc['title']}\n{doc['content']}" for doc in docs]
    vectors = _embed_texts(corpus)
    _kb_vector_cache = list(zip(docs, vectors))
    return _kb_vector_cache


def simple_rag_search(query: str, top_k: int = 3) -> list[dict]:
    docs = load_knowledge_base()
    query_vector = _embed_texts([query])[0]
    kb_vectors = _load_kb_vectors(docs)
    scored = [(_cosine_similarity(query_vector, doc_vec), doc) for doc, doc_vec in kb_vectors]
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]

