from pathlib import Path
from pypdf import PdfReader
from docx import Document


def load_file(path: Path) -> list[dict]:
    """Return a list of {text, source, page} dicts for one file."""
    suffix = path.suffix.lower()
    docs = []

    if suffix == ".pdf":
        reader = PdfReader(str(path))
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                docs.append({"text": text, "source": path.name, "page": i})

    elif suffix == ".txt" or suffix == ".md":
        text = path.read_text(encoding="utf-8", errors="ignore")
        docs.append({"text": text, "source": path.name, "page": 1})

    elif suffix == ".docx":
        doc = Document(str(path))
        text = "\n".join(p.text for p in doc.paragraphs)
        docs.append({"text": text, "source": path.name, "page": 1})

    return docs


def load_directory(folder: str) -> list[dict]:
    all_docs = []
    for path in Path(folder).rglob("*"):
        if path.is_file():
            all_docs.extend(load_file(path))
    return all_docs