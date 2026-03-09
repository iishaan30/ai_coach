from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(docs):
    """
    Split documents into semantic chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,   # ⭐ good balance for product docs
        chunk_overlap=100  # ⭐ preserves context across chunks
    )

    chunks = splitter.split_documents(docs)
    return chunks