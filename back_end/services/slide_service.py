from rag.embed_store import load_vector_store


def get_slide_content(course_id: str, slide_num: int, k: int = 6):
    """
    Retrieve slide-aware content filtered by course.
    """

    db = load_vector_store()

    docs = db.similarity_search(
        f"slide {slide_num} page {slide_num}",
        k=k,
    )

    # ✅ course filter (IMPORTANT)
    filtered = [
        d for d in docs
        if d.metadata.get("course_id") == course_id
    ]

    if not filtered:
        return None

    content = "\n\n".join(d.page_content for d in filtered)

    return {
        "course_id": course_id,
        "slide": slide_num,
        "content": content,
        "chunks_used": len(filtered),
    }