# Sandiwara AI — Drama Radio Indonesia, Dihidupkan Lagi oleh AI

**Kiroween 2026 — Resurrection**

Sandiwara radio adalah format drama audio yang pernah menguasai gelombang radio
Indonesia di era 1980–1990an, dan kini praktis mati. Sandiwara AI menghidupkannya
kembali: pilih cerita klasik Indonesia (Tutur Tinular, Mahabharata, Legenda Danau
Toba) atau tulis idemu sendiri — AI menulis naskah, memberi tiap tokoh suara
yang berbeda, menambah efek suara dan musik, lalu menyajikan drama audio yang
siap didengar, diunduh, dan dibagikan.

## Cara jalan

```bash
python3 -m venv .venv && .venv/bin/pip install fastapi uvicorn
.venv/bin/uvicorn backend.app:app --port 8000
# Buka http://localhost:8000
```

## Arsitektur

- **Backend** (Python FastAPI): `backend/app.py` + `drama.py` (generator naskah),
  `voices.py` (TTS multi-suara), `mixer.py` (ffmpeg: suara + SFX + musik).
- **Frontend**: HTML/CSS/JS polos, tanpa build step.
- **Cerita**: JSON di `stories/` — Tutur Tinular, Mahabharata, Danau Toba.
- **Audio**: MP3 hasil generate di `audio/`.

## Kiro

Proyek ini dibangun dengan pendekatan spec-driven Kiro:

- `.kiro/specs/sandiwara-radio/` — requirements (EARS), design, tasks
- `.kiro/steering/` — product, tech, structure
- `.kiro/hooks/` — verify-on-save (syntax check + import check)

## API

- `GET /api/stories` — daftar cerita
- `GET /api/stories/{id}` — detail cerita + episode
- `POST /api/generate` — buat episode baru dari ide cerita
- `GET /api/episodes/{id}/audio` — unduh/stream MP3 episode
