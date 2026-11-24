"""Word count and runtime check for every part script in a series.

Usage: python tools/vo_stats.py series/001-some-series [--wpm 170] [--target 75,105] [--gap 0]
Counts the words between <!-- VO:START --> and <!-- VO:END --> in each part-*/script*.md.
Delivery [tags], {SPEAKER} names and (pause N) lines aren't spoken; pauses and --gap seconds between
paragraphs are added to the runtime. Horror (cast) series: --wpm 150 --target 60,80 --gap 0.3
"""
import argparse
import pathlib
import re

parser = argparse.ArgumentParser()
parser.add_argument("series_dir")
parser.add_argument("--wpm", type=float, default=170, help="narrator speaking rate (words per minute)")
parser.add_argument("--target", default="75,105", help="allowed runtime range in seconds")
parser.add_argument("--gap", type=float, default=0.0, help="silence between paragraphs (cast-mode voiceovers)")
args = parser.parse_args()
TARGET_SECONDS = tuple(float(x) for x in args.target.split(","))

scripts = sorted(pathlib.Path(args.series_dir).glob("part-*/script*.md"))
if not scripts:
    raise SystemExit(f"No part-*/script*.md files found in {args.series_dir}")

for script in scripts:
    text = script.read_text(encoding="utf-8")
    match = re.search(r"<!-- VO:START -->(.*?)<!-- VO:END -->", text, re.S)
    if not match:
        print(f"{script}: no VO block")
        continue
    vo = match.group(1)
    pauses = sum(float(x) for x in re.findall(r"\(pause\s+([\d.]+)s?\)", vo))
    paras = len([p for p in re.split(r"\n\s*\n", vo) if p.strip() and not re.fullmatch(r"\s*\(pause[^)]*\)\s*", p)])
    vo = re.sub(r"\(pause[^)]*\)|\{[^}]*\}", " ", vo)
    untagged = re.sub(r"\[[^\]]*\]", " ", vo)  # delivery tags aren't spoken
    lines = [l.strip() for l in untagged.splitlines() if l.strip()]
    words = sum(len(l.split()) for l in lines)
    sentences = [s for s in re.split(r"[.!?]+[\"”']?\s", " ".join(lines)) if s.strip()]
    longest = max(len(s.split()) for s in sentences)
    seconds = words / args.wpm * 60 + pauses + args.gap * max(paras - 1, 0)
    flag = "" if TARGET_SECONDS[0] <= seconds <= TARGET_SECONDS[1] else f"  <-- outside {TARGET_SECONDS[0]:g}-{TARGET_SECONDS[1]:g}s"
    print(f"{script.parent.name}/{script.name}: {words} words, ~{seconds:.0f}s, "
          f"avg {words / len(sentences):.1f} words/sentence, longest {longest}{flag}")
