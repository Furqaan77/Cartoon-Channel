# Don't Let Me In: reference images and look

The house look (playbook §11.1), made darker for horror. Every part's `reference-images/` folder holds the same 7 files. **Two already exist** (YOU). **Five are new and must be made first**, before any part's images. Their prompts are below and in [reference-brief/](../reference-brief/), which has its own hand-off PDF.

## Reference images

| File | Status | What it is |
|---|---|---|
| `you.png` | ✅ copied from `channel/characters/you/` | YOU, the locked main character (never redesigned) |
| `you-wet.png` | ✅ copied from `channel/characters/you/` | YOU when wet, which is the base for **the copy** |
| `lily.png` | ⬜ **make first** | Lily, your little sister (8) |
| `pruitt.png` | ⬜ **make first** | Walt Pruitt, the old neighbor across the lake |
| `cabin.png` | ⬜ **make first** | The family cabin on Hollow Lake at night: porch, dock, boathouse |
| `cabin-inside.png` | ⬜ **make first** | Inside the cabin at night: front door, couch, stairs, the hall to the kitchen |
| `boathouse.png` | ⬜ **make first** | Inside the boathouse: slips of black water, gaps in the floorboards |

## Prompts for the five new references

**`lily.png`**
```text
Character turnaround sheet: front, three-quarter and back views of the same character standing side by side on a plain off-white background. A small stick-figure girl about eight years old with a smooth white egg-shaped head, light-brown hair in two short pigtails tied with red hair ties, small simple black oval eyes, an oversized faded purple T-shirt with a small green dinosaur on the front worn as a nightshirt, pink shorts and bare feet, thin black stick arms and legs, white cartoon hands, holding a small gray stuffed rabbit by one ear. 2D hand-drawn cartoon illustration, bold clean black ink outlines, simple flat shading, vertical 9:16, no text, no lettering, no watermark
```

**`pruitt.png`**
```text
Character turnaround sheet: front, three-quarter and back views of the same character standing side by side on a plain off-white background. An old stick-figure man with a smooth white egg-shaped head, thin wispy white hair, thick round black-rimmed glasses, a gray knitted cardigan over a red-and-black plaid flannel shirt, baggy khaki trousers and green rubber boots, thin black stick arms and legs, white cartoon hands, a slight stoop, holding an old metal flashlight. 2D hand-drawn cartoon illustration, bold clean black ink outlines, simple flat shading, vertical 9:16, no text, no lettering, no watermark
```

**`cabin.png`**
```text
An old wooden lake cabin at night seen from the end of its dock: a covered front porch with one dim warm porch light and a screen door, dark windows, tall black pine trees behind, a long weathered wooden dock leading to it across still black water, a small wooden boathouse on stilts to one side, low mist on the lake, a full moon reflected in the water, cold blue moonlight. 2D hand-drawn cartoon illustration, bold clean black ink outlines, richly detailed textured background, muted painterly colors, dark moody night lighting with cold blue moonlight, eerie horror atmosphere, vertical 9:16, no text, no lettering, no watermark
```

**`cabin-inside.png`**
```text
The inside of an old wooden lake cabin at night, wide view: knotty pine walls, a worn plaid couch with a blanket, a stone fireplace gone cold, a wooden front door with a small square window and a brass deadbolt, a narrow staircase going up on the right, a dark hallway leading back to the kitchen, moonlight through the windows making long blue shapes on the floor, one small lamp glowing. 2D hand-drawn cartoon illustration, bold clean black ink outlines, richly detailed textured background, muted painterly colors, dark moody night lighting with cold blue moonlight, eerie horror atmosphere, vertical 9:16, no text, no lettering, no watermark
```

**`boathouse.png`**
```text
Inside an old wooden boathouse over a lake at night: two slips of still black water, an old rowboat tied up, oars and orange life rings on the walls, coiled ropes, a narrow plank walkway, gaps between the floorboards showing black water below, thin bars of moonlight through the slatted walls, mist on the water. 2D hand-drawn cartoon illustration, bold clean black ink outlines, richly detailed textured background, muted painterly colors, dark moody night lighting with cold blue moonlight, eerie horror atmosphere, vertical 9:16, no text, no lettering, no watermark
```

## Character phrases (use these exact words in every prompt)
- **YOU:** the locked phrases in [`channel/characters/you/CHARACTER.md`](../../../channel/characters/you/CHARACTER.md), word for word.
- **The copy** (YOU, from the lake): the locked **wet** phrase, then: `a strand of dark green lake weed hanging from his hair, water dripping from his sleeves, a smile slightly too wide, unblinking eyes`. Attach `you-wet.png`. His design never changes; only his state and expression are wrong.
- **Lily:** `a small stick-figure girl about eight years old with a smooth white egg-shaped head, light-brown hair in two short pigtails tied with red hair ties, small simple black oval eyes, an oversized faded purple T-shirt with a small green dinosaur on the front worn as a nightshirt, pink shorts and bare feet, thin black stick arms and legs, white cartoon hands`
  - Her tell (from Part 1 on, subtle until Part 4): `her pigtails still damp, a single drop of water at the end of one pigtail`
- **Walt Pruitt:** `an old stick-figure man with a smooth white egg-shaped head, thin wispy white hair, thick round black-rimmed glasses, a gray knitted cardigan over a red-and-black plaid flannel shirt, baggy khaki trousers and green rubber boots, thin black stick arms and legs, white cartoon hands`
- **Style tail (every prompt):** `2D hand-drawn cartoon illustration, bold clean black ink outlines, stick-figure characters with smooth white egg-shaped heads and thin black stick limbs, richly detailed textured background, muted painterly colors, dark moody night lighting with cold blue moonlight, eerie horror atmosphere, vertical 9:16, no text, no lettering, no watermark`

## Look and edit styles
- **Palette:** blue-black night, one warm lamp or porch light, and wet highlights on the copy. Flashbacks to sunset are warm orange. YOU's yellow is still the brightest thing in every frame.
- **Doorbell camera:** generated as a normal image from a high, slightly fish-eye angle. In the edit it's desaturated, with a cold grade and a "FRONT DOOR · REC" chip.
- **Captions:** 1–3 words, white, with the key word in **red** (`"accent": "#E3262E"` in `edit.json`). A small "PART N" tag sits top-left all the way through (`"corner_tag"`).
- **Cards:** used rarely. A dark card for Pruitt's rules: `RULE 1` in red monospace, the rule in bold white.
- **Vote:** two stacked images, with pill buttons in white and red.
