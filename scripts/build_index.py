from src.ingestion.loaders import load_directory
from src.ingestion.cleaner import clean_text
from src.ingestion.chunker import chunk_documents
from src.embeddings.embedder import embed_texts
from src.vectorstore.store import add_chunks

docs = load_directory("data/raw")
for d in docs:
    d["text"] = clean_text(d["text"])

chunks = chunk_documents(docs)
print(f"{len(chunks)} chunks created")

embeddings = embed_texts([c["text"] for c in chunks])
add_chunks(chunks, embeddings)
print("Index built and saved to vector_db/")