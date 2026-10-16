from src.embeddings.embedder import embed_query
from src.vectorstore.store import search
from src.generation.prompts import build_prompt
from src.generation.llm import generate


def answer(question: str, top_k: int = 4) -> dict:
    chunks = search(embed_query(question), top_k=top_k)
    reply = generate(build_prompt(question, chunks))
    return {"answer": reply, "sources": chunks}