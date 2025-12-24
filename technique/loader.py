import os

def load_document_as_string(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Document not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()

