import re, pathlib, shutil

ROOT = pathlib.Path(r"d:/CORTOON CHANNEL")
SER = ROOT / "series/004-the-ship-kept-going-s3"

TAIL = ("2D hand-drawn cartoon illustration, bold clean black ink outlines, stick-figure characters with smooth white egg-shaped heads "
        "and thin black stick limbs, richly detailed textured background, muted painterly colors, moody cinematic lighting, {fmt}, "
        "no text, no lettering, no watermark")
Y = ("a stick-figure man with a smooth white egg-shaped head, short messy black hair, small simple black oval eyes, a bright yellow zip-up "
     "windbreaker with a high collar worn open over a plain white crew-neck T-shirt, knee-length dark navy drawstring shorts and black "
     "flip-flops, thin black stick arms and legs, white cartoon hands")
YZ = Y.replace("worn open over", "zipped up to the chin over")
YW = ("a stick-figure man with a smooth white egg-shaped head, wet black hair plastered flat, small simple black oval eyes, a soaked bright "
      "yellow zip-up windbreaker worn open over a wet white crew-neck T-shirt, knee-length dark navy drawstring shorts, thin black stick arms "
      "and legs, white cartoon hands")
YC = ("a stick-figure man with a smooth white egg-shaped head, short messy black hair, small simple black oval eyes and the high collar of "
      "a bright yellow windbreaker")
M = ("a stick-figure man with a white egg-shaped head, short neat black hair, a short black beard, a navy button-up shirt with rolled "
     "sleeves and a gold watch")
D = ("a broad-shouldered stick-figure man with a bald white egg-shaped head, heavy black brows, a flat expressionless mouth, a gray polo "
     "shirt and a chunky steel dive watch on his left wrist")
K = ("a stick-figure woman with a white egg-shaped head, short gray-streaked hair, round reading glasses, tired eyes, a dark blazer over a "
     "white shirt and a blue ID lanyard")
L = ("a stick-figure woman with a white egg-shaped head, long curly dark-brown hair tied back with a red bandana, a teal rash-guard top, "
     "khaki cargo shorts and a shark-tooth necklace")
DB = "a low matte-black speedboat with no lights at all and two big outboard motors"
CREW = "two stick-figure men with white egg-shaped heads in black hooded rain jackets and black caps, their faces in shadow"
FB = "a battered white sport-fishing boat with a faded blue stripe, tall outriggers and a small cabin"
CAR = "a dark gray sedan with tinted windows"
JK = "a second bright yellow zip-up windbreaker with a high collar, soaked and dripping, its collar whole and uncut"


def vo_words(vo):
    out = []
    for para in re.split(r"\n\s*\n", vo.strip()):
        para = re.sub(r"^\[[^\]]*\]\s*", "", para.strip())
        out += re.findall(r"[A-Za-z0-9$']+", para.replace("’", "'"))
    return [w.lower() for w in out]


def time_of(vo, anchor, wpm=170):
    words = vo_words(vo)
    a = [w.lower() for w in re.findall(r"[A-Za-z0-9$']+", anchor.replace("’", "'"))]
    for i in range(len(words) - len(a) + 1):
        if words[i:i + len(a)] == a:
            s = i / wpm * 60
            return f"{int(s // 60)}:{int(s % 60):02d}"
    raise SystemExit(f"anchor not found: {anchor!r}")


def img(id, anchor, vis, refs, prompt, on="", move="slow push-in", sound="", fmt="vertical 9:16"):
    return dict(kind="img", id=id, anchor=anchor, vis=vis, refs=refs, prompt=prompt, on=on, move=move, sound=sound, fmt=fmt)


def reuse(id, anchor, vis, src, on="", move="slow push-in", sound=""):
    return dict(kind="reuse", id=id, anchor=anchor, vis=vis, src=src, on=on, move=move, sound=sound)


def card(id, anchor, style, lines, vis, sound="Card thump"):
    return dict(kind="card", id=id, anchor=anchor, style=style, lines=lines, vis=vis, on="(card)", sound=sound)


def vote(id, anchor, a, b, pa, pb, refs, nxt, sound="Light pulse"):
    return dict(kind="vote", id=id, anchor=anchor, a=a, b=b, pa=pa, pb=pb, refs=refs, nxt=nxt, sound=sound,
                vis=f"Vote: {id}A {a} · {id}B {b}", on=f"{a} / {b}")


PARTS = []

# ------------------------------------------------------------------ PART 1
PARTS.append(dict(
    n=1, title="No Lights", cliff="reveal (the man from table nine), then a decision vote",
    loops="half-closes L1 (who's on the boat) · opens L4 (Doyle: enemy or ally?)",
    pays="Season 2's finale (the boat with no lights), from the first line",
    branch="Part 1 of the season: no vote to pay off. It opens on Season 2's last image.",
    first_text="SEASON 3 · PART 1 · \"A BOAT WITH NO LIGHTS\"",
    first_vis="YOU in the bow of the drifting dive boat, the black speedboat with no lights racing toward him",
    look="black sea and starlight, one flashlight beam, then a pink-gold Caribbean dawn on the fishing boat. No HUD in this part; Doyle's deadline doesn't exist yet.",
    vo="""[low, tense, almost a whisper] Midnight. Black water. A boat with no lights, coming straight at you.

[quick, building] Three weeks ago, you fell off a cruise ship in your brother's yellow jacket. Tonight, you're back on the sea. With him.

[cold, flat] His two million dollars vanished this morning. And your engine is off.

[urgent, whispering] "Start it," you whisper. Marcus doesn't move.

[quick, factual] Here's what you should know. At night, boats are supposed to show lights. A boat with no lights doesn't want to be seen.

[tense, slower] Its engines cut out. It drifts right up beside you. Two men in black. A flashlight in your eyes.

[low, cold] One of them says your brother's name. "Marcus. Come on."

[slow, uneasy] He doesn't fight. He doesn't even look surprised. He just steps across.

[desperate, shouting] "Marcus!"

[very quiet] He looks back once. Then the light clicks off. And the boat is gone.

[shaky, fast] You grab the engine. The key is gone.

[cold, quiet] Alone. On black water. Again.

[quiet, uneasy] Why did he stop the engine? Why didn't he fight?

[slow, heavy] You drift for hours. No lights. No land. You zip the jacket up to your chin.

[warming, hopeful] At dawn, a fishing boat. A horn. A rope hits the water next to you.

[relieved, soft] Hands pull you up. A towel. A bottle of water. You're alive.

[cold, slow] Then you see his wrist. A chunky steel dive watch.

[very quiet, menacing] The man from table nine. The man who pushed you off that ship.

[calm, polite, the man] "Morning. Where's your brother?"

[direct, tense] Do you tell him the truth, or lie?

[lighter, direct] Comment TELL or LIE. The majority writes Part 2.""",
    alt=None,
    shots=[
        img("01", "Midnight Black water", "YOU in the bow of the drifting dive boat, the black speedboat racing at him", ["you", "dark-boat"],
            f"Night at sea, low angle from the bow of a small open dive boat with a silent outboard motor: {Y}, crouched and gripping the side, staring back over his shoulder with wide frightened eyes, and behind the boat, cutting across the black water straight toward him with a white wake, {DB}, a sky full of stars",
            on="SEASON 3 · PART 1 · A BOAT WITH NO LIGHTS", move="slow push-in, then a jolt", sound="Speedboat engine rising"),
        reuse("02", "Three weeks ago", "Season 1: the fall from the cruise ship", "Season 1 Part 1's `01.png` (you falling off the cruise ship)", on="3 WEEKS AGO", move="fast push-in, desaturated", sound="Whoosh, splash"),
        reuse("03", "Tonight you're back", "YOU and Marcus in Lucía's boat at night", "Season 2 Part 5's `01.png` (you and Marcus in Lucía's boat at night)"),
        card("04", "His two million dollars", "cream", ["Label: THIS MORNING · 2:14 AM", "Big: BALANCE: **$0**", "Small: And your engine is off."], "Cream card: BALANCE $0"),
        reuse("05", "Start it", "Marcus at the silent wheel", "Season 2 Part 5's `15.png` (Marcus at the silent wheel)", move="slow push-in on his face", sound="Whisper"),
        card("06", "Here's what you should know", "cream", ["Label: BOATS AT NIGHT", "Big: **LIGHTS** ON", "Small: A boat with none doesn't want to be seen."], "Cream card: boats show lights at night"),
        img("07", "Its engines cut out", "The black boat alongside, a flashlight beam in YOU's eyes", ["you", "dark-boat"],
            f"Night at sea, side view: {DB} gliding silently right up alongside a small open dive boat, its motors off, {CREW} standing in it, one of them shining a flashlight beam straight into the face of {Y}, who shields his eyes with one white cartoon hand, the beam a hard white cone in the dark",
            move="slow push-in, flash on the beam", sound="Engines cut, water lapping"),
        img("08", "One of them says", "A gloved hand reaching across to Marcus", ["marcus", "dark-boat"],
            f"Night at sea, two boats side by side: one of {CREW} leaning across the gap from {DB} and holding out a gloved hand, and in the small dive boat {M} standing up calmly to take it, his face lit from below by a flashlight",
            on="\"MARCUS. COME ON.\"", move="slow push-in"),
        img("09", "He doesn't fight", "Marcus stepping across, YOU reaching after him", ["you", "marcus", "dark-boat"],
            f"Night at sea: {M} stepping calmly across from a small open dive boat onto {DB} without looking back, while behind him {Y} reaches out after him with an open hand, his eyes wide white circles with tiny pupils, the flashlight beam swinging away",
            move="pan right with Marcus"),
        img("10", "Marcus", "Close-up: YOU shouting into the dark", ["you"],
            f"Close-up at night: {YC}, shouting with his mouth wide open and his brows tilted up in panic, one white cartoon hand stretched out toward the dark, a flashlight beam sliding off his face, black water behind",
            move="shake", sound="Shout echoes over water"),
        img("11", "He looks back once", "Marcus looking back from the black boat as the light clicks off", ["marcus", "dark-boat"],
            f"Night at sea: at the stern of {DB} as it pulls away, {M} looking back over his shoulder with a blank, unreadable face, the flashlight in a crewman's hand just clicking off, a white wake starting behind the motors",
            move="slow pull-out, then cut to black", sound="Engines roar away"),
        img("12", "You grab the engine", "Close-up: the empty ignition, the key gone", ["you"],
            "Close-up at night: a white cartoon hand with a bright yellow elastic cuff gripping the tiller of a small outboard motor, the key slot empty, a cut black cord dangling where the key should hang, black water and starlight",
            on="NO KEY", move="fast push-in", sound="Click, click"),
        img("13", "Alone On black water", "Wide: one tiny yellow speck alone on the black sea", ["you"],
            "A wide high view of a vast black ocean at night under a sky full of stars: one tiny open dive boat drifting alone with a single small figure in it, a speck of bright yellow, no wake, no lights anywhere on the horizon",
            on="AGAIN", move="very slow push-in", sound="Silence, then waves"),
        img("14", "You drift for hours", "YOU hugging his knees in the boat, jacket zipped, stars", ["you"],
            f"Night at sea inside a small drifting dive boat: {YZ}, sitting in the bottom of the boat hugging his knees and staring up at a sky full of stars, exhausted and cold, a coil of rope and a scuba tank beside him",
            on="HOURS LATER", move="slow tilt up to the stars"),
        img("15", "At dawn a fishing boat", "Dawn: the fishing boat arrives, a rope flying", ["you", "fishing-boat"],
            f"Dawn at sea, pink and gold light on calm water: {FB} pulling up beside a small drifting dive boat, a coiled rope flying through the air from its deck, and in the dive boat a small figure in a bright yellow windbreaker waving both arms",
            on="DAWN", move="slow push-in", sound="Boat horn, gulls"),
        img("16", "Hands pull you up", "YOU on the fishing deck with a towel and water, relieved", ["you", "fishing-boat"],
            f"Dawn on the deck of a sport-fishing boat: {Y}, a gray towel around his shoulders, sitting on a white cooler and drinking from a plastic water bottle with his eyes closed in relief, golden morning light, fishing rods and outriggers behind him",
            move="slow push-in", sound="Warm swell in the music"),
        img("17", "Then you see his wrist", "Close-up: a steel dive watch on the wrist holding out water", ["table9"],
            "Close-up at dawn: a white cartoon hand holding out a second plastic water bottle, a chunky steel dive watch on the wrist, the short sleeve of a gray polo shirt, golden light glinting off the watch face",
            move="hold, then snap zoom on the watch", sound="Music cuts, sub drop"),
        img("18", "The man from table nine", "Reveal: the man from table nine smiling down at YOU", ["you", "table9", "fishing-boat"],
            f"Dawn on the deck of {FB}: {D} standing over {Y}, who sits frozen on a white cooler with a gray towel around his shoulders and wide white shocked eyes with tiny pupils, the bald man smiling politely down at him, golden light behind",
            on="THE MAN FROM TABLE NINE", move="slow push-in", sound="Stinger"),
        reuse("19", "Morning Where's your brother", "The man from table nine, pushed in on his face", "this part's `18.png`, pushed in on his polite smile",
              on="\"WHERE'S YOUR BROTHER?\"", move="slow push-in on his face"),
        vote("20", "Do you tell him", "TELL", "LIE",
             f"Dawn on the deck of {FB}: {Y}, a gray towel around his shoulders, talking fast with both hands open and an honest, desperate face, while {D} sits across from him on a cooler, listening with his hands folded",
             f"Dawn on the deck of {FB}: {Y}, a gray towel around his shoulders, looking away with a forced shrug and a tight, lying smile, while {D} watches him closely with flat, patient eyes",
             ["you", "table9", "fishing-boat"], "PART 2 TOMORROW · THE MAJORITY DECIDES"),
    ],
    caption="""Season 3 · Part 1/5 · A boat with no lights. And your engine is off. 🌊

The interactive survival story continues, and you decide every part.

Comment TELL or LIE. The majority writes Part 2.

#MidnightParts #TheShipKeptGoing #season3 #survivalstory #mysterystory""",
    pinned="TELL or LIE? And who do you think was on that boat? 👀",
    gate=["Hook ≤ 12 words, with a concrete detail plus a threat (midnight, no lights, coming at you)",
          "Hook is said and shown in the first frame",
          "A stranger understands it within 15s (cruise ship, brother, $2M gone, engine off)",
          "Previous cliffhanger (S2's boat) paid off from the first line; who's aboard by 0:30",
          "New information every ≤ 8s, a turn every ≤ 15s",
          "False relief (dawn, rescue, water) comes before the final turn",
          "Ends worse: rescued by the man who pushed you off the ship",
          "Loop ledger: half-closes L1 · opens L4",
          "Cliffhanger type differs from S2's finale (sting there, reveal here)"],
))

# ------------------------------------------------------------------ PART 2
PARTS.append(dict(
    n=2, title="Rule Four", cliff="impossible fact, then a decision vote",
    loops="opens L2 (is Marcus dead?) and L3 (who has the money?) · moves L4",
    pays="Part 1's \"Where's your brother?\", at ~0:05",
    branch="**Written for TELL winning.** LIE lines are below.",
    first_text="PART 2 · \"HE PUSHED YOU. NOW HE SAVED YOU.\"",
    first_vis="The man from table nine hauling YOU out of the sea by the jacket",
    look="hard Caribbean morning on the fishing boat; a dim cabin with one porthole; the found jacket in turquoise water. HUD DAYS LEFT appears at \"It's Thursday\": 3.",
    vo="""[low, tense, steady] The man who pushed you off a ship just pulled you out.

[firm] Most of you said tell him.

[quick, tense] So you do. Kerr's phone. The money, gone. The boat with no lights. Two men who knew your brother's name.

[knowing] Lie voters, he'd have known. He watched you for three weeks.

[calm, flat, the man] "Nobody took your brother," he says. "Not my people."

[cold, measured] He sits down across from you. Gray polo. Steel watch. Polite, like always.

[calm, dry, the man] "My name is Doyle. You can stop calling me table nine."

[slow, heavy] Doyle has a problem. He was sent to collect two million dollars. He failed. Twice.

[quiet, flat, Doyle] "They gave me until Sunday. The money, or the man who lost it."

[tense, realizing] It's Thursday. And you're the man who lost it.

[dry, almost relieved] Which means, until Sunday, he needs you alive.

[quick, factual] Here's what you need to know. A crypto wallet is public. Anyone can watch the money move. Nobody can see who moved it.

[slow, cold] Doyle turns his phone around. The money moved again. At 4:02 a.m. Hours after your brother was taken.

[calm, Doyle] "Rule four," he says. "The dead don't spend money."

[quiet, uneasy] Someone has it. And they're spending it.

[sharp, a jolt] Then the radio crackles. A search, off Isla Mujeres.

[slow, dread] For an American. Marcus. Presumed drowned.

[quick, tense] Divers found something in the water. The radio reads the description.

[very slow, quiet] A yellow windbreaker. High collar. Size large.

[barely a whisper] You look down. You're wearing it.

[direct, tense] Tell the police he's alive, or stay quiet and hunt him with Doyle?

[lighter, direct] Comment POLICE or QUIET. The majority writes Part 3.""",
    alt=("If LIE wins", """Replace "Most of you said tell him." through "…He watched you for three weeks." with:
```
[firm] Most of you said lie.

[flat, lying] "He drowned," you say. "They took him, and he went over."

[calm, dry, the man] "You're a bad liar. Same as him."

[knowing] Tell voters, he already knew more than you.
```
Image swaps: 03 becomes 20B from Part 1 (you lying) or a reuse of this part's 05.""", "LIE"),
    shots=[
        img("01", "The man who pushed you", "The man from table nine hauling YOU out of the sea", ["you-wet", "table9", "fishing-boat"],
            f"Dawn at sea, close on the side of {FB}: {D}, leaning over the rail and hauling {YW} up out of the water by the collar of his jacket with one strong hand, water pouring off him, pink and gold morning light",
            on="PART 2 · HE PUSHED YOU. NOW HE SAVED YOU.", move="slow push-in", sound="Splash, drone"),
        card("02", "Most of you said", "cream", ["Label: PART 1 · YOU VOTED", "Big: **TELL** WINS", "Small: The majority decided."], "Vote card: TELL WINS"),
        img("03", "So you do", "YOU talking fast in the cabin, Doyle listening", ["you", "table9", "fishing-boat"],
            f"Inside the small dim cabin of a sport-fishing boat, one porthole of morning light: {Y}, a gray towel around his shoulders, talking fast with both hands moving, while across a narrow table {D} listens without moving, hands folded",
            move="slow push-in"),
        reuse("04", "Lie voters", "The steel watch in Kerr's back seat", "Season 2 Part 4's `19.png` (the man from table nine in Kerr's back seat, checking his watch)", move="slow push-in", sound="Tick"),
        img("05", "Nobody took your brother", "Close-up: Doyle, calm, shaking his head", ["table9"],
            f"Close-up in a dim boat cabin: {D}, slowly shaking his head with a calm, certain face, a thin stripe of morning light across his eyes from a porthole",
            on="\"NOT MY PEOPLE.\"", move="slow push-in"),
        img("06", "He sits down across", "Doyle sitting across the narrow cabin table, hands folded", ["table9", "you"],
            f"Inside the small dim cabin of a sport-fishing boat, seen over the shoulder of {YC}: {D} sitting across a narrow table with his hands folded on it, the steel dive watch catching the light, polite and patient",
            on="DOYLE", move="slow push-in, chip on \"My name is Doyle\""),
        card("07", "Doyle has a problem", "cream", ["Label: DOYLE'S JOB", "Big: **$2,000,000**", "Small: Failed twice."], "Cream card: $2,000,000 · failed twice"),
        img("08", "They gave me until Sunday", "Doyle looking at his phone, grim", ["table9"],
            f"Inside a dim boat cabin: {D} looking down at a phone in his hand, the blank screen lighting his face cold blue, his jaw tight, the first crack in his calm",
            on="\"THE MONEY, OR THE MAN WHO LOST IT.\"", move="slow push-in"),
        img("09", "It's Thursday", "Close-up: YOU realizing he's the man who lost it", ["you"],
            f"Close-up in a dim boat cabin: {YC}, a gray towel on his shoulders, eyes wide as the realization hits, mouth slightly open, a stripe of porthole light across his face",
            on="HUD · DAYS LEFT 3 · THURSDAY", move="snap zoom", sound="Sub drop"),
        reuse("10", "Which means until Sunday", "Doyle across the table, held", "this part's `06.png`, wider", move="slow pull-out"),
        card("11", "Here's what you need to know", "cream", ["Label: A CRYPTO WALLET", "Big: **PUBLIC**", "Small: Anyone can watch the money move. Nobody can see who moved it."], "Cream card: a crypto wallet is public"),
        img("12", "Doyle turns his phone", "Doyle holding his phone out across the table", ["table9"],
            f"Inside a dim boat cabin: {D} holding a phone out across a narrow table toward the viewer, the phone screen glowing blank and bright, his face calm behind it",
            on="MOVED · 4:02 AM", move="push-in to the screen", sound="Glitch beep"),
        card("13", "Rule four", "dark", ["Label: RULE 4", "Line: The dead don't spend money."], "Dark card: RULE 4"),
        reuse("14", "Someone has it", "The glowing phone, pushed in", "this part's `12.png`, pushed in on the screen"),
        img("15", "Then the radio crackles", "The marine radio crackling, both men turning", ["you", "table9"],
            f"Inside a dim boat cabin: an old marine VHF radio mounted on the wall, its little red light on, and in the foreground {Y} and {D} both turning sharply toward it",
            move="whip to the radio", sound="Radio static, voice"),
        img("16", "For an American", "A navy boat and divers off the island", [],
            "Morning off a small tropical island with turquoise water: a gray navy patrol boat and two divers in black wetsuits in the water beside it, one diver lifting something bright yellow up out of the sea, palm trees on the shore",
            on="PRESUMED DROWNED", move="slow push-in", sound="Radio voice, waves"),
        img("17", "A yellow windbreaker", "Close-up: the yellow jacket floating, collar up", [],
            f"Close-up of turquoise sea water: {JK}, floating spread out just under the surface with its high collar up, sunlight rippling over it",
            move="very slow push-in", sound="Silence"),
        img("18", "You look down", "YOU looking down at the jacket he's wearing", ["you"],
            f"Inside a dim boat cabin: {Y}, standing and looking down at his own chest, both white cartoon hands holding the edges of the open yellow windbreaker, eyes wide white circles with tiny pupils",
            on="YOU'RE WEARING IT.", move="slow push-in", sound="Stinger"),
        vote("19", "Tell the police", "POLICE", "QUIET",
             f"Daytime in a small, shabby island police station: {Y} leaning over a wooden counter, talking urgently to a tired stick-figure police officer in a light-blue uniform shirt and cap, a ceiling fan above",
             f"Daytime on the deck of {FB} heading toward a tropical island: {Y} zipping his windbreaker up to the chin with a grim face, while {D} steers at the wheel behind him",
             ["you", "table9", "fishing-boat"], "PART 3 TOMORROW · THE MAJORITY DECIDES"),
    ],
    caption="""Season 3 · Part 2/5 · The man who pushed you off the ship just pulled you out of the sea. 🛟

An interactive survival story where you choose what happens next.

Comment POLICE or QUIET. The majority writes Part 3.

#MidnightParts #TheShipKeptGoing #season3 #survivalstory #mysterystory""",
    pinned="POLICE or QUIET? Rule four: the dead don't spend money. 👀",
    gate=["Hook ≤ 12 words-ish, concrete and a contradiction (the man who pushed you saved you)",
          "Previous cliffhanger paid off in the first 5s (he's on the boat; you answer him)",
          "Vote result, a line for the losing side, and the choice shapes the opening",
          "Stranger test: the ship, the killer, the brother and the money are all in the first 15s",
          "A small reveal at ~30% (\"Nobody took your brother. Not my people.\")",
          "False relief (until Sunday he needs you alive) before the final turn",
          "Ends worse: Marcus is officially dead, in the jacket you're wearing",
          "Cliffhanger type differs from Part 1's (impossible fact vs reveal)",
          "Loop ledger: opens L2 and L3 · moves L4"],
))

# ------------------------------------------------------------------ PART 3
PARTS.append(dict(
    n=3, title="Against the Current", cliff="arrival, after a photo reveal, then a decision vote",
    loops="half-closes L2 (he's alive) · moves L3 (he wrote the words) · opens L5 (Kerr's part)",
    pays="Part 2's \"You're wearing it\", at ~0:15",
    branch="**Written for QUIET winning.** POLICE lines are below.",
    first_text="PART 3 · \"HE DROWNED IN YOUR JACKET\"",
    first_vis="The second yellow jacket laid out on Lucía's pier, YOU's flip-flops at the edge of the frame",
    look="hard turquoise morning on Lucía's pier and dive shop; the photo from Puerto Morelos in flat bright daylight; dust in the sun when the car pulls up. HUD DAYS LEFT 2 (Friday).",
    vo="""[low, tense] Your brother "drowned." His jacket washed up. And you're wearing his jacket.

[firm] Most of you said stay quiet.

[knowing] Police voters, the officer already had a report. Signed by Agent Kerr. Case closed.

[quick] Doyle takes the boat to Isla Mujeres. To Lucía's pier. That's where it washed up.

[urgent, Lucía] Lucía runs the dive shop there. "They found it under my dock," she says. "At six this morning."

[slow, uneasy] It's laid out on the boards. Bright yellow. Your size. A high collar. And not a single cut in it.

[cold, realizing] Not yours. His.

[relieved, quiet] For one second, it's the best news you've had all week. If it's his, maybe he's alive.

[quick, Lucía] "He bought two," Lucía says. "Same size. A month before your cruise. He showed me the receipt."

[quick, factual] Here's what you don't know. The current here runs north. Fast. Anything lost out there ends up miles north.

[slow, cold] This jacket came south. Against the current. Nobody lost it. Somebody put it here.

[calm, Doyle] "Rule four," Doyle says quietly.

[slow, realizing] And then it hits you. Marcus wrote the twelve words himself. He never needed you to remember them.

[quiet, hurt] So why make you say them? Out loud. Next to Kerr's phone.

[low, Lucía] "There's something else," Lucía says. She shows you a photo from last month. A marina, in Puerto Morelos.

[very slow] Marcus. Laughing. Next to Agent Kerr.

[urgent, sharp] Then tires on the gravel. A dark gray sedan. Kerr's car.

[direct, tense] Run for the boat, or stay and face her?

[lighter, direct] Comment RUN or STAY. The majority writes Part 4.""",
    alt=("If POLICE wins", """Replace "Most of you said stay quiet." through "…That's where it washed up." with:
```
[firm] Most of you said police.

[quick, tense] At the island station, you tell them he's alive. The officer shows you a report. Signed by Agent Kerr. Case closed.

[knowing] Quiet voters, Doyle was waiting outside the whole time.

[quick] He takes you to Lucía's pier. That's where it washed up.
```
Image swaps: 03 becomes Part 2's `19A.png` (you at the police counter).""", "POLICE"),
    shots=[
        img("01", "Your brother drowned", "The second yellow jacket laid out on the pier boards", ["isla-dock"],
            f"Bright morning on a weathered wooden pier above turquoise water: {JK}, laid out flat on the sun-bleached boards and dripping, a dark wet stain spreading around it, and at the edge of the frame the black flip-flops and thin black stick legs of someone standing over it",
            on="PART 3 · HE DROWNED IN YOUR JACKET", move="slow push-in", sound="Waves, drone"),
        card("02", "Most of you said", "cream", ["Label: PART 2 · YOU VOTED", "Big: **QUIET** WINS", "Small: The majority decided."], "Vote card: QUIET WINS"),
        reuse("03", "Police voters", "Agent Kerr with her badge", "Season 2 Part 4's `16.png` (Agent Kerr with her badge)", on="REPORT SIGNED · AGENT KERR", move="slow push-in, desaturated"),
        img("04", "Doyle takes the boat", "The fishing boat pulling up to Lucía's pier", ["fishing-boat", "isla-dock"],
            f"Bright morning on a tropical island: {FB} pulling up alongside a long weathered wooden pier, a small open-front dive shop with racks of scuba tanks at the shore end, turquoise water, palm trees",
            on="ISLA MUJERES", move="slow push-in"),
        img("05", "Lucía runs the dive shop", "Lucía at the end of the pier, pointing down", ["lucia", "isla-dock"],
            f"Bright morning at the end of a wooden pier: {L}, worried, pointing down at the boards with one hand and looking at the viewer, turquoise water behind her",
            on="LUCÍA · THE DIVE SHOP", move="slow push-in"),
        reuse("06", "It's laid out on the boards", "The jacket, pushed in on the uncut collar", "this part's `01.png`, pushed in on the uncut collar", on="NO CUT", move="push-in on the collar"),
        reuse("07", "Not yours His", "YOU touching his own cut collar", "Season 2 Part 4's `10.png` (you looking down at the cut collar)", move="slow push-in", sound="Low note"),
        img("08", "For one second", "Close-up: YOU, a small hopeful smile", ["you"],
            f"Close-up in bright morning sun on a pier: {YC}, a small, disbelieving, hopeful smile, eyes shining, turquoise water behind him",
            move="slow push-in", sound="Warm swell"),
        img("09", "He bought two", "Lucía holding up two fingers", ["lucia", "dive-shop"],
            f"Bright morning in front of a small open-front dive shop: {L}, holding up two fingers with a knowing, serious face, scuba tanks and wetsuits on racks behind her",
            on="\"HE BOUGHT TWO.\"", move="slow push-in"),
        card("10", "Here's what you don't know", "cream", ["Label: THE CURRENT HERE", "Big: RUNS **NORTH**", "Small: Fast. Anything lost out there ends up miles north."], "Cream card: the current runs north"),
        card("11", "This jacket came south", "cream", ["Label: THIS JACKET", "Big: CAME **SOUTH**", "Small: Against the current."], "Cream card: this jacket came south"),
        reuse("11b", "Nobody lost it", "The jacket on the pier, held", "this part's `01.png`, wide", on="SOMEBODY PUT IT HERE", move="slow pull-out"),
        img("12", "Rule four Doyle says", "Doyle on the pier, arms folded, looking at the jacket", ["table9", "isla-dock"],
            f"Bright morning on a wooden pier: {D}, arms folded, looking down at something on the boards with a calm, satisfied face, the sun glinting on his steel watch, turquoise water behind",
            move="slow push-in", sound="Tick"),
        img("13", "And then it hits you", "Close-up: YOU, the realization", ["you"],
            f"Close-up in bright sun: {YC}, the hope draining from his face, eyes going wide white circles with tiny pupils, mouth slightly open",
            on="HUD · DAYS LEFT 2 · FRIDAY", move="snap zoom", sound="Sub drop"),
        reuse("14", "So why make you say them", "The phone face down on the nightstand", "Season 2 Part 3's `06.png` (Kerr's phone face down on the hotel nightstand)", on="KERR'S PHONE", move="slow push-in, desaturated", sound="Whisper"),
        img("15", "There's something else", "Lucía holding her phone out to YOU", ["lucia", "you", "dive-shop"],
            f"Bright morning in the shade of a dive shop: {L} holding her phone out toward {Y}, the phone screen glowing blank, both of them leaning in, her face serious",
            move="push-in to the phone"),
        img("16", "Marcus Laughing", "The photo: Marcus laughing with Agent Kerr at the marina", ["marcus", "kerr", "marina"],
            f"A bright daytime snapshot at a small fishing-town marina with an old lighthouse leaning to one side behind it: {M}, laughing with his head back, standing next to {K}, who is smiling, both holding coffee cups, boats tied up behind them",
            on="LAST MONTH · PUERTO MORELOS", move="slow push-in, flash", sound="Camera shutter, stinger"),
        img("17", "Then tires on the gravel", "Kerr's sedan pulling up outside the dive shop, dust", ["dive-shop"],
            f"Bright morning on a sandy gravel road beside a small open-front dive shop: {CAR} pulling up fast and stopping, a cloud of pale dust rolling off its tires, sun glare on the windshield",
            on="KERR", move="shake", sound="Tires on gravel, engine off"),
        vote("18", "Run for the boat", "RUN", "STAY",
             f"Bright morning on a long wooden pier: {Y} and {D} sprinting toward a sport-fishing boat at the end of the pier, mid-stride, the yellow windbreaker flapping",
             f"Bright morning on a wooden pier: {Y} standing still with his fists clenched, facing a dark gray sedan parked by a dive shop, {L} standing a step behind him",
             ["you", "table9", "lucia", "isla-dock"], "PART 4 TOMORROW · THE MAJORITY DECIDES"),
    ],
    caption="""Season 3 · Part 3/5 · Something washed up under the pier. 🌊

An interactive mystery story where the comments decide.

Comment RUN or STAY. The majority writes Part 4.

#MidnightParts #TheShipKeptGoing #season3 #mysterystory #survivalstory""",
    pinned="RUN or STAY? Rewatch Season 2, Part 4: Marcus's hand went straight to your collar. Why? 👀",
    gate=["Hook ≤ 12 words-ish, with a contradiction (his jacket washed up; you're wearing it)",
          "Previous cliffhanger paid off by ~0:15 (the jacket is his, not yours)",
          "Vote result, a line for the losing side, and the choice shapes the opening",
          "Evidence of the hidden truth (two jackets, the current, he wrote the words) and a returning ally (Lucía)",
          "False relief (\"maybe he's alive\") turned into dread (he planned it)",
          "Ends worse: the FBI agent is his partner, and she's here",
          "Cliffhanger type differs from Part 2's (arrival vs impossible fact)",
          "Loop ledger: half-closes L2 · moves L3 · opens L5"],
))

# ------------------------------------------------------------------ PART 4
PARTS.append(dict(
    n=4, title="Him or Me", cliff="threat, then a decision vote",
    loops="moves L4 (Doyle's offer) and L5 (Kerr's frame) · L2 and L3 ready to close",
    pays="Part 3's arrival (Kerr's car), in the first 8s",
    branch="**Written for STAY winning.** RUN lines are below.",
    first_text="PART 4 · \"THE FBI HELPED HIM DIE\"",
    first_vis="Agent Kerr stepping out of her sedan in the hard sun, sunglasses on",
    look="hard white noon, a stuffy island police office with a ceiling fan, then sunset on the pier and long blue shade where Doyle waits. HUD DAYS LEFT 2 → 1 (Saturday).",
    vo="""[low, tense] Your brother faked his death. The FBI agent who helped him just pulled up.

[firm] Most of you said stay.

[knowing] Run voters, her people were already waiting at the end of the pier.

[calm, official, Kerr] Agent Kerr steps out. Sunglasses. Lanyard. "I'm so sorry for your loss," she says.

[cold, flat] You look around. Doyle's gone. Like he was never there.

[quick, tense] She drives you to the island police office. A file on the table. Your name on the front.

[slow, hurt] Across from you sits the woman from Lucía's photo. The one laughing with your brother.

[cold, measured, Kerr] "Two million dollars left from a phone in your hotel room. At 2:14 a.m."

[slow, dawning] The phone she gave you. The secure one.

[quiet, Kerr] "Your brother drowned. You said the words out loud. Who do you think they'll believe?"

[slow, cold] Then she lets you go. That's the worst part. She wants them to find you.

[quick] Outside, Lucía is waiting. She heard it on the harbor radio. A black boat with no lights, docked at Puerto Morelos.

[urgent, whispering, Lucía] "It leaves Sunday," she says. "Two fourteen in the morning."

[quick, Lucía] "Go tonight," she says. "Before she finds out I told you."

[relieved, almost hopeful] You know where he is. You know when. For the first time, you're ahead of them.

[cold] Then Doyle steps out of the shade. He heard every word.

[calm, flat, Doyle] "Saturday," he says. "One day left. My people want the man in the yellow jacket."

[slow, menacing, Doyle] "Take me to your brother. Or I take you."

[direct, tense] Your brother, or you?

[lighter, direct] Comment HIM or ME. The majority writes the finale.""",
    alt=("If RUN wins", """Replace "Most of you said stay." and "Run voters, her people were already waiting at the end of the pier." with:
```
[firm] Most of you said run.

[fast, tense] You make it halfway down the pier. Two of her people are waiting at the end.

[knowing] Stay voters, at least you'd have kept your dignity.
```
Image swaps: 03 stays (her two agents at the end of the pier).""", "RUN"),
    shots=[
        img("01", "Your brother faked his death", "Agent Kerr stepping out of her sedan in the sun", ["kerr", "dive-shop"],
            f"Bright noon on a sandy road outside a small open-front dive shop: {K}, now wearing dark sunglasses, stepping out of {CAR} and closing the door, calm and official, hard white sunlight and short black shadows",
            on="PART 4 · THE FBI HELPED HIM DIE", move="slow push-in", sound="Car door, drone"),
        card("02", "Most of you said", "cream", ["Label: PART 3 · YOU VOTED", "Big: **STAY** WINS", "Small: The majority decided."], "Vote card: STAY WINS"),
        img("03", "Run voters", "Two agents waiting at the end of the pier", ["isla-dock"],
            "Bright noon at the far end of a long wooden pier above turquoise water: two stick-figure men with white egg-shaped heads in dark suits and dark sunglasses, standing still side by side with their hands clasped, waiting",
            move="slow push-in"),
        img("04", "Agent Kerr steps out", "Close-up: Kerr, fake sympathy", ["kerr"],
            f"Close-up in hard noon sun: {K}, pushing her dark sunglasses up onto her head, her face arranged into soft, practiced sympathy, her eyes cold",
            on="\"I'M SO SORRY FOR YOUR LOSS.\"", move="slow push-in"),
        img("05", "You look around", "The empty pier where Doyle stood, the fishing boat gone", ["isla-dock"],
            "Bright noon on a long wooden pier: an empty patch of sun-bleached boards where someone stood a moment ago, a coil of rope, and far out on the turquoise water a white sport-fishing boat with tall outriggers motoring away",
            on="DOYLE'S GONE", move="slow pan"),
        img("06", "She drives you", "The island police office: YOU and Kerr, a file between them", ["you", "kerr"],
            f"Inside a small, stuffy island police office at noon, a slow ceiling fan and slatted blinds: {Y} sitting at a scratched wooden table with a thin closed file on it, and across from him {K}, her hand resting flat on the file",
            move="slow push-in", sound="Ceiling fan"),
        card("07", "Two million dollars left", "dark", ["Label: KERR'S REPORT", "Line: $2M moved from a phone in your hotel room.", "Small: 2:14 AM"], "Dark card: Kerr's report"),
        reuse("08", "The phone she gave you", "The phone face down on the nightstand", "Season 2 Part 3's `06.png` (the phone on the nightstand)", on="THE SECURE ONE", move="slow push-in, desaturated", sound="Sub drop"),
        img("09", "Your brother drowned", "Kerr leaning in close, quiet", ["kerr"],
            f"Close-up in a dim police office: {K} leaning in across a table toward the viewer, speaking quietly, a stripe of light from the blinds across her round glasses, a thin cold smile",
            on="\"WHO DO YOU THINK THEY'LL BELIEVE?\"", move="slow push-in"),
        img("10", "Then she lets you go", "YOU walking out of the police office into the sun, alone", ["you"],
            f"Bright afternoon outside a small whitewashed island police office: {Y}, walking out of the doorway into the hard sunlight alone, looking back over his shoulder, a long black shadow ahead of him",
            move="slow pull-out"),
        img("11", "Outside Lucía is waiting", "Lucía with a handheld marine radio", ["lucia"],
            f"Late afternoon in the shade of a palm tree beside a dusty island street: {L}, holding a handheld marine radio up near her ear, waving the viewer over urgently with her other hand",
            on="LUCÍA", move="slow push-in", sound="Radio static"),
        card("12", "It leaves Sunday", "dark", ["Label: THE BOAT WITH NO LIGHTS", "Line: SUNDAY · 2:14 AM", "Small: Puerto Morelos"], "Dark card: Sunday 2:14 AM, Puerto Morelos"),
        img("13", "You know where he is", "YOU at sunset on the pier, a determined half-smile", ["you", "isla-dock"],
            f"Sunset at the end of a wooden pier: {Y}, standing with his fists loose at his sides and a small, determined half-smile, looking out across orange water at the far, low line of the mainland coast",
            on="HUD · DAYS LEFT 2", move="slow push-in", sound="Warm swell"),
        img("14", "Then Doyle steps out", "Doyle stepping out of deep blue shade", ["table9", "dive-shop"],
            f"Sunset beside a small dive shop: {D} stepping calmly out of deep blue shadow between racks of scuba tanks into the orange light, his steel watch glinting",
            move="hold, then push-in", sound="Music cuts"),
        reuse("15", "Saturday he says", "Doyle in the light, pushed in", "this part's `14.png`, pushed in on his face", on="HUD · DAYS LEFT 1 · SATURDAY", move="push-in"),
        img("16", "Take me to your brother", "Close-up: Doyle, flat and menacing", ["table9"],
            f"Close-up at dusk: {D} staring straight at the viewer with flat, calm, unblinking eyes, his face half in orange light and half in blue shadow",
            on="\"OR I TAKE YOU.\"", move="very slow push-in", sound="Low hit"),
        vote("17", "Your brother or you", "HIM", "ME",
             f"Night in a car: {Y} in the passenger seat pointing ahead through the windshield at a dark coastal road, and {D} driving, both faces lit by the dashboard",
             f"Night on a dark dock: {Y} sitting alone on the edge with his jacket zipped up and his head down, and the tall silhouette of a broad-shouldered bald man walking toward him from the far end",
             ["you", "table9"], "THE FINALE TOMORROW · THE MAJORITY DECIDES"),
    ],
    caption="""Season 3 · Part 4/5 · The FBI says you did it. 🚔

An interactive survival story where you choose what happens next.

Comment HIM or ME. The majority writes the finale.

#MidnightParts #TheShipKeptGoing #season3 #survivalstory #mysterystory""",
    pinned="HIM or ME? There's no right answer this time. 👀",
    gate=["Hook ≤ 12 words-ish, concrete (faked death, the FBI agent, her car)",
          "Previous cliffhanger paid off in the first 8s (she steps out of the car)",
          "Vote result, a line for the losing side, and the choice shapes the opening",
          "The trusted person is the threat (Kerr's report frames you)",
          "False relief (you know where and when) before the final turn",
          "Ends worse: the man who pushed you off the ship makes you choose",
          "Cliffhanger type differs from Part 3's (threat vs arrival)",
          "Loop ledger: moves L4 and L5"],
))

# ------------------------------------------------------------------ PART 5
PARTS.append(dict(
    n=5, title="Man Overboard", cliff="final sting and callback",
    loops="closes L1–L5 · leaves L6 (who sent the photo) as the Season 4 door",
    pays="Part 4's HIM/ME vote (0:00–0:12)",
    branch="**Written for HIM winning.** ME lines are below.",
    first_text="FINALE · \"YOU BROUGHT A KILLER TO YOUR BROTHER\"",
    first_vis="YOU and Doyle walking down the marina dock at night toward the black boat, the leaning lighthouse behind",
    look="a fishing-town marina at 2 a.m.: sodium-orange dock lamps, black water, the old lighthouse leaning against the stars. Then home: blue-black, one streetlight, phone glow. HUD DAYS LEFT 0.",
    vo="""[low, tense, deliberate] Sunday. 2:14 a.m. You just brought a killer to your brother.

[firm, heavy] Most of you said him.

[knowing, quiet] Me voters, it wouldn't have mattered. Doyle was coming either way.

[tense, quiet] The marina at Puerto Morelos. An old lighthouse, leaning. And at the end of the dock, a black boat with no lights.

[cold, slow] Marcus is on deck. Dry. Alive. Not even surprised.

[quiet, dry, Doyle] "Rule four," Doyle says.

[hurt, steady] "You wrote the words," you say. "You never needed me to remember them."

[calm, almost proud, Marcus] "I moved it myself. At 2:14. While you slept."

[hurt, low] "Then why make me say them?"

[soft, Marcus] "So everyone would blame the phone. And you."

[cold, quick] The cabin door opens. Agent Kerr. A laptop under her arm. The money.

[calm, cold, Kerr] She points at you. "There's your man, Doyle. Yellow jacket. It's all in my report."

[very quiet] Doyle looks at you. At Marcus. At the laptop.

[quick, factual] Here's what you don't know. When nobody finds a body, a missing man can stay missing for years. No name. No bank. No way home.

[slow, cold, Doyle] Doyle takes the laptop. Then Kerr's arm. "The money," he says. "And the one who took it."

[very slow, Doyle] He looks at Marcus. "You drowned on Wednesday. Stay drowned."

[quiet, final] Your brother is alive. And he can never come home.

[slow, heavy] Three weeks ago, a ship left you behind. Tonight, you leave him.

[cold narrator, slow] Back home. 2:14 a.m. A photo from a number you don't know. Your front door. From across the street.

[whispered, final] "Whatever happens, I love you, okay?"

[lighter, inviting, a hint of a grin] Comment SEASON 4 if you want to know who sent it.""",
    alt=("If ME wins", """Replace "Most of you said him." and "Me voters, it wouldn't have mattered. Doyle was coming either way." with:
```
[firm, heavy] Most of you said me.

[quiet, steady] You refuse. Doyle shrugs. "Then you're the man in the yellow jacket." He drives you to the marina himself.

[knowing, quiet] Him voters, you'd have ended up here anyway.
```
Image swaps: 01 and 03 stay; the vote card says ME.""", "ME"),
    shots=[
        img("01", "Sunday 2:14 a.m.", "YOU and Doyle walking down the marina dock toward the black boat", ["you", "table9", "marina", "dark-boat"],
            f"Night at a small fishing-town marina, seen from behind: {Y} and {D} walking side by side down a long concrete dock lit by sodium-orange lamps toward {DB} moored at the very end, an old lighthouse leaning to one side against the stars behind it",
            on="FINALE · YOU BROUGHT A KILLER TO YOUR BROTHER", move="slow push-in", sound="Drone, footsteps"),
        card("02", "Most of you said", "cream", ["Label: PART 4 · YOU VOTED", "Big: **HIM** WINS", "Small: The majority decided."], "Vote card: HIM WINS"),
        reuse("03", "Me voters", "Doyle, flat and calm", "Part 4's `16.png` (Doyle close-up)", move="slow push-in"),
        reuse("04", "The marina at Puerto Morelos", "The marina and the leaning lighthouse", "this part's `01.png`, panned up to the leaning lighthouse",
              on="PUERTO MORELOS · 2:14 AM · HUD DAYS LEFT 0", move="tilt up"),
        img("05", "Marcus is on deck", "Marcus on the black boat's deck, dry, calm", ["marcus", "dark-boat", "marina"],
            f"Night at a marina under one sodium-orange dock lamp: {M} standing on the deck of {DB} with his hands in his pockets, dry and calm, looking at the viewer with no surprise at all",
            move="slow push-in", sound="Water lapping"),
        img("06", "Rule four Doyle says", "Close-up: Doyle, a very small satisfied smile", ["table9"],
            f"Close-up at night under an orange dock lamp: {D} with a very small, satisfied smile, his steel watch raised slightly as he checks the time",
            on="RULE 4", move="slow push-in", sound="Tick"),
        img("07", "You wrote the words", "Close-up: YOU, hurt and steady", ["you"],
            f"Close-up at night under an orange dock lamp: {YC}, jaw set, eyes wet but steady, looking straight ahead at someone",
            move="slow push-in"),
        img("08", "I moved it myself", "Close-up: Marcus, calm, almost proud", ["marcus"],
            f"Close-up at night under an orange dock lamp: {M}, a calm, almost proud half-smile, eyebrows slightly raised, the black boat's rail behind him",
            on="2:14 AM", move="slow push-in"),
        reuse("09", "Then why make me say them", "YOU, pushed in", "this part's `07.png`, pushed in", move="push-in"),
        reuse("10", "So everyone would blame", "Marcus, pushed in", "this part's `08.png`, pushed in",
              on="\"SO EVERYONE WOULD BLAME THE PHONE. AND YOU.\"", move="push-in", sound="Stinger"),
        img("11", "The cabin door opens", "Kerr stepping out of the cabin with a laptop", ["kerr", "dark-boat"],
            f"Night on {DB} at a marina: the small cabin door swinging open and {K} stepping out onto the deck with a closed laptop tucked under one arm, her face lit orange by a dock lamp",
            on="AGENT KERR", move="slow push-in", sound="Door creak"),
        img("12", "She points at you", "Kerr pointing at YOU, Doyle watching", ["kerr", "you", "table9", "marina"],
            f"Night on a marina dock, over the shoulder of {K}: she points straight at {Y} standing on the dock, while {D} stands beside him watching her",
            on="\"THERE'S YOUR MAN.\"", move="push-in on YOU"),
        img("13", "Doyle looks at you", "Doyle between the three of them, deciding", ["table9", "you", "marcus", "kerr", "marina"],
            f"Night on a marina dock beside a black boat: {D} standing in the middle under an orange lamp, looking from {YC} on his left to {M} and {K} on the boat on his right, everyone frozen",
            move="slow pan left to right", sound="Silence"),
        card("14", "Here's what you don't know", "cream", ["Label: NO BODY", "Big: MISSING FOR **YEARS**", "Small: No name. No bank. No way home."], "Cream card: missing for years"),
        img("15", "Doyle takes the laptop", "Doyle walking Kerr down the dock, the laptop under his arm", ["table9", "kerr", "marina"],
            f"Night on a long marina dock under orange lamps: {D} walking away from the camera with a laptop under one arm and his other hand firmly gripping the elbow of {K}, who looks back over her shoulder",
            on="\"THE MONEY. AND THE ONE WHO TOOK IT.\"", move="slow pull-out"),
        img("16", "He looks at Marcus", "Doyle looking back at Marcus over his shoulder", ["table9", "marcus", "dark-boat"],
            f"Night at a marina: {D} glancing back over his shoulder toward {M}, who stands small and alone on the deck of a black boat, the bald man's face flat and final",
            on="\"YOU DROWNED ON WEDNESDAY. STAY DROWNED.\"", move="slow push-in"),
        img("17", "Your brother is alive", "Marcus alone on the black boat, sinking", ["marcus", "dark-boat"],
            f"Night at a marina: {M} sitting down slowly on the deck of a black boat with no lights, alone, his head in his hands, the gold watch glinting, one dock lamp above him and black water all around",
            move="very slow pull-out", sound="Waves"),
        img("18", "Three weeks ago a ship", "YOU walking away down the dock, Marcus small behind", ["you", "marcus", "marina"],
            f"Night on a long marina dock, seen from behind: {Y} walking away toward the land under the orange lamps, hands in his pockets, and far behind him at the end of the dock, a tiny figure sitting alone on a black boat",
            move="slow pull-out", sound="Music swells, then drops"),
        reuse("19", "Back home 2:14 a.m.", "Your house at night, from across the street", "the `home.png` reference (your house at night, seen from across the street)",
              on="UNKNOWN NUMBER · 2:14 AM", move="slow push-in, phone-photo frame", sound="Phone buzz"),
        img("20", "Whatever happens", "Close-up: YOU in the dark, lit by the phone", ["you"],
            f"Close-up at night in a dark bedroom: {YC}, lit only by the cold white glow of a phone held close to his face, his eyes wide white circles with tiny pupils",
            on="\"WHATEVER HAPPENS, I LOVE YOU, OKAY?\"", move="very slow push-in", sound="Silence, then a sting"),
        reuse("21", "Comment SEASON 4", "The front door from across the street, pushed in", "the `home.png` reference again, pushed in on the front door",
              on="WHO SENT IT? · COMMENT: SEASON 4", move="slow push-in, cut to black", sound="Low sting"),
    ],
    caption="""Season 3 · Finale · Sunday, 2:14 a.m. ⚓

The end of an interactive survival story where you voted on every part.

Comment SEASON 4 if you want to know who sent it.

#MidnightParts #TheShipKeptGoing #season3 #survivalstory #mysterystory""",
    pinned="Comment SEASON 4. And be honest: did you see it coming? 👀",
    gate=["Hook ≤ 12 words, concrete (Sunday, 2:14 a.m.) with a threat",
          "Previous cliffhanger (HIM/ME) paid off in the first 10s",
          "Answers the series question (Marcus is alive; Marcus moved the money; Kerr helped)",
          "Pays off the biggest plants (he wrote the words, the stopped engine, \"Done.\", two jackets)",
          "Emotional button: irony (he wanted to be dead; now he has to stay dead)",
          "Final sting is a callback (S1's \"Whatever happens, I love you, okay?\")",
          "Loop ledger: closes L1–L5 · leaves only L6 as the Season 4 door"],
))


def ref_line(refs):
    return ", ".join(refs) if refs else "none"


def write_part(p):
    n = p["n"]
    d = SER / f"part-{n:02d}"
    (d / "images").mkdir(parents=True, exist_ok=True)
    (d / "reference-images").mkdir(exist_ok=True)
    vo = p["vo"]
    # ------------------------------------------------ script.md
    rows = []
    for s in p["shots"]:
        t = time_of(vo, s["anchor"])
        line = s["anchor"]
        on = s.get("on", "")
        if s["kind"] == "card":
            on = " · ".join(l.split(": ", 1)[1].replace("**", "") for l in s["lines"])
        rows.append(f"| {s['id']} | {t} | {line}… | {s['vis']} | {on} | {s.get('sound', '')} |")
    alt = ""
    if p["alt"]:
        alt = f"\n## {p['alt'][0]}\n{p['alt'][1]}\n"
    gate = "\n".join(f"- [x] {g}" for g in p["gate"]) + "\n- [x] VO word count in range (`tools/vo_stats.py`)\n- [ ] Read-aloud test: do this when recording the voice"
    script = f"""# The Ship Kept Going, Season 3: Part {n} of 5, "{p['title']}"{' (finale)' if n == 5 else ''}

| | |
|---|---|
| Target length | ~90s (about 250–290 VO words at 170 wpm) |
| VO word count | see `python tools/vo_stats.py series/004-the-ship-kept-going-s3` |
| Cliffhanger type | {p['cliff']} |
| Loops | {p['loops']} |
| Pays off | {p['pays']} |
| Branch | {p['branch']} |

## First frame
- **On-screen text:** {p['first_text']}
- **Visual:** {p['first_vis']}

## Voiceover (paste into TTS)
<!-- VO:START -->
{vo}
<!-- VO:END -->
{alt}
## Shot list
One image per shot, in the 2D look of the reference reels: see [image-prompts.md](image-prompts.md).

| # | Time | VO | Visual | On-screen text | Sound |
|---|---|---|---|---|---|
""" + "\n".join(rows) + f"""

## Caption
```
{p['caption']}
```

## Pinned comment
{p['pinned']}

## Quality gate
{gate}
"""
    (d / "script.md").write_text(script, encoding="utf-8")

    # ------------------------------------------------ image-prompts.md
    n_img = sum(1 for s in p["shots"] if s["kind"] == "img") + sum(2 for s in p["shots"] if s["kind"] == "vote")
    n_card = sum(1 for s in p["shots"] if s["kind"] == "card")
    n_re = sum(1 for s in p["shots"] if s["kind"] == "reuse")
    branch_note = ""
    if p["alt"]:
        branch_note = f" Written for **{p['branch'].split('**')[1].replace('Written for ', '').replace(' winning.', '')} winning**; for {p['alt'][2]}, see the swaps at the bottom."
    out = [f"""# Season 3, Part {n}, "{p['title']}"{' (finale)' if n == 5 else ''}: image prompts

One still image per shot, in the 2D look of the reference reels (playbook §11.1). Shot numbers and times follow [script.md](script.md).{branch_note}

**How to use**
1. The reference images are in this part's [reference-images/](reference-images/) folder. Attach the ones listed under **Refs** to each prompt. **Always attach `you.png` whenever YOU is in the shot**, so he stays on-model.
2. Paste each prompt exactly as written. Every prompt is complete, with the style included.
3. Save each image in `part-{n:02d}/images/` under the name shown in **Save as**. Type just the name, without `.png`.
4. **Text cards** need no image. I build them in the edit, as are all on-screen text, phone screens and the HUD.
5. Movement is added in the edit.

**This part's look:** {p['look']}

**To make:** {n_img} images, {n_card} text card{'s' if n_card != 1 else ''} and {n_re} reused image{'s' if n_re != 1 else ''} (I copy the reused ones in).

---
"""]
    for s in p["shots"]:
        t = time_of(vo, s["anchor"])
        if s["kind"] == "card":
            kind = "vote result, cream" if s["lines"][0].startswith("Label: PART") else s["style"]
            out.append(f"### {s['id']} · {t} · TEXT CARD ({kind}) · \"{s['anchor']}…\"\n" + "\n".join(f"- {l}" for l in s["lines"]) + "\n")
        elif s["kind"] == "reuse":
            on = f" · **On screen:** {s['on']}" if s["on"] else ""
            out.append(f"### {s['id']} · {t} · \"{s['anchor']}…\"\n**REUSE** {s['src']}.{on} · **Move:** {s['move']}\n")
        elif s["kind"] == "img":
            on = f" · **On screen:** {s['on']}" if s["on"] else ""
            out.append(f"""### {s['id']} · {t} · "{s['anchor']}…"
**Refs:** {ref_line(s['refs'])}{on} · **Move:** {s['move']}

**Save as:** `{s['id']}.png`

**Prompt -**
```text
{s['prompt']}. {TAIL.format(fmt=s['fmt'])}
```
""")
        else:
            out.append(f"""### {s['id']} · {t} · "{s['anchor']}…" (two images, stacked top and bottom)
**Refs:** {ref_line(s['refs'])} · **On screen:** vote buttons **{s['a']}** (white) / **{s['b']}** (yellow) · {s['nxt']}

**Save as:** `{s['id']}A.png`

**Prompt -**
```text
{s['pa']}. {TAIL.format(fmt='square 1:1')}
```

**Save as:** `{s['id']}B.png`

**Prompt -**
```text
{s['pb']}. {TAIL.format(fmt='square 1:1')}
```
""")
    if p["alt"]:
        swap = p["alt"][1].split("Image swaps:")[-1].strip() if "Image swaps:" in p["alt"][1] else "none"
        out.append(f"---\n\n## If {p['alt'][2]} wins\n- {swap}\n")
    (d / "image-prompts.md").write_text("\n".join(out), encoding="utf-8")
    return n_img, n_card, n_re


for p in PARTS:
    print(p["n"], write_part(p))
