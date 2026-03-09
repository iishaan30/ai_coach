import threading
import simpleaudio as sa

# =========================================================
# STATE
# =========================================================
_play_obj = None
_lock = threading.Lock()
_is_speaking = False


# =========================================================
# CORE PLAYER
# =========================================================
def play_audio(wav_path: str):
    """
    Play wav file asynchronously.
    Safe to interrupt.
    """
    global _play_obj, _is_speaking

    def _worker():
        global _play_obj, _is_speaking

        try:
            _is_speaking = True

            wave_obj = sa.WaveObject.from_wave_file(wav_path)
            _play_obj = wave_obj.play()

            while _play_obj.is_playing():
                pass

        except Exception as e:
            print(f"❌ Audio playback error: {e}")

        finally:
            _is_speaking = False

    stop()  # stop any existing audio
    threading.Thread(target=_worker, daemon=True).start()


# =========================================================
# STOP
# =========================================================
def stop():
    global _play_obj, _is_speaking

    _is_speaking = False

    try:
        if _play_obj and _play_obj.is_playing():
            _play_obj.stop()
    except Exception:
        pass


# =========================================================
# STATUS
# =========================================================
def is_speaking() -> bool:
    return _is_speaking