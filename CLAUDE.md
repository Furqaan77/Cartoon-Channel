# CORTOON CHANNEL

**Midnight Parts** (@midnightparts): a short-form serialized suspense channel on Instagram Reels and YouTube Shorts. The bios, descriptions and brand hashtag (#MidnightParts) are in `channel/PROFILE.md`. Each story runs 3–10 parts of about 90 seconds each.

**Start of every new chat:** read [HANDOFF.md](HANDOFF.md) (current state and exact next steps), [WORKING-RULES.md](WORKING-RULES.md) (the owner's standing preferences and lessons learned) and [README.md](README.md) (setup and pipeline). On a new PC, also read [MOVING-PC.md](MOVING-PC.md) and [research/free-tools-plan.md](research/free-tools-plan.md): the owner wants Claude to make whole videos using free local tools only, with ElevenLabs as the one paid API. Keep HANDOFF.md and `series/INDEX.md` up to date whenever a part is written, rendered or a vote result comes in.

## When the user asks for a story, an idea, a series, or the next part
Follow the `story-series` skill (`.claude/skills/story-series/SKILL.md`, also invocable as `/story-series`). Never answer with just an idea in chat. Deliver the full series plan, one folder per part, and a finished script for every part, then summarise the whole plan in chat.

## Two kinds of series (both run at the same time)
- **Suspense series** (001–002, *The Ship Kept Going*): ~90s parts. The user supplies images **and** the voiceover.
- **Horror series** (003 on, the @zerotales.stories format, see `research/competitor-reels/zerotales.stories.md` and playbook §16): 60–80s parts, "you" POV, a vote every part, red captions. **The user only supplies images; Claude writes everything and generates the voiceover with a cast of character voices** (`series/NNN/voices.json`).

## Layout
- `playbook/SERIAL-SUSPENSE-PLAYBOOK.md`: the craft rules (hooks, retention, structure, endings, publishing)
- `playbook/templates/`: `series-plan.md`, `part-script.md` and `image-prompts.md`
- `research/competitor-reels/`: transcripts and beat maps of the reference pages (@beanie.escape, @saveo.house)
- `library/LIBRARY.md`: the shared sound library (`library/sfx/`, `library/music/`). Each sound is generated once and reused in every part and series. Check here before generating any sound; add new ones to the table.
- `series/INDEX.md`: every series and its status
- `series/NNN-slug/00-SERIES-PLAN.md`, plus `series/NNN-slug/part-NN/script.md` for each part. Part folders also hold that part's production assets.
- `tools/vo_stats.py`: VO word count and runtime check (`python tools/vo_stats.py series/NNN-slug`; for a horror series add `--wpm 150 --target 60,80 --gap 0.3`)
- `tools/make_voiceover.py`: generates `part-NN/audio/voiceover.mp3` plus word timings with ElevenLabs v4, which reads the delivery tags (`python tools/make_voiceover.py series/NNN-slug/part-NN`). Needs `ELEVENLABS_API_KEY` in `.env`. **Cast mode:** when the series folder has a `voices.json`, each VO paragraph is voiced by the speaker named at its start (`{LILY} [whispering] "…"`; no name means the narrator), `(pause 1.2)` inserts silence, lines are cached in `audio/_lines/` (only changed lines are regenerated), and `voiceover.lines.json` records who speaks when. The API key can't list voices, so cast from known premade IDs and test a line first.
- `series/NNN-slug/reference/character-prompts.md`: the series' character and location reference-image prompts, plus its text-card styles. The generated images are copied into every part as `part-NN/reference-images/` (the same 10 files in each).
- `tools/make_library.py`: generates whatever is still ⬜ in `library/LIBRARY.md` (ElevenLabs sound effects and music) and marks it ✅.
- `tools/build_part.py`: renders the finished reel in one pass as `part-NN/part-NN-instagram.mp4` and `part-NN/part-NN-youtube.mp4` (identical files, one top-quality encode: CRF 12, preset slower, tune animation, 320k AAC) plus `part-NN/cover.jpg`, from `part-NN/edit.json` (shots anchored to voiceover phrases, camera moves, overlays, cards, HUD (TIME + STRENGTH, or `"mode": "days"` for DAYS LEFT), captions, sound effects, music). Check the layout first with `--preview 0,12.5,...` (PNGs in `part-NN/preview/`). A series can set `"accent"` (e.g. horror red `#E3262E`, replacing the channel yellow in captions, chips and vote buttons) and `"corner_tag": "PART N"` (a small tag top-left on every frame). For series 001–002 the user supplies the voiceover MP3; if it has no `voiceover.words.json`, transcribe it locally with `python -I -X utf8 tools/transcribe.py <mp3> <part>/audio/voiceover.words.json` (faster-whisper `medium.en`, CPU, word timestamps).
- `series/NNN-slug/part-NN/publish.md`: the posting kit for each part, covering the Instagram caption, hashtags and pinned comment, and the YouTube title, description, tags, pinned comment and settings. Write one for every finished part, and never reveal the part's twist in it. Every Instagram caption must also contain a search phrase as a normal sentence ("interactive horror story", "survival story"), because Instagram search reads the caption text, not the hashtags. Lint it with `python .claude/skills/ig-caption/caption.py caption.txt --keywords "horror story"`. The test results for the installed ig-audit, ig-caption and ig-viral skills are in `research/ig-skills-findings.md`.
- `tools/make_image_brief.py`: builds `part-NN/image-brief.pdf` (references to attach, the filename to save as, and the prompt after a "Prompt -" label, with none of the edit notes) plus a `part-NN/image-brief-references/` folder of plain PNGs (only the reference images that part uses; no zip). References that aren't made yet show in the PDF as "MAKE FIRST" placeholders. It's for handing image generation to another person. Run `python tools/make_image_brief.py series/NNN-slug/part-NN` after every change to `image-prompts.md`.
- `series/NNN-slug/part-NN/image-prompts.md`: one complete, copy-paste image prompt per shot in the house look, with on-screen text and a camera move for each. Generated stills go in `part-NN/images/NN.png`.

## Permanent main character: YOU (locked)
Every story stars the same main character: `channel/characters/you/` (spec in `CHARACTER.md`, master sheet `you.png`).
- Never redesign him or change his face, hair, proportions, style or outfit: messy black hair, white egg-shaped head, simple black oval eyes, the open yellow windbreaker, the white T-shirt, navy shorts and black flip-flops. Change any of it only if the user explicitly asks.
- Stories change only his expressions, poses, surroundings and physical state.
- Use the locked prompt phrases from `CHARACTER.md` word for word in every image prompt, and copy `you.png` and `you-wet.png` into every part's `reference-images/`.
- Don't write a new turnaround prompt for him in a series' `character-prompts.md`; point to the channel file instead. Supporting characters are designed per series and must not wear yellow.

## House visual style
Copy the reference reels (@saveo.house, @beanie.escape):
- 2D hand-drawn cartoon with bold black ink outlines.
- Stick-figure characters with white egg-shaped heads and thin black limbs, against richly detailed, moody backgrounds.
- One still image per shot (a new image every 3–6s), moved in the edit, with saveo-style cream or dark text cards in between.
- Always 9:16 vertical. All on-screen text is added in the edit, never by the image model.
