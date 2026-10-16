import json
from pathlib import Path
from src.ingestion.loaders import load_directory
from src.ingestion.cleaner import clean_text
from src.ingestion.chunker import chunk_documents

docs = load_directory("data/raw")
for d in docs:
    d["text"] = clean_text(d["text"])

chunks = chunk_documents(docs)
print(f"Loaded {len(docs)} pages -> {len(chunks)} chunks")
print("\nSample chunk:\n", chunks[0]["text"][:300])

Path("data/processed").mkdir(parents=True, exist_ok=True)
with open("data/processed/chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)