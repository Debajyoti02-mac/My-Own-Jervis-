        [ Wake Word ]  openWakeWord
              │
              ▼
        [ Ears ]  faster-whisper (speech → text)
              │
              ▼
   ┌──────── [ Agent Core ] ────────┐
   │  Brain: call_llm() (Ollama)    │
   │  Planner: ReAct → LangGraph    │
   │  Memory: ChromaDB              │
   │  Guard: confirm risky actions  │
   └──────────────┬─────────────────┘
                  │
              [ Tools ]  search, notes, calendar, gmail, files
                  │
                  ▼
        [ Mouth ]  Piper (text → speech)