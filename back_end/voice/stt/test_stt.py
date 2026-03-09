from voice.stt.whisper_stt import record_audio, transcribe_file

wav_path = record_audio(duration=5)
text = transcribe_file(wav_path)

print("🧠 You said:", text)