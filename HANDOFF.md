# HANDOFF: where the project stands (as of 2026-11-24)

> **New chat or new account? Start here.** Read in this order:
> 1. [CLAUDE.md](CLAUDE.md): project rules (loaded automatically).
> 2. [WORKING-RULES.md](WORKING-RULES.md): the owner's preferences and lessons learned.
> 3. This file: the current state and the exact next steps.
> 4. [README.md](README.md): setup and the pipeline.
> 5. **On a new PC:** [MOVING-PC.md](MOVING-PC.md) (setup and checks), then [research/free-tools-plan.md](research/free-tools-plan.md) (the new direction).
>
> Then open the series plan you're working on (`series/NNN-slug/00-SERIES-PLAN.md`).

## The channel
- **Midnight Parts.**
  - Instagram: currently **@midnight_parts_1**. The owner is moving content to a new account/ID; update `channel/PROFILE.md` and any `publish.md` handles once the new handle is known.
  - YouTube: **@midnightparts**.
- **Public numbers so far (2026-11-14):**
  - S2 Part 3 had 349 likes and 18 comments (5.2% comments per like, strong engagement but small reach).
  - Part 1s get 3–4× the likes of later parts on every account we studied.
  - YouTube is barely used (1 Short, 8 views).
  - Details: [research/ig-skills-findings.md](research/ig-skills-findings.md).
- **Still to do:** the `ig-audit` skill needs the owner's Instagram Insights screenshots (reach, views, watch time, follows per reel), which haven't been provided yet.

## ⭐ New direction (2026-11-24): Claude makes the whole video, using free tools only
- The owner **no longer wants to generate images**. They also **won't pay for any API except ElevenLabs**, so no Gemini, OpenAI or fal.
- They showed the format they want: [@theoddtilt's 3D "every fix makes it worse" reel](research/competitor-reels/theoddtilt.md) (39s, low-poly 3D, "you" POV, fast deadpan narrator, one-word white captions).
- **Two PCs from now on:**
  - The **old PC** continues the running series (Ship S3 Parts 4–5). It holds all the media.
  - The **new, more powerful PC** starts the new free-tools formats.
  - They sync through GitHub: **https://github.com/Furqaan77/Cartoon-Channel** (text, tools, character and sound library; no MP4s or per-part media, and no `.env`).
  - Setup for the new PC is in [MOVING-PC.md](MOVING-PC.md). `git pull` before working and push after.
- **Plan** ([research/free-tools-plan.md](research/free-tools-plan.md)):
  1. On the new PC, run the checks and record the GPU and VRAM.
  2. Install **Blender** (free) and make a **40s test reel** in that format starring YOU, built as a locked 3D asset. The owner judges it.
  3. If approved, make it a regular format. Optionally test free local image AI (ComfyUI with Flux Kontext / Qwen-Image-Edit) to make the 2D series' stills too.
- The running series continue in parallel (below).

## Series status

| # | Series | State | Votes so far |
|---|---|---|---|
| 001 | The Ship Kept Going, S1 | ✅ Complete, all 5 rendered + posting kits | FLOAT, KEEP, SIGNAL, TELL |
| 002 | The Ship Kept Going, S2 "Twelve Words" | ✅ Complete, all 5 rendered + posting kits | CALL, BURN, TEST, BROTHER |
| 003 | Don't Let Me In (horror) | ✅ Complete, all 5 rendered + posting kits | LOCK, PULL, GRAB, WINDOW |
| 004 | The Ship Kept Going, S3 "Man Overboard" | **Parts 1–3 rendered**; Parts 4–5 written + image prompts + PDFs | TELL, QUIET; P3 RUN/STAY pending |

### 003, *Don't Let Me In* (horror; Claude makes the VO)

| Part | Script | Images | VO | Rendered | Vote at end |
|---|---|---|---|---|---|
| 1 | ✅ | ✅ | ✅ | ✅ 76.2s | LOCK / HIDE → **LOCK won** |
| 2 | ✅ | ✅ | ✅ | ✅ 76.9s | PULL / LISTEN → **PULL won** |
| 3 | ✅ PULL version (LISTEN version kept at the bottom) | ✅ | ✅ 72.7s | ✅ 73.8s | GRAB / TALK → **GRAB won** |
| 4 | ✅ GRAB version (TALK version kept below it) | ✅ | ✅ 60.1s | ✅ 61.3s | WINDOW / BOAT → **WINDOW won** |
| 5 | ✅ WINDOW version (BOAT version kept below it) | ✅ | ✅ 73.5s | ✅ 75.3s | finale: YES/NO comment ask + follow |

**The series is complete.** The finale added two reusable library sounds: `sfx/morning-birds.mp3` and `music/dawn-relief.mp3` (a warm sunrise bed).
- Its sting (Ruth waving, dripping) is the open door for a possible *Don't Let Me In* Season 2. The next horror series could be that or a new story; a new one must use a non-water setting (WORKING-RULES §4).
- Caption-linter note: it counts the phrase "which one" as a second ask, so keep it out of caption hooks.

### 004, *The Ship Kept Going, Season 3: "Man Overboard"* (suspense; owner supplies the VO)
- **Plan:** [series/004-the-ship-kept-going-s3/00-SERIES-PLAN.md](series/004-the-ship-kept-going-s3/00-SERIES-PLAN.md).
  - It holds the hidden truth: Marcus moved the money himself, and Kerr is his partner.
  - Main branches: TELL, QUIET, STAY, HIM.
  - HUD DAYS LEFT: none, 3, 2, 2→1, 0.
- **Votes, part by part:** P1 TELL/LIE · P2 POLICE/QUIET · P3 RUN/STAY · P4 HIM/ME · P5 finale (the sting: a photo of your front door).
- **Part 1: ✅ rendered** (87.2s, −14.1 LUFS, posting kit written). The owner's VO is Cole ("Gritty-Rough-Strong" PVC, ElevenLabs v4, stability 50 / similarity 75).
  - Whisper returned almost no punctuation, so the punctuation was copied from the script onto the words (`audio/voiceover.words.raw.json` is the untouched transcript). See WORKING-RULES §8.
  - Reused stills: 02 = S1 P1 01, 03 = S2 P5 01, 05 and 13b = S2 P5 15, 19 = this part's 18.
- **Reference images:** `dark-boat.png`, `fishing-boat.png` and `marina.png` were never delivered to `reference-brief/reference-images/`. The owner made Part 1's images without them, and they came out fine. If the owner sends them later, copy them into `part-02`…`part-05/reference-images/` and rerun `make_image_brief.py` for those parts. Marina matters most for Part 5.

- **Part 2: ✅ rendered** (95.7s, −14.1 LUFS, posting kit written). TELL won Part 1 (the owner's VO says "Most of you said tell him").
  - Punctuation copied from the script again; the raw transcript is `audio/voiceover.words.raw.json`.
  - The DAYS LEFT counter (3) pops in at "It's Thursday" and shows on image shots only, not on the cards or the vote.
  - Reused stills: 04 = S2 P4 19, 10 = this part's 06, 14 = this part's 12.

- **Part 3: ✅ rendered** (95.3s, −14.0 LUFS, posting kit written). QUIET won Part 2.
  - **Voiceover fix:** the owner's MP3 had a stray "Lucía." at 19.5s, because ElevenLabs read the speaker note in `[urgent, Lucía]` aloud. I cut 19.40–20.12s from the audio (the original is `audio/voiceover.orig.mp3`) and shifted the word timings. Whisper had also skipped "At six this morning", so those words were added from a second transcription of that window. **Tell the owner:** when generating the VO in ElevenLabs, remove character names from inside the [tags]; only delivery words belong there. Parts 4–5 scripts have the same kind of tags (e.g. `[calm, Doyle]`).
  - The DAYS LEFT counter (2) is off on shot 12, where it would cover Doyle's head.
  - Reused stills: 03 = S2 P4 16, 06 and 11b = this part's 01, 07 = S2 P4 10, 14 = S2 P3 06.

**Next: Part 4.**
1. Get the Part 3 vote result (RUN or STAY). Part 4 is written for STAY; check its script for the RUN swap, rewrite it if RUN won, keep the losing version, and rebuild the brief.
2. When Part 4's images and VO arrive: move the MP3 to `audio/`, transcribe to `voiceover.words.raw.json`, align punctuation from the script, and **listen-check for spoken speaker names** (look for a name the transcript has twice in a row). Then copy `part-03/edit.json` as the template (HUD 2 → 1, HIM/ME vote), preview, render, check, `publish.md`.

### Other open items
- **S1 Part 5:** shot 13 uses a stand-in because the delivered 13.png was corrupt. Re-render it if the owner re-sends that image.
- **Next new series (005):** must use a non-water setting (WORKING-RULES §4). Ask the owner for new reference images first. Follow `.claude/skills/story-series/SKILL.md`.

## Moving to a new account or a new PC: checklist
- [ ] **New PC:** follow [MOVING-PC.md](MOVING-PC.md) first (`git clone` the repo, create `.env` by hand, install Python, the requirements, ffmpeg and Blender, then run the checks).
- [ ] Open this same folder (`D:\CORTOON CHANNEL`) in VS Code with the new Claude account. `CLAUDE.md`, the project skills in `.claude/skills/` and these files carry all the context.
- [ ] `.env` with `ELEVENLABS_API_KEY` stays in the folder. If the ElevenLabs account changes too, put the new key there yourself, and check the voice IDs in `series/003-dont-let-me-in/voices.json`. They're premade voices, so they should exist on any account.
- [ ] Global Claude skills (elevenlabs, ffmpeg, hyperframes…) were installed per user under `C:\Users\mac\.claude\skills`. The pipeline doesn't need them; only the project skills in `.claude/skills/` matter.
- [ ] If the Instagram handle changes, update `channel/PROFILE.md`. Old `publish.md` files don't need changing, because they're already posted.
- [ ] First message to the new chat: *"Read HANDOFF.md, WORKING-RULES.md and README.md, then continue."*
