# Moving the project to the new PC

Written 2026-11-24. The owner has a more powerful second PC, where Claude will make **new kinds of series** end to end with **free local tools** (Blender, and possibly local image AI). The running series continue on the old PC. Background is in [research/free-tools-plan.md](research/free-tools-plan.md).

After the move, a new Claude chat gets all the context from the files in this folder. Nothing important lives only in the old chat.

## 1. Get the project (owner)
**The split (owner's decision, 2026-11-24):**
- **The old PC** keeps making the running series: Ship S3 Parts 4–5 and anything that re-renders an old part. It has all the media.
- **The new PC** starts the **new kinds of series** (the free-tools 3D format).
- The GitHub repo **https://github.com/Furqaan77/Cartoon-Channel** connects the two.

On the new PC:
```bash
git clone https://github.com/Furqaan77/Cartoon-Channel.git "D:/CORTOON CHANNEL"
```
- **What the repo holds:** every doc, rule, playbook, tool and skill; every series' plan, scripts, image prompts, `edit.json` and `publish.md`; the locked character YOU (`channel/characters/you/`); the sound library (`library/`); and the research.
- **What it leaves out** (`.gitignore`): all MP4s, the per-part images, previews, audio and voiceovers, the image-brief PDFs and ZIPs, and `.env`. That media stays on the old PC. Copy it by USB only if an old part ever has to be re-rendered on the new PC.
- **`.env` is not in the repo, by design.** On the new PC, create `.env` in the project folder by hand with one line: `ELEVENLABS_API_KEY=...` (the same key as the old PC). Never paste the key into a chat or commit it.
- Optional: to skip a 1.5 GB download, copy the Whisper models from `C:\Users\mac\.cache\huggingface\hub` on the old PC to the same place under your user folder on the new PC.
- **Keeping both in sync:** commit and push after each change (`git add -A && git commit -m "..." && git push`), and run `git pull` before starting work on the other PC. HANDOFF.md and `series/INDEX.md` cover both machines.

## 2. Install on the new PC (owner, or ask Claude to do it)

| What | Why | How |
|---|---|---|
| **VS Code** + the **Claude Code** extension | Where Claude works | code.visualstudio.com, then Extensions → "Claude Code" |
| **Git for Windows** | Gives Claude its bash shell | git-scm.com (default options) |
| **Python 3.12** | All the tools in `tools/` | python.org. Tick "Add python.exe to PATH". |
| Python packages | The pipeline | `python -m pip install -r requirements.txt` in the project folder |
| **ffmpeg** (command line) | Loudness checks, audio cuts, contact sheets. The renderer has its own bundled copy, but checks use the command. | `winget install Gyan.FFmpeg` |
| **Chrome or Edge** | Prints the image-brief PDFs | Usually already installed |
| **Node.js** (optional) | Only for the HyperFrames/Remotion skills | nodejs.org (LTS) |
| **Blender** (new) | The 3D format | blender.org (free). Claude can also install it with `winget install BlenderFoundation.Blender`. |
| NVIDIA driver | Blender GPU rendering and local AI | Keep it up to date |

Fonts: the renderer uses Arial Black, Arial Bold, Segoe UI Bold and Consolas, which come with every Windows install.

## 3. Optional: the old PC's personal Claude skills
- The project's own skills (`story-series`, `ig-caption`, `ig-audit`, `ig-viral`) are in `.claude/skills/` and **move with the folder**.
- Skills installed for the user on the old PC live in `C:\Users\mac\.claude\skills` (elevenlabs, ffmpeg, hyperframes, remotion, resolve and others). The pipeline doesn't need them. To keep them, copy that folder to `C:\Users\<you>\.claude\skills` on the new PC.
- Claude's private memory from the old PC is **not** needed. Everything in it was copied into [WORKING-RULES.md](WORKING-RULES.md).

## 4. Check it works (Claude does this in the first chat)
```bash
python --version                      # 3.12.x
python -X utf8 tools/vo_stats.py series/004-the-ship-kept-going-s3
# Old parts can't be previewed on the new PC: their images aren't in git.
# To test the renderer, run --preview on a new part once one exists.
ffmpeg -version | head -1
nvidia-smi                            # GPU name + VRAM: record it in research/free-tools-plan.md
```
- Check that `.env` exists. Don't print it; `grep -c ELEVENLABS_API_KEY .env` is enough.

## 5. First message to the new chat
> Read HANDOFF.md, WORKING-RULES.md, README.md, MOVING-PC.md and research/free-tools-plan.md. Then run the checks in MOVING-PC.md §4, tell me my GPU, and continue.

## What the new chat should do next
These are in order. They are also in [HANDOFF.md](HANDOFF.md) under "Next".
1. Run the checks above and record the new PC's GPU, VRAM, RAM and free disk in `research/free-tools-plan.md`.
2. Install Blender and make the **40s @theoddtilt-style test reel** starring YOU. The plan is in `research/free-tools-plan.md`.
3. The running series (Ship S3 Parts 4–5) stay on the **old PC**. Don't render them on the new PC; their media isn't in git.
