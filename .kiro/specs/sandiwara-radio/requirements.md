# Requirements: Sandiwara AI — Radio Drama Generator

## Introduction

Sandiwara AI resurrects Indonesian radio drama (sandiwara radio) — a broadcast storytelling format that dominated Indonesian airwaves in the 1980s–1990s and is now effectively dead. The app lets anyone generate a full audio drama (script, character voices, sound effects, music) from a story idea, listen to it, and share it. Pre-loaded with classic Indonesian stories (Tutur Tinular, Mahabharata, local legends) and open to user-created stories.

## Glossary

- **Drama**: A generated audio drama — a sequence of voiced lines, narration, sound effects, and music, mixed into one audio file.
- **Episode**: One chapter of a story, roughly 3–5 minutes of audio.
- **Story**: A story definition — title, synopsis, characters, setting, genre.
- **Character**: A named role in a story, mapped to a distinct TTS voice.
- **Scene**: A block of script — a location + a sequence of dialogue/narration lines.

## Requirements

### Requirement 1: Story Library

**User Story:** As a listener, I want to browse classic Indonesian stories, so I can pick a drama to hear.

#### Acceptance Criteria

1. WHEN the user opens the app, THE Sandiwara AI SHALL display a library of pre-loaded stories with title, synopsis, genre, and episode count.
2. WHEN the user selects a story, THE Sandiwara AI SHALL show its episode list with duration and a play button per episode.
3. WHEN the user plays an episode, THE Sandiwara AI SHALL stream the generated audio and show the script lines synchronised with playback.
4. THE Sandiwara AI SHALL ship with at least 3 pre-loaded stories, including Tutur Tinular Episode 1.

### Requirement 2: AI Drama Generation

**User Story:** As a creator, I want to type a story idea and get a full audio drama, so I can hear my own story as radio drama.

#### Acceptance Criteria

1. WHEN the user submits a story idea (title + synopsis + genre), THE Sandiwara AI SHALL generate a structured script (scenes, dialogue lines, narration, sound-effect cues) for one episode.
2. WHEN the script is generated, THE Sandiwara AI SHALL assign each character a distinct voice and render every line to audio.
3. WHEN all lines are rendered, THE Sandiwara AI SHALL mix voices, sound effects, and background music into a single audio file.
4. WHEN generation finishes, THE Sandiwara AI SHALL save the episode to the story library and make it playable.
5. IF generation fails at any step, THEN THE Sandiwara AI SHALL report which step failed and keep any completed partial output.

### Requirement 3: Distinct Character Voices

**User Story:** As a listener, I want each character to sound different, so I can follow who is speaking.

#### Acceptance Criteria

1. WHEN a script is rendered, THE Sandiwara AI SHALL map each character to a distinct TTS voice.
2. WHEN two characters speak in the same scene, THE Sandiwara AI SHALL use different voices for each.
3. THE Sandiwara AI SHALL support at least 4 distinct voices (2 male, 2 female).

### Requirement 4: Sound Effects and Music

**User Story:** As a listener, I want sound effects and music in the drama, so it feels like real radio drama, not just people talking.

#### Acceptance Criteria

1. WHEN the script contains a sound-effect cue (e.g. rain, sword clash, footsteps), THE Sandiwara AI SHALL include a matching sound in the mix at the cued position.
2. WHEN a scene has a mood (tense, sad, triumphant), THE Sandiwara AI SHALL include matching background music at low volume under the dialogue.
3. WHEN no matching sound exists for a cue, THEN THE Sandiwara AI SHALL skip the cue and log it, rather than failing the episode.

### Requirement 5: Sharing and Download

**User Story:** As a listener, I want to download or share a drama episode, so I can listen offline or send it to friends.

#### Acceptance Criteria

1. WHEN the user opens an episode, THE Sandiwara AI SHALL offer a download link for the audio file.
2. WHEN the user shares an episode, THE Sandiwara AI SHALL provide a shareable link that opens the episode page.

### Requirement 6: Kiro Spec-Driven Development

**User Story:** As a Kiroween judge, I want to see real Kiro usage, so I can verify the project was built with Kiro.

#### Acceptance Criteria

1. THE repository SHALL contain a `.kiro/specs/sandiwara-radio/` directory with `requirements.md`, `design.md`, and `tasks.md`.
2. THE repository SHALL contain `.kiro/steering/` files describing product, tech, and structure rules.
3. THE repository SHALL contain at least one `.kiro/hooks/` definition that runs verification on save.
4. THE `.kiro/` directory SHALL be committed to the public repository (not gitignored).
