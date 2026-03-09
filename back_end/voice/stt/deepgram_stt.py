import requests
import os

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def transcribe_audio(audio_bytes: bytes) -> str:

    url = "https://api.deepgram.com/v1/listen"

    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav"
    }

    response = requests.post(url, headers=headers, data=audio_bytes)

    data = response.json()

    try:
        return data["results"]["channels"][0]["alternatives"][0]["transcript"]
    except:
        return ""