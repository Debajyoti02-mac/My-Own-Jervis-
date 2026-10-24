import sys

from core.agent import ask
from settings import ASSISTANT_NAME
from voice.audio import listen, speak, voice_confirm, wait_for_wake

THREAD = "jarvis2"
EXIT_WORDS = ("goodbye", "stop listening", "exit", "quit")


def safe_ask(text, confirm=None):
    try:
        if confirm:
            return ask(text, thread_id=THREAD, confirm=confirm)
        return ask(text, thread_id=THREAD)
    except Exception as e:
        print("Error:", e)
        return "Sorry, something went wrong. Please try again."


def voice_loop():
    print(f"{ASSISTANT_NAME} is ready. Say 'hey jarvis'. Say 'goodbye' or press Ctrl+C to quit.")
    while True:
        wait_for_wake()
        speak("Yes?")
        text = listen()
        print("You:", text)
        if not text:
            continue
        if text.lower().strip(".!?, ") in EXIT_WORDS:
            speak("Goodbye.")
            break
        reply = safe_ask(text, confirm=voice_confirm)
        print(f"{ASSISTANT_NAME}:", reply)
        speak(reply)


def text_loop():
    print(f"{ASSISTANT_NAME} text mode. Type 'exit' to quit.")
    while True:
        text = input("You: ").strip()
        if text.lower() in EXIT_WORDS:
            break
        if text:
            print(f"{ASSISTANT_NAME}:", safe_ask(text))


def main():
    try:
        text_loop() if "--text" in sys.argv else voice_loop()
    except KeyboardInterrupt:
        print("\nGoodbye.")


if __name__ == "__main__":
    main()