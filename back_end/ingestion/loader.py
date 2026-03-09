from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredPowerPointLoader,
    TextLoader,
)
from pathlib import Path


def load_pdf(file_path: str):
    """Load PDF page by page."""
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # ⭐ enrich metadata (VERY IMPORTANT for coach explanations)
    for i, d in enumerate(docs):
        d.metadata["type"] = "pdf"
        d.metadata["page"] = i + 1

    return docs


def load_ppt(file_path: str):
    """Load PPT/PPTX slide by slide."""
    loader = UnstructuredPowerPointLoader(file_path)
    docs = loader.load()

    # ⭐ add slide metadata
    for i, d in enumerate(docs):
        d.metadata["type"] = "ppt"
        d.metadata["slide"] = i + 1

    return docs


def load_txt(file_path: str):
    """Load transcript or text file."""
    loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()

    for d in docs:
        d.metadata["type"] = "txt"

    return docs


def load_documents(file_path: str):
    """Auto-detect file type."""
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        return load_pdf(file_path)
    elif suffix in [".ppt", ".pptx"]:
        return load_ppt(file_path)
    elif suffix == ".txt":
        return load_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")