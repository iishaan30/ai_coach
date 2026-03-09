import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty("voices")

print("\nAvailable voices:\n")
for v in voices:
    print("ID:", v.id)
    print("Name:", v.name)
    print("-" * 40)