# Don't Let Me In: Part 1 of 5, "Let Me In"

| | |
|---|---|
| Target length | 60–80s (about 150–190 words at ~150 wpm, plus pauses) |
| VO word count | see `python tools/vo_stats.py series/003-dont-let-me-in --wpm 150 --target 60,80 --gap 0.3` |
| Cliffhanger type | arrival (the back door handle), then a decision vote |
| Loops | opens L1 (who is the wet you?), L2 (why doesn't it break in?), L3 (which one is real / Lily's wet hair) |
| Pays off | — (Part 1) |

## First frame
- **On-screen text:** corner tag PART 1 · "2:47 AM" · big: **SOMEONE HAS YOUR VOICE**
- **Visual:** the cabin's front door from inside, at night, with a dark shape behind its little window

## Voiceover
Generated with `python tools/make_voiceover.py series/003-dont-let-me-in/part-01`. `{NAME}` picks the voice from [voices.json](../voices.json); no name means the narrator. `(pause N)` is N seconds of silence.

<!-- VO:START -->
[low, close, almost a whisper] Two forty-seven a.m. Someone knocks on the cabin door.

{COPY} [easy, warm, a little too cheerful] "Hey. It's me. Let me in."

[slow, uneasy] That's your voice. And you're on the couch.

(pause 0.6)

[quiet, quick] Your parents are at a wedding till Sunday. You're watching your little sister, Lily. She's eight.

[soft, remembering] At sunset, she fell asleep on the dock, her feet in the lake. You stepped in up to your knee to carry her inside.

[low, tense] The doorbell camera. A man on the porch. Yellow jacket. Soaking wet. Lake weed in his hair.

[very quiet, slow] It's you. Smiling right into the camera.

{LILY} [sleepy, small voice] "Who's at the door?"

[tense whisper] Lily, on the stairs. Her hair's still damp. She must have had a bath.

{COPY} [soft, gentle, sing-song] "Lily? It's me. Let's get you inside."

[cold, slow] Those are your words. What you said on the dock. Exactly.

{LILY} [small, unsure] "He sounds just like you. Which one of you is real?"

[hurried, low] You dial nine-one-one. One bar. Then none.

[exhaling, relieved] Then, the knocking stops. The porch is empty.

(pause 1.0)

[barely a whisper] Behind you, in the kitchen, the back door handle starts to turn.

{LILY} [whispering, frightened] "Did you lock that one?"

[direct, tense] Run and lock it, or grab Lily and hide upstairs?

[lighter, direct] Comment LOCK or HIDE.
<!-- VO:END -->

## Shot list
One still per shot, in the house look made darker: see [image-prompts.md](image-prompts.md). Times are approximate until the voiceover is cut.

| # | Time | VO | Visual | On-screen text | Sound |
|---|---|---|---|---|---|
| 01 | 0:00 | Two forty-seven a.m. Someone knocks… | The front door from inside, a dark shape behind its little window | 2:47 AM · SOMEONE HAS YOUR VOICE | Three knocks, a low drone |
| 02 | 0:04 | "Hey. It's me. Let me in." · That's your voice… | YOU bolt upright on the couch in the dark | | |
| 03 | 0:10 | Your parents are at a wedding… | The cabin from the lake at night: porch light, dock, boathouse | HOLLOW LAKE | Crickets, water |
| 04 | 0:15 | At sunset, she fell asleep on the dock… | Sunset flashback: Lily asleep on the dock, feet in the water | SUNSET | |
| 05 | 0:19 | You stepped in up to your knee… | Sunset flashback: YOU knee-deep, lifting Lily | | Splash |
| 06 | 0:23 | The doorbell camera. A man on the porch… | Doorbell-camera view: a soaked YOU on the porch | FRONT DOOR · REC | Static |
| 07 | 0:28 | It's you. Smiling right into the camera. | Doorbell close-up: his face, the too-wide smile | | Sting |
| 08 | 0:31 | "Who's at the door?" · Lily, on the stairs… | Lily on the stairs in her dinosaur shirt, holding a rabbit | LILY · 8 | |
| 09 | 0:35 | Her hair's still damp… | Close-up: a drop falling from Lily's pigtail | | Drip |
| 10 | 0:38 | "Lily? It's me. Let's get you inside." | YOU between Lily and the door, an arm out | | Knock |
| 11 | 0:42 | Those are your words… | REUSE 05, desaturated | "LET'S GET YOU INSIDE." | |
| 12 | 0:46 | "He sounds just like you. Which one of you is real?" | Lily looking up at YOU, unsure | | |
| 13 | 0:51 | You dial 911… | YOU's face lit by the phone | 911 · NO SIGNAL | Dial tone, cut |
| 14 | 0:55 | Then, the knocking stops… | Doorbell view: the empty porch, wet footprints leading away | | Silence |
| 15 | 1:00 | Behind you, in the kitchen… | The kitchen's back door in moonlight, water under the door | | Silence, then a creak |
| 15b | 1:03 | …the handle starts to turn. "Did you lock that one?" | REUSE 15, push in on the handle | | Handle rattle |
| 16 | 1:07 | Run and lock it, or… Comment LOCK or HIDE. | Vote: 16A YOU running down the hall · 16B YOU carrying Lily upstairs | LOCK / HIDE | Pulse |

## Caption
```
🚪 SOMEONE HAS YOUR VOICE…

2:47 a.m. A knock on the cabin door, and it sounds exactly like you. 😨

👀 Lock the back door, or hide upstairs?
Comment LOCK or HIDE. The majority decides Part 2.

🎬 DON'T LET ME IN · PART 1

#DontLetMeIn #MidnightParts #horrorstory #creepystories #scarystories
```

## Pinned comment
LOCK or HIDE? And… which one is real? 👀

## Quality gate
- [x] Hook ≤ 12 words with a concrete detail plus a threat ("Two forty-seven a.m. Someone knocks on the cabin door." then your own voice)
- [x] Hook said and shown in the first frame
- [x] A stranger understands it within 15s (the knock, your voice, the cabin, parents away, your sister)
- [x] New information every ≤ 8s, a turn every ≤ 15s
- [x] False relief before the final turn (the knocking stops, the porch is empty)
- [x] Ends worse than it started (it's at the back door)
- [x] The last line is a decision, after an arrival
- [x] Loops: opens L1, L2 and L3
- [x] 60–80s
- [ ] Listen-through of the generated voices
