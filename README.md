# Jarvis

A free, terminal-based voice assistant. Say "hey jarvis", ask something, and it answers aloud.

Built on Groq (LLM and Whisper), LangGraph, ChromaDB and openWakeWord.

## Features

- Voice loop: wake word, speech to text, reply, text to speech
- Tools: notes, long-term memory, web search, weather, Gmail, Google Calendar, YouTube search, open websites
- Confirmation guard: sending email, creating events and opening websites always show the details and wait for "yes"
- Memory: chat history in SQLite, lasting facts in ChromaDB

## Platform support

| Feature | macOS | Windows |
|---|---|---|
| Text mode | Yes | Expected to work (untested) |
| Voice input (wake word, Whisper) | Yes | Expected to work (untested) |
| Spoken replies | Yes (macOS `say`) | Not yet, needs a port |
| Browser tools (YouTube, open website) | Yes (macOS `open`) | Not yet, needs a port |
| Notes, memory, search, weather, Gmail, Calendar | Yes | Expected to work (untested) |

## Setup on macOS

```bash
brew install uv portaudio git
git clone https://github.com/Debajyoti02-mac/My-Own-Jervis-.git Jarvis
cd Jarvis
uv venv
uv pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > .env
```

Get a free key from the Groq console. If `openwakeword` fails to install, use `uv venv --python 3.12`.

## Setup on Windows (PowerShell)

```powershell
winget install astral-sh.uv Git.Git
cd $HOME\Documents
git clone https://github.com/Debajyoti02-mac/My-Own-Jervis-.git Jarvis
cd Jarvis
uv venv
uv pip install -r requirements.txt
Set-Content -Path .env -Value "GROQ_API_KEY=your_key_here" -Encoding ascii
```

Close and reopen PowerShell after installing, so `uv` and `git` are found. If one package fails to install, delete its line from `requirements.txt` and try again. You do not need PortAudio on Windows.

## Run

macOS:

```bash
.venv/bin/python main.py --text   # type instead of talk
.venv/bin/python main.py          # voice mode
```

Windows:

```powershell
.venv\Scripts\python main.py --text
.venv\Scripts\python main.py
```

Say "goodbye" or press Ctrl+C to quit. Allow microphone access for your terminal when asked (macOS: System Settings, Privacy and Security, Microphone. Windows: Settings, Privacy, Microphone).

## One-command launch

Add a `jarvis` command so you can start it from any folder.

macOS (zsh):

```bash
cat >> ~/.zshrc << 'EOT'

jarvis() {
  ( cd "$HOME/Documents/Jarvis" && .venv/bin/python main.py "$@" )
}
EOT
source ~/.zshrc
```

Windows (PowerShell):

```powershell
if (!(Test-Path $PROFILE)) { New-Item -Type File -Force $PROFILE }
Add-Content $PROFILE 'function jarvis { & "$HOME\Documents\Jarvis\.venv\Scripts\python.exe" "$HOME\Documents\Jarvis\main.py" @args }'
. $PROFILE
```

Then run `jarvis` for voice or `jarvis --text` for typing.

## Settings

Edit `settings.py`:

- `ASSISTANT_NAME`, `CREATOR`: how it introduces itself
- `MODEL`: the Groq model
- `VOICE`: the macOS voice (list them with `say -v '?'`)
- `BROWSER`: the app used for YouTube and websites, such as "Brave Browser" or "Google Chrome"
- `DEFAULT_CITY`: used when you ask for the weather without a city
- `WAKE_THRESHOLD`: raise it if it wakes by accident, lower it if it ignores you

## Google (optional)

Create a Desktop OAuth client in Google Cloud, enable the Gmail and Calendar APIs, and save the file as `credentials.json` in the project root. The first Google tool call opens a browser sign-in.

## Layout

```
main.py          voice and text loops
settings.py      names, paths, model, wake word
core/agent.py    prompt, graph, ask()
tools/           notes, memory and web, weather, google, browser
voice/audio.py   speak, listen, wake word
data/            local memory and tokens (not committed)
```

## Privacy

Never commit `.env`, `credentials.json`, `token.json` or `data/`. Audio and text sent to Groq's free tier carry no privacy guarantee, so do not use it for sensitive content.