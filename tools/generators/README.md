# Generator scripts (archive)

One-off scripts Claude used to write a whole season's files in one go. They are kept as a record and as a template for the next season; they are **not** part of the regular pipeline.

| Script | What it wrote |
|---|---|
| `gen_s3_season3.py` | Season 3 of The Ship Kept Going (`series/004-the-ship-kept-going-s3/`): every part's `script.md` and `image-prompts.md`, with VO, shot specs, captions and quality gates. Shot times are estimated from VO anchors at 170 wpm. |
| `gen_prompts_003.py` | The image prompts for `series/003-dont-let-me-in/`. |

**Don't re-run them blindly.** Files were edited by hand afterwards (003 Part 3 was rewritten for the PULL vote, for example), so re-running would overwrite those edits. Edit the series files directly instead.
