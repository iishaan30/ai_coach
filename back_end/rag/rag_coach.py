#from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from rag.embed_store import load_vector_store
from collections import deque
import os
import requests
from pathlib import Path
from playsound import playsound
# -----------------------------
# Load vector DB (your knowledge)
# -----------------------------
db = load_vector_store()


# -----------------------------
# Local LLM (Ollama)
# -----------------------------
# llm = ChatOllama(
#     model="llama3.1:8b",   # adjust if needed
#     temperature=0.2,
# )
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------
# Conversation memory (sliding window)
# -----------------------------
memory = deque(maxlen=6)  # keeps last 6 turns

# -----------------------------
# Prompt template (VERY IMPORTANT)
# -----------------------------
SYSTEM_PROMPT = """
You are a helpful virtual coach for product training.

Rules:
- Answer ONLY using the provided context.
- If the answer is not in the context, say "I don't know based on the provided material."
- Explain in simple, learner-friendly language.
- Be concise but clear.
"""

def format_memory():
    """Convert memory into prompt text."""
    if not memory:
        return ""

    history_text = "\n".join(memory)
    return f"\nCONVERSATION HISTORY:\n{history_text}\n"


# -----------------------------
# Core RAG function
# -----------------------------
def ask_coach(question: str, k: int = 4):
    """
    Memory-aware RAG pipeline.
    """

    # 🔍 Step 1 — Retrieve relevant chunks
    docs = db.similarity_search(question, k=k)
    context = "\n\n".join([d.page_content for d in docs])

    # 🧠 Step 2 — get conversation history
    history_block = format_memory()

    # 🧠 Step 3 — Build final prompt
    final_prompt = f"""
{SYSTEM_PROMPT}

{history_block}

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    # 🤖 Step 4 — Call LLM
    response = llm.invoke(final_prompt)
    answer = response.content

    # 🧠 Step 5 — update memory
    memory.append(f"User: {question}")
    memory.append(f"Coach: {answer}")

    return answer, docs

# TTS
import os
import requests
import urllib3
import pyttsx3
from pathlib import Path
from playsound import playsound

urllib3.disable_warnings()

# -----------------------------
# Local TTS engine (initialize once)
# -----------------------------
_local_engine = None


def _get_local_engine():
    global _local_engine
    if _local_engine is None:
        _local_engine = pyttsx3.init()

        # ⭐ FIX: explicitly select Windows voice
        voices = _local_engine.getProperty("voices")
        if voices:
            _local_engine.setProperty("voice", voices[0].id)

        _local_engine.setProperty("rate", 170)
        _local_engine.setProperty("volume", 1.0)

    return _local_engine


def speak_text(text: str, output_file: str = "coach_audio.mp3"):
    """
    Robust TTS:
    1) Try ElevenLabs
    2) Fallback to local pyttsx3
    """

    api_key = os.getenv("ELEVENLABS_API_KEY") or "YOUR_HARDCODED_KEY"

    # =============================
    # TRY ELEVENLABS FIRST
    # =============================
    # try:
    #     if api_key and not api_key.startswith("YOUR_"):

    #         url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"

    #         headers = {
    #             "xi-api-key": api_key,
    #             "Content-Type": "application/json",
    #         }

    #         payload = {
    #             "text": text[:2500],  # safety limit
    #             "model_id": "eleven_multilingual_v2",
    #             "voice_settings": {
    #                 "stability": 0.4,
    #                 "similarity_boost": 0.7,
    #             },
    #         }

    #         response = requests.post(
    #             url,
    #             json=payload,
    #             headers=headers,
    #             timeout=30,
    #             verify=False,  # corporate SSL workaround
    #         )

    #         if response.status_code == 200:
    #             output_path = Path(output_file)
    #             output_path.write_bytes(response.content)

    #             print("✅ ElevenLabs TTS used")
    #             playsound(str(output_path))
    #             return str(output_path)
    #         else:
    #             print("⚠️ ElevenLabs failed → falling back")

    # except Exception as e:
    #     print(f"⚠️ ElevenLabs error → fallback: {e}")

    # =============================
    # FALLBACK: LOCAL TTS
    # =============================
    try:
        print("🔁 Using LOCAL TTS fallback")

        engine = _get_local_engine()

        # ⭐ DIRECT SPEAK — NO FILE SAVE
        engine.say(text)
        engine.runAndWait()

        return "LOCAL_TTS_SPOKEN"

    except Exception as e:
        print(f"❌ Local TTS also failed: {e}")
        return None


# -----------------------------
# Streaming RAG Answer (for WebSocket runtime)
# -----------------------------
async def stream_answer(question: str, websocket, k: int = 4):

    # 🔍 Step 1 — Retrieve relevant chunks
    docs = db.similarity_search(question, k=k)
    context = "\n\n".join([d.page_content for d in docs])

    # 🧠 Step 2 — conversation history
    history_block = format_memory()

    # 🧠 Step 3 — Build prompt
    final_prompt = f"""
{SYSTEM_PROMPT}

{history_block}

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    full_answer = ""

    # 🤖 Step 4 — Stream tokens from LLM
    async for chunk in llm.astream(final_prompt):

        token = chunk.content

        if token:
            full_answer += token

            await websocket.send_json({
                "type": "token",
                "content": token
            })

    # 🧠 Step 5 — Update memory after streaming
    memory.append(f"User: {question}")
    memory.append(f"Coach: {full_answer}")

    # Signal completion
    await websocket.send_json({
        "type": "done"
    })

    return full_answer

# -----------------------------
# CLI loop
# -----------------------------
def main():
    print("🧠 Virtual Coach ready! Type 'exit' to quit.\n")

    while True:
        query = input("You: ")

        if query.lower() == "exit":
            break

        answer, docs = ask_coach(query)

        print("\n🎓 Coach:", answer, "\n")
        # 🔊 Generate speech
        audio_file = speak_text(answer)
       
        if audio_file:
            print(f"🔊 Audio saved to: {audio_file}")
            try:
                playsound(audio_file)
            except Exception as e:
                print("⚠️ Could not play audio:", e)

        # 🔍 Debug sources (VERY useful during dev)
        print("📚 Sources:")
        for i, d in enumerate(docs, 1):
            print(f"  {i}.", d.metadata)
        print()


if __name__ == "__main__":
    main()