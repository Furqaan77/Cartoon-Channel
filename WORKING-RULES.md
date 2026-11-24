# Working rules: how the owner wants this project run

These are the owner's standing preferences and the lessons learned while making series 001–004. Until 2026-11-16 they lived in Claude's private memory for the old account. They're copied here so any new chat or account follows them. **Read this together with [CLAUDE.md](CLAUDE.md) and [HANDOFF.md](HANDOFF.md).**

## 1. The division of work

| | Suspense: *The Ship Kept Going* (001, 002, 004…) | Horror line (003 on, @zerotales format) |
|---|---|---|
| Images | The owner generates them from our prompts | The owner generates them from our prompts |
| Voiceover | **The owner** supplies the MP3 (ElevenLabs voice **"Cole"**, the Season 1 Parts 2–4 settings). Claude transcribes it locally. | **Claude** generates it with a cast: `series/NNN/voices.json` and `tools/make_voiceover.py` |
| Everything else (story, scripts, prompts, edit, render, posting kit) | Claude | Claude |

- Both lines run **in parallel**. The owner said explicitly: never drop The Ship Kept Going for the horror line.
- When the owner says "make part N", the images (and for suspense, the VO) are already in that part's folder. Do the whole job without asking: rename files, transcribe or generate the VO, write `edit.json`, preview, render, check, and write `publish.md`. Then give the caption in chat.
- When the owner reports a vote ("people chose PULL"), rewrite the next part for that branch. Keep the losing version in the script under "If X had won (kept for reference)", and update the series plan's status, its vote record and `series/INDEX.md`.

- **Free tools only, apart from ElevenLabs (owner's decision, 2026-11-24).** The owner pays for ElevenLabs (voice, sound effects, music) and nothing else.
  - Never propose or install anything that needs a paid API key (Gemini/Nano Banana, OpenAI/GPT Image, fal, Replicate, Runway and so on).
  - Use free local tools instead: Blender, ComfyUI with open models, and code-drawn graphics.
- **The owner no longer wants to make images (2026-11-24).** The goal is for Claude to make videos end to end. See [research/free-tools-plan.md](research/free-tools-plan.md). Until that pipeline works, the running series still use the owner's images.

## 2. Visual style (owner's correction, 2026-10-27)
- Every part gets its own `part-NN/image-prompts.md`, with **one complete, copy-paste prompt per single still image**, in the reference reels' look (@saveo.house, @beanie.escape).
- That look: 2D hand-drawn cartoon, bold black ink outlines, stick figures with white egg-shaped heads, rich moody backgrounds, 9:16, and **no text in the image**.
- **Never** write 3D, cinematic-keyframe or video-clip prompts. I did once, and the owner redirected me to these stills.
- Use fixed character phrases word for word and the fixed style tail. Turn diagrams, rules, facts and vote results into text cards made in the edit, not into images.
- Include the image swaps for every vote branch. Mark reused images instead of asking for near-duplicates.
- After any change to `image-prompts.md`, rebuild the hand-off PDF: `python tools/make_image_brief.py series/NNN/part-NN`.

## 3. YOU, the locked main character
- Spec: `channel/characters/you/CHARACTER.md`. Never change his face, hair, proportions, style or outfit (messy black hair, white egg-shaped head, black oval eyes, open **yellow** windbreaker, white T-shirt, navy shorts, black flip-flops).
- Only expressions, poses, surroundings and his physical state change.
- **Nobody else wears yellow.** The one exception is Season 3's "second jacket" prop, which is never worn on screen.

## 4. Settings: keep series apart (owner's feedback, 2026-11-15)
- From the next **new** series (005+), use a world clearly different from every series still running. While The Ship Kept Going is live, avoid water, boats, docks, lakes, islands and the sea. Good options: a city apartment block, a desert motel, a snowy road, a school at night, a hospital, a farmhouse in a cornfield, a subway.
- 003's lake cabin was accepted, but the owner worried viewers would link it to the ship series. 004 is Ship Season 3, so it keeps the sea and island world.
- The owner will generate new reference images for a new world, so design fresh locations and supporting characters freely, and **ask for the reference images first**.

## 5. The horror line (started 2026-11-12)
- It's modelled on @zerotales.stories ("The Second Mom"): "you" POV, a copy of someone trusted as the monster, a vote at the end of every part, 60–80s parts, red key-word captions (`"accent": "#E3262E"`) and a `"corner_tag": "PART N"`.
- It still uses YOU and the house look's still images (no animation).
- The research is in `research/competitor-reels/zerotales.stories.md` and playbook §16.
- The owner wants these stories to be "very similar" to that page, because it grew fast.

## 6. Publishing rules
- Every finished part gets a `publish.md` (Instagram caption, hashtags, pinned comment; YouTube title, description, tags, pinned comment, settings).
- **Never reveal the part's twist** in `publish.md`.
- Every Instagram caption must contain a **search phrase as a normal sentence**, such as "An interactive horror story where you decide what happens next." or "…an interactive survival story where you voted on every part." Instagram search reads the caption, not the hashtags.
- Lint every caption: `python -X utf8 .claude/skills/ig-caption/caption.py caption.txt --keywords "horror story"`.
- Use #MidnightParts plus the series tag on every post.

## 7. Safety and privacy (hard rules)
- The ElevenLabs key lives only in `.env`. Never paste it into chat, a file or a commit.
- Never ask for social-media passwords, and never log in to Instagram or YouTube for the owner.
- The owner's email and personal details stay private. Never send them to any external service.
- Crime stories are consequence stories. Never give operational how-to.

## 8. Technical gotchas (learned the hard way)
- **Windows encoding.** Run repo Python with `python -X utf8` (or set `PYTHONUTF8=1`). Otherwise cp1252 crashes on emoji or "é".
- **The owner's image filenames** arrive as `01 (1).png` or `01.png.png`. Rename them before building:
  - In bash: `for f in *" ("*").png"; do mv -n "$f" "${f%% (*}.png"; done`.
  - For `.png.png`, strip one `.png`.
  - Always check the names against the shot IDs in `image-prompts.md` (01, 02, 14b, 16A/16B…).
- **Corrupt or missing image.** If an image won't open, reuse the nearest similar still and tell the owner. S1 Part 5 shot 13 uses a stand-in for this reason.
- **Vote screens.** Square A/B images crop heads. Use the taller bands (`band_h 680`, `band_y [0.335, 0.695]`, buttons at `a_pos [0.5,0.48]`, `b_pos [0.5,0.84]`) and `focus_y` per band.
- **Preview before rendering.** Run `--preview` at title, card and vote moments, and check:
  - long titles don't wrap into the chip (use `max_w` or a smaller `size`);
  - overlays don't sit on a character's face;
  - the burned captions don't repeat on-screen text (set `"captions": false` on that shot);
  - card `keys` highlight only the meaningful word.
- **Whisper sometimes returns no punctuation**, and then captions run sentences together. Fix it by aligning the script's VO words to the transcript with difflib and copying the script's punctuated tokens onto the matched words. Keep the timings, and keep the raw file as `voiceover.words.raw.json`. This was done for S3 Part 1.
- **The owner may drop the VO MP3 into `images/`** with its long ElevenLabs filename. Move it to `audio/voiceover.mp3`.
- **Never put a character name inside a delivery tag** in a suspense script, e.g. `[calm, Doyle]`. The owner pastes the VO into ElevenLabs as written, and it reads the name aloud (S3 Part 3 had a stray "Lucía." that had to be cut out of the MP3). Tags hold delivery words only, and the speaker is named in the line ("…," Doyle says). After transcribing, look for a name repeated twice in a row.
- **Whisper mishears names and times** ("Lucia's", "Blackwater", "2 .14"). Fix them with `caption_fixes`, never by editing the timings.
- **Checks after every render:**
  - loudness about −14 LUFS (ffmpeg `ebur128`);
  - the instagram and youtube MP4s are byte-identical (`cmp`);
  - length within target (suspense 85–105s, horror 60–80s).
- **Stats.** yt-dlp gets Instagram likes and comments without a login, but not views. For YouTube use `--flat-playlist -J` and parse the JSON.
