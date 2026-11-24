# The Ship Kept Going, Season 3: Part 3 of 5, "Against the Current"

| | |
|---|---|
| Target length | ~90s (about 250–290 VO words at 170 wpm) |
| VO word count | see `python tools/vo_stats.py series/004-the-ship-kept-going-s3` |
| Cliffhanger type | arrival, after a photo reveal, then a decision vote |
| Loops | half-closes L2 (he's alive) · moves L3 (he wrote the words) · opens L5 (Kerr's part) |
| Pays off | Part 2's "You're wearing it", at ~0:15 |
| Branch | **Written for QUIET winning.** POLICE lines are below. |

## First frame
- **On-screen text:** PART 3 · "HE DROWNED IN YOUR JACKET"
- **Visual:** The second yellow jacket laid out on Lucía's pier, YOU's flip-flops at the edge of the frame

## Voiceover (paste into TTS)
<!-- VO:START -->
[low, tense] Your brother "drowned." His jacket washed up. And you're wearing his jacket.

[firm] Most of you said stay quiet.

[knowing] Police voters, the officer already had a report. Signed by Agent Kerr. Case closed.

[quick] Doyle takes the boat to Isla Mujeres. To Lucía's pier. That's where it washed up.

[urgent, Lucía] Lucía runs the dive shop there. "They found it under my dock," she says. "At six this morning."

[slow, uneasy] It's laid out on the boards. Bright yellow. Your size. A high collar. And not a single cut in it.

[cold, realizing] Not yours. His.

[relieved, quiet] For one second, it's the best news you've had all week. If it's his, maybe he's alive.

[quick, Lucía] "He bought two," Lucía says. "Same size. A month before your cruise. He showed me the receipt."

[quick, factual] Here's what you don't know. The current here runs north. Fast. Anything lost out there ends up miles north.

[slow, cold] This jacket came south. Against the current. Nobody lost it. Somebody put it here.

[calm, Doyle] "Rule four," Doyle says quietly.

[slow, realizing] And then it hits you. Marcus wrote the twelve words himself. He never needed you to remember them.

[quiet, hurt] So why make you say them? Out loud. Next to Kerr's phone.

[low, Lucía] "There's something else," Lucía says. She shows you a photo from last month. A marina, in Puerto Morelos.

[very slow] Marcus. Laughing. Next to Agent Kerr.

[urgent, sharp] Then tires on the gravel. A dark gray sedan. Kerr's car.

[direct, tense] Run for the boat, or stay and face her?

[lighter, direct] Comment RUN or STAY. The majority writes Part 4.
<!-- VO:END -->

## If POLICE wins
Replace "Most of you said stay quiet." through "…That's where it washed up." with:
```
[firm] Most of you said police.

[quick, tense] At the island station, you tell them he's alive. The officer shows you a report. Signed by Agent Kerr. Case closed.

[knowing] Quiet voters, Doyle was waiting outside the whole time.

[quick] He takes you to Lucía's pier. That's where it washed up.
```
Image swaps: 03 becomes Part 2's `19A.png` (you at the police counter).

## Shot list
One image per shot, in the 2D look of the reference reels: see [image-prompts.md](image-prompts.md).

| # | Time | VO | Visual | On-screen text | Sound |
|---|---|---|---|---|---|
| 01 | 0:00 | Your brother drowned… | The second yellow jacket laid out on the pier boards | PART 3 · HE DROWNED IN YOUR JACKET | Waves, drone |
| 02 | 0:04 | Most of you said… | Vote card: QUIET WINS | PART 2 · YOU VOTED · QUIET WINS · The majority decided. | Card thump |
| 03 | 0:06 | Police voters… | Agent Kerr with her badge | REPORT SIGNED · AGENT KERR |  |
| 04 | 0:11 | Doyle takes the boat… | The fishing boat pulling up to Lucía's pier | ISLA MUJERES |  |
| 05 | 0:16 | Lucía runs the dive shop… | Lucía at the end of the pier, pointing down | LUCÍA · THE DIVE SHOP |  |
| 06 | 0:23 | It's laid out on the boards… | The jacket, pushed in on the uncut collar | NO CUT |  |
| 07 | 0:30 | Not yours His… | YOU touching his own cut collar |  | Low note |
| 08 | 0:31 | For one second… | Close-up: YOU, a small hopeful smile |  | Warm swell |
| 09 | 0:37 | He bought two… | Lucía holding up two fingers | "HE BOUGHT TWO." |  |
| 10 | 0:44 | Here's what you don't know… | Cream card: the current runs north | THE CURRENT HERE · RUNS NORTH · Fast. Anything lost out there ends up miles north. | Card thump |
| 11 | 0:50 | This jacket came south… | Cream card: this jacket came south | THIS JACKET · CAME SOUTH · Against the current. | Card thump |
| 11b | 0:53 | Nobody lost it… | The jacket on the pier, held | SOMEBODY PUT IT HERE |  |
| 12 | 0:55 | Rule four Doyle says… | Doyle on the pier, arms folded, looking at the jacket |  | Tick |
| 13 | 0:57 | And then it hits you… | Close-up: YOU, the realization | HUD · DAYS LEFT 2 · FRIDAY | Sub drop |
| 14 | 1:03 | So why make you say them… | The phone face down on the nightstand | KERR'S PHONE | Whisper |
| 15 | 1:08 | There's something else… | Lucía holding her phone out to YOU |  |  |
| 16 | 1:14 | Marcus Laughing… | The photo: Marcus laughing with Agent Kerr at the marina | LAST MONTH · PUERTO MORELOS | Camera shutter, stinger |
| 17 | 1:16 | Then tires on the gravel… | Kerr's sedan pulling up outside the dive shop, dust | KERR | Tires on gravel, engine off |
| 18 | 1:20 | Run for the boat… | Vote: 18A RUN · 18B STAY | RUN / STAY | Light pulse |

## Caption
```
Season 3 · Part 3/5 · Something washed up under the pier. 🌊

An interactive mystery story where the comments decide.

Comment RUN or STAY. The majority writes Part 4.

#MidnightParts #TheShipKeptGoing #season3 #mysterystory #survivalstory
```

## Pinned comment
RUN or STAY? Rewatch Season 2, Part 4: Marcus's hand went straight to your collar. Why? 👀

## Quality gate
- [x] Hook ≤ 12 words-ish, with a contradiction (his jacket washed up; you're wearing it)
- [x] Previous cliffhanger paid off by ~0:15 (the jacket is his, not yours)
- [x] Vote result, a line for the losing side, and the choice shapes the opening
- [x] Evidence of the hidden truth (two jackets, the current, he wrote the words) and a returning ally (Lucía)
- [x] False relief ("maybe he's alive") turned into dread (he planned it)
- [x] Ends worse: the FBI agent is his partner, and she's here
- [x] Cliffhanger type differs from Part 2's (arrival vs impossible fact)
- [x] Loop ledger: half-closes L2 · moves L3 · opens L5
- [x] VO word count in range (`tools/vo_stats.py`)
- [ ] Read-aloud test: do this when recording the voice
