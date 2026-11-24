"""Generate a part's voiceover with ElevenLabs, plus word timings for captions.

Usage: python tools/make_voiceover.py series/003-some-series/part-01 [--redo] [--voice-id ID] [--model eleven_v4]
Reads ELEVENLABS_API_KEY from the environment or from .env in the project root.
Writes <part>/audio/voiceover.mp3, voiceover.words.json and (cast mode) voiceover.lines.json.

Two modes:
  * Cast mode (the series folder has a voices.json): every VO paragraph is voiced on its own by the speaker
    named at its start, e.g.  {LILY} [whispering, scared] "Which one of you is real?"
    A paragraph without a {NAME} is read by the default voice (the narrator). A paragraph that is only
    (pause 1.5) inserts that many seconds of silence. Each line's audio is cached in audio/_lines/, so after
    a script edit only the changed lines are regenerated (--redo regenerates everything).
  * Single-voice mode (no voices.json): the whole VO is read by one voice, as before.

voices.json:
  {"model": "eleven_v4", "default": "NARRATOR", "gap": 0.3,
   "voices": {"NARRATOR": {"id": "...", "stability": 0.5, "similarity": 0.75}, "LILY": {"id": "..."}}}
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess

import imageio_ffmpeg
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAX_CHARS = 2000  # reliable per-request limit for text-to-dialogue
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SR = 44100

parser = argparse.ArgumentParser()
parser.add_argument("part_dir")
parser.add_argument("--voice-id", default="pNInz6obpgDQGcFmaJgB", help="single-voice mode; default: Adam (deep, calm male narrator)")
parser.add_argument("--model", default="eleven_v4", help="eleven_v4 reads the [delivery tags]; eleven_multilingual_v2 ignores them")
parser.add_argument("--stability", type=float, default=0.5, help="lower = more expressive")
parser.add_argument("--similarity", type=float, default=0.75)
parser.add_argument("--redo", action="store_true", help="cast mode: regenerate every line, ignoring the cache")
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


def vo_paragraphs(script):
    match = re.search(r"<!-- VO:START -->(.*?)<!-- VO:END -->", script.read_text(encoding="utf-8"), re.S)
    if not match:
        raise SystemExit(f"No VO block in {script}")
    if "{{" in match.group(1):
        raise SystemExit("Fill in the {{...}} placeholders (vote % / top comment) before recording.")
    return [" ".join(p.split()) for p in match.group(1).split("\n\n") if p.strip()]


def chunk(paragraphs):
    chunks, current = [], ""
    for p in paragraphs:
        if current and len(current) + len(p) + 2 > MAX_CHARS:
            chunks.append(current)
            current = p
        else:
            current = f"{current}\n\n{p}" if current else p
    return chunks + [current]


def synthesize(client, text, voice_id, model, stability, similarity):
    if model.startswith("eleven_v4"):
        from elevenlabs import DialogueInput
        audio = client.text_to_dialogue.convert(
            inputs=[DialogueInput(text=text, voice_id=voice_id)],
            model_id=model,
            settings={"stability": stability, "similarity": similarity},
        )
    else:
        audio = client.text_to_speech.convert(text=text, voice_id=voice_id, model_id=model)
    return b"".join(audio)


def decode(data_or_path):
    cmd = [FFMPEG, "-nostdin", "-v", "error", "-i", "pipe:0" if isinstance(data_or_path, bytes) else str(data_or_path),
           "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]
    out = subprocess.run(cmd, input=data_or_path if isinstance(data_or_path, bytes) else None, capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32).copy()


def trim(x, thresh_db=-45, pad=0.04):
    """Cut the silence the model leaves at both ends of a line, keeping a short pad."""
    win = int(0.01 * SR)
    n = len(x) // win
    if n == 0:
        return x
    rms = np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12)
    loud = np.where(20 * np.log10(rms) > thresh_db)[0]
    if not len(loud):
        return x[:0]
    a = max(0, loud[0] * win - int(pad * SR))
    b = min(len(x), (loud[-1] + 1) * win + int(pad * SR))
    return x[a:b]


def level(x, target_db=-20.0):
    """Bring every line to the same speech loudness, so voices sit evenly in the mix."""
    loud = x[np.abs(x) > 0.01]
    if not len(loud):
        return x
    gain = 10 ** ((target_db - 20 * np.log10(np.sqrt((loud ** 2).mean()) + 1e-9)) / 20)
    return np.clip(x * gain, -0.99, 0.99)


part = pathlib.Path(args.part_dir)
out_dir = part / "audio"
out_dir.mkdir(exist_ok=True)
mp3 = out_dir / "voiceover.mp3"
cast_file = part.resolve().parent / "voices.json"

from elevenlabs.client import ElevenLabs

client = ElevenLabs(api_key=load_key())
paragraphs = vo_paragraphs(part / "script.md")

if cast_file.exists():
    cast = json.loads(cast_file.read_text(encoding="utf-8"))
    model = cast.get("model", args.model)
    voices, default, gap = cast["voices"], cast.get("default", "NARRATOR"), cast.get("gap", 0.3)
    cache = out_dir / "_lines"
    cache.mkdir(exist_ok=True)
    track, lines, used, t = [], [], set(), 0.0
    for i, p in enumerate(paragraphs):
        m = re.fullmatch(r"\(pause\s+([\d.]+)s?\)", p)
        if m:
            track.append(np.zeros(int(float(m.group(1)) * SR), np.float32))
            t += float(m.group(1))
            continue
        m = re.match(r"\{([A-Z0-9_ -]+)\}\s*", p)
        speaker = m.group(1).strip() if m else default
        text = p[m.end():] if m else p
        if speaker not in voices:
            raise SystemExit(f"Speaker {{{speaker}}} isn't in {cast_file}")
        v = voices[speaker]
        settings = (v["id"], model, v.get("stability", 0.5), v.get("similarity", 0.75))
        key = hashlib.sha1(json.dumps([text, *settings]).encode()).hexdigest()[:12]
        f = cache / f"{i:02d}-{speaker.lower()}-{key}.mp3"
        if args.redo or not f.exists():
            print(f"  voicing {speaker:<9} {text[:70]}")
            f.write_bytes(synthesize(client, text, *settings))
        used.add(f)
        clip = level(trim(decode(f.read_bytes())))
        if track:
            track.append(np.zeros(int(gap * SR), np.float32))
            t += gap
        lines.append({"speaker": speaker, "text": re.sub(r"\[[^\]]*\]\s*", "", text), "start": round(t, 2), "end": round(t + len(clip) / SR, 2)})
        track.append(clip)
        t += len(clip) / SR
    for old in cache.glob("*.mp3"):  # drop cached lines the script no longer uses
        if old not in used:
            old.unlink()
    audio = np.concatenate(track + [np.zeros(int(0.3 * SR), np.float32)])
    subprocess.run([FFMPEG, "-y", "-v", "error", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-i", "-",
                    "-c:a", "libmp3lame", "-b:a", "256k", str(mp3)], input=audio.tobytes(), check=True)
    (out_dir / "voiceover.lines.json").write_text(json.dumps(lines, indent=1, ensure_ascii=False), encoding="utf-8")
else:
    pieces = []
    for i, text in enumerate(chunk(paragraphs)):
        piece = out_dir / f"_chunk{i}.mp3"
        piece.write_bytes(synthesize(client, text, args.voice_id, args.model, args.stability, args.similarity))
        pieces.append(piece)
    if len(pieces) == 1:
        pieces[0].replace(mp3)
    else:
        listing = out_dir / "_chunks.txt"
        listing.write_text("".join(f"file '{p.name}'\n" for p in pieces), encoding="utf-8")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(mp3)], check=True)
        for p in pieces + [listing]:
            p.unlink()

# Word timings for burned-in captions, from the generated audio itself.
from faster_whisper import WhisperModel

raw = subprocess.run([FFMPEG, "-nostdin", "-i", str(mp3), "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True).stdout
audio16 = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
segments, _ = WhisperModel("medium.en", device="cpu", compute_type="int8").transcribe(audio16, word_timestamps=True, language="en", beam_size=5)
words = [{"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)} for s in segments for w in s.words]

# Whisper sometimes drops punctuation and capitals. Where its words match the script, take the script's spelling,
# so captions get "Lily?" and "inside." back (and group on punctuation); mismatches (numbers etc.) keep Whisper's.
import difflib

script_words = [w for p in paragraphs if not re.fullmatch(r"\(pause[^)]*\)", p)
                for w in re.sub(r"^\{[^}]*\}\s*|\[[^\]]*\]\s*", "", p).split()]
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))
sm = difflib.SequenceMatcher(None, [norm(w["word"]) for w in words], [norm(w) for w in script_words], autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            words[i1 + k]["word"] = script_words[j1 + k]
(out_dir / "voiceover.words.json").write_text(json.dumps(words, indent=1), encoding="utf-8")

duration = len(audio16) / 16000
print(f"{mp3}: {duration:.1f}s, {len(words)} words, {len(words) / duration * 60:.0f} wpm")
