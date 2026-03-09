import os

from rag.embed_store import load_vector_store
from langchain_groq import ChatGroq
from rag.rag_coach import speak_text

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

Your job:
- Explain the slide clearly to a learner
- Be concise but friendly
- Use simple language
- Do NOT invent information
"""


# -----------------------------
# Slide narration generator
# -----------------------------
def generate_slide_narration(slide_num: int):
    """
    Generate narration for a specific slide/page.
    Works with both 0-based and 1-based metadata.
    """

    # 🔍 broad semantic search first
    docs = db.similarity_search(
        f"slide {slide_num} page {slide_num}",
        k=6,
    )

    # ⭐ robust page matching
    slide_docs = [
        d for d in docs
        if (
            d.metadata.get("page") in [slide_num, slide_num - 1]
            or d.metadata.get("slide") == slide_num
        )
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


# -----------------------------
# Narrate a slide
# -----------------------------
def narrate_slide(slide_num: int):
    print(f"\n📄 Presenting Slide {slide_num}")

    narration = generate_slide_narration(slide_num)

    if not narration:
        print(f"⚠️ No content found for slide/page {slide_num}")
        return

    print("\n🎤 Coach:", narration)

    # ✅ single audio entry point
    audio_file = speak_text(narration)

    if audio_file:
        print(f"🔊 Audio: {audio_file}")


# -----------------------------
# CLI runner
# -----------------------------
def main():
    print("🎬 Slide Presenter ready. Type slide number or 'exit'.\n")

    while True:
        user_input = input("Slide number: ").strip()

        if user_input.lower() == "exit":
            break

        try:
            slide_num = int(user_input)
            narrate_slide(slide_num)
        except ValueError:
            print("⚠️ Please enter a valid number")


if __name__ == "__main__":
    main()