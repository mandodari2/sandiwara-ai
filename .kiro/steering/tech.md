# Tech Steering — Sandiwara AI

## Stack

- Backend: Python 3.11+, FastAPI. One app file (`app.py`) + modules (`drama.py`, `voices.py`, `mixer.py`).
- Frontend: plain HTML/CSS/JS, no build step. Static files served by the backend.
- Audio: ffmpeg for mixing. TTS via the system `tts` CLI. Output MP3 128k, 44.1kHz, faststart.
- Storage: local JSON files for stories/episodes, local MP3 files for audio. No database needed for the hackathon.

## Tech rules

- No paid API keys. The generation pipeline must work with local tools (TTS CLI, ffmpeg) and deterministic templates.
- Every audio file is exported with faststart so it streams on phones.
- A missing SFX file is skipped and logged, never fatal.
- Every API endpoint returns JSON; errors return a JSON error object, never an HTML stack trace.
- Keep the backend to a few small files; no framework sprawl.
