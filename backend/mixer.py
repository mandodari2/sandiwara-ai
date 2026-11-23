"""Audio mixing for Sandiwara AI.

Takes the rendered voice MP3 and optionally layers background music
(ducked under dialogue) and sound effects, then exports a single
faststart MP3.
"""

import subprocess
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")


def _asset(name):
    path = os.path.join(ASSETS_DIR, name)
    return path if os.path.exists(path) else None


def mix_episode(voice_mp3, output_mp3, mood="tense", sfx_cues=None):
    """Mix voice audio with optional music bed. Returns (ok, error).

    - voice_mp3: the rendered dialogue MP3.
    - output_mp3: final mixed MP3 (faststart).
    - mood: music bed to use (tense/sad/triumphant/mysterious), if present.
    - sfx_cues: list of (timestamp_sec, sfx_name); only applied when the
      SFX file exists. Missing files are skipped, never fatal.
    """
    music = _asset(f"music_{mood}.mp3") or _asset("music_tense.mp3")

    if music is None and not sfx_cues:
        # Nothing to mix — just remux with faststart.
        cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-i", voice_mp3,
            "-c:a", "libmp3lame", "-b:a", "128k",
            "-movflags", "+faststart",
            output_mp3,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return False, (result.stderr or "ffmpeg failed").strip()
        return True, ""

    # Build a filter graph: voice at full volume, music ducked to ~18%.
    inputs = ["-i", voice_mp3]
    filter_parts = ["[0:a]volume=1.0[voice]"]
    mix_inputs = ["[voice]"]
    idx = 1
    if music is not None:
        inputs += ["-i", music]
        filter_parts.append(f"[{idx}:a]volume=0.18,aloop=loop=-1:size=2e+09[music]")
        mix_inputs.append("[music]")
        idx += 1
    # SFX cues are layered at their timestamps (adelay + amix).
    # For the hackathon MVP we layer at most the first 3 cues.
    for ts, sfx_name in (sfx_cues or [])[:3]:
        sfx_path = _asset(f"sfx_{sfx_name}.mp3")
        if sfx_path is None:
            continue
        inputs += ["-i", sfx_path]
        delay_ms = int(ts * 1000)
        filter_parts.append(
            f"[{idx}:a]volume=0.6,adelay={delay_ms}|{delay_ms}[sfx{idx}]"
        )
        mix_inputs.append(f"[sfx{idx}]")
        idx += 1

    filter_complex = (
        ";".join(filter_parts)
        + ";"
        + "".join(mix_inputs)
        + f"amix=inputs={len(mix_inputs)}:duration=first:normalize=0[aout]"
    )
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[aout]",
        "-c:a", "libmp3lame", "-b:a", "128k",
        "-movflags", "+faststart",
        output_mp3,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        return False, (result.stderr or "ffmpeg mix failed").strip()
    return True, ""
