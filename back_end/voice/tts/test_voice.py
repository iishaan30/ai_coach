from TTS.api import TTS
import simpleaudio as sa

print("Loading model... (first time is slow)")

tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

output_path = "coqui_test.wav"

tts.tts_to_file(
    text="Hello. If you hear this, Coqui TTS is working perfectly.",
    file_path=output_path,
)

print("Playing audio...")
wave_obj = sa.WaveObject.from_wave_file(output_path)
play_obj = wave_obj.play()
play_obj.wait_done()
print("Done.")