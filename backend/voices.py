"""Voice rendering for Sandiwara AI.

Maps each character to a distinct TTS voice and renders a script to a
single MP3 using the system `tts synthesize-script` command (multi-speaker,
parallel synthesis, concatenation).
"""

import subprocess
import tempfile
import os

# Voice pool. Helio + Aria are the known good Indonesian voices; the
# vg_id_* voices are additional male voices from the voice catalog.
VOICE_POOL_MALE = [
    "avocado_v2:MAI_03",   # Helio
    "avocado_v2:vg_id_m44",
    "avocado_v2:vg_id_m41",
    "avocado_v2:vd2_r8_rep1k_0363_v068_28k_g5k",
]
VOICE_POOL_FEMALE = [
    "avocado_v2:MAI_01",   # Aria
]

NARRATOR_VOICE = "avocado_v2:MAI_03"


def assign_voices(characters):
    """Assign a distinct voice to each character.

    characters: list of {"name": ..., "gender": "male"|"female", ...}.
    Returns dict: character name -> voice id. The narrator always gets
    the narrator voice.
    """
    mapping = {"Narator": NARRATOR_VOICE}
    male_idx = 0
    female_idx = 0
    for ch in characters:
        name = ch["name"]
        gender = (ch.get("gender") or "male").lower()
        if gender == "female":
            voice = VOICE_POOL_FEMALE[female_idx % len(VOICE_POOL_FEMALE)]
            female_idx += 1
        else:
            # Skip the narrator voice for the first male character so the
            # hero does not sound identical to the narrator.
            voice = VOICE_POOL_MALE[(male_idx + 1) % len(VOICE_POOL_MALE)]
            male_idx += 1
        mapping[name] = voice
    return mapping


def render_script_to_mp3(script_text, voice_mapping, output_path, language="id"):
    """Render speaker-labeled script text to a single MP3.

    script_text: lines of "Speaker: text".
    voice_mapping: speaker name -> voice id.
    Returns (ok, error_message).
    """
    # Write the script to a temp file.
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    ) as f:
        f.write(script_text)
        script_path = f.name
    try:
        cmd = [
            "/opt/hatch/bin/tts", "synthesize-script",
            "--script", script_path,
            "--output", output_path,
            "--language", language,
        ]
        for speaker, voice in voice_mapping.items():
            cmd += ["--speaker", f"{speaker}={voice}"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode != 0:
            return False, (result.stderr or result.stdout or "TTS failed").strip()
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            return False, "TTS produced no audio file"
        return True, ""
    except subprocess.TimeoutExpired:
        return False, "TTS timed out"
    except Exception as e:  # noqa: BLE001
        return False, str(e)
    finally:
        try:
            os.unlink(script_path)
        except OSError:
            pass
