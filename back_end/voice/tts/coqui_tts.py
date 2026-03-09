import threading
from pathlib import Path
import re
import uuid
import os

from TTS.api import TTS
from voice.tts.tts_provider import TTSProvider

# =========================================================

# Text cleaning

# =========================================================

def clean_tts_text(text: str) -> str:
    text = re.sub(r"`.*?`", "", text, flags=re.DOTALL)
    text = re.sub(r"[#*_`{}[]|<>]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# =========================================================

# Lazy model loading

# =========================================================

_tts_model = None
_model_lock = threading.Lock()

def _get_model():
    global _tts_model


    with _model_lock:
        if _tts_model is None:
            print("🔄 Loading Coqui model (first time only)...")

            _tts_model = TTS(
                # model_name="tts_models/en/ljspeech/tacotron2-DDC",
                model_name="tts_models/en/ljspeech/glow-tts",
                progress_bar=False
            )

            print("✅ Coqui model ready")

    return _tts_model


# =========================================================

# Provider

# =========================================================

class CoquiTTSProvider(TTSProvider):


    def __init__(self, output_dir: str = "temp_audio"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def synthesize(self, text: str) -> bytes:

        tts = _get_model()

        clean_text = clean_tts_text(text)

        if len(clean_text) < 5:
            return b""

        output_path = Path(self.output_dir) / f"coqui_{uuid.uuid4().hex}.wav"

        tts.tts_to_file(
            text=clean_text[:800],
            file_path=str(output_path),
        )

        # Read generated audio
        with open(output_path, "rb") as f:
            audio_bytes = f.read()

        # Cleanup temp file
        try:
            os.remove(output_path)
        except:
            pass

        return audio_bytes
    
    

