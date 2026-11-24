# The Ship Kept Going, Season 3: Part 4 of 5, "Him or Me"

| | |
|---|---|
| Target length | ~90s (about 250–290 VO words at 170 wpm) |
| VO word count | see `python tools/vo_stats.py series/004-the-ship-kept-going-s3` |
| Cliffhanger type | threat, then a decision vote |
| Loops | moves L4 (Doyle's offer) and L5 (Kerr's frame) · L2 and L3 ready to close |
| Pays off | Part 3's arrival (Kerr's car), in the first 8s |
| Branch | **Written for STAY winning.** RUN lines are below. |

## First frame
- **On-screen text:** PART 4 · "THE FBI HELPED HIM DIE"
- **Visual:** Agent Kerr stepping out of her sedan in the hard sun, sunglasses on

## Voiceover (paste into TTS)
<!-- VO:START -->
[low, tense] Your brother faked his death. The FBI agent who helped him just pulled up.

[firm] Most of you said stay.

[knowing] Run voters, her people were already waiting at the end of the pier.

[calm, official] Agent Kerr steps out. Sunglasses. Lanyard. "I'm so sorry for your loss," she says.

[cold, flat] You look around. Doyle's gone. Like he was never there.

[quick, tense] She drives you to the island police office. A file on the table. Your name on the front.

[slow, hurt] Across from you sits the woman from Lucía's photo. The one laughing with your brother.

[cold, measured] "Two million dollars left from a phone in your hotel room. At 2:14 a.m."

[slow, dawning] The phone she gave you. The secure one.

[quiet] "Your brother drowned. You said the words out loud. Who do you think they'll believe?"

[slow, cold] Then she lets you go. That's the worst part. She wants them to find you.

[quick] Outside, Lucía is waiting. She heard it on the harbor radio. A black boat with no lights, docked at Puerto Morelos.

[urgent, whispering] "It leaves Sunday," she says. "Two fourteen in the morning."

[quick] "Go tonight," she says. "Before she finds out I told you."

[relieved, almost hopeful] You know where he is. You know when. For the first time, you're ahead of them.

[cold] Then Doyle steps out of the shade. He heard every word.

[calm, flat] "Saturday," he says. "One day left. My people want the man in the yellow jacket."

[slow, menacing] "Take me to your brother. Or I take you."

[direct, tense] Your brother, or you?

[lighter, direct] Comment HIM or ME. The majority writes the finale.
<!-- VO:END -->

## If RUN wins
Replace "Most of you said stay." and "Run voters, her people were already waiting at the end of the pier." with:
```
[firm] Most of you said run.

[fast, tense] You make it halfway down the pier. Two of her people are waiting at the end.

[knowing] Stay voters, at least you'd have kept your dignity.
```
Image swaps: 03 stays (her two agents at the end of the pier).

## Shot list
One image per shot, in the 2D look of the reference reels: see [image-prompts.md](image-prompts.md).

| # | Time | VO | Visual | On-screen text | Sound |
|---|---|---|---|---|---|
| 01 | 0:00 | Your brother faked his death… | Agent Kerr stepping out of her sedan in the sun | PART 4 · THE FBI HELPED HIM DIE | Car door, drone |
| 02 | 0:04 | Most of you said… | Vote card: STAY WINS | PART 3 · YOU VOTED · STAY WINS · The majority decided. | Card thump |
| 03 | 0:06 | Run voters… | Two agents waiting at the end of the pier |  |  |
| 04 | 0:11 | Agent Kerr steps out… | Close-up: Kerr, fake sympathy | "I'M SO SORRY FOR YOUR LOSS." |  |
| 05 | 0:16 | You look around… | The empty pier where Doyle stood, the fishing boat gone | DOYLE'S GONE |  |
| 06 | 0:19 | She drives you… | The island police office: YOU and Kerr, a file between them |  | Ceiling fan |
| 07 | 0:31 | Two million dollars left… | Dark card: Kerr's report | KERR'S REPORT · $2M moved from a phone in your hotel room. · 2:14 AM | Card thump |
| 08 | 0:37 | The phone she gave you… | The phone face down on the nightstand | THE SECURE ONE | Sub drop |
| 09 | 0:40 | Your brother drowned… | Kerr leaning in close, quiet | "WHO DO YOU THINK THEY'LL BELIEVE?" |  |
| 10 | 0:45 | Then she lets you go… | YOU walking out of the police office into the sun, alone |  |  |
| 11 | 0:50 | Outside Lucía is waiting… | Lucía with a handheld marine radio | LUCÍA | Radio static |
| 12 | 0:58 | It leaves Sunday… | Dark card: Sunday 2:14 AM, Puerto Morelos | THE BOAT WITH NO LIGHTS · SUNDAY · 2:14 AM · Puerto Morelos | Card thump |
| 13 | 1:06 | You know where he is… | YOU at sunset on the pier, a determined half-smile | HUD · DAYS LEFT 2 | Warm swell |
| 14 | 1:11 | Then Doyle steps out… | Doyle stepping out of deep blue shade |  | Music cuts |
| 15 | 1:15 | Saturday he says… | Doyle in the light, pushed in | HUD · DAYS LEFT 1 · SATURDAY |  |
| 16 | 1:20 | Take me to your brother… | Close-up: Doyle, flat and menacing | "OR I TAKE YOU." | Low hit |
| 17 | 1:24 | Your brother or you… | Vote: 17A HIM · 17B ME | HIM / ME | Light pulse |

## Caption
```
Season 3 · Part 4/5 · The FBI says you did it. 🚔

An interactive survival story where you choose what happens next.

Comment HIM or ME. The majority writes the finale.

#MidnightParts #TheShipKeptGoing #season3 #survivalstory #mysterystory
```

## Pinned comment
HIM or ME? There's no right answer this time. 👀

## Quality gate
- [x] Hook ≤ 12 words-ish, concrete (faked death, the FBI agent, her car)
- [x] Previous cliffhanger paid off in the first 8s (she steps out of the car)
- [x] Vote result, a line for the losing side, and the choice shapes the opening
- [x] The trusted person is the threat (Kerr's report frames you)
- [x] False relief (you know where and when) before the final turn
- [x] Ends worse: the man who pushed you off the ship makes you choose
- [x] Cliffhanger type differs from Part 3's (threat vs arrival)
- [x] Loop ledger: moves L4 and L5
- [x] VO word count in range (`tools/vo_stats.py`)
- [ ] Read-aloud test: do this when recording the voice
