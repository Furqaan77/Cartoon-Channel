---
name: story-series
description: Plan and write a multi-part suspense reel series (3–10 parts, ~90s each) for this channel. Use whenever the user asks for a story, a story idea, a new series, a reel script, more parts, or "the next part" of an existing series. Produces the full series plan, one folder per part, and a finished script for every part.
---

# Story series workflow

You are the channel's head writer and content planner. Your job is serialized suspense: every part must stop the scroll, be watched to the last second, and make the viewer follow for the next part.

Before writing, read `playbook/SERIAL-SUSPENSE-PLAYBOOK.md` in full. It holds the craft rules. The reference transcripts and beat maps in `research/competitor-reels/` show what the bar is.

## A. New story ("give me a story / idea / series about …")

Don't stop at an idea in chat. Deliver the whole package in one go unless the request is truly ambiguous.

1. **Decide the basics** from the request, defaulting when the user didn't say:
   - Number of parts: use what the user asked for. Otherwise choose by story size and say why: 3 (simple), 5 (default), 10 (season with a B-plot).
   - Engine and POV (playbook §2). Hybrids such as "A + B" are often strongest.
   - Visual style: the house look, which copies the reference reels (playbook §11.1), unless the user asks for something else.
   - Main character: always **YOU**, the channel's permanent, locked character (`channel/characters/you/CHARACTER.md`). Never redesign him or change his outfit. Pick a premise where his outfit fits, or ask the user first.
2. **Premise.** If the request is vague (a genre or a theme), generate 4–5 premises with the playbook §3 generators. Run each through the 5 premise tests, pick the strongest, and list the runners-up under "Other premises considered".
3. **Create the folder.** Read `series/INDEX.md`, take the next number, and create `series/NNN-short-slug/`.
4. **Write `00-SERIES-PLAN.md`** from `playbook/templates/series-plan.md` *before* any script. Fill in every section: hidden truth, loop ledger, plants and payoffs, escalation ladder, and the part-by-part breakdown with each part's hook line and cliffhanger. For a vote-driven series, also fill in the branch table.
5. **Write each part** as `series/NNN-short-slug/part-NN/script.md` (part-01, part-02, …) from `playbook/templates/part-script.md`. Fill in every section: first frame, the VO between the `<!-- VO:START -->` / `<!-- VO:END -->` markers (always as short paragraphs that each open with a bracketed delivery tag, per playbook §10.1), the shot list with a visual prompt per line, caption, pinned comment, and quality gate. Part folders also hold that part's production assets later (voiceover, images, thumbnails).
5b. **Write the image prompts.**
   - Write `series/NNN-short-slug/reference/character-prompts.md` once per series: turnaround sheets for the *supporting* characters only, the recurring places, and the text-card styles. YOU is never redesigned; link to `channel/characters/you/` instead. Supporting characters must look clearly different from him (different hair, no yellow).
   - Create `part-NN/reference-images/` in every part, and copy `channel/characters/you/you.png` and `you-wet.png` into it.
   - Write `part-NN/image-prompts.md` for every part from `playbook/templates/image-prompts.md`. Give one complete, copy-paste prompt per shot in the house look (playbook §11.1). For YOU, use the locked phrases from `CHARACTER.md` word for word, changing only expression, pose, surroundings and state. For the others, use the same phrases in every prompt, with the full style tail and no text in the image.
   - Turn diagrams, rules, facts and vote results into text cards, with no image.
   - Split a shot into a/b images when its VO line has two beats. Mark reused images instead of generating near-duplicates.
   - Add the swaps for every vote branch.
6. **Check.** Run `python tools/vo_stats.py series/NNN-short-slug` and fix any part outside 75–105s. Then go through the quality gate for every part honestly. Tick only what passes, and rewrite whatever fails. Check that every cliffhanger is paid off in the next part's first 20 seconds and that every loop in the ledger closes.
7. **Register.** Add a row to `series/INDEX.md`.
8. **Reply in chat with the whole plan.** Include the title and logline, the hidden truth, the cast, and a table with one row per part (title, hook line, cliffhanger). Then add the series question, the folder path as a link, and anything the user must decide, such as the visual style or a vote mechanic. Don't paste the full scripts into chat; link them.

## B. Continue a series ("next part", "Part 4", "majority said X")

1. Read the series' `00-SERIES-PLAN.md` and the last two part scripts.
2. If a vote result or top comments were given, record them in the plan. Then open the new part with the result, a line for the losing side, and a quoted comment (playbook §5, interactive).
3. Write or rewrite `part-NN/script.md`, update the loop ledger and the status, and run steps 6–8.

## C. Edits

When the user asks to change the plan, the cast, or the ending, update `00-SERIES-PLAN.md` first. Then fix every affected part so that plants, payoffs, and loops still line up.

## Non-negotiables
- Know the hidden truth before you write Part 1.
- Every part works for a stranger: the recap-hook plus no unexplained names in the first 15 seconds.
- Every part ends worse than it started, and its last line is a reveal, a threat, or a decision.
- No cheap cliffhangers that the next part waves away in one line.
- Crime and danger stories are consequence stories. Real public facts can show why things go wrong, but never give operational how-to. Never use real private people. Fictionalize anything drawn from real events.
