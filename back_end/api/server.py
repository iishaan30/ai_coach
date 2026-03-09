from fastapi import FastAPI
from pydantic import BaseModel 

from core.interrupt import generate_slide_narration
from rag.rag_coach import ask_coach

from api.routes.content_routes import router as content_router
from api.routes.course_routes import router as course_router
from api.routes.coach_routes import router as coach_router
from api.routes.coach_ws import router as coach_ws

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Virtual Coach API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(content_router)
app.include_router(course_router)
app.include_router(coach_router)
app.include_router(coach_ws)

class QuestionRequest(BaseModel):
    question:str
    
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("slide/{slide_num}")
def get_slide(slide_num: int):
    narration = generate_slide_narration(slide_num)
    return {"slide": slide_num, "content": narration}

@app.post("/ask")
def ask_question(req: QuestionRequest):
    answer = ask_coach(req.question)
    return {"answer": answer}