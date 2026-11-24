# Part {{N}}, "{{PART TITLE}}": image prompts

One still image per shot, in the 2D look of the reference reels (playbook §11.1). Shot numbers and times follow [script.md](script.md). {{If it's a vote part: Prompts are written for **OPTION A winning**. The OPTION B swaps are at the bottom.}}

**How to use**
1. The reference images are in this part's [reference-images/](reference-images/) folder. Attach the ones listed under **Refs** to each prompt (e.g. **Refs:** you-wet = `reference-images/you-wet.png`).
2. Paste each prompt exactly as written. Every prompt is complete, with the style included.
3. Save each image as `part-{{NN}}/images/NN.png` (e.g. `07a.png`).
4. **Text cards** need no image. Build them in the edit, using the card styles in the reference file. All on-screen text is added in the edit, never by the image model.
5. Movement is added in the edit, as in the reference reels. You can also animate a still with image-to-video.

**This part's look:** {{palette and light per section of the part, and the HUD values}}

**To make:** {{n}} images, {{n}} text cards and {{n}} reused images.

---

### 01 · 0:00 · "{{VO line}}"
**Refs:** {{reference files}} · **On screen:** PART {{N}} · {{HOOK TEXT}} · **Move:** {{push-in / pan / shake / hold}}

**Prompt -**
```text
{{Shot and angle}}: {{the exact character phrase from the series plan}} {{action and expression}}, {{setting}}, {{light}}. 2D hand-drawn cartoon illustration, bold clean black ink outlines, stick-figure characters with smooth white egg-shaped heads and thin black stick limbs, richly detailed textured background, muted painterly colors, moody cinematic lighting, vertical 9:16, no text, no lettering, no watermark
```

### 02a · 0:05 · TEXT CARD (vote result, cream) · "{{VO line}}"
- Label: PART {{N-1}} · YOU VOTED
- Bars: {{A}} {{A_%}} (accent color) · {{B}} {{B_%}} (black)

### 05 · 0:23 · TEXT CARD (dark) · "{{VO line}}"
- Label (accent monospace): {{RULE N}}
- Line (bold white): {{the rule}}
- Small gray line: {{earlier rule or context}}

### 07 · 0:31 · TEXT CARD (cream) · "{{VO line}}"
- Label: {{SMALL MONOSPACE LABEL}}
- Big: **{{number or short line}}** (the key word on an accent highlight)
- Small line: {{one short line}}

### 10b · 0:49 · "{{VO line}}"
**REUSE** `part-{{NN}}/images/{{NN}}.png` ({{what it shows}}), with {{the move}}.

### 20 · 1:30 · "{{CTA line}}" (two images, stacked top and bottom)
**Refs:** {{refs}} · **On screen:** vote buttons **{{A}}** (white) / **{{B}}** (accent) · PART {{N+1}} TOMORROW · THE MAJORITY DECIDES

**20A**

**Prompt -**
```text
{{option A image}}. 2D hand-drawn cartoon illustration, bold clean black ink outlines, stick-figure characters with smooth white egg-shaped heads and thin black stick limbs, richly detailed textured background, muted painterly colors, moody cinematic lighting, square 1:1, no text, no lettering, no watermark
```
**20B**

**Prompt -**
```text
{{option B image}}. 2D hand-drawn cartoon illustration, bold clean black ink outlines, stick-figure characters with smooth white egg-shaped heads and thin black stick limbs, richly detailed textured background, muted painterly colors, moody cinematic lighting, square 1:1, no text, no lettering, no watermark
```

---

## If {{OPTION B}} wins
- {{shot}}: {{replacement prompt or reuse}}
