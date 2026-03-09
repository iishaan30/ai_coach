from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json

from core.interrupt import decide_coach_action, generate_slide_narration
from rag.rag_coach import ask_coach
# from voice.tts.coqui_tts import CoquiTTSProvider
# from voice.stt.whisper_stt import whisper_transcribe
from voice.tts.elevenlabs_tts import synthesize
from voice.stt.deepgram_stt import transcribe_audio
router = APIRouter()

# tts = CoquiTTSProvider()

class CoachSession:


    def __init__(self):
        self.current_slide = 1
        self.current_narration = ""
        self.running = True
        self.started = False


@router.websocket("/ws/coach")
async def coach_socket(ws: WebSocket):


    await ws.accept()

    print("Coach connected")

    session = CoachSession()

    try:

        # -----------------------------
        # WAIT FOR START COMMAND
        # -----------------------------
        while not session.started:

            data = await ws.receive_json()

            if data["type"] == "start_training":

                print("Training started")

                session.current_slide = 1
                session.started = True

        # -----------------------------
        # MAIN COACH LOOP
        # -----------------------------
        while session.running:

            narration = generate_slide_narration(session.current_slide)

            if not narration:

                await ws.send_json({
                    "type": "training_complete"
                })

                break

            session.current_narration = narration

            # Send slide text
            await ws.send_json({
                "type": "slide",
                "slide": session.current_slide,
                "content": narration
            })

            # Generate narration speech
            audio = await asyncio.to_thread(synthesize, narration)

            if audio:
                await ws.send_bytes(audio)

            # -----------------------------
            # WAIT FOR EVENTS
            # -----------------------------
            while True:

                message = await ws.receive()

                # -----------------------------
                # HANDLE JSON MESSAGE
                # -----------------------------
                if "text" in message:

                    data = json.loads(message["text"])

                    # NEXT SLIDE
                    if data["type"] == "next":

                        session.current_slide += 1
                        break

                    # QUESTION
                    elif data["type"] == "question":

                        question = data["question"]

                        action = decide_coach_action(
                            question,
                            session.current_slide
                        )

                        print("Action decided:", action)

                        print("Question received:", question)

                        if "stop" in question:

                            print("Training stopped by user")

                            await ws.send_json({
                                "type": "stop_training",
                                "content": "Okay, stopping the training session."
                            })

                            session.running = False
                            break

                        answer, _ = ask_coach(question)

                        await ws.send_json({
                            "type": "answer",
                            "content": answer
                        })

                        # Generate answer speech
                        audio = await asyncio.to_thread(synthesize, narration)

                        if audio:
                            await ws.send_bytes(audio)

                    # RESUME TRAINING
                    elif data["type"] == "resume":

                        print("Training Resumed")

                        await ws.send_json({
                            "type": "slide",
                            "slide": session.current_slide,
                            "content": session.current_narration
                        })

                        audio = await asyncio.to_thread(synthesize, narration)

                        if audio:
                            await ws.send_bytes(audio)

                    # STOP SESSION
                    elif data["type"] == "stop":

                        session.running = False
                        break

                # -----------------------------
                # HANDLE AUDIO MESSAGE (future STT)
                # -----------------------------
                elif "bytes" in message:

                    print("Voice input received")

                    audio_bytes = message["bytes"]

                    # Convert speech → text
                    question = transcribe_audio(audio_bytes)

                    if not question:
                        print("No speech detected")
                        continue

                    question = question.lower()

                    print("Transcribed:", question)

                    # STOP COMMAND
                    if "stop" in question:

                        print("Training stopped by user")

                        await ws.send_json({
                            "type": "stop_training",
                            "content": "Okay, stopping the training session."
                        })

                        session.running = False
                        break

                    # NORMAL QUESTION
                    answer, _ = ask_coach(question)

                    await ws.send_json({
                        "type": "answer",
                        "content": answer
                    })

                    # Generate answer speech
                    audio = await asyncio.to_thread(synthesize, narration)

                    if audio:
                        await ws.send_bytes(audio)

    except WebSocketDisconnect:

        print("Client disconnected")

