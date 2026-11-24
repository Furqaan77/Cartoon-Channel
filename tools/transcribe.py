"""Transcribe a voiceover MP3 to word timings for the renderer (used when the user supplies the VO, series 001/002/004).

Usage: python -I -X utf8 tools/transcribe.py series/NNN-slug/part-NN/audio/voiceover.mp3 series/NNN-slug/part-NN/audio/voiceover.words.json
Runs faster-whisper medium.en on the CPU (int8), English, word timestamps. Takes a few minutes for a 90s VO.
Prints the transcript so you can spot mis-heard words; fix those in edit.json "caption_fixes" (never edit the timings by hand).
"""
import json
import subprocess
import sys

import imageio_ffmpeg
import numpy as np
from faster_whisper import WhisperModel

src, out = sys.argv[1], sys.argv[2]
raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", src, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                     capture_output=True, check=True).stdout
audio = np.frombuffer(raw, np.float32)
model = WhisperModel("medium.en", device="cpu", compute_type="int8")
segs, info = model.transcribe(audio, word_timestamps=True, language="en", beam_size=5)
words = [{"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)} for s in segs for w in s.words]
with open(out, "w", encoding="utf-8") as f:
    json.dump(words, f, indent=1)
print(len(words), "words; duration", round(info.duration, 2))
print(" ".join(w["word"] for w in words))
