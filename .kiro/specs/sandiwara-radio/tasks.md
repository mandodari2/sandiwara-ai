# Tasks: Sandiwara AI — Radio Drama Generator

## Phase 1: Foundation (Kiro specs + skeleton)

- [x] 1. Create project structure with `.kiro/` (specs, steering, hooks)
- [x] 2. Write `requirements.md` (EARS format)
- [x] 3. Write `design.md` (architecture, data model)
- [ ] 4. Write `tasks.md` (this file)
- [ ] 5. Write steering files (`product.md`, `tech.md`, `structure.md`)
- [ ] 6. Write hook definition (verify on save)

## Phase 2: Backend — generation pipeline

- [ ] 7. Create `backend/drama.py` — script generator (genre templates → structured script JSON)
- [ ] 8. Create `backend/voices.py` — voice map (character → TTS voice), render line to audio
- [ ] 9. Create `backend/assets/` — SFX + music library (rain, sword, footsteps, fire, wind; moods: tense, sad, triumphant, mysterious)
- [ ] 10. Create `backend/mixer.py` — ffmpeg mix (voices + SFX + music → single MP3, faststart)
- [ ] 11. Create `backend/app.py` — FastAPI app (`/api/stories`, `/api/generate`, `/api/episodes/{id}/audio`, static frontend)

## Phase 3: Content — pre-loaded stories

- [ ] 12. Write story definition: Tutur Tinular Episode 1 (Bara Naga Puspa) — characters, synopsis, script
- [ ] 13. Write story definition: Mahabharata Episode 1 (Kurukshetra) — characters, synopsis, script
- [ ] 14. Write story definition: Legenda Danau Toba — characters, synopsis, script
- [ ] 15. Generate audio for all 3 pre-loaded episodes, verify playback

## Phase 4: Frontend

- [ ] 16. Build `frontend/index.html` — story library view
- [ ] 17. Build episode player view (audio + synchronised script)
- [ ] 18. Build create-drama form (title, synopsis, genre → POST /api/generate)
- [ ] 19. Style the app (dark, cinematic, radio-drama theme)

## Phase 5: Verify + deploy + submit

- [x] 20. End-to-end test: browse → play Tutur Tinular → generate a new drama → download
- [x] 21. Deploy config ready (Dockerfile, render.yaml, requirements.txt) — needs hosting choice
- [x] 22. Record 3-minute demo video (demo/sandiwara-ai-demo.mp4, 2:58)
- [x] 23. Write README + submission docs
- [ ] 24. Submit on Devpost (kiroween.devpost.com) before 4 Dec 2026 22:00 UTC — Joe
