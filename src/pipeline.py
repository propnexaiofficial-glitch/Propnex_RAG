from src.embeddings.embedder import embed_query
from src.vectorstore.store import search
from src.generation.prompts import build_prompt
from src.generation.llm import generate


def to_roman(question: str) -> str:
    prompt = (
        "Rewrite this question in Roman Hinglish (Hindi written in English letters), "
        "as it would appear in a company FAQ. Keep company names as 'Propnex AI Technology'. "
        "Output only the rewritten question, nothing else.\n\n"
        f"Question: {question}"
    )
    try:
        return generate(prompt).strip()
    except Exception:
        return question


def answer(question: str, top_k: int = 5) -> dict:
    search_q = to_roman(question)
    chunks = search(embed_query(search_q), top_k=top_k)
    reply = generate(build_prompt(question, chunks))
    return {"answer": reply, "sources": chunks, "search_query": search_q}