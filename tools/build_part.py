"""Build a finished 9:16 reel for one part from its stills, voiceover and edit.json.

Usage: python tools/build_part.py series/001-some-series/part-01 [--preview 0,12.5,31] [--no-video]
Reads <part>/edit.json, <part>/images/, <part>/audio/voiceover.mp3 and voiceover.words.json,
and the shared sounds in library/. Writes <part>/part-NN-instagram.mp4, <part>/part-NN-youtube.mp4
and <part>/cover.jpg (the first frame).
--preview renders only those timestamps to <part>/preview/ as PNGs (fast check of the layout).

Times in edit.json ("at", "until", move keys) are anchors:
  "deck five"        start of the first occurrence of that phrase in the voiceover
  "deck five@2"      second occurrence
  "shove+0.2"        an anchor plus or minus seconds
  "#05", "#05+0.3"   start of shot 05;  "end" = end of the reel;  12.5 = absolute seconds
Move keys use a number from 0 to 1 for a fraction of the shot instead.
"""
import argparse
import json
import math
import pathlib
import re
import shutil
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS, SR = 1080, 1920, 30, 48000
FONTS = pathlib.Path("C:/Windows/Fonts")
BLACK, BOLD, SEMI, MONO = "ariblk.ttf", "arialbd.ttf", "segoeuib.ttf", "consolab.ttf"
YELLOW = (255, 199, 44)
CREAM, DARK = (242, 236, 224), (21, 18, 15)

parser = argparse.ArgumentParser()
parser.add_argument("part_dir")
parser.add_argument("--preview", help="comma-separated timestamps to render as PNGs")
parser.add_argument("--no-video", action="store_true", help="only mix the audio")
args = parser.parse_args()
PART = (ROOT / args.part_dir).resolve() if not pathlib.Path(args.part_dir).is_absolute() else pathlib.Path(args.part_dir)
EDIT = json.loads((PART / "edit.json").read_text(encoding="utf-8"))
if "accent" in EDIT:  # a series' own accent color (e.g. horror red) replaces the channel yellow everywhere
    YELLOW = tuple(int(EDIT["accent"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) if isinstance(EDIT["accent"], str) else tuple(EDIT["accent"])


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def rgb(c):
    return tuple(int(c.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) if isinstance(c, str) else tuple(c)


def clean(s):
    return re.sub(r"[^A-Z0-9:']", "", s.upper())


# ---------------------------------------------------------------- timing
WORDS = json.loads((PART / "audio" / "voiceover.words.json").read_text(encoding="utf-8"))
NORM = [re.sub(r"[^a-z0-9']", "", w["word"].lower()) for w in WORDS]
SHOT_START = {}
END = WORDS[-1]["end"] + EDIT.get("tail", 1.0)


def phrase_start(phrase, nth=1):
    p = [re.sub(r"[^a-z0-9']", "", t.lower()) for t in phrase.split()]
    hits = [i for i in range(len(NORM)) if NORM[i:i + len(p)] == p]
    if len(hits) < nth:
        raise SystemExit(f"anchor not found in voiceover: {phrase!r}")
    return WORDS[hits[nth - 1]]["start"]


def at(spec):
    if isinstance(spec, (int, float)):
        return float(spec)
    m = re.fullmatch(r"(.+?)(?:@(\d+))?([+-]\d+(?:\.\d+)?)?", spec.strip())
    base, nth, off = m.group(1).strip(), int(m.group(2) or 1), float(m.group(3) or 0)
    if base == "end":
        t = END
    elif base.startswith("#"):
        t = SHOT_START[base[1:]]
    else:
        t = phrase_start(base, nth)
    return t + off


SHOTS = EDIT["shots"]
for s in SHOTS:
    s["t0"] = at(s["at"])
    SHOT_START[s["id"]] = s["t0"]
for a, b in zip(SHOTS, SHOTS[1:]):
    a["t1"] = b["t0"]
SHOTS[-1]["t1"] = END


def ease(x, kind="inout"):
    x = min(max(x, 0.0), 1.0)
    if kind == "linear":
        return x
    if kind == "out":
        return 1 - (1 - x) ** 3
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- drawing helpers
def rich_lines(text, keys, fnt, max_w):
    """Split text into lines of (word, is_key) that fit max_w."""
    keyset = {clean(k) for k in keys}
    words = text.strip().split(" ")  # split on single spaces so runs of spaces (letter-spaced labels) keep their width
    lines, cur = [], []
    for w in words:
        trial = " ".join(x for x, _ in cur + [(w, 0)])
        if cur and fnt.getlength(trial) > max_w:
            lines.append(cur)
            cur = []
        cur.append((w, clean(w) in keyset or bool(re.search(r"\d", w)) and "#digits" in keys))
    if cur:
        lines.append(cur)
    return lines


def text_block(text, fnt, keys=(), max_w=940, color=(255, 255, 255), key_color=YELLOW, stroke=0,
               stroke_color=(0, 0, 0), spacing=1.12, align="center", highlight=None):
    """Render wrapped text to an RGBA array. highlight=(rgb) paints a marker swipe behind key words."""
    lines = rich_lines(text, keys, fnt, max_w)
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * spacing)
    widths = [fnt.getlength(" ".join(w for w, _ in ln)) for ln in lines]
    pad = stroke + 12
    img = Image.new("RGBA", (int(max(widths)) + 2 * pad, lh * len(lines) + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    space = fnt.getlength(" ")
    for li, ln in enumerate(lines):
        x = pad + ((max(widths) - widths[li]) / 2 if align == "center" else 0)
        y = pad + li * lh
        for w, is_key in ln:
            wl = fnt.getlength(w)
            if is_key and highlight:
                d.rectangle([x - 8, y + asc * 0.30, x + wl + 8, y + asc + desc * 0.4], fill=highlight)
            d.text((x, y), w, font=fnt, fill=(key_color if is_key and not highlight else color),
                   stroke_width=stroke, stroke_fill=stroke_color)
            x += wl + space
    return np.array(img)


def pill(text, keys=(), size=52, bg=(15, 15, 20, 225), fg=(255, 255, 255), padx=34, pady=16, fnt_name=BLACK):
    t = text_block(text, font(fnt_name, size), keys, max_w=2000, color=fg, spacing=1.0)
    th, tw = t.shape[:2]
    img = Image.new("RGBA", (tw + 2 * padx - 24, th + 2 * pady - 24), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=img.height // 2, fill=bg)
    arr = np.array(img)
    blend(arr, t, arr.shape[1] / 2, arr.shape[0] / 2)
    return arr


def blend(dst, src, cx, cy, alpha=1.0, scale=1.0):
    """Alpha-composite RGBA src onto dst (RGB or RGBA array) centred at (cx, cy)."""
    if alpha <= 0:
        return
    if scale != 1.0:
        src = cv2.resize(src, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR)
    h, w = src.shape[:2]
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    sx0, sy0 = max(0, -x0), max(0, -y0)
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(dst.shape[1], x0 + w - sx0), min(dst.shape[0], y0 + h - sy0)
    if x1 <= x0 or y1 <= y0:
        return
    s = src[sy0:sy0 + (y1 - y0), sx0:sx0 + (x1 - x0)].astype(np.float32)
    a = s[..., 3:4] / 255.0 * alpha
    region = dst[y0:y1, x0:x1, :3].astype(np.float32)
    dst[y0:y1, x0:x1, :3] = (s[..., :3] * a + region * (1 - a)).astype(np.uint8)
    if dst.shape[2] == 4:
        da = dst[y0:y1, x0:x1, 3:4].astype(np.float32) / 255.0
        dst[y0:y1, x0:x1, 3:4] = ((a + da * (1 - a)) * 255).astype(np.uint8)


def pop(t, t_in, t_out, enabled=True, dur=0.16):
    """(alpha, scale) for an element that pops in at t_in and cuts at t_out."""
    if t < t_in or t >= t_out:
        return 0.0, 1.0
    if not enabled:
        return 1.0, 1.0
    x = min((t - t_in) / dur, 1.0)
    back = 1 + 2.2 * (x - 1) ** 3 + 1.2 * (x - 1) ** 2
    return min(x * 1.6, 1.0), 0.82 + 0.18 * back


# ---------------------------------------------------------------- overlays
def build_overlay(o):
    kind = o["type"]
    if kind == "chip":
        o["img"] = pill(o["text"], o.get("keys", []), o.get("size", 52))
    elif kind == "big":
        o["img"] = text_block(o["text"], font(BLACK, o.get("size", 118)), o.get("keys", []), max_w=o.get("max_w", 960),
                              stroke=o.get("stroke", 11), spacing=1.0)
    elif kind == "mono":
        o["img"] = text_block(o["text"], font(MONO, o.get("size", 34)), max_w=1000,
                              color=rgb(o.get("color", "#FFFFFF")), stroke=o.get("stroke", 5), spacing=1.0)
    elif kind == "vote_buttons":
        o["a_img"] = pill(o["a"], size=60, bg=(255, 255, 255, 255), fg=(15, 15, 20), padx=70, pady=22)
        o["b_img"] = pill(o["b"], size=60, bg=YELLOW + (255,), fg=(15, 15, 20), padx=70, pady=22)
    return o


def draw_overlay(frame, o, t, shot, M):
    t_in = at(o["at"]) if "at" in o else shot["t0"]
    t_out = at(o["until"]) if "until" in o else shot["t1"]
    if o["type"] == "arc":
        if t < t_in:
            return
        p = ease((t - t_in) / max(at(o["draw_until"]) - t_in, 0.01), "out")
        (x0, y0), (cx, cy), (x1, y1) = o["src"]
        n = 60
        pts = []
        for i in range(int(n * p) + 1):
            u = i / n
            sx = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x1
            sy = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y1
            pts.append(M @ np.array([sx * shot["src_w"], sy * shot["src_h"], 1.0]))
        col = rgb(o.get("color", "#FFC72C"))
        for i in range(0, len(pts) - 1, 2):
            a, b = pts[i], pts[min(i + 1, len(pts) - 1)]
            cv2.line(frame, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), (0, 0, 0), 13, cv2.LINE_AA)
            cv2.line(frame, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), col, 7, cv2.LINE_AA)
        if pts:
            cv2.circle(frame, (int(pts[0][0]), int(pts[0][1])), 12, col, -1, cv2.LINE_AA)
        if p >= 1:
            e = pts[-1]
            cv2.ellipse(frame, (int(e[0]), int(e[1])), (34, 11), 0, 0, 360, col, 5, cv2.LINE_AA)
        return
    if o["type"] == "vote_buttons":
        for key, img, pos in (("a_at", o["a_img"], o["a_pos"]), ("b_at", o["b_img"], o["b_pos"])):
            a, s = pop(t, at(o[key]), t_out)
            blend(frame, img, pos[0] * W, pos[1] * H, a, s)
        return
    a, s = pop(t, t_in, t_out, o.get("pop", True))
    blend(frame, o["img"], o["pos"][0] * W, o["pos"][1] * H, a, s)


# ---------------------------------------------------------------- HUD
HUD = EDIT.get("hud", {"values": []})
HUD_VALUES = sorted(({**v, "t": at(v["at"])} for v in HUD["values"]), key=lambda v: v["t"])
F_HUD_LABEL, F_HUD_VALUE = font(MONO, 26), font(BLACK, 50)


def hud_state(t):
    time_s, strength, prev, t_change = "", 100, 100, -9
    for v in HUD_VALUES:
        if v["t"] > t:
            break
        time_s = v.get("time", time_s)
        if "strength" in v:
            prev, strength, t_change = strength, v["strength"], v["t"]
    k = ease((t - t_change) / 0.6)
    return time_s, prev + (strength - prev) * k


def draw_hud(frame, t, alpha, scale):
    time_s, strength = hud_state(t)
    img = Image.new("RGBA", (660, 150), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for x, label, value in ((0, "TIME", time_s), (342, "STRENGTH", f"{round(strength)}%")):
        d.rounded_rectangle([x, 0, x + 318, 146], radius=24, fill=(14, 16, 22, 215))
        d.text((x + 26, 16), " ".join(label), font=F_HUD_LABEL, fill=(150, 150, 158))
        d.text((x + 24, 44), value, font=F_HUD_VALUE, fill=(255, 255, 255))
    d.rounded_rectangle([342 + 26, 116, 342 + 292, 128], radius=6, fill=(60, 62, 70))
    d.rounded_rectangle([342 + 26, 116, 342 + 26 + int(266 * strength / 100), 128], radius=6, fill=YELLOW)
    blend(frame, np.array(img), W / 2, HUD.get("y", 0.115) * H, alpha, scale)


def draw_days(frame, t, alpha, scale):
    """"mode": "days" HUD: DAYS LEFT with one pip per day; a lost day's pip fades from yellow to gray."""
    days, prev, t_change, total = HUD.get("total", 7), HUD.get("total", 7), -9, HUD.get("total", 7)
    for v in HUD_VALUES:
        if v["t"] > t:
            break
        if "days" in v:
            prev, days, t_change = days, v["days"], v["t"]
    k = ease((t - t_change) / 0.6)
    img = Image.new("RGBA", (440, 150), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, 439, 146], radius=24, fill=(14, 16, 22, 215))
    d.text((26, 16), " ".join("DAYS LEFT"), font=F_HUD_LABEL, fill=(150, 150, 158))
    d.text((24, 44), str(days), font=F_HUD_VALUE, fill=(255, 255, 255))
    gray = np.array((60, 62, 70))
    for i in range(total):
        x = 116 + i * 44
        col = YELLOW if i < days else tuple((gray + (np.array(YELLOW) - gray) * (1 - k)).astype(int)) if i < prev else (60, 62, 70)
        d.rounded_rectangle([x, 62, x + 34, 96], radius=8, fill=col)
    blend(frame, np.array(img), W / 2, HUD.get("y", 0.115) * H, alpha, scale)


# ---------------------------------------------------------------- captions
def caption_groups():
    fixes = EDIT.get("caption_fixes", {})
    toks = [dict(w) for w in WORDS]
    out = []
    i = 0
    while i < len(toks):
        for pattern, repl in fixes.items():
            parts = pattern.split()
            if [t["word"] for t in toks[i:i + len(parts)]] == parts:
                toks[i:i + len(parts)] = [{"word": repl, "start": toks[i]["start"], "end": toks[i + len(parts) - 1]["end"]}]
                break
        out.append(toks[i])
        i += 1
    groups, cur = [], []
    for j, w in enumerate(out):
        cur.append(w)
        nxt = out[j + 1] if j + 1 < len(out) else None
        chars = sum(len(x["word"]) + 1 for x in cur)
        if (nxt is None or len(cur) >= 3 or chars + len(nxt["word"]) > 16 or re.search(r"[.,?!:]$", w["word"])
                or nxt["start"] - w["end"] > 0.35):
            groups.append(cur)
            cur = []
    keys = EDIT.get("caption_keys", []) + ["#digits"]
    fnt = font(BLACK, EDIT.get("caption_size", 84))
    res = []
    for g, nxt in zip(groups, groups[1:] + [None]):
        text = " ".join(x["word"] for x in g).upper().replace("A.M.", "AM")
        t1 = min(nxt[0]["start"], g[-1]["end"] + 0.6) if nxt else g[-1]["end"] + 0.6
        res.append({"t0": g[0]["start"], "t1": t1, "img": text_block(text, fnt, keys, max_w=940, stroke=9, spacing=1.0)})
    return res


# ---------------------------------------------------------------- cards
def draw_card(frame, card, t, shot):
    bg = DARK if card["style"] == "dark" else CREAM
    frame[:] = bg
    ink = (255, 255, 255) if card["style"] == "dark" else (17, 17, 17)
    t_rel = t - shot["t0"]
    y = card.get("y", 0.36) * H
    if "label" not in card.get("_cache", {}):
        c = card["_cache"] = {}
        c["label"] = text_block("   ".join(" ".join(w) for w in card["label"].split()), font(MONO, 40), color=YELLOW if card["style"] == "dark" else (60, 60, 60))
        if card.get("line"):
            c["line"] = text_block(card["line"], font(BLACK, card.get("line_size", 96)), card.get("keys", []), max_w=900,
                                   color=ink, spacing=1.08, highlight=(YELLOW if card["style"] == "cream" else None))
        if card.get("small"):
            c["small"] = text_block(card["small"], font(SEMI, 40), max_w=860, color=(140, 140, 140) if card["style"] == "dark" else (90, 90, 90))
    c = card["_cache"]
    a, s = pop(t_rel, 0, 99)
    blend(frame, c["label"], W / 2, y, a, s)
    t_line = at(card["line_at"]) - shot["t0"] if "line_at" in card else 0.18
    a, s = pop(t_rel, t_line, 99)
    line_h = c["line"].shape[0] if "line" in c else 0
    line_y = y + 60 + line_h / 2
    diagram = card.get("diagram")
    if diagram == "distance":
        draw_distance(frame, t_rel, shot["t1"] - shot["t0"], card, y + 330)
        line_y = y + 640 + line_h / 2
    elif diagram == "speed":
        draw_speed(frame, t, card, y + 90)
        line_y = y + 740 + line_h / 2
    elif diagram == "horizon":
        draw_horizon(frame, t, card, y + 90)
        line_y = y + 700 + line_h / 2
    elif diagram == "drift":
        draw_drift(frame, t, card, y + 70)
        line_y = y + 740 + line_h / 2
    if "line" in c:
        blend(frame, c["line"], W / 2, line_y, a, s)
    if "small" in c:
        t_small = at(card["small_at"]) - shot["t0"] if "small_at" in card else t_line + 0.27
        a, s = pop(t_rel, t_small, 99)
        blend(frame, c["small"], W / 2, line_y + line_h / 2 + 40, a, s)


def draw_speed(frame, t, card, top):
    """Two bars race: the swimmer's short bar against the ship's full one. cues: a, a_fill, b, b_fill (anchors)."""
    cue = {k: at(v) for k, v in card["cues"].items()}
    ink = (17, 17, 17, 255)
    rows = [("FASTEST HUMAN SWIMMER", "5 MPH", 5 / 23, "a", 0.9, False), ("THE SHIP", "23 MPH", 1.0, "b", 0.45, True)]
    for r, (name, value, frac, k, dur, hi) in enumerate(rows):
        a, sc = pop(t, cue[k], 1e9, dur=0.2)
        if a <= 0:
            continue
        p = ease((t - cue[k + "_fill"]) / dur, "out") if t >= cue[k + "_fill"] else 0.0
        layer = Image.new("RGBA", (W, 250), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.rounded_rectangle([90, 132, 990, 222], radius=45, fill=(252, 249, 242, 255), outline=ink, width=7)
        if p > 0:
            x1 = 90 + max(90, 900 * frac * p)
            d.rounded_rectangle([90, 132, x1, 222], radius=45, fill=(YELLOW + (255,)) if hi else ink, outline=ink, width=7)
        arr = np.array(layer)
        name_img = text_block(name, font(MONO, 36), color=(60, 60, 60))
        blend(arr, name_img, 90 + name_img.shape[1] / 2, 52)
        val = text_block(value, font(BLACK, 84), ["23", "MPH"] if hi else [], color=(17, 17, 17), highlight=YELLOW if hi else None)
        blend(arr, val, 990 - val.shape[1] / 2, 62)
        blend(frame, arr, W / 2, top + r * 310 + 125, a, sc)


def draw_horizon(frame, t, card, top):
    """Earth's curve: a head at water level sees a horizon about a mile away, so a ship's tall lights outlast its hull.
    cues: line, mile, ship, gone (anchors)."""
    cue = {k: at(v) for k, v in card["cues"].items()}
    Wd, Hd = W, 500
    R, cx0 = 700.0, 540.0
    cy0 = 150.0 + R
    arc_y = lambda x: cy0 - math.sqrt(R * R - (x - cx0) ** 2)
    xs = np.arange(30, 1051, 4)
    ays = np.array([arc_y(x) for x in xs])
    arr = np.zeros((Hd, Wd, 4), np.uint8)
    # water: fills below the curve and fades out toward the bottom
    cols = np.arange(Wd)
    full_ay = np.interp(cols, xs, ays)
    yy = np.arange(Hd)[:, None]
    alpha = np.clip(1 - (yy - full_ay[None, :]) / 240.0, 0, 1) * (yy >= full_ay[None, :]) * ((cols >= 30) & (cols <= 1050))[None, :]
    arr[..., :3] = (226, 218, 200)
    arr[..., 3] = (alpha * 255).astype(np.uint8)
    pts = np.stack([xs, ays], axis=1).astype(np.int32)
    cv2.polylines(arr, [pts], False, (17, 17, 17, 255), 9, cv2.LINE_AA)
    vx, vh = 330.0, 40.0
    V = np.array([vx, arc_y(vx) - vh])
    Cc = np.array([cx0, cy0])
    th = math.atan2(V[1] - Cc[1], V[0] - Cc[0])
    phi = math.acos(R / np.linalg.norm(V - Cc))
    cands = [Cc + R * np.array([math.cos(th + sg * phi), math.sin(th + sg * phi)]) for sg in (-1, 1)]
    Tp = max(cands, key=lambda q: q[0])
    dirv = (Tp - V) / np.linalg.norm(Tp - V)
    line_y = lambda x: V[1] + (x - V[0]) * dirv[1] / dirv[0]
    if t >= cue["line"]:
        pr = ease((t - cue["line"]) / 0.9, "out")
        x_end = V[0] + (1040 - V[0]) * pr
        xx = V[0]
        while xx < x_end:
            x2 = min(xx + 26, x_end)
            cv2.line(arr, (int(xx), int(line_y(xx))), (int(x2), int(line_y(x2))), (17, 17, 17, 255), 7, cv2.LINE_AA)
            xx += 46
    if t >= cue["ship"]:
        u = min(max((t - cue["ship"]) / max(cue["gone"] - cue["ship"], 0.1), 0.0), 1.0)
        k = 1.2
        sx = 660 + 300 * u
        sy = arc_y(sx)
        shp = np.zeros((Hd, Wd), np.uint8)
        P = lambda dx, dy: (int(sx + dx * k), int(sy + dy * k))
        cv2.fillPoly(shp, [np.array([P(-70, -22), P(76, -22), P(58, 6), P(-58, 6)], np.int32)], 255)
        cv2.rectangle(shp, P(-48, -54), P(40, -22), 255, -1)
        cv2.rectangle(shp, P(-6, -90), P(16, -54), 255, -1)
        below = np.zeros((Hd, Wd), np.uint8)
        cv2.fillPoly(below, [np.array([[0, line_y(0)], [Wd, line_y(Wd)], [Wd, Hd], [0, Hd]], np.int32)], 255)
        shape, below = shp > 0, below > 0
        arr[shape & ~below] = (17, 17, 17, 255)
        arr[shape & below] = (17, 17, 17, 85)
        for dx in range(-40, 38, 16):
            for dy in (-46, -34):
                lx, ly = P(dx, dy)
                if 0 <= ly < Hd and not below[ly, lx]:
                    cv2.rectangle(arr, (lx, ly), (lx + 10, ly + 8), YELLOW + (255,), -1)
        lx, ly = P(5, -84)
        if 0 <= ly < Hd and not below[ly, lx]:
            cv2.circle(arr, (lx, ly), 7, YELLOW + (255,), -1, cv2.LINE_AA)
    cv2.circle(arr, (int(V[0]), int(V[1])), 22, YELLOW + (255,), -1, cv2.LINE_AA)
    cv2.circle(arr, (int(V[0]), int(V[1])), 22, (17, 17, 17, 255), 6, cv2.LINE_AA)
    cv2.line(arr, (int(V[0]), int(V[1]) + 24), (int(V[0]), int(arc_y(vx)) - 4), (17, 17, 17, 255), 6, cv2.LINE_AA)
    blend(arr, text_block("YOU", font(MONO, 40), color=(17, 17, 17)), V[0] + 4, arc_y(vx) + 56)
    if t >= cue["mile"]:
        a, sc = pop(t, cue["mile"], 1e9, dur=0.2)
        lab = text_block("HORIZON: 1 MILE", font(MONO, 44), color=(17, 17, 17))
        mx = (V[0] + Tp[0]) / 2 + 60
        blend(arr, lab, mx, line_y(mx) - 62, a, sc)
    blend(frame, arr, W / 2, top + Hd / 2)


def draw_drift(frame, t, card, top):
    """A flat sea map: an X where you fell, and a dotted yellow arrow to where the current carries you.
    cues: x, arrow, arrow_end (anchors)."""
    cue = {k: at(v) for k, v in card["cues"].items()}
    ink = (17, 17, 17, 255)
    layer = Image.new("RGBA", (W, 640), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([90, 10, 990, 630], radius=36, fill=(214, 224, 230, 255), outline=ink, width=6)
    for wx, wy in ((200, 120), (560, 90), (380, 330), (820, 380), (260, 560), (640, 540)):
        d.arc([wx, wy, wx + 70, wy + 30], 200, 340, fill=(160, 178, 190, 255), width=4)
    d.text((935, 60), "N", font=font(BLACK, 40), fill=ink, anchor="mm")
    d.line([(935, 120), (935, 90)], fill=ink, width=5)
    d.polygon([(925, 98), (945, 98), (935, 82)], fill=ink)
    (x0, y0), (cx, cy), (x1, y1) = (260, 470), (380, 170), (770, 170)
    if t >= cue["arrow"]:
        p = ease((t - cue["arrow"]) / max(cue["arrow_end"] - cue["arrow"], 0.1), "out")
        n = 16
        for i in range(int(n * p) + 1):
            u = i / n
            px = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x1
            py = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y1
            d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=YELLOW + (255,), outline=ink, width=4)
        if p >= 1:
            d.ellipse([x1 - 30, y1 - 30, x1 + 30, y1 + 30], fill=YELLOW + (255,), outline=ink, width=6)
    arr = np.array(layer)
    if t >= cue["x"]:
        cv2.line(arr, (x0 - 34, y0 - 34), (x0 + 34, y0 + 34), ink, 14, cv2.LINE_AA)
        cv2.line(arr, (x0 - 34, y0 + 34), (x0 + 34, y0 - 34), ink, 14, cv2.LINE_AA)
        lab = text_block("WHERE YOU FELL", font(MONO, 40), color=(17, 17, 17))
        blend(arr, lab, x0 + 70 + lab.shape[1] / 2 - 40, y0 + 80)
    if t >= cue["arrow_end"]:
        a, sc = pop(t, cue["arrow_end"], 1e9, dur=0.2)
        lab = text_block("WHERE THE CURRENT TAKES YOU", font(MONO, 40), max_w=470, color=(17, 17, 17))
        blend(arr, lab, 730, 335, a, sc)
    blend(frame, arr, W / 2, top + 320)


def draw_distance(frame, t_rel, dur, card, cy):
    """The ship pulls away from a yellow dot; a dashed line and a mileage counter between them."""
    dot_x = 150
    p = ease(t_rel / dur, "linear")
    ship_x = 330 + 560 * p
    cv2.circle(frame, (dot_x, int(cy)), 22, YELLOW, -1, cv2.LINE_AA)
    cv2.circle(frame, (dot_x, int(cy)), 22, (17, 17, 17), 4, cv2.LINE_AA)
    x = dot_x + 40
    while x < ship_x - 70:
        cv2.line(frame, (int(x), int(cy)), (int(min(x + 22, ship_x - 70)), int(cy)), (17, 17, 17), 6, cv2.LINE_AA)
        x += 40
    hull = np.array([[-70, -10], [80, -10], [60, 30], [-60, 30]]) + [ship_x, cy]
    deck = np.array([[-45, -42], [40, -42], [40, -10], [-45, -10]]) + [ship_x, cy]
    stack = np.array([[-5, -66], [15, -66], [15, -42], [-5, -42]]) + [ship_x, cy]
    for poly in (hull, deck, stack):
        cv2.fillPoly(frame, [poly.astype(np.int32)], (17, 17, 17), cv2.LINE_AA)
    steps = card.get("counter", ["0.3 MI", "0.6 MI", "1.0 MI"])
    label = steps[min(int(p * len(steps)), len(steps) - 1)]
    img = text_block(label, font(MONO, 54), color=(17, 17, 17))
    blend(frame, img, (dot_x + ship_x) / 2, cy - 70)


# ---------------------------------------------------------------- images and camera
def load_shot(s):
    if "image" in s:
        img = cv2.cvtColor(cv2.imread(str(PART / "images" / s["image"]), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        if "phone" in s:
            img = bake_phone(img, s["phone"])
        if "note" in s:
            img = bake_note(img, s["note"])
        s["src"] = img
        s["src_h"], s["src_w"] = img.shape[:2]
    if "vote" in s:
        s["vote_imgs"] = [cv2.cvtColor(cv2.imread(str(PART / "images" / f)), cv2.COLOR_BGR2RGB) for f in s["vote"]["images"]]
        s["vote_top"] = text_block(s["vote"]["top"], font(MONO, 36), color=(255, 255, 255))
    for o in s.get("overlays", []):
        build_overlay(o)


def bake_phone(img, ph):
    """Draw a text-message screen onto a blank phone screen in the source image."""
    sw, sh = ph["size"]
    scr = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(scr)
    d.text((sw / 2, 46), ph["name"], font=font(SEMI, 34), fill=(20, 20, 20), anchor="mm")
    d.text((sw / 2, 84), ph.get("time", ""), font=font(SEMI, 22), fill=(140, 140, 140), anchor="mm")
    d.line([(16, 110), (sw - 16, 110)], fill=(225, 225, 228), width=2)
    out = ph.get("outgoing", False)
    body = text_block(ph["text"], font(SEMI, ph.get("text_size", 30)), max_w=sw - 90,
                      color=(255, 255, 255) if out else (20, 20, 20), align="left", spacing=1.15)
    bh, bw = body.shape[:2]
    bubble = Image.new("RGBA", (bw + 16, bh + 8), (0, 0, 0, 0))
    ImageDraw.Draw(bubble).rounded_rectangle([0, 0, bubble.width - 1, bubble.height - 1], radius=28,
                                             fill=(10, 132, 255, 255) if out else (233, 233, 236, 255))
    b = np.array(bubble)
    blend(b, body, b.shape[1] / 2, b.shape[0] / 2)
    scr_arr = np.array(scr)
    bx = sw - 20 - b.shape[1] / 2 if out else 20 + b.shape[1] / 2
    blend(scr_arr, b, bx, 140 + b.shape[0] / 2)
    if ph.get("status"):
        st = text_block(ph["status"], font(SEMI, 24), color=(140, 140, 140))
        blend(scr_arr, st, sw - 20 - st.shape[1] / 2, 140 + b.shape[0] + 26)
    if "quad" in ph:  # a screen seen in perspective: warp into its corners (top-left, top-right, bottom-right, bottom-left)
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [sw, 0], [sw, sh], [0, sh]]), np.float32(ph["quad"]))
        warped = cv2.warpPerspective(scr_arr, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR)
        out = img.copy()
        blend(out, warped, img.shape[1] / 2, img.shape[0] / 2)
        return out
    rot = Image.fromarray(scr_arr).rotate(ph["angle"], resample=Image.BICUBIC, expand=True)
    out = img.copy()
    blend(out, np.array(rot), ph["center"][0], ph["center"][1])
    return out


def bake_note(img, nt):
    """Handwrite lines onto a blank sheet of paper in the source image, warped into its corner quad
    (top-left, top-right, bottom-right, bottom-left). "circle": line index to ring in yellow."""
    cw, ch = nt.get("canvas", [1100, 850])
    can = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(can)
    f = font(nt.get("font", "Inkfree.ttf"), nt.get("size", 150))
    lh = f.size * nt.get("line_h", 1.15)
    y0 = (ch - lh * len(nt["lines"])) / 2
    x0 = cw * nt.get("left", 0.14)
    for i, line in enumerate(nt["lines"]):
        y = y0 + i * lh
        d.text((x0, y), line, font=f, fill=rgb(nt.get("color", "#1C2340")) + (235,))
        if nt.get("circle") == i:
            w = f.getlength(line)
            d.ellipse([x0 - 45, y - 10, x0 + w + 45, y + lh + 5], outline=YELLOW + (255,), width=16)
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [cw, 0], [cw, ch], [0, ch]]), np.float32(nt["quad"]))
    warped = cv2.warpPerspective(np.array(can), M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR)
    out = img.copy()
    blend(out, warped, img.shape[1] / 2, img.shape[0] / 2)
    return out


def camera(s, t):
    """Affine matrix from source pixels to screen pixels at time t."""
    mv = s.get("move", {})
    keys = mv.get("keys", [[0, 1.08, 0.5, 0.5], [1, 1.18, 0.5, 0.5]])
    dur = s["t1"] - s["t0"]
    kt = [s["t0"] + k[0] * dur if isinstance(k[0], (int, float)) else at(k[0]) for k in keys]
    if t <= kt[0]:
        z, fx, fy = keys[0][1:]
    elif t >= kt[-1]:
        z, fx, fy = keys[-1][1:]
    else:
        i = max(j for j in range(len(kt)) if kt[j] <= t)
        u = ease((t - kt[i]) / max(kt[i + 1] - kt[i], 1e-3), mv.get("ease", "inout"))
        z, fx, fy = (keys[i][n] + (keys[i + 1][n] - keys[i][n]) * u for n in (1, 2, 3))
    sw, sh = s["src_w"], s["src_h"]
    sc = max(W / sw, H / sh) * z
    hw, hh = W / 2 / sc, H / 2 / sc
    cx = min(max(fx * sw, hw), sw - hw)
    cy = min(max(fy * sh, hh), sh - hh)
    dx = dy = 0.0
    for sh_ in mv.get("shake", []):
        t_s = at(sh_["at"]) if isinstance(sh_["at"], str) else s["t0"] + sh_["at"] * dur
        if t_s <= t < t_s + sh_.get("dur", 0.4):
            k = 1 - (t - t_s) / sh_.get("dur", 0.4)
            amp = sh_.get("amp", 22) * k
            dx += amp * math.sin(t * 71.3) * math.cos(t * 23.1)
            dy += amp * math.sin(t * 57.7 + 1.3)
    return np.array([[sc, 0, W / 2 - sc * cx + dx], [0, sc, H / 2 - sc * cy + dy]])


def render_vote(frame, s, t):
    frame[:] = (8, 11, 17)
    v = s["vote"]
    blend(frame, s["vote_top"], W / 2, v.get("top_y", 0.13) * H)
    band_h = v.get("band_h", 590)
    for i, (img, y) in enumerate(zip(s["vote_imgs"], v["band_y"])):
        p = (t - s["t0"]) / (s["t1"] - s["t0"])
        z = 1.0 + 0.06 * p
        ih, iw = img.shape[:2]
        sc = W / iw * z
        crop_h = band_h / sc
        fy = v.get("focus_y", [0.5] * len(v["band_y"]))[i]  # which height of the image sits in the band's middle (0 top, 1 bottom)
        cy = min(max(ih * fy, crop_h / 2), ih - crop_h / 2)
        M = np.array([[sc, 0, W / 2 - sc * iw / 2], [0, sc, band_h / 2 - sc * cy]])
        band = cv2.warpAffine(img, M, (W, band_h), flags=cv2.INTER_CUBIC)
        y0 = int(y * H - band_h / 2)
        frame[y0:y0 + band_h] = band
        cv2.rectangle(frame, (0, y0), (W - 1, y0 + band_h - 1), (8, 11, 17), 6)


# ---------------------------------------------------------------- frame
CAPTIONS = caption_groups()
CORNER = None
if EDIT.get("corner_tag"):  # a small tag in the top-left corner of every frame, e.g. "PART 1"
    _ct = text_block(" ".join(EDIT["corner_tag"].upper()), font(MONO, 34), color=YELLOW)
    CORNER = np.zeros((_ct.shape[0] + 20, _ct.shape[1] + 32, 4), np.uint8)
    CORNER[..., :3], CORNER[..., 3] = (12, 12, 16), 215
    blend(CORNER, _ct, CORNER.shape[1] / 2, CORNER.shape[0] / 2)


def render_frame(t):
    s = next(x for x in SHOTS if x["t0"] <= t < x["t1"]) if t < END else SHOTS[-1]
    frame = np.zeros((H, W, 3), np.uint8)
    M = None
    if "card" in s:
        draw_card(frame, s["card"], t, s)
    elif "vote" in s:
        render_vote(frame, s, t)
    else:
        M = camera(s, t)
        cv2.warpAffine(s["src"], M, (W, H), dst=frame, flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        if s.get("sat") is not None:
            f32 = frame.astype(np.float32)
            gray = f32.mean(axis=2, keepdims=True)
            frame[:] = np.clip(gray + (f32 - gray) * s["sat"], 0, 255).astype(np.uint8)
        if s.get("grade"):
            g = np.array(s["grade"], np.float32)
            frame[:] = np.clip(frame.astype(np.float32) * g, 0, 255).astype(np.uint8)
    for o in s.get("overlays", []):
        draw_overlay(frame, o, t, s, M)
    if s.get("hud"):  # true, or an anchor for the HUD to pop in partway through the shot
        t_hud = at(s["hud"]) if isinstance(s["hud"], str) else s["t0"]
        first = SHOTS.index(s) == 0 or not SHOTS[SHOTS.index(s) - 1].get("hud") or t_hud > s["t0"]
        if t >= t_hud:
            a, sc = pop(t, t_hud, s["t1"], enabled=first and s.get("hud_pop", True))
            (draw_days if HUD.get("mode") == "days" else draw_hud)(frame, t, a, sc)
    if CORNER is not None and "vote" not in s:
        blend(frame, CORNER, 60 + CORNER.shape[1] / 2, 70 + CORNER.shape[0] / 2)
    if s.get("captions", True):
        for c in CAPTIONS:
            if c["t0"] <= t < c["t1"]:
                a, sc = pop(t, c["t0"], c["t1"], dur=0.10)
                blend(frame, c["img"], W / 2, EDIT.get("caption_y", 0.70) * H, a, sc)
                break
    return frame


# ---------------------------------------------------------------- audio
def decode(path):
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def rms_db(x):
    x = x[np.abs(x).max(axis=1) > 1e-3] if len(x) else x
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9) if len(x) else -90


def place(mix, clip, t0, t1=None, gain_db=0.0, fade_in=0.02, fade_out=0.08, loop=False, src_offset=0.0):
    i0 = int(t0 * SR)
    if src_offset:
        clip = clip[int(src_offset * SR):]
    if t1 is not None:
        n = int((t1 - t0) * SR)
        if loop and len(clip) < n:
            clip = np.concatenate([clip] * (n // len(clip) + 1))
        clip = clip[:n]
    clip = clip * (10 ** (gain_db / 20))
    env = np.ones(len(clip), np.float32)
    fi, fo = int(fade_in * SR), int(fade_out * SR)
    if fi:
        env[:fi] = np.linspace(0, 1, min(fi, len(env)))[:len(env[:fi])]
    if fo:
        env[-fo:] *= np.linspace(1, 0, min(fo, len(env)))[-len(env[-fo:]):]
    clip = clip * env[:, None]
    i0c = max(i0, 0)
    clip = clip[i0c - i0:]
    n = min(len(clip), len(mix) - i0c)
    if n > 0:
        mix[i0c:i0c + n] += clip[:n]


def build_audio(out_wav):
    n = int(END * SR) + SR
    vo = decode(PART / "audio" / "voiceover.mp3")
    target = -20.0
    vo *= 10 ** ((target - rms_db(vo)) / 20)
    voice = np.zeros((n, 2), np.float32)
    place(voice, vo, 0, fade_in=0, fade_out=0)
    # duck envelope from the voice: 1 while speaking
    hop = SR // 100
    frames = voice[: len(voice) // hop * hop].reshape(-1, hop, 2)
    talk = (np.sqrt((frames ** 2).mean(axis=(1, 2))) > 10 ** (-42 / 20)).astype(np.float32)
    env, g = np.zeros_like(talk), 0.0
    for i, v in enumerate(talk):
        g += (v - g) * (0.5 if v > g else 0.04)
        env[i] = g
    duck = np.repeat(env, hop)
    duck = np.pad(duck, (0, n - len(duck)))
    bed = np.zeros((n, 2), np.float32)
    for m in EDIT.get("music", []):
        clip = decode(ROOT / "library" / "music" / f"{m['file']}.mp3")
        clip *= 10 ** ((target - rms_db(clip)) / 20)
        place(bed, clip, at(m["from"]), at(m["to"]), m.get("gain", -9), m.get("fade_in", 0.8), m.get("fade_out", 0.4),
              src_offset=m.get("src_offset", 0))
    bed *= (10 ** (-EDIT.get("duck_db", 8) * duck / 20))[:, None]
    fx = np.zeros((n, 2), np.float32)
    cache = {}
    for e in EDIT.get("sfx", []):
        if e["file"] not in cache:
            c = decode(ROOT / "library" / "sfx" / f"{e['file']}.mp3")
            cache[e["file"]] = c * 10 ** ((target - rms_db(c)) / 20)
        t0 = at(e["at"])
        t1 = at(e["until"]) if "until" in e else (t0 + e["dur"] if "dur" in e else None)
        place(fx, cache[e["file"]], t0, t1, e.get("gain", -6), e.get("fade_in", 0.02), e.get("fade_out", 0.15),
              loop=e.get("loop", False))
    mix = voice + bed + fx
    tmp = out_wav.with_suffix(".raw.wav")
    write_wav(tmp, mix)
    # two-pass loudness normalisation to -14 LUFS, -1.5 dBTP (Instagram / Shorts)
    probe = subprocess.run([FFMPEG, "-hide_banner", "-i", str(tmp), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                            "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run([FFMPEG, "-v", "error", "-y", "-i", str(tmp), "-af", af, "-ar", str(SR), str(out_wav)], check=True)
    tmp.unlink()
    return {"voice_db": rms_db(voice), "bed_db": rms_db(bed), "fx_db": rms_db(fx)}


def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    subprocess.run([FFMPEG, "-v", "error", "-y", "-f", "s16le", "-ac", "2", "-ar", str(SR), "-i", "-", str(path)],
                   input=pcm.tobytes(), check=True)


# ---------------------------------------------------------------- main
for s in SHOTS:
    load_shot(s)

if args.preview:
    out = PART / "preview"
    out.mkdir(exist_ok=True)
    for ts in args.preview.split(","):
        t = float(ts)
        Image.fromarray(render_frame(t)).save(out / f"t{t:06.2f}.png")
    print(f"wrote {len(args.preview.split(','))} preview frames to {out.relative_to(ROOT)}")
    raise SystemExit

name = PART.name
wav = PART / "audio" / "mix.wav"
levels = build_audio(wav)
print("mix levels (dB RMS before loudnorm):", {k: round(v, 1) for k, v in levels.items()})
if args.no_video:
    raise SystemExit

# one top-quality encode, copied to one file per platform (both platforms re-encode on upload,
# so the cleanest possible source gives the best result on each); tune animation suits flat-shaded cartoon art
PLATFORMS = ["instagram", "youtube"]
master = PART / f"{name}-{PLATFORMS[0]}.mp4"
cmd = [FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
       "-i", "-", "-i", str(wav),
       "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slower", "-tune", "animation", "-crf", "12",
       "-profile:v", "high", "-pix_fmt", "yuv420p", "-g", str(FPS),
       "-c:a", "aac", "-b:a", "320k", "-ar", str(SR), "-t", f"{END:.3f}", "-movflags", "+faststart", str(master)]
enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
Image.fromarray(render_frame(0)).convert("RGB").save(PART / "cover.jpg", quality=92)
total = int(END * FPS)
for f in range(total):
    enc.stdin.write(render_frame(f / FPS).tobytes())
    if f % (FPS * 10) == 0:
        print(f"  {f / FPS:5.1f}s / {END:.1f}s", flush=True)
enc.stdin.close()
enc.wait()
for platform in PLATFORMS[1:]:
    shutil.copyfile(master, PART / f"{name}-{platform}.mp4")
for platform in PLATFORMS:
    f = PART / f"{name}-{platform}.mp4"
    print(f"wrote {f.relative_to(ROOT)} ({f.stat().st_size / 1e6:.1f} MB, {END:.1f}s)")
print(f"wrote {(PART / 'cover.jpg').relative_to(ROOT)}")
