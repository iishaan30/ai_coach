from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from rag.embed_store import (
    build_vector_store,
    load_vector_store,
    FAISS_PATH,
)
import os


# =========================================================
# ⭐ PRIMARY INGEST FUNCTION (used by FastAPI)
# =========================================================
def ingest_documents(file_path: str, course_id: str):
    """
    Production ingestion entrypoint.
    Safe for API usage.
    """

    print("📥 Loading documents...")
    docs = load_documents(file_path)
    for d in docs:
        d.metadata["course_id"] = course_id
    print(f"Loaded {len(docs)} base documents")

    print("✂️ Chunking...")
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks")

    # -----------------------------------------------------
    # Incremental FAISS update (IMPORTANT)
    # -----------------------------------------------------
    if os.path.exists(FAISS_PATH):
        print("📦 Updating existing vector store...")
        db = load_vector_store()
        db.add_documents(chunks)
        db.save_local(FAISS_PATH)
    else:
        print("🆕 Creating new vector store...")
        build_vector_store(chunks, FAISS_PATH)

    print("✅ Ingestion complete!")
    return len(chunks)


# =========================================================
# ⭐ OPTIONAL CLI SUPPORT (kept for manual runs)
# =========================================================
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ingestion.py <file_path>")
        sys.exit(1)

    ingest_documents(sys.argv[1])