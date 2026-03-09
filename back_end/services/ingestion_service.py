import os
from storage.file_store import save_upload
from ingestion.ingestion import ingest_documents


UPLOAD_DIR = "uploaded_content"


async def process_uploaded_content(
    course_id: str,
    content_file,
    transcript_file=None,
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # -----------------------------
    # Save main file
    # -----------------------------
    content_path = save_upload(content_file, UPLOAD_DIR)

    transcript_path = None
    if transcript_file:
        transcript_path = save_upload(transcript_file, UPLOAD_DIR)

    # -----------------------------
    # TODO: detect file type
    # -----------------------------
    # For now assume PDF pipeline
    ingest_documents(content_path, course_id)

    return {
        "course_id": course_id,
        "content_path": content_path,
        "transcript_path": transcript_path,
    }