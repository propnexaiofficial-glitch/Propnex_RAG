from src.embeddings.embedder import embed_query
from src.vectorstore.store import search
from src.generation.prompts import build_prompt
from src.generation.llm import generate


def to_roman(question: str) -> str:
    prompt = f"""Transliterate this Hindi question into Roman script (English letters), the way people type Hinglish in a FAQ.
Do NOT use Devanagari characters in the output. Remove filler words like "toh kya aap mujhe bata sakte hain"; keep only the core question.
Output only the question, nothing else.

Examples:
Input: प्रॉपनेक्स के फाउंडर कौन हैं?
Output: Propnex AI Technology ke founder kaun hain?

Input: बिजनेस प्रोसेस ऑटोमेशन क्या होता है?
Output: Business process automation kya hota hai?

Input: तो क्या आप मुझे बता सकते हैं कि वॉइस एजेंट क्या होता है?
Output: Voice agent kya hota hai?

Input: {question}
Output:"""
    try:
        out = generate(prompt).strip()
        if any("\u0900" <= ch <= "\u097F" for ch in out):
            return question
        return out
    except Exception as e:
        print("to_roman error:", e)
        return question


def answer(question: str, top_k: int = 5) -> dict:
    search_q = to_roman(question)
    chunks = search(embed_query(search_q), top_k=top_k)
    reply = generate(build_prompt(question, chunks))
    return {"answer": reply, "sources": chunks, "search_query": search_q}