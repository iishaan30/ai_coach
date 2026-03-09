import tempfile
from faster_whisper import WhisperModel

# Load model once

_model = None

def _get_model():
    global _model


    if _model is None:
        print("🔄 Loading Whisper model...")

        _model = WhisperModel(
            "tiny",
            device="cpu",
            compute_type="int8"
        )

        print("✅ Whisper ready")

    return _model


def whisper_transcribe(audio_bytes: bytes) -> str:
    """
    Transcribe audio bytes received from WebSocket
    """


    model = _get_model()

    # Save audio to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
        f.write(audio_bytes)
        audio_path = f.name

    segments, _ = model.transcribe(audio_path)

    text = " ".join(seg.text for seg in segments)

    return text.strip()

