# Jarvis

A free, terminal-based voice assistant. Say "hey jarvis", ask something, and it answers aloud.

Built on Groq (LLM and Whisper), LangGraph, ChromaDB and openWakeWord.

## Features

- Voice loop: wake word, speech to text, reply, text to speech (macOS `say`)
- Tools: notes, long-term memory, web search, weather, Gmail, Google Calendar
- Confirmation guard: sending email or creating events always shows the draft and waits for "yes"
- Memory: chat history in SQLite, lasting facts in ChromaDB

## Setup

```bash
brew install uv portaudio git
git clone https://github.com/Debajyoti02-mac/My-Own-Jervis-.git Jarvis
cd Jarvis
uv venv
uv pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
```

Get a free key from the Groq console. If `openwakeword` fails to install, use `uv venv --python 3.12`.

## Run

```bash
.venv/bin/python main.py --text   # type instead of talk
.venv/bin/python main.py          # voice mode
```

Say "goodbye" or press Ctrl+C to quit. Allow microphone access for your terminal when macOS asks.

## Google (optional)

Create a Desktop OAuth client in Google Cloud, enable the Gmail and Calendar APIs, and save the file as `credentials.json` in the project root. The first Google tool call opens a browser sign-in.

## Layout

```
main.py          voice and text loops
settings.py      names, paths, model, wake word
core/agent.py    prompt, graph, ask()
tools/           notes, memory and web, weather, google
voice/audio.py   speak, listen, wake word
data/            local memory and tokens (not committed)
```

## Privacy

Never commit `.env`, `credentials.json`, `token.json` or `data/`. Audio and text sent to Groq's free tier carry no privacy guarantee, so do not use it for sensitive content.
