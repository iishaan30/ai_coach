import requests

BASE = "http://localhost:8000"

print("Health:", requests.get(f"{BASE}/health").json())

print("Slide:", requests.get(f"{BASE}/slide/1").json())

print(
    "Ask:",
    requests.post(
        f"{BASE}/ask",
        json={"question": "Explain this slide"},
    ).json(),
)