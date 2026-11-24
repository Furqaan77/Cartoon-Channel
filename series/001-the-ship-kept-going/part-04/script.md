# The Ship Kept Going: Part 4 of 5, "From Behind"

| | |
|---|---|
| Target length | ~90s (about 250–290 VO words at 170 wpm) |
| VO word count | 266 words, ~94s (`tools/vo_stats.py`) |
| Cliffhanger type | threat ("Lie, and you slip again."), then a decision vote |
| Loops | closes L5 (rescued) · opens L7 (where is Marcus?), L9 (will the killer come for you?) |
| Pays off | Part 3's "the ship is coming back… the killer is watching" (0:00–0:20) and the yellow jacket (0:10–0:16) |
| Branch | **SIGNAL won the Part 3 vote** (chosen for the series; FLOAT and KEEP before it). STRENGTH 70% → 62% before the rescue. |

## First frame
- **On-screen text:** PART 4 · "THE SHIP CAME BACK"
- **Visual:** the two hands on YOU's back (reused from Part 1), then the ship coming back with its searchlights (reused from Part 3).

## Voiceover (paste into TTS)
<!-- VO:START -->
[low, tense, steady] At 2:14 a.m., a man pushed you off a cruise ship. At 4:31, the ship came back.

[firm, urgent] Most of you said signal.

[strained, hoarse] You try to shout. Nothing comes out but salt.

[slow, hopeful, holding breath] So you raise one arm. Bright yellow sleeve. The searchlight slides past you.

[a beat of silence, then a whisper] Stops.

[rising relief] Comes back.

[exhaling, emotional] 5:20 a.m. A rescue boat drags you out. Three hours, six minutes in the water.

[matter-of-fact, quick] Hide voters, rescuers search where the current carries you, not where you fell. They'd have found you around nine.

[clinical, calm] Medical center. A security officer with a notepad.

[confident, revealing] Here's what you don't know. A 2010 US law says cruise ships should have systems that detect people going overboard. "To the extent available." This ship doesn't have one.

[suspicious, pointed] And the camera on deck five?

[tired, official] "Broken since Tuesday," she says. "Where's your brother?"

[uneasy, quick] Not in his cabin. Bed not slept in.

[official, reassuring] "We dock in Cozumel at ten. We'll find him before then."

[slowing down, dread building] She turns her laptop around. Deck six camera. 2:13 a.m. A man at the rail, right above where you fell. Watching.

[quiet, heavy] At 2:15, he walks away.

[breaking, barely a whisper] It's Marcus.

[hurt, slow, cold] Your brother watched you go over. And did nothing.

[sharp, a jolt] Then, a knock.

[official, unaware] "A passenger saw what happened," she says.

[low, recognizing, menace] Gray polo. Steel watch. Table nine.

[smooth, fake sympathy] "Poor guy," he tells her. "I saw him slip."

[tense, slow] She steps out to make a call. He sits on the edge of your bed.

[whispering, cold, intimate] "From behind, you really do look like him. Where's he going?"

[whispering, menacing, slow] "Tell me, and you slipped. Lie, and you slip again."

[direct, tense] Tell him about the ferry, or lie?

[lighter, inviting] Comment TELL or LIE. The majority writes the final part.
<!-- VO:END -->

**Optional:** a real vote percentage or a real top comment can replace "Most of you said signal." Never invent a comment.

## If the real vote is HIDE
Replace everything from "Most of you said signal." through "Medical center. A security officer with a notepad." with:

```
[firm, uneasy] Most of you said hide.

[hushed, tense] You sink low. The searchlight slides past you. Twice. At sunrise, the ship gives up and sails on.

[quick, factual] But rescuers don't search where you fell. They search where the current would carry you.

[rising relief] 8:52 a.m. A navy helicopter. A rescue swimmer drops beside you. He spotted the yellow first. Six hours, thirty-eight minutes in the water.

[matter-of-fact] Signal voters, you'd have been out three hours sooner.

[clinical, calm] A hospital in Cozumel. The ship's security officer is already there.
```
Also change "We dock in Cozumel at ten. We'll find him before then." to **"We docked an hour ago. Nobody saw him get off."** The images for this branch would need new prompts; ask before recording.

## Shot list
One image per shot, in the 2D look of the reference reels: see [image-prompts.md](image-prompts.md).

| # | Time | VO | Visual | On-screen text | Sound |
|---|---|---|---|---|---|
| 1 | 0:00 | At 2:14 a.m.… the ship came back. | Flash of the two hands on YOU's back (Part 1), then the ship's lights coming back (Part 3) | PART 4 · THE SHIP CAME BACK · 4:31 AM | Low drone, no fade |
| 2 | 0:05 | Most of you said signal. You try to shout… salt. | Vote card, then YOU opening his mouth to scream; only a rasp, a wave slapping his face | PART 3 · YOU VOTED · SIGNAL | Card thump, hoarse rasp |
| 3 | 0:10 | So you raise one arm… slides past you. | A yellow sleeve raised out of black water; a searchlight beam sweeps past it | HUD STRENGTH 62% | Searchlight hum |
| 4 | 0:16 | Stops. Comes back. | The beam halts, swings back, and locks onto the yellow arm | | Total silence, then a swell |
| 5 | 0:19 | 5:20 a.m. A rescue boat… in the water. | An orange rescue boat; crew hauling YOU over the side | 5:20 AM · 3H 06M IN THE WATER | Outboard motor, shouting |
| 6 | 0:25 | Hide voters… around nine. | Map card: a drift arrow showing the current carrying a dot north | THEY SEARCH THE DRIFT | Quick whoosh |
| 7 | 0:30 | Medical center. A security officer with a notepad. | Ship's medical bay: YOU in the damp yellow jacket under a foil blanket; the SECURITY OFFICER with a notepad | | Monitor beeps |
| 8 | 0:33 | Here's what you don't know… doesn't have one. | Card: the 2010 law, with "to the extent available" highlighted | 2010 US LAW | Typewriter clicks |
| 9 | 0:43 | And the camera on deck five? "Broken since Tuesday." | A CCTV monitor wall; one tile is static | DECK 5 AFT · NO SIGNAL | Static |
| 10 | 0:48 | "Where's your brother?" Not in his cabin… | Empty cabin; a made bed, the suitcase gone | | Door creak |
| 11 | 0:53 | "We dock in Cozumel at ten…" | The officer checking her watch | 10:00 AM DOCKING | |
| 12 | 0:57 | She turns her laptop… Watching. | Laptop CCTV: grainy deck 6 footage, a figure at the rail looking straight down | DECK 6 · 2:13 AM | Drone rises |
| 13 | 1:05 | At 2:15, he walks away. | The figure turns and walks out of frame | 2:15 AM | |
| 14 | 1:08 | It's Marcus. | The CCTV freeze-frame zooms in on the face: MARCUS | | Music cuts; heartbeat |
| 15 | 1:10 | Your brother watched you go over. And did nothing. | YOU's face, foil blanket, eyes filling | | Single low note |
| 16 | 1:14 | Then, a knock. "A passenger saw what happened." | The door opens; the officer gestures someone in | | Knock, two hits |
| 17 | 1:18 | Gray polo. Steel watch. Table nine. | Three quick inserts: gray polo, steel dive watch, the TABLE 9 MAN's face | TABLE 9 | A sting on each insert |
| 18 | 1:22 | "Poor guy… I saw him slip." | The TABLE 9 MAN, warm and concerned, talking to the officer | | |
| 19 | 1:25 | She steps out… edge of your bed. | The door closes behind the officer; he sits; the mattress dips | | Door click, silence |
| 20 | 1:29 | "From behind… Where's he going?" | Close two-shot: he leans in to YOU's ear | "FROM BEHIND, YOU REALLY DO LOOK LIKE HIM." | Whisper |
| 21 | 1:33 | "Tell me, and you slipped. Lie, and you slip again." | Extreme close-up on his eyes, then on YOU's | | Silence, then a deep sting |
| 22 | 1:37 | Tell him… the final part. | Split screen: YOU holding out the ferry ticket vs YOU hiding the wallet under the blanket | COMMENT: TELL or LIE · FINAL PART TOMORROW | Light pulse |

## Caption
```
Part 4/5 · Your brother watched you fall. 💔 Now the man who pushed you is sitting on your bed.

You signaled, and they pulled you out. Then the "witness" walked in.

👇 Comment TELL or LIE. The majority writes the FINAL part.
New here? Start with Part 1 (pinned on my profile).
Follow so you don't miss the finale tomorrow.

#MidnightParts #TheShipKeptGoing #survivalstory #cruiseship #mysterystory
```

## Pinned comment
TELL or LIE? Your brother left you in the water, so do you still protect him? This one decides the ending. ⚖️

## Quality gate
- [x] Hook ≤ 12 words, with a concrete detail plus a threat ("At 2:14 a.m., a man pushed you off a cruise ship.")
- [x] Hook is said and shown in the first frame
- [x] A stranger understands it within 15s
- [x] Previous cliffhanger paid off within the first 20s (the signal decision and the searchlight by 0:19)
- [x] Vote result, a line for the losing side ("Hide voters…"), and the choice shapes the first third (signalling with the yellow sleeve)
- [x] New information every ≤ 8s, a turn every ≤ 15s
- [x] False relief comes before the final turn (rescue and a helpful officer, then Marcus on the footage, then table 9 at the bed)
- [x] Ends worse than it started
- [x] Cliffhanger type differs from Part 3's (arrival there, a direct threat here)
- [x] Last line before the CTA is a threat ("Lie, and you slip again.")
- [x] Loop ledger: closes L5, opens L7 and L9
- [x] VO word count in range
- [ ] Read-aloud test: do this when recording the voice
