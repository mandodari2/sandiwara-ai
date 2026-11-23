# Design: Sandiwara AI — Radio Drama Generator

## Overview

Sandiwara AI is a web app that generates Indonesian radio dramas with AI. A user picks a story (or writes their own idea), the system generates a structured script, renders each line with a distinct TTS voice, adds sound effects and music, mixes everything with ffmpeg, and serves the finished audio for listening, download, and sharing.

## Architecture

```
User (browser)
  → Frontend (static web app: HTML/CSS/JS)
  → Backend API (Python FastAPI)
      → Script generator (LLM / template engine)
      → Voice renderer (TTS, multiple voices)
      → SFX + music library (local files)
      → Audio mixer (ffmpeg)
  → Audio files served as static MP3
```

### Components

1. **Frontend** (`frontend/`)
   - Single-page web app, no build step (plain HTML/CSS/JS) so it deploys anywhere.
   - Views: story library, episode player (with synchronised script), create-drama form.
   - Audio playback via native `<audio>` element.
   - Talks to the backend over REST (`/api/stories`, `/api/generate`, `/api/episodes/{id}`).

2. **Backend** (`backend/`)
   - Python FastAPI, one file `app.py` plus a `drama.py` module for the generation pipeline.
   - Endpoints:
     - `GET /api/stories` — list stories.
     - `GET /api/stories/{id}` — story detail + episodes.
     - `POST /api/generate` — accept a story idea, run the pipeline, return the episode.
     - `GET /api/episodes/{id}/audio` — serve the mixed MP3.
   - Static file serving for the frontend and audio.

3. **Script generator** (`backend/drama.py`)
   - Input: title, synopsis, genre, characters.
   - Output: structured script JSON — scenes, each with location, mood, and lines. Each line has `speaker`, `text`, and optional `sfx` cue.
   - For the hackathon demo, generation uses a template + LLM-style expansion. The pipeline is deterministic and testable without a live LLM key: a built-in story engine expands a synopsis into scenes using genre templates.

4. **Voice renderer**
   - Each character maps to a distinct TTS voice (minimum 4 voices: 2 male, 2 female).
   - Renders each script line to a WAV/MP3 segment, with per-line timing.
   - Narration uses a separate neutral voice.

5. **SFX + music library** (`backend/assets/`)
   - Small library of royalty-free / synthesised sounds: rain, footsteps, sword clash, fire, wind, crowd murmur.
   - Background music loops per mood: tense, sad, triumphant, mysterious.
   - Missing SFX for a cue is skipped and logged, never fatal.

6. **Audio mixer**
   - ffmpeg: concatenate voice segments with silences, layer SFX at cued timestamps, duck music under dialogue, export a single MP3 (128k, 44.1kHz).
   - Output is a faststart MP3 so it streams on phones.

## Data Model

### Story
```json
{
  "id": "tutur-tinular",
  "title": "Tutur Tinular",
  "synopsis": "...",
  "genre": "wuxia / historical",
  "characters": [
    {"name": "Kamandanu", "voice": "male_1", "description": "..."},
    {"name": "Dwipangga", "voice": "male_2", "description": "..."},
    {"name": "Mei Shin", "voice": "female_1", "description": "..."}
  ],
  "episodes": ["ep1", "ep2"]
}
```

### Episode
```json
{
  "id": "tutur-tinular-ep1",
  "story_id": "tutur-tinular",
  "title": "Bara Naga Puspa",
  "duration_sec": 240,
  "audio_url": "/audio/tutur-tinular-ep1.mp3",
  "script": [
    {"type": "narration", "text": "..."},
    {"type": "dialogue", "speaker": "Kamandanu", "text": "...", "sfx": "rain"},
    {"type": "sfx", "cue": "sword_draw"}
  ]
}
```

### Script (generation output)
```json
{
  "scenes": [
    {
      "location": "Candi berlumut, malam hujan",
      "mood": "tense",
      "lines": [
        {"speaker": "Narrator", "text": "..."},
        {"speaker": "Kamandanu", "text": "...", "sfx": "rain"}
      ]
    }
  ]
}
```

## Correctness Properties

- Every episode audio file exists on disk before it is listed as playable.
- Every dialogue line has a speaker that maps to a known voice; unknown speakers fall back to the narrator voice and are logged.
- The mixer never fails the whole episode for a missing SFX file.
- The API never returns an episode with a missing audio file.

## Testing

- Unit: script generator produces valid scenes/lines for each genre template; voice map covers all characters in a story.
- Integration: `POST /api/generate` with a test idea returns a playable MP3; `GET /api/stories` lists the pre-loaded stories.
- Manual: play Tutur Tinular Episode 1 end-to-end in the browser, verify voices differ per character and SFX/music are audible.
