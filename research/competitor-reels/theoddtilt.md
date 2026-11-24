# @theoddtilt ("The Odd Tilt"): the 3D "every fix makes it worse" format

- **Reel:** https://www.instagram.com/reel/DfsBDQKE8_A/ ("How you stopped rain putting out your fire! 🌦️ #oddtilt #inventions")
- **Local copy:** `theoddtilt/reel-DfsBDQKE8_A.mp4`. It isn't in git (MP4s are ignored). Re-download it with `yt-dlp -o research/competitor-reels/theoddtilt/reel-DfsBDQKE8_A.mp4 https://www.instagram.com/reel/DfsBDQKE8_A/`
- **Contact sheet:** [theoddtilt/contact-sheet-1s.jpg](theoddtilt/contact-sheet-1s.jpg) (one frame per second)
- **Stats when saved (2026-11-24):** about 23,000 likes and 140 comments.
- **Why it's here:** on 2026-11-24 the owner shared it as the kind of video they want Claude to make **end to end**: Claude does everything, ElevenLabs does the voice, and the owner makes no images. See [../free-tools-plan.md](../free-tools-plan.md).

## What it is
- **Length and size:** 39.1s, 1080×1920, 30 fps.
- **Look:** simple low-poly 3D, which looks like a Blender Eevee render.
  - Flat-shaded huts, stones and logs, and a cartoon flame.
  - Rolling green hills and a blue sky.
  - Rain streaks and puffy smoke particles.
  - The people are plain, barely animated cavemen.
- **Camera:** always moving, with slow orbits and push-ins. Each new invention appears in the shot (it pops or grows in), and the camera re-frames to show it.
- **Escalation:** the scene keeps building on the same set. Fire, then roof, walls, chimney, chimney cap, ropes, rocket, space, glass dome, and finally the Earth seen from orbit.
- **Captions:** white, bold, one or two words at a time, in the middle of the screen.
- **Voice:** one fast, deadpan, slightly sarcastic narrator speaking 143 words in about 37s, which is roughly **230 wpm**. Light music and rain sounds play underneath.
- **POV:** "you" ("you're a genius caveman").

## Structure (the joke engine)
**Problem → "so you" fix → "Except/But" new problem caused by the fix → bigger fix → …** The chain runs absurdly far (into space) and ends by solving the original tiny problem. Interjections ("Genius!", "Clever!") act as beat punctuation.

| t (s) | Line |
|---|---|
| 0.0–1.5 | Rain keeps putting out your fire, |
| 1.8–3.3 | but you're a genius caveman. |
| 3.8–5.0 | So you build a roof over it. |
| 5.5–7.4 | Except the wind blows the rain in from the side, |
| 7.5–9.1 | so you add walls around the fire. |
| 9.4–12.1 | But now smoke fills the room and your tall friend suffocates, |
| 12.4–14.3 | so you build a chimney to carry it outside. |
| 14.8–15.1 | Genius! |
| 15.8–18.7 | But the rain gets down the chimney and puts your fire out anyway, |
| 18.8–20.6 | so you put a little roof over that too. |
| 21.0–21.3 | Clever! |
| 21.9–23.9 | Except the wind keeps blowing the roof off, |
| 24.0–25.3 | so you tie it down with ropes. |
| 25.7–26.9 | But the storm is so strong, |
| 27.1–28.8 | it starts pulling the ground up with it. |
| 28.8–31.3 | So you build a rocket and launch it into space. |
| 31.7–33.2 | Except there's no air in space, |
| 33.5–36.5 | so you install a glass dome around the building pumped full of air. |
| 36.9–38.8 | Now your fire finally stays dry! |

## Notes for making our own
- It is a **one-part** comedy format, not a serial. A new line for the channel would run alongside the suspense and horror series.
- Everything on screen is simple geometry, so a Blender Python script can build all of it. Our locked character YOU (egg head, stick limbs, yellow windbreaker) is easy to build from primitives, and he stays identical in every video.
- The hard part is character animation (walking, gestures). The reference barely animates its people, so poses plus small bobs are enough.
- Keep it to a new image or invention every 2–4s, with one camera move per beat, and finish on a wide "final contraption" shot.
- Ideas in the same shape: keep your ice cream from melting, keep your phone charged on a desert island, stop your neighbour's dog barking, and keep your coffee hot.
