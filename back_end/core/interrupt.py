import os

from rag.embed_store import load_vector_store
from langchain_groq import ChatGroq

class LearnerState:
    def __init__(self):
        self.current_slide = 1
        self.total_questions = 0
        self.slide_question_count = {}
        self.confusion_score = 0.0


    def record_question(self, slide_num: int):
        self.total_questions += 1
        self.slide_question_count[slide_num] = (
            self.slide_question_count.get(slide_num, 0) + 1
        )

        if self.slide_question_count[slide_num] >= 2:
            self.confusion_score += 0.5

    def is_learner_confused(self, slide_num: int) -> bool:
        return self.slide_question_count.get(slide_num, 0) >= 2


# -----------------------------

# Load components

# -----------------------------

db = load_vector_store()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are a virtual training coach.
Explain slides clearly and naturally.
Be concise and helpful.
"""

def generate_slide_narration(slide_num: int):


    docs = db.similarity_search(
        f"slide {slide_num} page {slide_num}",
        k=4,
    )

    slide_docs = [
        d for d in docs
        if d.metadata.get("slide") == slide_num
        or d.metadata.get("page") == slide_num
    ]

    if not slide_docs:
        return None

    context = "\n\n".join(d.page_content for d in slide_docs)

    prompt = f"""


    {SYSTEM_PROMPT}

    SLIDE CONTENT:
    {context}

    Explain this slide to the learner.
    """


    response = llm.invoke(prompt)

    return response.content


def decide_coach_action(
    user_query: str,
    current_slide: int,
    is_confused: bool = False
) -> str:

    decision_prompt = f"""
You are an intelligent virtual training coach.

A learner asked the following during slide {current_slide}:

"{user_query}"

Learner confusion status: {"CONFUSED" if is_confused else "NOT_CONFUSED"}

If the learner is CONFUSED, prefer ELABORATE unless they clearly request another action.

Return ONLY one of these actions:

ANSWER
ELABORATE
REPEAT_SLIDE
NEXT_SLIDE
PREVIOUS_SLIDE
PAUSE
STOP
ASK_CLARIFICATION

Guidelines:

- asking a question → ANSWER
- "go ahead", "continue", "next" → NEXT_SLIDE
- "go back", "previous" → PREVIOUS_SLIDE
- "repeat", "say again" → REPEAT_SLIDE
- confusion or repeated questions → ELABORATE
- "wait", "hold on", "pause" → PAUSE
- "stop training", "end session" → STOP
- unclear input → ASK_CLARIFICATION

Output ONLY the action name.
"""

    try:
        response = llm.invoke(decision_prompt)
        action = response.content.strip().upper()

        valid_actions = {
            "ANSWER",
            "ELABORATE",
            "REPEAT_SLIDE",
            "NEXT_SLIDE",
            "PREVIOUS_SLIDE",
            "PAUSE",
            "STOP",
            "ASK_CLARIFICATION"
        }

        if action in valid_actions:
            return action

    except Exception as e:
        print("Decision error:", e)

    # fallback
    return "ANSWER"