def build_prompt(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join(c["text"] for c in chunks)
    return f"""You are a helpful assistant for Propnex AI Technology.
Answer the question using ONLY the context below.
Reply in the same language/style as the question (Hinglish, Hindi or English).
If the answer is not in the context, say you don't have that information
and suggest contacting the Propnex team. Never make up prices, policies or facts.

Context:
{context}

Question: {question}

Answer:"""