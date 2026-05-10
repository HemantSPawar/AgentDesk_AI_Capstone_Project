import json
import math
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent
KB_PATH = BASE_DIR / "data" / "company_knowledge_base.json"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
_KB_VECTOR_CACHE = None

load_dotenv()


def load_knowledge_base():
    with open(KB_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def _embed_texts(texts):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def _cosine_similarity(vec_a, vec_b):
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _load_kb_vectors(docs):
    global _KB_VECTOR_CACHE
    if _KB_VECTOR_CACHE is not None and len(_KB_VECTOR_CACHE) == len(docs):
        return _KB_VECTOR_CACHE

    corpus = [f"{doc['title']}\n{doc['content']}" for doc in docs]
    vectors = _embed_texts(corpus)
    _KB_VECTOR_CACHE = list(zip(docs, vectors))
    return _KB_VECTOR_CACHE


def simple_rag_search(query, top_k=2):
    docs = load_knowledge_base()
    query_vector = _embed_texts([query])[0]
    kb_vectors = _load_kb_vectors(docs)
    scored = [(_cosine_similarity(query_vector, doc_vector), doc) for doc, doc_vector in kb_vectors]
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]
