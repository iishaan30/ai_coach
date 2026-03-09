from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import os
from langchain_community.vectorstores import FAISS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAISS_PATH = os.path.join(BASE_DIR, "ingestion", "faiss_index")

def get_embeddings():
    """
    Use Ollama local embedding model.

    Why:
    - fully local
    - no SSL issues
    - free
    - good enough for POC
    """
    return OllamaEmbeddings(
        model="nomic-embed-text"
    )


def build_vector_store(chunks, save_path="faiss_index"):
    """
    Create FAISS vector store.
    """
    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    vectorstore.save_local(save_path)
    return vectorstore


def load_vector_store(save_path="faiss_index"):
    """
    Load existing FAISS index.
    """
    embeddings = get_embeddings()

    return FAISS.load_local(
        FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )