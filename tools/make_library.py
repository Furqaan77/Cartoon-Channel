"""Generate the missing sounds in library/LIBRARY.md with ElevenLabs, then mark them done.

Usage: python tools/make_library.py [--only name1,name2] [--dry-run]
Reads ELEVENLABS_API_KEY from the environment or from .env in the project root.
Each ⬜ row is generated once into library/sfx/ or library/music/ and its status flips to ✅.
Rows already ✅, or whose file already exists, are never regenerated.
"""
import argparse
import os
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "library"
INDEX = LIB / "LIBRARY.md"

parser = argparse.ArgumentParser()
parser.add_argument("--only", help="comma-separated file names (without .mp3) to generate")
parser.add_argument("--dry-run", action="store_true", help="list what would be generated and stop")
args = parser.parse_args()


def load_key():
    if os.getenv("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"]
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            name, _, value = line.partition("=")
            if name.strip() == "ELEVENLABS_API_KEY":
                return value.strip().strip("\"'")
    raise SystemExit(f"ELEVENLABS_API_KEY not found. Add a line ELEVENLABS_API_KEY=... to {env}")


def rows(text):
    """Yield (line, kind, file, seconds, loop, prompt) for every table row with a status cell."""
    kind = None
    for line in text.splitlines():
        if line.startswith("## Sound effects"):
            kind = "sfx"
        elif line.startswith("## Music"):
            kind = "music"
        elif line.startswith("## "):
            kind = None
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if kind and len(cells) >= 4 and cells[0] in ("⬜", "✅"):
            file = cells[1].strip("`")
            if kind == "sfx":
                yield line, kind, file, float(cells[2]), cells[3] == "✓", cells[4], cells[0]
            else:
                yield line, kind, file, float(cells[2]), False, cells[3], cells[0]


text = INDEX.read_text(encoding="utf-8")
only = set(args.only.split(",")) if args.only else None
todo = []
for line, kind, file, secs, loop, prompt, status in rows(text):
    out = LIB / kind / file
    if only and pathlib.Path(file).stem not in only:
        continue
    if status == "✅" or out.exists():
        continue
    todo.append((line, kind, file, secs, loop, prompt, out))

print(f"{len(todo)} to generate")
for _, kind, file, secs, loop, _, _ in todo:
    print(f"  {kind:5} {file} {secs:g}s{' loop' if loop else ''}")
if args.dry_run or not todo:
    raise SystemExit

from elevenlabs.client import ElevenLabs  # noqa: E402

client = ElevenLabs(api_key=load_key())
for line, kind, file, secs, loop, prompt, out in todo:
    print(f"-> {file} ...", flush=True)
    try:
        if kind == "sfx":
            audio = client.text_to_sound_effects.convert(
                text=prompt, duration_seconds=secs, loop=loop, prompt_influence=0.5,
                model_id="eleven_text_to_sound_v2", output_format="mp3_44100_128")
        else:
            audio = client.music.compose(prompt=prompt, music_length_ms=int(secs * 1000),
                                         force_instrumental=True, output_format="mp3_44100_128")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(b"".join(audio))
    except Exception as e:  # keep going; the row stays ⬜ so a rerun retries it
        print(f"   FAILED: {getattr(e, 'body', None) or str(e)[:300]}")
        continue
    text = text.replace(line, line.replace("⬜", "✅", 1), 1)
    INDEX.write_text(text, encoding="utf-8")
    print(f"   saved {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")
