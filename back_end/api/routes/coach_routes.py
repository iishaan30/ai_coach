from fastapi import APIRouter
from core.interrupt import generate_slide_narration
from rag.rag_coach import ask_coach

router = APIRouter()

current_slide = 1

@router.post("/coach/start")
def start():

    global current_slide

    current_slide = 1

    narration = generate_slide_narration(current_slide)

    return {
        "slide": current_slide,
        "content": narration
    }


@router.post("/coach/next")
def next_slide():

    global current_slide

    current_slide += 1

    narration = generate_slide_narration(current_slide)

    return {
        "slide": current_slide,
        "content": narration
    }


@router.post("/coach/ask")
def ask(question: dict):

    answer,_ = ask_coach(question["question"])

    return {
        "answer": answer
    }