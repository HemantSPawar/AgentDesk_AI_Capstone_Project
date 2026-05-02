import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
KB_PATH = BASE_DIR / "data" / "company_knowledge_base.json"


def load_knowledge_base():
    with open(KB_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def simple_rag_search(query, top_k=2):
    query_words = set(query.lower().split())
    docs = load_knowledge_base()
    scored = []

    for doc in docs:
        text = (doc["title"] + " " + doc["content"]).lower()
        score = sum(1 for word in query_words if word in text)
        scored.append((score, doc))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for score, doc in scored[:top_k] if score > 0] or docs[:top_k]
