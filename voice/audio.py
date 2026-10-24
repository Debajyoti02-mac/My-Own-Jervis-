import io
import subprocess
import wave
from pathlib import Path

import openwakeword
import sounddevice as sd
from groq import Groq
from openwakeword.model import Model

from settings import WAKE_MODEL, WAKE_THRESHOLD   # also loads your .env

RATE = 16000
_stt = None
_oww = None


def _client():
    global _stt
    if _stt is None:
        _stt = Groq()
    return _stt


def _wake_model():
    global _oww
    if _oww is None:
        path = Path(openwakeword.__file__).parent / "resources" / "models" / WAKE_MODEL
        _oww = Model(wakeword_model_paths=[str(path)])
    return _oww


def speak(text: str):
    subprocess.run(["say", text])


def listen(seconds: int = 5) -> str:
    print("Listening...")
    audio = sd.rec(int(seconds * RATE), samplerate=RATE, channels=1, dtype="int16")
    sd.wait()
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(audio.tobytes())
    result = _client().audio.transcriptions.create(
        file=("input.wav", buf.getvalue()),
        model="whisper-large-v3-turbo",
        language="en",
    )
    return result.text.strip()


def wait_for_wake(threshold: float = WAKE_THRESHOLD):
    model = _wake_model()
    print("Waiting for wake word...")
    model.reset()
    with sd.InputStream(samplerate=RATE, channels=1, dtype="int16", blocksize=1280) as stream:
        while True:
            frame, _ = stream.read(1280)
            if max(model.predict(frame[:, 0]).values()) > threshold:
                return


def voice_confirm(question: str) -> str:
    print(question)                       # the full draft stays on screen
    speak("Please confirm. Say yes or no.")
    return listen(seconds=4)