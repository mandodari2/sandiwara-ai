"""Script generator for Sandiwara AI.

Turns a story idea (title, synopsis, genre, characters) into a structured
radio-drama script: scenes with location, mood, and lines. Each line has a
speaker, text, and an optional sound-effect cue.

Deterministic and template-based (no paid API key needed). Genre templates
expand a synopsis into scenes; the story's characters are cast into the
dialogue roles.
"""

import json
import re

# Genre templates: each defines the scene arc and narration style.
GENRE_TEMPLATES = {
    "wuxia": {
        "moods": ["tense", "mysterious", "triumphant"],
        "opening": "Di sebuah malam yang hujan, di tengah hutan yang gelap...",
        "scene_locations": [
            "Candi berlumut, malam hujan",
            "Jalan setapak hutan jati",
            "Lembah berkabut di kaki gunung",
        ],
    },
    "historical": {
        "moods": ["tense", "sad", "triumphant"],
        "opening": "Pada zaman dahulu kala, di sebuah kerajaan yang besar...",
        "scene_locations": [
            "Balairung istana",
            "Medan perang di kala senja",
            "Desa di tepi sungai",
        ],
    },
    "legend": {
        "moods": ["mysterious", "sad", "triumphant"],
        "opening": "Konon, di sebuah tempat yang jauh, hiduplah...",
        "scene_locations": [
            "Danau yang tenang di pagi hari",
            "Hutan larangan",
            "Puncak gunung berkabut",
        ],
    },
    "mystery": {
        "moods": ["mysterious", "tense", "sad"],
        "opening": "Tidak ada yang menyangka, malam itu akan mengubah segalanya...",
        "scene_locations": [
            "Rumah tua di ujung desa",
            "Pasar malam yang sepi",
            "Jembatan kayu di atas sungai",
        ],
    },
}

DEFAULT_GENRE = "historical"

# SFX cues that fit common moments.
SFX_RAIN = "rain"
SFX_SWORD = "sword_clash"
SFX_FOOTSTEPS = "footsteps"
SFX_FIRE = "fire"
SFX_WIND = "wind"


def _split_synopsis(synopsis):
    """Split a synopsis into sentences for narration beats."""
    sentences = [s.strip() for s in re.split(r"[.!?]+", synopsis) if s.strip()]
    return sentences


def generate_script(title, synopsis, genre, characters, num_scenes=3):
    """Generate a structured script dict for one episode.

    Returns a dict: {"title": ..., "scenes": [{"location", "mood", "lines": [...]}]}.
    Each line: {"speaker": "Narator"|character name, "text": ..., "sfx": optional}.
    """
    template = GENRE_TEMPLATES.get(genre, GENRE_TEMPLATES[DEFAULT_GENRE])
    sentences = _split_synopsis(synopsis)
    locations = template["scene_locations"]
    moods = template["moods"]

    # Character roles: first character is the hero, second the rival, rest supporting.
    hero = characters[0]["name"] if characters else "Tokoh Utama"
    rival = characters[1]["name"] if len(characters) > 1 else "Lawan"
    supporter = characters[2]["name"] if len(characters) > 2 else "Sahabat"

    scenes = []

    # Scene 1: opening narration + hero introduction.
    opening_lines = [
        {"speaker": "Narator", "text": template["opening"], "sfx": SFX_RAIN},
    ]
    if sentences:
        opening_lines.append({"speaker": "Narator", "text": sentences[0] + "."})
    opening_lines.append(
        {"speaker": hero, "text": "Aku tidak akan mundur, apa pun yang terjadi."}
    )
    opening_lines.append(
        {"speaker": "Narator", "text": f"Dan di situlah kisah {title} dimulai."}
    )
    scenes.append(
        {"location": locations[0], "mood": moods[0], "lines": opening_lines}
    )

    # Scene 2: confrontation — hero meets rival.
    conflict_lines = []
    if len(sentences) > 1:
        conflict_lines.append({"speaker": "Narator", "text": sentences[1] + "."})
    conflict_lines.append(
        {"speaker": rival, "text": "Akhirnya kita bertemu lagi. Kau tidak bisa lari dariku."}
    )
    conflict_lines.append(
        {"speaker": hero, "text": "Aku tidak lari. Aku datang untuk mengakhiri ini."}
    )
    conflict_lines.append(
        {"speaker": supporter, "text": "Hati-hati. Dia tidak seperti dulu."}
    )
    conflict_lines.append(
        {
            "speaker": "Narator",
            "text": "Pedang terhunus. Hujan semakin deras.",
            "sfx": SFX_SWORD,
        }
    )
    scenes.append(
        {"location": locations[1], "mood": moods[1] if len(moods) > 1 else moods[0], "lines": conflict_lines}
    )

    # Scene 3: climax + cliffhanger.
    climax_lines = []
    if len(sentences) > 2:
        climax_lines.append({"speaker": "Narator", "text": sentences[2] + "."})
    climax_lines.append(
        {"speaker": hero, "text": "Ampuni aku... hari ini aku harus memilih."}
    )
    climax_lines.append(
        {"speaker": rival, "text": "Pilihlah. Tapi ingat, pilihanmu ada harganya."}
    )
    climax_lines.append(
        {
            "speaker": "Narator",
            "text": "Dan di situlah episode ini berakhir. Bersambung...",
            "sfx": SFX_WIND,
        }
    )
    scenes.append(
        {"location": locations[2], "mood": moods[2] if len(moods) > 2 else moods[0], "lines": climax_lines}
    )

    return {"title": title, "scenes": scenes[:num_scenes]}


def script_to_text(script):
    """Render a script dict to the speaker-labeled text format for TTS.

    Format per line: "Speaker: text"
    """
    out = []
    for scene in script["scenes"]:
        out.append(f"Narator: [{scene['location']}]")
        for line in scene["lines"]:
            out.append(f"{line['speaker']}: {line['text']}")
    return "\n".join(out)


def speakers_in_script(script):
    """Return the ordered list of unique speakers in a script."""
    seen = []
    for scene in script["scenes"]:
        for line in scene["lines"]:
            if line["speaker"] not in seen:
                seen.append(line["speaker"])
    return seen
