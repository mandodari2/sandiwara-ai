# Structure Steering — Sandiwara AI

## Repository layout

```
kiroween-sandiwara/
  .kiro/
    specs/sandiwara-radio/   # requirements.md, design.md, tasks.md
    steering/                # product.md, tech.md, structure.md
    hooks/                   # verify-on-save.json
  backend/
    app.py                   # FastAPI app + static serving
    drama.py                 # script generator
    voices.py                # voice map + TTS rendering
    mixer.py                 # ffmpeg audio mixing
    assets/                  # SFX + music files
  frontend/
    index.html               # story library + player + create form
    style.css
    app.js
  stories/
    tutur-tinular.json       # story + episode definitions
    mahabharata.json
    danau-toba.json
  audio/                     # generated MP3 output (gitignored)
  README.md
```

## Structure rules

- The `.kiro/` directory is committed, never gitignored — judges inspect it.
- Generated audio goes in `audio/` and is gitignored (large binaries).
- Story definitions are JSON in `stories/`, one file per story.
- Keep each backend module under 300 lines; split before it grows.
