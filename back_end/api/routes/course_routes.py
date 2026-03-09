from fastapi import APIRouter, HTTPException
from services.slide_service import get_slide_content

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("/{course_id}/slides/{slide_num}")
def fetch_slide(course_id: str, slide_num: int):
    result = get_slide_content(course_id, slide_num)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Slide not found for this course",
        )

    return result