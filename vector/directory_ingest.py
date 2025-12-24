import os
from vector import chroma_store


SUPPORTED_EXTENSIONS = {".txt", ".md"}  # extend if needed

import pdfplumber

def read_pdf(path: str) -> str:
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)


def generate_doc_id(file_path: str) -> str:
    """
    Generate a stable doc_id from relative file path
    """
    doc_id = file_path.replace(os.sep, "_")
    doc_id = doc_id.replace(".", "_")
    return doc_id.lower()


def read_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

import xmlschema

def parse_xsd(xsd_path: str):
    schema = xmlschema.XMLSchema(xsd_path)

    elements = []
    complex_types = []
    simple_types = []

    # Global elements
    for e in schema.elements.values():
        elements.append({
            "kind": "element",
            "name": e.name,
            "type": str(e.type.name),
            "namespace": e.target_namespace,
            "doc": e.annotation.documentation if e.annotation else ""
        })

    # Types
    for t in schema.types.values():
        if t.is_complex():
            children = []
            if t.content:
                for c in t.content.iter_elements():
                    children.append({
                        "name": c.name,
                        "type": str(c.type.name),
                        "min": c.min_occurs,
                        "max": c.max_occurs
                    })

            complex_types.append({
                "kind": "complexType",
                "name": t.name,
                "children": children
            })
        else:
            simple_types.append({
                "kind": "simpleType",
                "name": t.name,
                "base": str(t.base_type.name),
                "facets": list(t.facets.keys())
            })

    return elements, complex_types, simple_types

def ingest_directory(directory_path: str):
    """
    Scan directory and ingest all supported files
    """

    if not os.path.isdir(directory_path):
        raise ValueError(f"{directory_path} is not a directory")

    print(f"📂 Scanning directory: {directory_path}")

    for root, _, files in os.walk(directory_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            full_path = os.path.join(root, file)

            # Create stable ID relative to base folder
            relative_path = os.path.relpath(full_path, directory_path)
            doc_id = generate_doc_id(relative_path)

            print(f"\n📄 Processing file: {relative_path}")
            print(f"🆔 doc_id: {doc_id}")

            try:
                text=""
                print(ext)
                if ext == ".txt":
                    text = read_text_file(full_path)
                elif ext == ".pdf":
                    text = read_pdf(full_path)
                elif ext == ".xsd":

                print("Text\n"+text)
                if text != "" :
                    chroma_store.ingest_document(
                        doc_id=doc_id,
                        source=relative_path,
                        text=text
                    )
                else :
                    print("\n Text is Empty\n")


            except Exception as e:
                print(f"❌ Failed to ingest {relative_path}: {e}")

    print("\n✅ Directory ingestion completed")
    return None
