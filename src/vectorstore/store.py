import chromadb

DB_PATH = "vector_db"
COLLECTION = "propnex_docs"


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(chunks: list[dict], embeddings: list[list[float]]):
    col = get_collection()
    col.upsert(
        ids=[c["chunk_id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        embeddings=embeddings,
        metadatas=[{"source": c["source"], "page": c["page"]} for c in chunks],
    )


def search(query_embedding: list[float], top_k: int = 4) -> list[dict]:
    col = get_collection()
    res = col.query(query_embeddings=[query_embedding], n_results=top_k)
    results = []
    for i in range(len(res["ids"][0])):
        results.append({
            "text": res["documents"][0][i],
            "source": res["metadatas"][0][i]["source"],
            "page": res["metadatas"][0][i]["page"],
            "distance": res["distances"][0][i],
        })
    return results