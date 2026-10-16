import re


def clean_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"-\n(\w)", r"\1", text)      # fix words split across lines
    text = re.sub(r"[ \t]+", " ", text)          # collapse spaces
    text = re.sub(r"\n{3,}", "\n\n", text)       # collapse blank lines
    return text.strip()