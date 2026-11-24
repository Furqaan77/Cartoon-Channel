"""Write image-prompts.md for Don't Let Me In, Parts 2-5, from compact shot specs (keeps the locked phrases exact)."""
import pathlib

ROOT = pathlib.Path("D:/CORTOON CHANNEL/series/003-dont-let-me-in")
P = {
    "YOU": "a stick-figure man with a smooth white egg-shaped head, short messy black hair, small simple black oval eyes, a bright yellow zip-up windbreaker with a high collar worn open over a plain white crew-neck T-shirt, knee-length dark navy drawstring shorts and black flip-flops, thin black stick arms and legs, white cartoon hands",
    "YOUC": "a stick-figure man with a smooth white egg-shaped head, short messy black hair, small simple black oval eyes and the high collar of a bright yellow windbreaker",
    "COPY": "a stick-figure man with a smooth white egg-shaped head, wet black hair plastered flat, small simple black oval eyes, a soaked bright yellow zip-up windbreaker worn open over a wet white crew-neck T-shirt, knee-length dark navy drawstring shorts, thin black stick arms and legs, white cartoon hands, a strand of dark green lake weed hanging from his hair, water dripping from his sleeves, a smile slightly too wide, unblinking eyes",
    "COPYC": "a stick-figure man with a smooth white egg-shaped head, wet black hair plastered flat, small simple black oval eyes and the high collar of a soaked bright yellow windbreaker, a strand of dark green lake weed hanging from his hair, water running down his face, a smile slightly too wide, unblinking eyes",
    "LILY": "a small stick-figure girl about eight years old with a smooth white egg-shaped head, light-brown hair in two short pigtails tied with red hair ties, small simple black oval eyes, an oversized faded purple T-shirt with a small green dinosaur on the front worn as a nightshirt, pink shorts and bare feet, thin black stick arms and legs, white cartoon hands",
    "LILYS": "a small stick-figure girl with light-brown pigtails tied with red hair ties and an oversized purple dinosaur nightshirt",
    "PRUITT": "an old stick-figure man with a smooth white egg-shaped head, thin wispy white hair, thick round black-rimmed glasses, a gray knitted cardigan over a red-and-black plaid flannel shirt, baggy khaki trousers and green rubber boots, thin black stick arms and legs, white cartoon hands",
}
BASE = "2D hand-drawn cartoon illustration, bold clean black ink outlines, stick-figure characters with smooth white egg-shaped heads and thin black stick limbs, richly detailed textured background, muted painterly colors, "
LIGHT = {
    "night": "dark moody night lighting with cold blue moonlight, eerie horror atmosphere",
    "sepia": "faded sepia tones like an old photograph, dim lamplight, quiet eerie atmosphere",
    "dawn": "cold gray-blue dawn light with the first gold on the horizon, eerie hushed atmosphere",
    "sunrise": "warm golden sunrise light breaking through mist, hopeful but uneasy atmosphere",
    "morning": "soft bright morning light, calm but uneasy atmosphere",
}


def tail(light, square=False):
    return BASE + LIGHT[light] + (", square 1:1" if square else ", vertical 9:16") + ", no text, no lettering, no watermark"


def fill(s):
    for k in sorted(P, key=len, reverse=True):
        s = s.replace("{" + k + "}", P[k])
    return s


def render(part, title, intro, look, shots, swaps):
    n_img = sum(1 for s in shots if s.get("prompt") or s.get("vote"))
    n_img += sum(1 for s in shots if s.get("vote"))
    n_card = sum(1 for s in shots if s.get("card"))
    n_reuse = sum(1 for s in shots if s.get("reuse"))
    out = [f"# Part {part}, \"{title}\": image prompts", "",
           f"One still image per shot, in the house look made darker for horror (see [reference/character-prompts.md](../reference/character-prompts.md)). Shot numbers follow [script.md](script.md). {intro}", "",
           "**How to use**",
           "1. The reference images are in this part's [reference-images/](reference-images/) folder. Attach the ones listed under **Refs** to each prompt. **Always attach `you.png` whenever YOU is in the shot, and `you-wet.png` for the copy.**",
           "2. Paste each prompt exactly as written. Every prompt is complete, with the style included.",
           f"3. Save each image in `part-0{part}/images/` under the name shown in **Save as**.",
           "4. All on-screen text, cards, captions and vote buttons are added in the edit, never by the image model.", "",
           f"**This part's look:** {look}", "",
           f"**To make:** {n_img} images, {n_card} text cards and {n_reuse} reused images.", "", "---", ""]
    for s in shots:
        head = f"### {s['id']} · {s['t']} · "
        if s.get("card"):
            out += [head + f"TEXT CARD (dark) · \"{s['vo']}\"", *[f"- {x}" for x in s["card"]], ""]
            continue
        if s.get("reuse"):
            out += [head + f"\"{s['vo']}\"", f"**REUSE** {s['reuse']}", ""]
            continue
        if s.get("vote"):
            out += [head + f"\"{s['vo']}\" (two images, stacked top and bottom)",
                    f"**Refs:** {s['refs']} · **On screen:** vote buttons **{s['vote'][0]}** (white) / **{s['vote'][1]}** (red)", ""]
            for suffix, prompt, light in (("A", s["a"], s.get("light", "night")), ("B", s["b"], s.get("light_b", s.get("light", "night")))):
                out += [f"**Save as:** `{s['id']}{suffix}.png`", "", "**Prompt -**", "```text", fill(prompt) + ". " + tail(light, square=True), "```", ""]
            continue
        meta = f"**Refs:** {s['refs']}"
        if s.get("on"):
            meta += f" · **On screen:** {s['on']}"
        meta += f" · **Move:** {s['move']}"
        out += [head + f"\"{s['vo']}\"", meta, "", f"**Save as:** `{s['id']}.png`", "", "**Prompt -**", "```text",
                fill(s["prompt"]) + ". " + tail(s.get("light", "night")), "```", ""]
    if swaps:
        out += ["---", "", f"## If {swaps[0]} wins"]
        for line in swaps[1:]:
            out.append(fill(line))
        out.append("")
    (ROOT / f"part-0{part}" / "image-prompts.md").write_text("\n".join(out), encoding="utf-8")


# ------------------------------------------------------------------ Part 2
render(2, "Rule One", "Written for **LOCK winning**; the HIDE swaps are at the bottom.",
       "blue-black night in the cabin; Pruitt's side of the lake has one warm lamp. Two dark rule cards. The copy is always soaked and smiling.",
       [
           {"id": "01", "t": "0:00", "vo": "You chose lock.", "refs": "you-wet, cabin-inside", "on": "PART 2 (corner) · YOU CHOSE LOCK", "move": "slow push-in on the face",
            "prompt": "Inside a dark cabin kitchen at night, looking at a back door with small glass panes: pressed against the glass from outside, the face and hands of {COPYC}, his breath fogging the pane, water streaming down the glass, the brass handle turned halfway down, cold moonlight behind him"},
           {"id": "02", "t": "0:02", "vo": "Down the hall. Past the dark windows. The handle is still turning.", "reuse": "Part 1's `16A.png` (YOU sprinting down the hall). I copy it in."},
           {"id": "03", "t": "0:06", "vo": "You slam the bolt. Click.", "refs": "you", "move": "fast push-in, shake on the click",
            "prompt": "Extreme close-up at night of a white cartoon hand coming out of a bright yellow sleeve slamming an old brass slide bolt shut on a wooden back door, the door frame shaking, a sliver of moonlight, water seeping under the door onto the floorboards"},
           {"id": "04", "t": "0:08", "vo": "On the other side of the glass, your own face. Dripping. Smiling. 'Let's get you inside.'", "reuse": "`01.png`, pushed in close on the face, with \"LET'S GET YOU INSIDE.\" on screen."},
           {"id": "05", "t": "0:15", "vo": "Same words. Same voice. Like a recording. Then the old phone on the kitchen wall rings.", "refs": "you, cabin-inside", "move": "slow push-in, shake on each ring",
            "prompt": "A dark old cabin kitchen at night: an old yellowed corded telephone mounted on the knotty pine wall, its handset rattling as it rings, {YOU}, standing frozen beside it with his back pressed to the bolted back door, staring at the phone with wide eyes, a dripping tap, moonlight through the window"},
           {"id": "06", "t": "0:21", "vo": "'This is Walt Pruitt, across the lake. I can see your porch.'", "refs": "pruitt", "on": "WALT PRUITT · ACROSS THE LAKE", "move": "slow push-in",
            "prompt": "Inside a cluttered old cabin across a lake at night, lit by one warm table lamp: {PRUITT}, standing at a dark window holding an old corded phone to his ear with one hand and a pair of binoculars in the other, peering out across the black water, fishing rods and old photographs on the wall behind him"},
           {"id": "07", "t": "0:26", "vo": "'Who's standing out there?' You almost say, 'Me.'", "refs": "cabin", "move": "slow push-in toward the porch",
            "prompt": "A view across a wide black lake at night from a far shore, as if through binoculars, with a soft dark circular vignette: a small wooden cabin on the opposite shore with one dim porch light, and on the porch a tiny figure in a bright yellow jacket standing perfectly still facing the door, mist on the water, pine trees, moonlight"},
           {"id": "08", "t": "0:31", "vo": "'Listen. Rule one. It can't come in unless someone who lives there lets it in.'", "card": ["Label (red monospace): RULE 1", "Line (bold white): It can't come in unless someone who lives there lets it in."]},
           {"id": "09", "t": "0:38", "vo": "'Rule two. It only says words it heard by the water.'", "card": ["Label (red monospace): RULE 2", "Line (bold white): It only says words it heard by the water.", "Small gray line: RULE 1 · It can't come in unless someone who lives there lets it in."]},
           {"id": "10", "t": "0:42", "vo": "Your words. From the dock. At sunset.", "reuse": "Part 1's `05.png` (YOU lifting Lily at sunset), desaturated. I copy it in."},
           {"id": "11", "t": "0:46", "vo": "'Don't open a door. Don't open a window. At sunrise, it goes back in the lake.'", "refs": "pruitt", "move": "slow push-in on his eyes",
            "prompt": "Close-up at night in a dim old cabin lit by one warm lamp: {PRUITT}, holding an old corded phone to his ear, his face grave and frightened behind thick glasses, a lamp reflected in the lenses, old framed photographs of a smiling woman on the wall behind him"},
           {"id": "12", "t": "0:52", "vo": "Sunrise is five fifty-one. It's three twenty. Two and a half hours. Locked doors. You can do that.", "refs": "you, cabin-inside", "on": "SUNRISE 5:51 · NOW 3:20", "move": "slow pull-out",
            "prompt": "A dark cabin kitchen at night: {YOU}, sliding down to sit on the floor with his back against a bolted wooden back door, knees up, head tipped back, letting out a long shaky breath of relief, an old round wall clock above the sink, moonlight on the floorboards, small wet smudges on the outside of the door's glass panes"},
           {"id": "13", "t": "1:00", "vo": "Upstairs, Lily is talking to someone. 'Okay. I'll ask him.'", "refs": "cabin-inside", "move": "slow push-in toward the door",
            "prompt": "The narrow upstairs hallway of an old lake cabin at night, seen from the top of the stairs: a child's bedroom door at the end standing ajar, cold moonlight and a breeze spilling out of the gap, a curtain moving inside, a small gray stuffed rabbit dropped on the hallway floor, deep shadows on the pine walls"},
           {"id": "14", "t": "1:05", "vo": "Her window is open.", "refs": "lily", "move": "slow push-in",
            "prompt": "A small child's bedroom in a lake cabin at night, seen from the doorway: {LILY}, kneeling on her bed in front of a wide-open window with thin white curtains blowing inward, leaning out on her elbows and talking down to someone below, her pigtails still damp, cold moonlight pouring in, the black lake and pine trees outside"},
           {"id": "15", "t": "1:08", "vo": "And you are standing under it. Looking up.", "refs": "you-wet, cabin", "move": "very slow push-in down onto him",
            "prompt": "Looking straight down from an upstairs window at night onto a dark lawn beside a lake cabin: {COPY}, standing on the wet grass directly below, his head tipped all the way back, looking straight up at the viewer, a puddle around his bare feet, moonlight glinting on the wet jacket, the black lake behind him"},
           {"id": "16", "t": "1:12", "vo": "Pull her away from the window, or listen first? Comment PULL or LISTEN.", "refs": "you, lily", "vote": ("PULL", "LISTEN"),
            "a": "A child's bedroom at night with an open window and blowing curtains: {YOU}, grabbing {LILYS} around the waist and pulling her back from the open window, her arms reaching toward it, moonlight",
            "b": "A dark upstairs hallway at night: {YOUC}, frozen in the half-open doorway of a child's bedroom, holding his breath and listening, one hand on the door frame, a small girl's silhouette at the moonlit window inside"},
       ],
       ["HIDE", "- **01 and 04:** make this instead of `01.png`, then REUSE it for 04:", "```text",
        "Inside a dark lake cabin at night, at the top of a narrow staircase: a small landing window with its curtain half open, and pressed against the glass from outside, the face and hands of {COPYC}, water streaming down the glass, cold moonlight behind him. " + tail("night"),
        "```", "- **02:** REUSE Part 1's `16B.png` (YOU carrying Lily up the stairs)."])

# ------------------------------------------------------------------ Part 3
render(3, "It Never Dries", "Written for **LISTEN winning**; the PULL swap is at the bottom.",
       "blue-black night; the three 1987 flashbacks (06–08) are faded sepia. Small wet footprints glint in the moonlight.",
       [
           {"id": "01", "t": "0:00", "vo": "You chose listen. You stop in the doorway. Lily's at the window. Below it, your voice. Soft.", "refs": "lily, you-wet, cabin", "on": "PART 3 (corner) · YOU CHOSE LISTEN", "move": "slow push-in past her toward the yard",
            "prompt": "A small child's bedroom at night seen from behind: {LILY}, kneeling on the bed at a wide-open window with white curtains blowing, leaning out, and far below on the moonlit lawn, a small figure in a soaked bright yellow jacket looking up at her, the black lake beyond"},
           {"id": "02", "t": "0:05", "vo": "'Ask him to open the door, Lily.'", "refs": "you-wet, cabin", "move": "slow push-in",
            "prompt": "Low angle at night on the wet lawn beside a lake cabin: {COPY}, standing under a lit upstairs window and looking up at it, his mouth open mid-word as if whispering up to someone, one white cartoon hand cupped beside his mouth, moonlight and mist"},
           {"id": "03", "t": "0:08", "vo": "Not 'let me in.' Ask him. It needs you to do it.", "reuse": "`02.png`, pushed in hard on his face, with IT NEEDS YOU on screen."},
           {"id": "04", "t": "0:13", "vo": "'He says he's cold. Can we let him in?'", "refs": "lily", "move": "slow push-in on her face",
            "prompt": "A child's bedroom at night: {LILY}, turning around from an open window to look at the viewer with a sweet, hopeful smile, her pigtails damp and a drop of water falling from one, white curtains blowing behind her, cold moonlight on half her face"},
           {"id": "05", "t": "0:17", "vo": "You shut the window. You call Pruitt back.", "refs": "you, cabin-inside", "move": "slow push-in",
            "prompt": "A dark old cabin kitchen at night: {YOU}, holding an old yellowed corded wall phone to his ear and looking up at the ceiling toward the upstairs rooms with a worried face, the curly phone cord stretched tight, moonlight through the window"},
           {"id": "06", "t": "0:20", "vo": "'Summer of eighty-seven, my wife Ruth went swimming after dark. Came home at two a.m. I let her in.'", "refs": "pruitt", "on": "1987", "move": "slow push-in", "light": "sepia",
            "prompt": "An old photograph-style flashback at night: a younger stick-figure man with a smooth white egg-shaped head, short dark hair, thick round black-rimmed glasses and a plaid flannel shirt, opening a cabin front door, and standing on the porch a stick-figure woman with a smooth white egg-shaped head and long dark hair in a white nightgown, soaking wet, water dripping from her hair and hem onto the porch boards, smiling"},
           {"id": "07", "t": "0:27", "vo": "'She never dried.'", "refs": "none", "move": "slow push-in", "light": "sepia",
            "prompt": "An old photograph-style flashback: a bed in a dim cabin bedroom, a white pillow soaked dark with water in the shape of long spread-out hair, water dripping from the edge of the mattress onto the floorboards into a puddle, a bedside lamp, a calendar on the wall"},
           {"id": "08", "t": "0:31", "vo": "'Ten days later, the divers found the real Ruth. Under my boathouse.'", "refs": "none", "move": "slow push-in toward the water", "light": "sepia",
            "prompt": "An old photograph-style flashback at dawn: an old wooden boathouse on stilts over a misty lake, two divers' dark shapes in the water beside it, a rowboat, and a single woman's slipper floating on the black water under the boards"},
           {"id": "09", "t": "0:36", "vo": "'Who touched the water tonight? After dark?' You did. Up to your knee. Carrying Lily.", "refs": "you", "move": "fast push-in",
            "prompt": "Close-up in a dark cabin kitchen at night: {YOUC}, holding an old corded phone to his ear, his eyes going wide as big white circles with tiny pupils as he realizes something terrible, moonlight on one side of his face"},
           {"id": "10", "t": "0:42", "vo": "'Then that thing is you. And it wants your place.' 'Walt? Come back to bed.'", "refs": "pruitt", "move": "slow push-in on the doorway behind him",
            "prompt": "Inside a dim old cabin at night lit by one warm lamp: {PRUITT}, holding an old corded phone to his ear and speaking urgently, and behind him, in a dark open bedroom doorway, the faint silhouette of an old woman with long gray hair standing very still, a small puddle on the floor at her bare feet"},
           {"id": "11", "t": "0:48", "vo": "'Rule three. It never dries.'", "card": ["Label (red monospace): RULE 3", "Line (bold white): It never dries.", "Small gray line: RULE 1 · It can't come in unless someone who lives there lets it in. RULE 2 · It only says words it heard by the water."]},
           {"id": "12", "t": "0:51", "vo": "You check your leg. Dry. You're you.", "refs": "you", "move": "slow push-in",
            "prompt": "Close-up at night in a dim cabin kitchen of a stick-figure man's thin black stick leg and knee below knee-length dark navy drawstring shorts, with the hem of a bright yellow windbreaker at the top of the frame, a white cartoon hand pressed against the knee, the leg completely dry, a black flip-flop on the wooden floor, moonlight"},
           {"id": "13", "t": "0:56", "vo": "Then you see the footprints. Small. Wet. From Lily's room to the front door.", "refs": "cabin-inside", "move": "slow push along the footprints",
            "prompt": "The floor of a dark old lake cabin at night, low angle: a trail of small wet bare child's footprints glistening in the moonlight, coming down the wooden staircase and crossing the floorboards straight to the closed front door, a few drops of water between them"},
           {"id": "14", "t": "1:01", "vo": "She's standing there. Hand on the bolt. 'He says there's room for both of you.'", "refs": "lily, cabin-inside", "move": "very slow push-in",
            "prompt": "Inside a dark lake cabin at night: {LILY}, standing on tiptoe at the wooden front door with one small white cartoon hand on the brass deadbolt, looking back over her shoulder at the viewer with a calm sweet smile, her damp pigtails dripping onto a small puddle at her feet, a dark shape behind the door's little window"},
           {"id": "15", "t": "1:08", "vo": "Grab her, or talk her away from the door? Comment GRAB or TALK.", "refs": "you, lily, cabin-inside", "vote": ("GRAB", "TALK"),
            "a": "Inside a dark cabin at night by the front door: {YOU}, lunging forward to grab the small wrist of {LILYS}, whose hand is on the brass deadbolt, moonlight",
            "b": "Inside a dark cabin at night by the front door: {YOU}, kneeling a few steps away with both open hands held out calmly, talking gently to {LILYS} standing at the door with her hand on the deadbolt, moonlight"},
       ],
       ["PULL", "- **01:** REUSE Part 2's `16A.png` (YOU pulling Lily back from the window)."])

# ------------------------------------------------------------------ Part 4
render(4, "Which One Is Real", "Written for **GRAB winning**; the TALK swap is at the bottom.",
       "blue-black night going toward a gray-blue pre-dawn by shot 11. Lily now drips openly, and the copy stands at the open door, unable to cross.",
       [
           {"id": "01", "t": "0:00", "vo": "You chose grab. You lunge. You catch her wrist.", "refs": "you, lily, cabin-inside", "on": "PART 4 (corner) · YOU CHOSE GRAB", "move": "fast push-in, shake",
            "prompt": "Close-up inside a dark cabin at night by the front door: a white cartoon hand coming out of a bright yellow sleeve gripping the thin wrist of {LILYS}, whose hand is on a brass deadbolt, water running off her small fingers and spattering on the floor, moonlight"},
           {"id": "02", "t": "0:05", "vo": "It's ice cold. And wet. Like something pulled from the lake.", "refs": "lily", "move": "slow push-in",
            "prompt": "Extreme close-up at night of a small child's white cartoon hand, pale and faintly blue-white, soaking wet, water dripping from each fingertip, a thin strand of dark green lake weed caught around the wrist, cold moonlight"},
           {"id": "03", "t": "0:09", "vo": "Her hair is dripping onto the floor. It never dried.", "refs": "lily, cabin-inside", "on": "IT NEVER DRIES", "move": "slow push-in on the drips",
            "prompt": "Inside a dark lake cabin at night, from behind: {LILY}, standing at the front door, her two pigtails soaking wet and dripping steadily onto a widening puddle around her bare feet on the floorboards, moonlight on the water"},
           {"id": "04", "t": "0:14", "vo": "She slides the bolt anyway. Opens the door wide.", "refs": "lily, cabin-inside", "move": "slow push-in",
            "prompt": "Inside a dark lake cabin at night: the wooden front door swinging wide open, pulled by {LILYS}, cold mist and moonlight spilling in from the porch across the floor, a dim porch light outside"},
           {"id": "05", "t": "0:17", "vo": "The copy is right there. Toes on the line. It doesn't come in. It can't.", "refs": "you-wet, cabin", "move": "very slow push-in",
            "prompt": "Looking out through a wide-open cabin front door at night: {COPY}, standing on the porch exactly at the threshold, his bare toes touching the edge of the door frame and not one inch further, arms hanging at his sides, water pooling around his feet, the dim porch light above, the black misty lake behind him"},
           {"id": "06", "t": "0:23", "vo": "'It doesn't work when I do it. It has to be you.'", "refs": "lily, cabin-inside", "move": "slow push-in",
            "prompt": "Inside a dark cabin at night by an open front door: {LILY}, looking back over her shoulder at the viewer with a flat, patient, unblinking expression, her pigtails dripping, a soaked figure in a yellow jacket standing just outside the doorway behind her"},
           {"id": "07", "t": "0:27", "vo": "'Which one of you is real? I was just checking.'", "refs": "lily", "move": "very slow push-in, hold",
            "prompt": "Close-up at night: {LILY}, her head tilted to one side with a sweet, too-calm smile, unblinking eyes, water running from her pigtails down her cheeks, a strand of dark green lake weed in her hair, cold moonlight on her face, darkness behind her"},
           {"id": "08", "t": "0:32", "vo": "At sunset, you carried her in from the dock. You carried it in.", "reuse": "Part 1's `05.png` (YOU lifting Lily at sunset), darkened, with a slow push onto the dark water and YOU CARRIED IT IN on screen. I copy it in."},
           {"id": "09", "t": "0:37", "vo": "Then where's Lily?", "refs": "you, cabin-inside", "move": "fast push-in",
            "prompt": "Inside a dark lake cabin at night: {YOU}, stumbling backward away from an open front door, his eyes huge white circles with tiny pupils, mouth open in horror, moonlight across the floor"},
           {"id": "10", "t": "0:40", "vo": "'Under your boathouse. Till sunrise. After that, the lake keeps her.'", "refs": "boathouse", "move": "slow push-in on the hand",
            "prompt": "Inside an old wooden boathouse at night, low angle at the floor: between two dark floorboards, a narrow gap over black water, and just under the surface a small pale child's hand with its fingers spread against the underside of the boards, a strand of lake weed drifting, thin bars of moonlight"},
           {"id": "11", "t": "0:46", "vo": "Five twenty-one. Thirty minutes.", "refs": "cabin-inside", "on": "SUNRISE IN 0:30", "move": "slow push-in on the clock", "light": "dawn",
            "prompt": "A dark old cabin kitchen just before dawn: an old round wall clock with plain hands pointing to twenty past five, a window above the sink turning gray-blue, the black lake beginning to show through the mist outside, a dripping tap"},
           {"id": "12", "t": "0:49", "vo": "You slam the door. When you look again, the porch is empty.", "refs": "cabin", "move": "hold, then slow push-in", "light": "dawn",
            "prompt": "Looking through the small square window of a closed cabin front door just before dawn: an empty porch, only a large puddle where someone stood and a trail of wet bare footprints leading off the porch steps, the lake and mist beyond in gray-blue light"},
           {"id": "13", "t": "0:55", "vo": "Wet footprints lead down the lawn. Straight to the boathouse.", "refs": "cabin, boathouse", "move": "slow push along the footprints", "light": "dawn",
            "prompt": "A sloping lawn behind a lake cabin just before dawn: a trail of wet bare footprints glistening in the dewy grass, leading straight down to a small wooden boathouse on stilts at the water's edge, its door hanging open, black inside, mist on the lake"},
           {"id": "14", "t": "1:00", "vo": "Climb out the window and run, or call Pruitt to row across? Comment WINDOW or BOAT.", "refs": "you, pruitt", "vote": ("WINDOW", "BOAT"), "light": "dawn",
            "a": "The back of a lake cabin just before dawn: {YOU}, climbing out of a ground-floor window, one flip-flopped foot reaching for the wet grass, the boathouse visible down the slope in the mist",
            "b": "A misty lake just before dawn: {PRUITT}, rowing an old wooden rowboat hard across the gray water toward a small cabin and boathouse on the far shore, a metal flashlight lit in the bow"},
       ],
       ["TALK", "- **01:** make this instead of `01.png`:", "```text",
        "Inside a dark cabin at night by the front door: {YOU}, kneeling with both open hands held out, and {LILYS} turning away from the deadbolt toward him, water running off her small fingers onto the floor. " + tail("night"),
        "```"])

# ------------------------------------------------------------------ Part 5
render(5, "Sunrise", "Written for **WINDOW winning**; the BOAT swap is at the bottom.",
       "pre-dawn gray-blue in the boathouse, then the sunrise turns everything gold at shot 08; morning light for the ending, and the last sting is soft and bright.",
       [
           {"id": "01", "t": "0:00", "vo": "You chose window. Out the back window. Down the wet grass.", "refs": "you, cabin, boathouse", "on": "PART 5 · FINALE (corner) · YOU CHOSE WINDOW · SUNRISE IN 0:30", "move": "fast push toward the boathouse", "light": "dawn",
            "prompt": "Behind a lake cabin just before dawn: {YOU}, landing in a crouch on the wet grass under an open window, already looking down the slope toward a small wooden boathouse on stilts in the mist, wet footprints in the grass leading to it"},
           {"id": "02", "t": "0:05", "vo": "The boathouse door hangs open.", "refs": "boathouse, cabin", "move": "slow push-in into the dark", "light": "dawn",
            "prompt": "Close to an old wooden boathouse on stilts at the edge of a misty lake just before dawn: its door hanging open on one hinge, pitch black inside, a trail of wet bare footprints on the planks leading in, water lapping at the pilings"},
           {"id": "03", "t": "0:08", "vo": "Inside, black water. And between the floorboards, a small white hand.", "refs": "boathouse", "move": "slow push-in on the hand",
            "prompt": "Inside an old wooden boathouse in faint gray dawn light: black still water in the slips, and in a gap between two floorboards a small pale child's hand reaching up out of the water, fingers curled over the edge of a board, thin bars of light through the slatted walls"},
           {"id": "04", "t": "0:13", "vo": "You rip up a board. You reach in. You pull.", "refs": "you, boathouse", "move": "fast push-in, shake", "light": "dawn",
            "prompt": "Inside an old wooden boathouse in faint dawn light: {YOU}, on his knees, having ripped up a floorboard and thrown it aside, plunging both arms elbow-deep into the black water below, straining, splinters flying, water splashing"},
           {"id": "05", "t": "0:17", "vo": "'It's so cold.' The real Lily. Freezing. Breathing.", "refs": "you, lily, boathouse", "on": "THE REAL LILY", "move": "slow push-in", "light": "dawn",
            "prompt": "Inside an old wooden boathouse in faint dawn light: {YOU}, kneeling on the boards and hugging {LILY} to his chest, her hair and nightshirt soaked, strands of lake weed on her, shivering, her eyes half open, his face full of relief"},
           {"id": "06", "t": "0:24", "vo": "Behind you, the doorway goes dark. 'Let's get you inside.'", "refs": "you-wet, boathouse", "move": "very slow push-in", "light": "dawn",
            "prompt": "Inside an old wooden boathouse at dawn, looking toward the open door: {COPY}, filling the doorway as a dark backlit silhouette against the gray-gold dawn mist, water pouring off him onto the planks, his too-wide smile just visible"},
           {"id": "07", "t": "0:30", "vo": "You hold her tight. And you say it too. To her. 'Let's get you inside.'", "refs": "you, lily", "move": "slow push-in, hold", "light": "dawn",
            "prompt": "Close-up in dim dawn light: {YOUC}, his eyes shut, pressing his forehead gently to the forehead of a shivering small stick-figure girl with soaked light-brown pigtails tied with red hair ties, holding her tight, a tear on his face"},
           {"id": "08", "t": "0:37", "vo": "Five fifty-one. The sun hits the lake.", "refs": "cabin", "on": "5:51 AM", "move": "slow pull-out", "light": "sunrise",
            "prompt": "A calm lake at sunrise: the sun breaking over the pine-covered far shore, golden light racing across the water and burning through the mist, a small wooden boathouse on stilts in the foreground catching the first light"},
           {"id": "09", "t": "0:41", "vo": "The thing in the doorway sags. Then it falls. Just water, splashing over the boards.", "refs": "you-wet, boathouse", "move": "shake on the splash", "light": "sunrise",
            "prompt": "The open doorway of an old wooden boathouse hit by golden sunrise light: the figure of a stick-figure man in a soaked bright yellow windbreaker collapsing straight down into a huge splash of lake water, his shape breaking apart into falling water mid-air, a strand of dark green lake weed flying, sparkling droplets"},
           {"id": "10", "t": "0:47", "vo": "Up at the cabin, the front door hangs open. In the hall, a puddle. And a small gray rabbit.", "refs": "cabin-inside", "move": "slow push-in on the rabbit", "light": "morning",
            "prompt": "Inside an old lake cabin in early morning light: the front door hanging wide open, sunlight streaming across the floorboards, and in the middle of the floor a puddle of lake water with a strand of dark green lake weed and a small wet gray stuffed rabbit lying in it, nobody there"},
           {"id": "11", "t": "0:53", "vo": "Morning. Mom calls. 'Honey? Everything okay last night?'", "refs": "you, cabin", "move": "slow push-in", "light": "morning",
            "prompt": "The front porch of a lake cabin in soft morning light: {YOU}, sitting exhausted on the porch steps holding a phone to his ear, dark circles under his eyes, the calm sparkling lake and dock behind him, birds in the trees"},
           {"id": "12", "t": "0:59", "vo": "Lily's asleep on the couch. Her hair is dry.", "refs": "lily, cabin-inside", "move": "slow push-in", "light": "morning",
            "prompt": "Inside a lake cabin in warm morning light: {LILY}, fast asleep on a worn plaid couch under a thick blanket, her light-brown pigtails completely dry and fluffy, holding a small gray stuffed rabbit, sunlight on her face, peaceful"},
           {"id": "13", "t": "1:03", "vo": "Across the lake, Walt Pruitt waves from his dock.", "refs": "pruitt", "move": "slow push-in across the water", "light": "morning",
            "prompt": "A view across a calm sunny lake in the morning: on the far shore a small old cabin with its own wooden dock, and on the dock {PRUITT}, waving slowly, a rowboat tied beside him, pine trees and blue sky"},
           {"id": "14", "t": "1:07", "vo": "Next to him, his wife waves too. Her hair is dripping.", "refs": "pruitt", "move": "very slow push-in, hold", "light": "morning",
            "prompt": "Closer view in bright morning light of a wooden dock on a lake: {PRUITT}, waving, and standing beside him a stick-figure old woman with a smooth white egg-shaped head, long gray hair and a white nightgown, also waving with the same slow motion, her long hair and nightgown soaking wet and dripping onto the dock boards, a smile slightly too wide"},
           {"id": "15", "t": "1:12", "vo": "Would you have opened the door? Comment YES or NO. And follow for the next story.", "refs": "cabin-inside", "on": "YES / NO · FOLLOW FOR THE NEXT STORY", "move": "slow push-in", "light": "morning",
            "prompt": "Inside a lake cabin in morning light, looking straight at the wooden front door with a small square window and a brass deadbolt, the door closed and bolted, sunlight on the floorboards, a faint dried water stain on the floor in front of it"},
       ],
       ["BOAT", "- **01:** REUSE Part 4's `14B.png` (Pruitt rowing across)."])
print("ok")
