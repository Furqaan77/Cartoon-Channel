# Plan: Claude makes the whole video, using only free tools

**Decided 2026-11-24.**
- The owner doesn't want to generate images any more.
- The owner **won't use any paid API except ElevenLabs** (voice, sound effects, music). No Gemini, OpenAI, fal, Replicate or other paid image or video APIs.
- Everything else must be free and run **locally**.
- This work happens on the owner's **more powerful second PC**, synced through GitHub (https://github.com/Furqaan77/Cartoon-Channel). The running series stay on the old PC. See [../MOVING-PC.md](../MOVING-PC.md).

The reference format they want is [competitor-reels/theoddtilt.md](competitor-reels/theoddtilt.md): a 39s low-poly 3D "every fix makes it worse" reel.

## The free options (researched 2026-11-24)

| # | Tool | Makes | Quality | Needs |
|---|---|---|---|---|
| 1 | **Blender** (free), driven by Python scripts (`blender -b -P script.py`) or the free [Blender MCP](https://github.com/ahujasid/blender-mcp) | 3D reels like @theoddtilt. Claude scripts the scene, objects popping in, camera moves, rain and smoke, then renders headless. | **High** for this look, which is built from simple shapes. YOU is built from primitives and stays locked. The weak spot is character animation. | Blender install (~400 MB). Any NVIDIA GPU works; a faster one renders faster. |
| 2 | **Local image AI**: ComfyUI with free open models (SDXL; Flux; reference-editing models such as **Flux Kontext dev** and **Qwen-Image-Edit**, which take `you.png` as a reference) | 2D stills for the current series (Ship, horror), replacing the owner's image work | **Medium to high**, depending on VRAM. With 16–24 GB, reference-editing models can keep YOU consistent. With 8 GB, only small models fit and consistency is weak. | 15–40 GB of model downloads. Ideally 16 GB+ VRAM. |
| 3 | **Local video AI**: Wan 2.1/2.2, LTX-Video | Short animated clips | Low at 8 GB (480p). Usable 720p with 24 GB (Wan 2.2 14B). Characters drift between clips. | 10–30 GB. Several minutes per 5s clip. |
| 4 | **Code-drawn graphics**: the HyperFrames / Three.js skills already installed for the user | Simple vector cartoons or basic browser 3D | Low to medium (plain backgrounds) | Nothing |

Paid options were looked at and **rejected by the owner**: Nano Banana/Gemini, GPT Image, and fal.ai (Kling/Veo/Seedance).

## Hardware
- **Old PC:** RTX 2070 Super (8 GB VRAM), 50 GB free on C: and 133 GB on D:. Blender works there, but local image and video AI is limited.
- **New PC:** the specs aren't known yet. **First job on the new PC:** run `nvidia-smi` and check RAM and disk. Then choose the model sizes for option 2 and 3. 16 GB+ VRAM unlocks Flux Kontext / Qwen-Image-Edit; 24 GB unlocks Wan 2.2 14B.

## Agreed order of work
1. **Install Blender** on the new PC and **make one 40s test reel** in the @theoddtilt format, starring YOU. The owner judges the quality before we commit.
   - Build YOU as a reusable 3D asset with the locked design from `channel/characters/you/CHARACTER.md`: white egg head, black oval eyes, messy black hair, open yellow windbreaker, white T-shirt, navy shorts, black flip-flops, thin black stick limbs. Save it as `channel/characters/you/you.blend`.
   - Suggested pipeline: write the script, then `tools/make_voiceover.py` (ElevenLabs), then use the word timings to drive the Blender scene script (`tools/build_3d.py`, still to be written), then a headless Eevee render, then audio, captions and music. Either use `tools/build_part.py` with video shots, or add a small mux step.
   - Captions: white, one or two words at a time, mid-screen, matching the reference.
2. If the owner wants the 2D series automated too, **install ComfyUI** and test reference-editing models on Ship S3 Part 4's shot list. Compare them with the owner's own images before switching.
3. Write a new skill or playbook section for the 3D format once the test is approved.

## Rules that still apply
- YOU is locked: never redesign him, and nobody else wears yellow.
- No text inside generated images or renders; all text is added in the edit.
- The ElevenLabs key lives only in `.env`.
- Any third-party skill or MCP must be **read before installing**, and it must not need a paid key.
