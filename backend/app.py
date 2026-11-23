"""Sandiwara AI — FastAPI backend.

Endpoints:
  GET  /api/stories              — list stories
  GET  /api/stories/{id}         — story detail + episodes
  POST /api/generate             — generate a new episode from a story idea
  GET  /api/episodes/{id}/audio — serve the episode MP3
  GET  /                        — serve the frontend
"""

import json
import os
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from drama import generate_script, script_to_text, speakers_in_script
from voices import assign_voices, render_script_to_mp3
from mixer import mix_episode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
STORIES_DIR = os.path.join(PROJECT_DIR, "stories")
AUDIO_DIR = os.path.join(PROJECT_DIR, "audio")
FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend")

os.makedirs(AUDIO_DIR, exist_ok=True)

app = FastAPI(title="Sandiwara AI")


# --- Story store (JSON files) ---

def _load_story(story_id):
    path = os.path.join(STORIES_DIR, f"{story_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _list_stories():
    stories = []
    for name in sorted(os.listdir(STORIES_DIR)):
        if name.endswith(".json"):
            with open(os.path.join(STORIES_DIR, name), encoding="utf-8") as f:
                data = json.load(f)
            stories.append({
                "id": data["id"],
                "title": data["title"],
                "synopsis": data["synopsis"],
                "genre": data["genre"],
                "episode_count": len(data.get("episodes", [])),
                "characters": [c["name"] for c in data.get("characters", [])],
            })
    return stories


def _save_story(story):
    path = os.path.join(STORIES_DIR, f"{story['id']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(story, f, ensure_ascii=False, indent=2)


# --- API ---

@app.get("/api/stories")
def list_stories():
    return {"stories": _list_stories()}


@app.get("/api/stories/{story_id}")
def get_story(story_id: str):
    story = _load_story(story_id)
    if story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


class GenerateRequest(BaseModel):
    title: str
    synopsis: str
    genre: str = "historical"
    characters: list = []


@app.post("/api/generate")
def generate_episode(req: GenerateRequest):
    """Generate a new episode from a story idea. Returns the episode."""
    if not req.title.strip() or not req.synopsis.strip():
        raise HTTPException(status_code=400, detail="Title and synopsis are required")

    characters = req.characters or [
        {"name": "Tokoh Utama", "gender": "male"},
        {"name": "Lawan", "gender": "male"},
        {"name": "Sahabat", "gender": "female"},
    ]

    # 1. Generate the script.
    script = generate_script(req.title, req.synopsis, req.genre, characters)
    script_text = script_to_text(script)

    # 2. Assign voices and render to MP3.
    # assign_voices already maps "Narator" internally; pass story chars only.
    voice_mapping = assign_voices(characters)
    episode_id = f"gen-{uuid.uuid4().hex[:8]}"
    voice_mp3 = os.path.join(AUDIO_DIR, f"{episode_id}-voice.mp3")
    ok, err = render_script_to_mp3(script_text, voice_mapping, voice_mp3)
    if not ok:
        raise HTTPException(status_code=500, detail=f"Voice rendering failed: {err}")

    # 3. Mix with music bed.
    mood = script["scenes"][0].get("mood", "tense") if script["scenes"] else "tense"
    final_mp3 = os.path.join(AUDIO_DIR, f"{episode_id}.mp3")
    ok, err = mix_episode(voice_mp3, final_mp3, mood=mood)
    if not ok:
        raise HTTPException(status_code=500, detail=f"Mixing failed: {err}")

    # 4. Save as a new story (so it appears in the library).
    story_id = f"gen-{uuid.uuid4().hex[:8]}"
    story = {
        "id": story_id,
        "title": req.title,
        "synopsis": req.synopsis,
        "genre": req.genre,
        "characters": characters,
        "episodes": [{
            "id": episode_id,
            "title": req.title,
            "audio_url": f"/api/episodes/{episode_id}/audio",
            "duration_sec": 0,
            "script": script,
        }],
    }
    _save_story(story)

    return {
        "story_id": story_id,
        "episode_id": episode_id,
        "title": req.title,
        "audio_url": f"/api/episodes/{episode_id}/audio",
        "script": script,
        "speakers": speakers_in_script(script),
    }


@app.get("/api/episodes/{episode_id}/audio")
def get_episode_audio(episode_id: str):
    path = os.path.join(AUDIO_DIR, f"{episode_id}.mp3")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(path, media_type="audio/mpeg")


# --- Static frontend ---

if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
