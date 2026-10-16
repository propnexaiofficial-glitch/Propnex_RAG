import chromadb
from src.ingestion.loaders import load_directory
from src.ingestion.cleaner import clean_text
from src.ingestion.chunker import chunk_qa
from src.embeddings.embedder import embed_texts
from src.vectorstore.store import add_chunks, DB_PATH, COLLECTION

# wipe the old index
client = chromadb.PersistentClient(path=DB_PATH)
try:
    client.delete_collection(COLLECTION)
except Exception:
    pass

docs = load_directory("data/raw")
for d in docs:
    d["text"] = clean_text(d["text"])

chunks = chunk_qa(docs)
print(f"{len(chunks)} chunks created")   # should be about 150
print(chunks[0]["text"][:300])

embeddings = embed_texts([c["text"] for c in chunks])
add_chunks(chunks, embeddings)
print("Index rebuilt.")