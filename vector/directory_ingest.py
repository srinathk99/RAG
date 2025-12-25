import os
from vector import chroma_store
from technique import loader
from ample_from_xsd import ingest_xsd
SUPPORTED_EXTENSIONS = {".txt", ".md"}  # extend if needed

def generate_doc_id(file_path: str) -> str:

    doc_id = file_path.replace(os.sep, "_")
    doc_id = doc_id.replace(".", "_")
    return doc_id.lower()



def ingest_directory(directory_path: str):

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

            #try:
            text=""
            print(ext)
            if ext == ".txt":
                text = loader.read_text_file(full_path)
            elif ext == ".pdf":
                text = loader.read_pdf(full_path)
            elif ext == ".xsd":
                text=ingest_xsd.ingest_xsd_file(full_path,)

            #print("Text\n"+text)
            if text != "" :
                chroma_store.ingest_document(
                    doc_id=doc_id,
                    source=relative_path,
                    text=text
                )
            else :
                print("\n Text is Empty\n")


           # except Exception as e:
               # print(f"❌ Failed to ingest {relative_path}: {e}")

    print("\n✅ Directory ingestion completed")
    return None
