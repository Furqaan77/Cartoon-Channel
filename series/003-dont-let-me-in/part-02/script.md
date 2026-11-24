# Don't Let Me In: Part 2 of 5, "Rule One"

| | |
|---|---|
| Target length | 60–80s |
| VO word count | see `python tools/vo_stats.py series/003-dont-let-me-in --wpm 150 --target 60,80 --gap 0.3` |
| Cliffhanger type | overheard ("Okay. I'll ask him."), then a decision vote |
| Loops | closes L2 (why doesn't it break in? Rule 1) · opens L4 (who is Lily talking to?) |
| Pays off | Part 1's back door, in the first 5s |
| Branch | **Written for LOCK winning.** HIDE lines are below. |

## First frame
- **On-screen text:** PART 2 (corner) · big: **YOU CHOSE LOCK**
- **Visual:** your own dripping face pressed to the back door's glass

## Voiceover
<!-- VO:START -->
[low, urgent] You chose lock.

[fast, breathless] Down the hall. Past the dark windows. The handle is still turning.

[hard, sharp] You slam the bolt. Click.

[very quiet, slow] On the other side of the glass, your own face. Dripping. Smiling.

{COPY} [gentle, too friendly] "Let's get you inside."

[uneasy, low] Same words. Same voice. Like a recording.

(pause 0.6)

[startled] Then the old phone on the kitchen wall rings.

{PRUITT} [old, raspy, urgent] "This is Walt Pruitt, across the lake. I can see your porch. Who's standing out there?"

[whispering] You almost say, "Me."

{PRUITT} [grave, slow] "Listen. Rule one. It can't come in unless someone who lives there lets it in."

{PRUITT} [lower, careful] "Rule two. It only says words it heard by the water."

[realizing, quiet] Your words. From the dock. At sunset.

{PRUITT} [firm] "Don't open a door. Don't open a window. At sunrise, it goes back in the lake."

[quick, checking] Sunrise is five fifty-one. It's three twenty.

[exhaling, almost relieved] Two and a half hours. Locked doors. You can do that.

(pause 0.8)

[cold, quiet] Upstairs, Lily is talking to someone.

{LILY} [sweet, sleepy] "Okay. I'll ask him."

[very slow, dread] Her window is open. And you are standing under it. Looking up.

[direct, tense] Pull her away from the window, or listen first?

[lighter, direct] Comment PULL or LISTEN.
<!-- VO:END -->

## If HIDE wins
Replace the first five paragraphs, from "You chose lock." through the copy's "Let's get you inside.", with:
```
[low, urgent] You chose hide.

[fast, breathless] You scoop up Lily and take the stairs two at a time. Behind you, the handle rattles. Then it stops.

[slow, cold] It was locked all along. At the landing window, your own face. Dripping. Smiling.

{COPY} [gentle, too friendly] "Let's get you inside."
```
Image swaps: 02 becomes Part 1's `16B.png` (YOU carrying Lily up the stairs), and 01 and 04 become the copy at the landing window (prompt in image-prompts.md).

## Shot list
| # | Time | VO | Visual | On-screen text | Sound |
|---|---|---|---|---|---|
| 01 | 0:00 | You chose lock. | The copy's dripping, smiling face pressed to the back door glass | YOU CHOSE LOCK | Sting, rain-drip |
| 02 | 0:02 | Down the hall… still turning. | REUSE Part 1 `16A.png` (YOU sprinting down the hall) | | Footsteps, rattle |
| 03 | 0:06 | You slam the bolt. Click. | Close-up: YOU's hand slamming the brass bolt | | Bolt click |
| 04 | 0:08 | On the other side of the glass… "Let's get you inside." | REUSE 01, pushed in | "LET'S GET YOU INSIDE." | |
| 05 | 0:15 | Same words… Then the old phone rings. | The yellowed wall phone ringing, YOU frozen beside it | | Old phone ring |
| 06 | 0:21 | "This is Walt Pruitt, across the lake…" | Pruitt at his dark window with binoculars and a phone | WALT PRUITT · ACROSS THE LAKE | |
| 07 | 0:26 | "Who's standing out there?" · You almost say, "Me." | His view across the lake: your porch light, a tiny yellow figure | | |
| 08 | 0:31 | "Rule one…" | Dark card: RULE 1 · It can't come in unless someone who lives there lets it in. | | Card thump |
| 09 | 0:38 | "Rule two…" | Dark card: RULE 2 · It only says words it heard by the water. | | Card thump |
| 10 | 0:42 | Your words. From the dock. At sunset. | REUSE Part 1 `05.png`, desaturated | | |
| 11 | 0:46 | "Don't open a door…" | Close-up: Pruitt, grave, phone to his ear | | |
| 12 | 0:52 | Sunrise is five fifty-one… You can do that. | YOU sliding down to sit against the locked back door, exhaling | SUNRISE 5:51 · NOW 3:20 | Clock tick |
| 13 | 1:00 | Upstairs, Lily is talking to someone. "Okay. I'll ask him." | The upstairs hall, Lily's door ajar, moonlight | | Silence, a whisper |
| 14 | 1:05 | Her window is open… | Lily kneeling on her bed at the open window, curtains blowing | | Night wind |
| 15 | 1:08 | And you are standing under it. Looking up. | Looking down from her window: the copy in the yard, looking up | | Low note |
| 16 | 1:12 | Pull her away… Comment PULL or LISTEN. | Vote: 16A YOU pulling Lily back from the window · 16B YOU frozen in the doorway, listening | PULL / LISTEN | Pulse |

## Caption
```
📞 THE NEIGHBOR KNOWS THE RULES…

You chose lock. It didn't need the door. 😨

👀 Pull her away from the window, or listen first?
Comment PULL or LISTEN. The majority decides Part 3.

🎬 DON'T LET ME IN · PART 2

#DontLetMeIn #MidnightParts #horrorstory #creepystories #scarystories
```

## Pinned comment
PULL or LISTEN? Who do you think Lily is talking to? 👀

## Quality gate
- [x] Hook: the vote result plus the most frightening image (your face at the glass)
- [x] Previous cliffhanger paid off in the first 5s
- [x] Stranger test: the copy, the cabin and Lily are all clear by 0:15
- [x] False relief ("You can do that.") before the turn
- [x] Ends worse (it's talking to Lily through an open window)
- [x] Cliffhanger type differs from Part 1's (overheard vs arrival)
- [x] Loops: closes L2 · opens L4
