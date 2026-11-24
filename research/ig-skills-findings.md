# Instagram agent skills: test results (2026-11-14)

Installed for this project only: `.claude/skills/ig-audit`, `ig-caption`, `ig-viral` (from github.com/Jakeschincariol/instagram-agent-skill, MIT). Its hook scorer (`ig-reel/hookscore.py`) was run from a temporary copy, not installed.

## Public numbers we could get (no login)

Instagram hides view counts without a login, so likes are the stand-in. Comments per like is a rough measure of how strongly viewers react.

| Reel | Account | Likes | Comments | Comments per like | Spoken hook |
|---|---|---|---|---|---|
| Day 1 | @saveo.house | 989,512 | 13,128 | 1.3% | You just stole $10 million dollars. |
| Day 2 | @saveo.house | 257,277 | 7,174 | 2.8% | You just stole 10 million dollars. |
| Day 3 | @saveo.house | 187,103 | 11,671 | 6.2% | You stole 10 million dollars. |
| Part 1 | @beanie.escape | 79,612 | 259 | 0.3% | I woke up to someone violently banging on my apartment door at 3 a.m. |
| Part 2 | @beanie.escape | 25,768 | 139 | 0.5% | At 3 a.m., six of my neighbors banged… |
| Part 4 | @beanie.escape | 10,748 | 118 | 1.1% | My neighbors are trying to kill me. |
| Part 2 | @zerotales.stories | 17,937 | 325 | 1.8% | You chose the phone. |
| S2 Part 3 | @midnight_parts_1 | 349 | 18 | 5.2% | Your brother stitched two million dollars into your collar… |

YouTube: our @midnightparts channel has 1 Short (8 views, 3 subscribers). @saveohouse on YouTube has 61 subscribers and a median of 149 views. The YouTube @zerotales.stories is an unrelated Spanish account. YouTube is not where these formats grow.

## What the skills said

1. **ig-viral (ranking):** the Part 1s are the outliers: saveo Day 1 at 3.9x its own median, beanie Part 1 at 3.1x. Every later part falls off (saveo 990k → 257k → 187k; beanie 80k → 26k → 11k). Sample: 8 reels from 4 accounts. The skill itself says that's too few to prove anything, so treat this as a strong hint, not proof.
2. **ig-viral (formulas):** all 8 hooks were "unclassified". Its 26 formulas are built for talking-head and business reels. Our niche's two hook shapes, "You just [did something huge]" and "You chose [X]" (the vote result), aren't in its library.
3. **Hook scorer:** it does **not** predict results in our niche. Top-third and bottom-third hooks scored the same (62 vs 63), and it rated "You chose the phone." 26/100 although that reel has 18k likes. Don't rewrite hooks to raise this score.
4. **ig-caption:** all 12 of our captions pass every format check: the first line lands before "… more", hashtags sit below the fold, there's one ask, and there are ≤ 5 tags. **One real failure: search terms.** Instagram search reads the caption sentences, not the hashtags, and none of our captions contained "horror story", "survival story" or "interactive story" as words. Fixed in 003 Part 2 and S2 Part 5; do it in every caption from now on.
5. **ig-audit:** it can't run without your Insights. It ranks posts on **hold at 3 seconds**, **shares (sends) per reach**, **follows per reach** and **non-follower reach**, not views. It also separates a reach problem (the hook) from a conversion problem (the profile).

## What to do with it

- **Part 1 is the advert for the whole series.** It gets about 3–4x the reach of later parts, so put the most effort into Part 1's first frame and line, pin each new Part 1 to the profile, and open later captions with "New here? Start with Part 1 (pinned)", as saveo does on Day 3.
- **Post vote percentages** in the next part's caption ("61% of you said HIDE…"). saveo does it every day and its comment rate rises each day (1.3% → 2.8% → 6.2%).
- **Our engagement is not the problem; reach is.** At 5.2% comments per like, people who see us react more than beanie's or zerotales' viewers do. The fix is getting seen: hooks, Part 1s, shares.
- **Put a search phrase in every caption** as a normal sentence ("An interactive horror story where you decide what happens next.").
- **For a real audit, the account owner exports Insights** for the last 10–15 reels (views, reach, non-follower %, 3-second hold, average watch time, shares, saves, follows). Screenshots are fine.
