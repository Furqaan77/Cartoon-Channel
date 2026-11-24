"""Build a hand-off PDF for the person who generates a part's images, plus a folder with only the reference images they need.

Usage: python tools/make_image_brief.py series/001-some-series/part-02
Reads <part>/image-prompts.md and <part>/reference-images/.
Writes <part>/image-brief.pdf and <part>/image-brief-references/ (plain PNGs, no zip).
The PDF holds only what the artist needs: the references to attach, the filename to save as, and the prompt.
Edit moves, on-screen text and other notes in image-prompts.md are left out on purpose.
"""
import argparse
import base64
import html
import io
import pathlib
import re
import subprocess
import tempfile
import shutil

from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = next((p for p in ("C:/Program Files/Google/Chrome/Application/chrome.exe",
                           "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe") if pathlib.Path(p).exists()), None)
CHANNEL = "Midnight Parts"
REF_NOTES = {
    "you": "The main character, a turnaround sheet (front, side, back). Attach it whenever he is in the shot.",
    "you-wet": "The main character when wet (hair flat, jacket soaked).",
    "marcus": "Marcus, his older brother (beard, navy shirt, gold watch).",
    "table9": "The man from table 9 (bald, gray polo, steel dive watch).",
    "officer": "The ship's security officer.",
    "cabin": "The cabin (place).",
    "deck5-aft": "Deck 5 at the back of the ship (place).",
    "dining-room": "The ship's dining room (place).",
    "ship": "The cruise ship (place).",
    "medical-bay": "The medical bay (place).",
    "kerr": "Agent Kerr, the FBI agent (gray-streaked hair, round glasses, dark blazer, blue lanyard).",
    "lucia": "Lucía, the dive-shop owner (curly hair, red bandana, teal top, shark-tooth necklace).",
    "home": "Your house at night, seen from across the street (place).",
    "bedroom": "Your bedroom at night (place).",
    "isla-dock": "The ferry dock and pier on Isla Mujeres (place).",
    "dive-shop": "Lucía's dive shop (place).",
    "lily": "Lily, his little sister, 8 (light-brown pigtails with red ties, purple dinosaur nightshirt, pink shorts).",
    "pruitt": "Walt Pruitt, the old neighbor (white hair, round glasses, gray cardigan, plaid flannel, green boots).",
    "cabin-inside": "Inside the lake cabin at night (place).",
    "boathouse": "Inside the boathouse (place).",
    "dark-boat": "The boat with no lights (place).",
    "fishing-boat": "Doyle's rented sport-fishing boat (place).",
    "marina": "The marina at Puerto Morelos at night, with the leaning lighthouse (place).",
}

parser = argparse.ArgumentParser()
parser.add_argument("part_dir")
args = parser.parse_args()
PART = pathlib.Path(args.part_dir)
PART = PART if PART.is_absolute() else ROOT / PART
if CHROME is None:
    raise SystemExit("Chrome or Edge not found; needed to print the PDF.")
text = (PART / "image-prompts.md").read_text(encoding="utf-8")
series = PART.parent.name.split("-", 1)[1].replace("-", " ").title()
title_line = text.splitlines()[0].lstrip("# ").strip()          # Part 2, "Done": image prompts
part_title = title_line.replace(": image prompts", "")


def thumb(name, width):
    path = PART / "reference-images" / f"{name}.png"
    if not path.exists():  # a reference that still has to be made: show a placeholder
        img = Image.new("RGB", (width, int(width * 16 / 9)), (225, 222, 214))
        ImageDraw.Draw(img).text((width / 2, width * 8 / 9), "MAKE FIRST", fill=(120, 110, 90), anchor="mm")
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=82)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    img = Image.open(path).convert("RGB")
    img.thumbnail((width, width * 2))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------- parse
shots = []
for block in re.split(r"(?m)^### ", text)[1:]:
    head, _, body = block.partition("\n")
    sid = head.split("·")[0].strip()
    vo = re.search(r'"(.*)"', head)
    shot = {"id": sid, "vo": vo.group(1) if vo else "", "text_card": "TEXT CARD" in head,
            "reuse": "**REUSE**" in body, "refs": [], "images": []}
    m = re.search(r"\*\*Refs:\*\* (.*?)(?: ·|\n)", body + "\n")
    if m and m.group(1).strip() != "none":
        shot["refs"] = [r.strip() for r in m.group(1).split(",")]
    pending = None
    for line in body.splitlines():
        s = re.match(r"\*\*Save as:\*\* `(.+?)\.png`", line)
        if s:
            pending = s.group(1)
    for s, prompt in re.findall(r"\*\*Save as:\*\* `(.+?)\.png`\s+\*\*Prompt -\*\*\s+```text\n(.*?)\n```", body, re.S):
        shot["images"].append((s, prompt.strip()))
    shot["note"] = body.split("\n", 1)[0] if shot["reuse"] else ""
    shots.append(shot)

make = [s for s in shots if s["images"]]
n_images = sum(len(s["images"]) for s in make)
skip_text = [s["id"] for s in shots if s["text_card"]]
skip_reuse = [s for s in shots if s["reuse"]]
used_refs = []
for s in make:
    for r in s["refs"]:
        if r not in used_refs and not r.startswith("images/"):  # images/NN.png = an image made earlier in this batch
            used_refs.append(r)
squares = [name for s in make for name, prompt in s["images"] if "square 1:1" in prompt]
format_note = (f", except {', '.join(squares[:-1]) + ' and ' + squares[-1] if len(squares) > 1 else squares[0]}, "
               f"which {'are' if len(squares) > 1 else 'is'} <b>square 1:1</b>") if squares else " for every image"
missing = [r for r in used_refs if not (PART / "reference-images" / f"{r}.png").exists()]
if missing:
    print(f"warning: reference images not made yet (shown as placeholders): {missing}")

# ---------------------------------------------------------------- html
esc = html.escape
parts = []
parts.append(f"""
<div class="cover">
  <div class="kicker">{esc(CHANNEL)} · {esc(series)}</div>
  <h1>{esc(part_title)}</h1>
  <div class="sub">Image brief: {n_images} images to generate</div>
</div>

<div class="how">
  <h2>How to use this document</h2>
  <ol>
    <li><b>Attach the reference images</b> listed under <b>Attach</b> for each shot. They are in the folder of reference images that came with this PDF. They keep the characters and places looking identical in every image.</li>
    <li><b>Copy only the text after “Prompt -”</b>, the whole paragraph, and paste it into the image generator exactly as written. Don’t shorten it or change any words. The art style is already inside the prompt.</li>
    <li><b>Save each image with the name shown under “Save as”</b> (for example <code>01b.png</code>). The names are used by the editor, so please don’t rename them.</li>
    <li><b>Format:</b> vertical <b>9:16</b>{format_note}.</li>
    <li><b>No text, letters or logos</b> may appear inside any image. All text is added later. If any text shows up, generate again.</li>
    <li><b>Never change the main character</b> (messy black hair, white egg-shaped head, simple black oval eyes, bright yellow windbreaker, white T-shirt, navy shorts, black flip-flops). If the face, hair or outfit drifts, regenerate until it matches the reference.</li>
    <li>Generate a few options per shot and send the best one.</li>
  </ol>
  <div class="skip"><b>Not needed:</b> {esc(", ".join("shot " + i for i in skip_text))} are text cards{"; " if skip_reuse else ""}{esc("; ".join(f"shot {s['id']} reuses an existing image" for s in skip_reuse))}.</div>
</div>

<h2 class="pb">Reference images (attach these)</h2>
<div class="refgrid">""")
for r in used_refs:
    todo = "" if r not in missing else "<br><b>Not made yet: generate it first from the series' reference brief.</b>"
    parts.append(f'<div class="ref"><img src="{thumb(r, 330)}"><div><b>{esc(r)}.png</b><br>{esc(REF_NOTES.get(r, ""))}{todo}</div></div>')
parts.append("</div>")

parts.append(f'<h2 class="pb">The {n_images} prompts</h2>')
for s in make:
    refs_html = "".join(f'<span class="chip none">your {esc(r[7:])} (made earlier in this batch)</span>' if r.startswith("images/")
                        else f'<span class="chip"><img src="{thumb(r, 90)}">{esc(r)}.png</span>' for r in s["refs"]) \
        or '<span class="chip none">no reference needed</span>'
    for k, (name, prompt) in enumerate(s["images"]):
        label = f"Shot {s['id']}" if len(s["images"]) == 1 or k == 0 else f"Shot {s['id']}"
        ratio = "square 1:1" if "square 1:1" in prompt else "vertical 9:16"
        parts.append(f"""
<div class="shot">
  <div class="shothead"><span class="num">{esc(name)}</span><span class="vo">{esc(('Scene line: “' + s['vo'] + '”') if s['vo'] else '')}</span></div>
  <table class="meta">
    <tr><th>Save as</th><td><b>{esc(name)}.png</b> <span class="ratio">({ratio})</span></td></tr>
    <tr><th>Attach</th><td class="chips">{refs_html}</td></tr>
  </table>
  <div class="prompt"><span class="plabel">Prompt -</span> {esc(prompt)}</div>
</div>""")

css = """
@page { size: A4; margin: 14mm 14mm 16mm; }
* { box-sizing: border-box; }
body { font-family: "Segoe UI", Arial, sans-serif; color: #1b1b1f; font-size: 10.5pt; line-height: 1.45; margin: 0; }
.cover { padding: 18mm 0 8mm; border-bottom: 3px solid #FFC72C; margin-bottom: 8mm; }
.kicker { font-size: 10pt; letter-spacing: .14em; text-transform: uppercase; color: #6b6b75; }
h1 { font-size: 30pt; margin: 4px 0 2px; line-height: 1.1; }
.sub { font-size: 13pt; color: #44444d; }
h2 { font-size: 15pt; margin: 0 0 6px; }
.pb { break-before: page; }
.how ol { padding-left: 18px; margin: 6px 0 10px; }
.how li { margin: 0 0 6px; }
code { background: #f0eee6; padding: 0 4px; border-radius: 3px; font-family: Consolas, monospace; }
.skip { background: #f6f3e9; border-left: 4px solid #FFC72C; padding: 8px 10px; border-radius: 0 4px 4px 0; }
.refgrid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
.ref { break-inside: avoid; border: 1px solid #ddd; border-radius: 6px; padding: 6px; font-size: 9pt; }
.ref img { width: 100%; display: block; border-radius: 4px; margin-bottom: 4px; }
.shot { break-inside: avoid; border: 1px solid #d6d6dc; border-radius: 8px; padding: 10px 12px; margin: 0 0 10px; }
.shothead { display: flex; align-items: baseline; gap: 10px; margin-bottom: 6px; }
.num { background: #15120F; color: #FFC72C; font-weight: 700; font-size: 13pt; padding: 1px 9px; border-radius: 5px; font-family: Consolas, monospace; }
.vo { color: #6b6b75; font-size: 9pt; font-style: italic; }
.meta { border-collapse: collapse; margin-bottom: 8px; }
.meta th { text-align: left; font-weight: 600; color: #6b6b75; padding: 2px 12px 2px 0; vertical-align: middle; white-space: nowrap; font-size: 9.5pt; }
.meta td { padding: 2px 0; }
.ratio { color: #6b6b75; font-size: 9pt; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip { display: inline-flex; align-items: center; gap: 6px; border: 1px solid #d6d6dc; border-radius: 6px; padding: 2px 8px 2px 3px; font-size: 9pt; background: #fafafa; }
.chip img { height: 34px; border-radius: 3px; }
.chip.none { padding: 2px 8px; color: #6b6b75; }
.prompt { background: #f6f3e9; border-left: 4px solid #FFC72C; border-radius: 0 6px 6px 0; padding: 9px 12px; font-size: 10pt; }
.plabel { font-weight: 800; color: #15120F; background: #FFC72C; padding: 1px 7px; border-radius: 4px; margin-right: 4px; white-space: nowrap; }
"""
doc = f'<!doctype html><html><head><meta charset="utf-8"><title>{esc(part_title)} image brief</title><style>{css}</style></head><body>{"".join(parts)}</body></html>'

with tempfile.TemporaryDirectory() as tmp:
    src = pathlib.Path(tmp) / "brief.html"
    src.write_text(doc, encoding="utf-8")
    out = PART / "image-brief.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", src.as_uri()], check=True, capture_output=True, timeout=180)

refdir = PART / "image-brief-references"
refdir.mkdir(exist_ok=True)
for old in refdir.glob("*.png"):
    old.unlink()
for r in used_refs:
    if r not in missing:
        shutil.copy2(PART / "reference-images" / f"{r}.png", refdir / f"{r}.png")
(PART / "image-brief-references.zip").unlink(missing_ok=True)  # older briefs shipped a zip

print(f"images to make: {n_images} | text cards skipped: {skip_text} | reuse skipped: {[s['id'] for s in skip_reuse]}")
print(f"references used: {used_refs}")
print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB), {refdir.relative_to(ROOT)}/ ({len(list(refdir.glob('*.png')))} images)")
