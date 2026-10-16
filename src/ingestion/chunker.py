import re

HEADER_RE = re.compile(r"Propnex AI Technology \| Hinglish Voice Agent Q&A\s*\n\s*Page \d+")
Q_RE = re.compile(r"^Q(\d+)\.", re.MULTILINE)


def chunk_qa(docs: list[dict]) -> list[dict]:
    """One chunk per Q&A pair. Works across page breaks."""
    chunks = []
    by_source = {}
    for d in docs:
        by_source.setdefault(d["source"], []).append(d)

    for source, pages in by_source.items():
        full, page_starts = "", []
        for p in pages:
            text = HEADER_RE.sub("", p["text"]).strip()
            page_starts.append((len(full), p["page"]))
            full += text + "\n"

        def page_at(pos):
            page = page_starts[0][1]
            for start, pg in page_starts:
                if start <= pos:
                    page = pg
            return page

        matches = list(Q_RE.finditer(full))
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(full)
            text = full[m.start():end].strip()
            chunks.append({
                "text": text,
                "source": source,
                "page": page_at(m.start()),
                "chunk_id": f"{source}_q{m.group(1)}",
            })
    return chunks