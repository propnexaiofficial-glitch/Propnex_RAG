from src.embeddings.embedder import embed_query
from src.vectorstore.store import search

while True:
    q = input("\nAsk (or 'exit'): ")
    if q.lower() == "exit":
        break
    results = search(embed_query(q), top_k=3)
    for r in results:
        print(f"\n[{r['source']} p{r['page']}] (distance {r['distance']:.3f})")
        print(r["text"][:600])
