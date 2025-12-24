import hashlib
from datetime import datetime
import chromadb
from chromadb.config import Settings
import os

from technique import chunker, embedder

# ==========================================================
# Chroma Initialization
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.join(BASE_DIR, "chroma_store")
#PERSIST_DIR = "./chroma_store"
REGISTRY_COLLECTION = "document_registry"
CHUNKS_COLLECTION = "document_chunks"



client = chromadb.PersistentClient(
    path=PERSIST_DIR,
    settings=Settings(
        anonymized_telemetry=False
    )
)

def get_registry_collection():
    return client.get_or_create_collection(name=REGISTRY_COLLECTION)


def get_chunks_collection():
    return client.get_or_create_collection(name=CHUNKS_COLLECTION)

def get_schema_collection():
    return client.get_or_create_collection("xsd_schema")


# ==========================================================
# Utilities
# ==========================================================

def _content_hash(text: str) -> str:
    """Compute stable hash for document content"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def print_registry_collection():
    registry = get_registry_collection()

    data = registry.get()

    print("\n📚 Document Registry Contents:\n")

    for i in range(len(data["ids"])):
        print(f"🆔 doc_id      : {data['ids'][i]}")
        print(f"📄 metadata    : {data['metadatas'][i]}")
        print("-" * 50)

# ==========================================================
# INGEST OPERATION (SAFE & VERSIONED)
# ==========================================================

def ingest_document(doc_id: str, source: str, text: str):
    """
    Ingest a document safely:
    - Skip if unchanged
    - Delete old chunks if changed
    - Reinsert fresh chunks
    """

    registry = get_registry_collection()
    chunks_collection = get_chunks_collection()

    new_hash = _content_hash(text)
    now = datetime.utcnow().isoformat()

    print("PERSIST_DIR\n"+PERSIST_DIR)

    # ------------------------------------------------------
    # 1️⃣ Check registry
    # ------------------------------------------------------
    existing = registry.get(
        where={"content_hash": new_hash}
    )
    print_registry_collection();

    if existing["ids"]:
        old_meta = existing["metadatas"][0]
        old_hash = old_meta["content_hash"]
        old_version = old_meta["version"]

        if old_hash == new_hash:
            print("⏭️ Document unchanged. Skipping ingestion.")
            return

        print("🔄 Document changed. Re-indexing...")
        chunks_collection.delete(where={"doc_id": doc_id})
        version = old_version + 1
    else:
        print("🆕 New document detected.")
        version = 1

    # ------------------------------------------------------
    # 2️⃣ Chunk & Embed
    # ------------------------------------------------------
    chunks = chunker.chunk_text(text)
    embeddings = embedder.embed_texts(chunks)
    print("chunk and embed done\n")
    # ------------------------------------------------------
    # 3️⃣ Generate IDs & Metadata
    # ------------------------------------------------------
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]

    metadatas = [
        {
            "doc_id": doc_id,
            "version": version
        }
        for _ in chunks
    ]

    print("id and metadata finish")

    # ------------------------------------------------------
    # 4️⃣ Insert into vector DB
    # ------------------------------------------------------
    chunks_collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    print("added\n")

    # ------------------------------------------------------
    # 5️⃣ Update registry
    # ------------------------------------------------------
    registry.upsert(
        ids=[doc_id],
        documents=["__registry__"],  # 👈 dummy document
        metadatas=[{
            "source": source,
            "content_hash": new_hash,
            "version": version,
            "updated_at": now
        }]
    )
    print("added\n")
    print_registry_collection();



    print(f"✅ Inserted {len(chunks)} chunks (version {version}) into Chroma DB")


# ==========================================================
# RETRIEVE OPERATION
# ==========================================================

def retrieve_context(question: str, top_k: int = 3) -> str:
    """
    Retrieve relevant chunks for a user question
    """

    chunks_collection = get_chunks_collection()

    q_embedding = embedder.embed_texts([question])[0]

    results = chunks_collection.query(
        query_embeddings=[q_embedding],
        n_results=top_k
    )

    return "\n".join(results["documents"][0])


# ==========================================================
# DELETE DOCUMENT
# ==========================================================

def delete_document(doc_id: str):
    """
    Completely remove a document (registry + chunks)
    """
    registry = get_registry_collection()
    chunks_collection = get_chunks_collection()

    registry.delete(ids=[doc_id])
    chunks_collection.delete(where={"doc_id": doc_id})

    print(f"🗑️ Deleted document '{doc_id}'")
