# @zerotales.stories (Zerotales): "The Second Mom"

The user sent this page on 2026-11-12 as the model for our horror format. It grew very fast. yt-dlp can't list an Instagram profile without logging in, so only the reel the user linked was downloaded and transcribed (faster-whisper medium.en). The visuals were reviewed from a contact sheet at one frame every 2 seconds.

## Part 2 (DfkMoUGp9aD)

- URL: https://www.instagram.com/reel/DfkMoUGp9aD/
- Posted 2026-11-10. Stats at download on 2026-11-12: 8,063 likes and 191 comments (2.4% comments per like).
- **Duration 68s · 135 spoken words · about 120 words/min.** That's much slower than our 170 wpm, with long silences.
- 720×1280. Plain first-person POV renders: dark, flat colours, with a gray-blue palette and lamp light.

**Caption:**

> 📱 THERE ARE TWO MOMS…
>
> You chose the phone. She didn't like that. 😨
>
> Something is waiting upstairs, and you have to make another choice.
>
> 👀 Would you leave the closet or stay hidden?
>
> 🎬 THE SECOND MOM – PART 2
>
> Follow @zerotales for more Animated Thrills.
>
> #TheSecondMom #HorrorTok #CreepyStories #AnimatedThrills #ZeroTales

**Transcript:**

| Time | Voice | Line |
|---|---|---|
| 0:00 | Narrator | You chose the phone. |
| 0:01 | "Mom" (sweet, wrong) | "Sweetie, where are you going?" |
| 0:04 | Narrator | It's Mom's face. Almost. Stretched long, the eyes too far apart, and her mouth hangs open. Wide open. Far too long. |
| 0:14 | Narrator | And she runs. You run, too. Your room. The door. You slam it shut. |
| 0:22 | Narrator | Then, quiet. |
| 0:25 | "Mom" | "Sweetie, why did you run? It's just me. It's Mom. Open the door, please. Your pancakes are getting cold." |
| 0:35 | Narrator | Behind you, the closet door creaks. A hand. A blue sleeve. A hospital badge. |
| 0:41 | Real Mom (whisper) | "Sweetie, in here. Quick, get in. Shh, it's me. It's really me." |
| 0:47 | Narrator | You climb in. She holds you tight. Her heart is pounding. |
| 0:51 | Real Mom | "I came home early. It was already in the kitchen." |
| 0:54 | Narrator | Outside, the scratching stops. Downstairs, the pan starts hissing again. |
| 1:00 | Real Mom | "It's gone. The front door. Now." |
| 1:03 | Narrator | Do you leave the closet or stay? |
| end | On screen | **LEAVE** / **STAY** labels, then "COMMENT →" |

## What it does (and what we copy)

| Device | In the reel | Our version |
|---|---|---|
| **Engine** | A + B: survival horror, and the viewer votes on every move | The same: horror plus a vote at the end of every part |
| **POV** | "You", present tense, and you never speak | The same. YOU is "you"; only his double speaks in his voice. |
| **The vote opens the part** | The first 3 words are the result: "You chose the phone." | "You chose lock." Then show the consequence immediately; no vote card, percentages or "most of you". |
| **Monster** | A **copy of a trusted person**, almost right ("It's Mom's face. Almost.") | A copy of YOU and of your little sister |
| **Ordinary menace** | Polite, sweet lines from the monster: "Your pancakes are getting cold." | The copy says your own kind words back: "Let's get you inside." |
| **Character voices** | The narrator, the fake mom and the real mom are clearly different reads | A cast of ElevenLabs voices (`series/NNN/voices.json`) |
| **Pacing** | 120 wpm, fragments of 1–4 words ("Your room. The door."), and silence used as a beat ("Then, quiet.") | About 150 wpm with `(pause N)` beats, for 60–80s parts |
| **Withhold, then show** | The face is described in three escalating details before we hold on it | Describe in threes, and show the wrong detail (the dripping, the smile) |
| **False relief** | The real mom in the closet, then "the pan starts hissing again" | Locked doors and "two and a half hours, you can do that", then something upstairs |
| **Ending** | A pure decision, with no reveal stacked on it, 65s in | A short reveal or threat, then the decision; the CTA lasts ≤ 4s |
| **Captions** | 1–3 words, white, with the key word in **red**. A tiny "PART 2" tag sits top-left all the way through. | `"accent": "#E3262E"` and `"corner_tag": "PART N"` in `edit.json` |
| **Vote screen** | Two plain labels (white LEAVE, red STAY) over the last frame | Our two stacked images with pill buttons, in red and white |
| **Caption copy** | An emoji headline, a recap with a "she didn't like that" sting, a question, then the series title in caps | The same structure in `publish.md` |

**What we don't copy:** the 3D-ish flat renders and animation. We keep our still-image house look (2D ink, stick figures), darker for horror. We also don't copy their characters, monster design or story.

## Our own reel at the time (for comparison)

@midnight_parts_1, Season 2 Part 3 (`Dfl9mZRRrdd`): posted 2026-11-11, with 230 likes and 14 comments at 1 day (6.1% comments per like, higher than Zerotales). The comment mechanic works; the gap is reach. Shorter parts, a monster hook in the first second, and more voices are the bets for the horror series.
