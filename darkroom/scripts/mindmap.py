"""darkroom: draw a post's question map as an Excalidraw file, in the series' style.

    python mindmap.py fig/name.toml            # writes fig/name.excalidraw, prints checks

Spec (TOML), branches listed anticlockwise from top-left (top-left, left, bottom-left, bottom,
bottom-right, right, top-right; fewer branches use a subset of these slots):

    question = "What could go wrong\\nwith the probe?"
    [[branch]]
    name = "Labels"                  # the abstraction: one or two words
    group = 1                        # colour: 1 sienna, 2 slate, 3 olive, 0 grey
    lines = ["needs ground truth?"]  # the concrete: one or two lines, <= 22 chars each
    answer = "contrast pairs"        # optional: what was done; drawn as "→ answer" in colour

Render with the excalidraw-diagram skill's render_excalidraw.py, then view the PNG.
"""
import json
import math
import sys
import tomllib
from pathlib import Path

INK, MUTED, RULE, HUB_FILL, PAPER = "#1e1d1a", "#6b675f", "#aaa498", "#f3efe6", "#fffdf9"
GROUP = {0: "#aaa498", 1: "#a9502c", 2: "#3e6a88", 3: "#6f7f38"}
CX, CY, RX, RY = 700, 400, 155, 60  # hub centre and half-axes
SLOTS = {"UL": (330, 170), "L": (290, 400), "LL": (330, 630), "B": (700, 690),
         "LR": (1070, 630), "R": (1110, 400), "UR": (1070, 170)}
LAYOUT = {3: ["L", "B", "R"], 4: ["UL", "LL", "LR", "UR"], 5: ["UL", "LL", "B", "LR", "UR"],
          6: ["UL", "L", "LL", "LR", "R", "UR"], 7: ["UL", "L", "LL", "B", "LR", "R", "UR"]}
MAX_CHARS, MAX_LINES, MAX_NAME_WORDS = 22, 2, 2

_seed = [1000]


def _base(kind, eid, x, y, w, h, stroke, bg="transparent", sw=1):
    _seed[0] += 1
    return {"type": kind, "id": eid, "x": x, "y": y, "width": w, "height": h,
            "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid",
            "strokeWidth": sw, "strokeStyle": "solid", "roughness": 0, "opacity": 100,
            "angle": 0, "seed": _seed[0], "version": 1, "versionNonce": 1, "isDeleted": False,
            "groupIds": [], "boundElements": None, "link": None, "locked": False}


def _text(eid, x, y, s, size, color, align):
    rows = s.split("\n")
    w = math.ceil(max(map(len, rows)) * size * 0.6) + 10
    h = round(len(rows) * size * 1.25)
    x = {"left": x, "right": x - w, "center": x - w / 2}[align]
    e = _base("text", eid, x, y, w, h, color)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=3, textAlign=align,
             verticalAlign="top", containerId=None, lineHeight=1.25)
    return e, h


def build(spec):
    branches, warn = spec["branch"], []
    if len(branches) not in LAYOUT:
        sys.exit(f"mindmap: {len(branches)} branches; use 3 to 7")
    q = spec["question"]
    if any(len(r) > MAX_CHARS for r in q.split("\n")) or q.count("\n") > 1:
        warn.append("question: wrap to two lines of <= 22 chars")
    els = [_base("ellipse", "hub", CX - RX, CY - RY, 2 * RX, 2 * RY, INK, HUB_FILL, 2)]
    hub, _ = _text("hub_text", CX, CY - 25 if "\n" in q else CY - 12, q, 20, INK, "center")
    lines, nodes = [], []
    for b, slot in zip(branches, LAYOUT[len(branches)]):
        key, (dx, dy) = b["name"].lower().replace(" ", "_"), SLOTS[slot]
        col = GROUP[b.get("group", 0)]
        t = 1 / math.hypot((dx - CX) / RX, (dy - CY) / RY)  # where the ray leaves the hub
        sx, sy = round(CX + t * (dx - CX)), round(CY + t * (dy - CY))
        ln = _base("line", f"ln_{key}", sx, sy, abs(dx - sx), abs(dy - sy), RULE, sw=2)
        ln["points"] = [[0, 0], [dx - sx, dy - sy]]
        lines.append(ln)
        nodes.append(_base("ellipse", f"dot_{key}", dx - 8, dy - 8, 16, 16, col, col))
        if slot == "B":
            ax, ay, align = dx, dy + 18, "center"
        elif slot in ("UL", "L", "LL"):
            ax, ay, align = dx - 18, dy - 14, "right"
        else:
            ax, ay, align = dx + 18, dy - 14, "left"
        e, h = _text(f"name_{key}", ax, ay, b["name"], 22, col, align)
        nodes.append(e)
        y = ay + 32
        rows = b.get("lines", [])
        blocks = [("txt", "\n".join(rows), MUTED)]
        if b.get("answer"):
            blocks.append(("ans", "→ " + b["answer"].replace("\n", "\n  "), col))
        for tag, s, c in blocks:
            if s:
                e, h = _text(f"{tag}_{key}", ax, y, s, 16, c, align)
                nodes.append(e)
                y += h + 4
        if len(b["name"].split()) > MAX_NAME_WORDS:
            warn.append(f"{b['name']}: branch name over {MAX_NAME_WORDS} words")
        if len(rows) > MAX_LINES or any(len(r) > MAX_CHARS for r in rows):
            warn.append(f"{b['name']}: keep to {MAX_LINES} lines of <= {MAX_CHARS} chars")
    doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
           "elements": lines + els + [hub] + nodes,
           "appState": {"viewBackgroundColor": PAPER, "gridSize": 20}, "files": {}}
    return doc, warn


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    doc, warn = build(tomllib.loads(src.read_text()))
    out = src.with_suffix(".excalidraw")
    out.write_text(json.dumps(doc, indent=1, ensure_ascii=False))
    print(f"wrote {out}  ({len(doc['elements'])} elements)")
    for w in warn:
        print("  warn:", w)
    print("  ok" if not warn else "  fix the warnings, then render and look")


if __name__ == "__main__":
    main()
