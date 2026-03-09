from fastapi import APIRouter, UploadFile, File, Form
from services.ingestion_service import process_uploaded_content

router = APIRouter(prefix="/content", tags=["content"])


@router.post("/upload")
async def upload_content(
    course_id: str = Form(...),
    transcript: UploadFile | None = File(None),
    file: UploadFile = File(...),
):
    result = await process_uploaded_content(
        course_id=course_id,
        content_file=file,
        transcript_file=transcript,
    )

    return {"status": "processed", "details": result}