# Midnight Parts: serialized story reels

A production workspace for **Midnight Parts**: short serialized suspense and horror stories for Instagram Reels and YouTube Shorts. Each story runs 3–10 parts. The viewer is "YOU" (a locked cartoon character), and the comments vote on what happens next.

**Status and next steps:** [HANDOFF.md](HANDOFF.md) · **Owner's rules:** [WORKING-RULES.md](WORKING-RULES.md) · **Project instructions for Claude:** [CLAUDE.md](CLAUDE.md)

## Folder map

| Path | What's there |
|---|---|
| `channel/` | `PROFILE.md` (bios, handles, hashtags) and `characters/you/` (the locked main character: spec + reference sheets) |
| `playbook/SERIAL-SUSPENSE-PLAYBOOK.md` | The craft rules: hooks, retention, structure, endings, votes, visuals, publishing |
| `playbook/templates/` | Templates for a series plan, a part script and an image-prompt file |
| `research/competitor-reels/` | Transcripts and beat maps of @saveo.house, @beanie.escape and @zerotales.stories |
| `research/ig-skills-findings.md` | Instagram numbers and the results of testing the ig-* skills |
| `library/` | The shared sound library (`sfx/`, `music/`, listed in `LIBRARY.md`). It's generated once and reused everywhere |
| `series/INDEX.md` | Every series and its status |
| `series/NNN-slug/` | One series: `00-SERIES-PLAN.md`, `reference/` (character and location prompts), `reference-brief/` (a PDF to hand off the reference images), `voices.json` (horror only) and `part-NN/` |
| `tools/` | The production pipeline (below) |
| `tools/generators/` | An archive of one-off scripts that wrote whole seasons |
| `.claude/skills/` | Project skills: `story-series` (how to write a series), `ig-caption`, `ig-viral`, `ig-audit` |

### Inside a part folder (`series/NNN-slug/part-NN/`)

| File | Made by | Purpose |
|---|---|---|
| `script.md` | Claude | VO (between `<!-- VO:START/END -->`), shot list, caption, quality gate |
| `image-prompts.md` | Claude | One copy-paste prompt per still |
| `image-brief.pdf` + `image-brief-references/` | `make_image_brief.py` | The hand-off for whoever generates the images |
| `reference-images/` | copied | The series' reference sheets (YOU, cast, locations) |
| `images/NN.png` | **owner** | The generated stills |
| `audio/voiceover.mp3` | owner (suspense) or `make_voiceover.py` (horror) | The voiceover |
| `audio/voiceover.words.json` | `transcribe.py` or `make_voiceover.py` | Word timings that drive the edit and the captions |
| `edit.json` | Claude | The edit: shots, moves, overlays, cards, HUD, vote, music, sfx |
| `part-NN-instagram.mp4`, `part-NN-youtube.mp4`, `cover.jpg` | `build_part.py` | The finished reel (both MP4s identical) |
| `publish.md` | Claude | The posting kit (captions, hashtags, titles, pinned comments). Never reveals the twist |

## Setup (Windows)
Moving to a new PC? Follow [MOVING-PC.md](MOVING-PC.md), which has the full install list and checks.
```bash
python -m pip install -r requirements.txt
```
- `.env` in the project root must hold `ELEVENLABS_API_KEY=...`. Never commit or paste it.
- Chrome or Edge must be installed; it prints the image-brief PDFs.
- The ffmpeg command line (`winget install Gyan.FFmpeg`) is used for checks and audio cuts.
- For the planned 3D format, install Blender (free); see [research/free-tools-plan.md](research/free-tools-plan.md).
- Run scripts with `python -X utf8 ...` to avoid Windows encoding errors.

## Pipeline: making one part

1. **Write.** The `story-series` skill produces the plan, the scripts and the image prompts. Check lengths with `python tools/vo_stats.py series/NNN-slug` (horror: `--wpm 150 --target 60,80 --gap 0.3`).
2. **Hand off images.** Run `python tools/make_image_brief.py series/NNN-slug/part-NN`. The owner generates the stills into `images/`.
3. **Voiceover.**
   - Horror: `python tools/make_voiceover.py series/NNN-slug/part-NN` (cast mode reads `voices.json`; only changed lines regenerate).
   - Suspense: the owner's MP3 goes to `audio/voiceover.mp3`. Then run `python -I -X utf8 tools/transcribe.py audio/voiceover.mp3 audio/voiceover.words.json`.
4. **Edit.** Write `edit.json`. Copy the closest previous part's file as a template:
   - horror: `series/003-dont-let-me-in/part-02/edit.json`;
   - suspense: `series/002-the-ship-kept-going-s2/part-05/edit.json`.
5. **Preview.** Run `python tools/build_part.py series/NNN-slug/part-NN --preview 0,12.5,40`. The PNGs go to `part-NN/preview/`.
6. **Render.** Run `python tools/build_part.py series/NNN-slug/part-NN` (CRF 12, slower, 320k AAC).
7. **Check.** Loudness should be about −14 LUFS, the two MP4s identical (`cmp`), and the length on target.
8. **Publish kit.** Write `publish.md`, then lint the caption with `python -X utf8 .claude/skills/ig-caption/caption.py caption.txt --keywords "horror story"`.
9. **Sounds.** If you need a new sound, add a ⬜ row to `library/LIBRARY.md` and run `python tools/make_library.py`.

## `edit.json` cheat sheet (full details in the `tools/build_part.py` docstring)

**Top level:**
- `tail`
- `accent` (`"#E3262E"` for horror)
- `corner_tag` (`"PART N"`)
- `caption_y`, `caption_size`
- `caption_fixes` (`{"heard": "shown"}`)
- `caption_keys` (words drawn in the accent color)
- `hud`: either `{"mode":"days","total":7,"values":[{"at":0,"days":4}]}` or the TIME + STRENGTH form from Season 1
- `shots`, `music`, `sfx`

**Anchors (`at`, `until`, `from`, `to`):**
- `0` (seconds)
- `"phrase"` (the first time those words are spoken)
- `"phrase@2"` (the second time)
- `"phrase+0.3"` (an offset in seconds)
- `"#05"` (the start of shot 05)
- `"end"`

**A shot:** `{"id","at","image","move":{"keys":[[t,zoom,x,y],…],"shake":[…]},"sat","captions":false,"overlays":[…]}`
- Instead of an image, a shot can be a `card` (`style` cream/dark, `label`, `line`, `keys`, `small`, `diagram`), a `phone` mock-up or a `vote`.
- **Overlay types:**
  - `chip`: a small label
  - `big`: a title, with `size`, `max_w` and `pop`
  - `mono`: plain text, with `color` and `stroke`
  - `vote_buttons`: `a`, `b`, `a_at`, `b_at`, `a_pos`, `b_pos`
- **Vote:** `{"images":["16A.png","16B.png"],"top":"PART 3 TOMORROW · YOU DECIDE","band_y":[0.335,0.695],"band_h":680,"focus_y":[0.5,0.5]}`.

**Music and sfx entries:** `{"file","from"/"at","to","gain","fade_in","fade_out","src_offset","loop"}`. Music ducks under the VO (`duck_db`).
