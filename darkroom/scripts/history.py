"""darkroom: draw a post's work history as an Excalidraw file, in the series' style.

    python history.py fig/name.toml            # writes fig/name.excalidraw, prints checks

The work history closes a post. It is a chain of numbered boxes, one per task, read top to bottom.
Each box says why the task was done (blue) and what it found (red). Each arrow carries the reason
that finding prompted the next task (green, "so"). When one finding prompted two tasks the chain
forks: the first follow-up stays in the column, the others move to a column on the right.

Spec (TOML), tasks in the order they are numbered, which is the order of the post's sections:

    [[task]]
    id = "halves"
    title = "Compare two halves of the texts"
    date = "20 Nov"                  # optional
    exp = "E014"                     # optional experiment number, or a list
    why = "a lens should not depend on which texts it saw"
    found = ["Qwen: agreement rises with depth, 0.46 to 1.00",
             "Gemma: none below layer 27; one text 9,000x too large"]     # one or two findings
    after = "fit100"                 # the task whose finding prompted this one; none on the first
    so = "would other texts have given the same lens?"   # why that finding prompted this task

Render with the excalidraw-diagram skill's render_excalidraw.py, then view the PNG.
"""
import json
import math
import sys
import textwrap
import tomllib
from pathlib import Path

INK, RULE, TINT, PAPER = "#1e1d1a", "#aaa498", "#f3efe6", "#fffdf9"
SIENNA, SLATE, OLIVE = "#a9502c", "#3e6a88", "#6f7f38"
W_MAIN, W_SIDE, GAP_X, GAP_Y, PAD, KEY_W, ARROW_X = 650, 440, 90, 56, 16, 62, 50
MAX_TASKS, MAX_COLS, MAX_CHARS, MAX_FOUND = 12, 2, 90, 2

_seed = [1000]


def _base(kind, eid, x, y, w, h, stroke, bg="transparent", sw=1):
    _seed[0] += 1
    return {"type": kind, "id": eid, "x": x, "y": y, "width": w, "height": h,
            "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid",
            "strokeWidth": sw, "strokeStyle": "solid", "roughness": 0, "opacity": 100,
            "angle": 0, "seed": _seed[0], "version": 1, "versionNonce": 1, "isDeleted": False,
            "groupIds": [], "boundElements": None, "link": None, "locked": False}


def _wrap(s, width, size):
    return textwrap.wrap(s, max(8, int(width / (size * 0.6)))) or [""]


def _text(eid, x, y, rows, size, color):
    e = _base("text", eid, x, y, math.ceil(max(map(len, rows)) * size * 0.6) + 10,
              round(len(rows) * size * 1.25), color)
    s = "\n".join(rows)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=3, textAlign="left",
             verticalAlign="top", containerId=None, lineHeight=1.25)
    return e


def _arrow(eid, pts):
    (x0, y0), xs, ys = pts[0], [p[0] for p in pts], [p[1] for p in pts]
    e = _base("arrow", eid, x0, y0, max(xs) - min(xs), max(ys) - min(ys), RULE, sw=2)
    e.update(points=[[x - x0, y - y0] for x, y in pts], startArrowhead=None, endArrowhead="arrow",
             startBinding=None, endBinding=None, lastCommittedPoint=None)
    return e


def _keyed(els, eid, x, y, key, rows, color):
    """A coloured key word ("why", "found", "so") and its wrapped text. Returns the height."""
    els.append(_text(f"{eid}_key", x, y, [key], 16, color))
    e = _text(eid, x + KEY_W, y, rows, 16, color)
    els.append(e)
    return e["height"]


def build(spec):
    tasks, warn, by_id = spec.get("task", []), [], {}
    if not tasks:
        sys.exit("history: no [[task]] tables")
    if len(tasks) > MAX_TASKS:
        warn.append(f"{len(tasks)} tasks; keep to <= {MAX_TASKS} by joining steps that share one finding")
    for n, t in enumerate(tasks, 1):
        if t["id"] in by_id:
            sys.exit(f"history: task id {t['id']} is used twice")
        parent = t.get("after")
        if parent and parent not in by_id:
            sys.exit(f"history: task {t['id']} comes after {parent}, which is not defined before it")
        if n > 1 and not parent:
            warn.append(f"{t['id']}: no 'after'; every task but the first follows from a finding")
        if parent and not t.get("so"):
            warn.append(f"{t['id']}: no 'so'; say why the earlier finding prompted this task")
        found = t.get("found", [])
        found = [found] if isinstance(found, str) else list(found)
        if not 1 <= len(found) <= MAX_FOUND:
            warn.append(f"{t['id']}: {len(found)} findings; give 1 or {MAX_FOUND}")
        if not t.get("why"):
            warn.append(f"{t['id']}: no 'why'")
        for name, s in [("why", t.get("why", "")), ("so", t.get("so", ""))] + [("found", f) for f in found]:
            if len(s) > MAX_CHARS:
                warn.append(f"{t['id']}: {name} is {len(s)} chars; keep each line to <= {MAX_CHARS}")
        exp = t.get("exp", "")
        exp = ", ".join(map(str, exp)) if isinstance(exp, list) else str(exp)
        head = " · ".join(p for p in (t["title"], exp, t.get("date", "")) if p)
        t.update(n=n, kids=[], parent=parent, head=f"{n}  {head}", found=found)
        by_id[t["id"]] = t
        if parent:
            by_id[parent]["kids"].append(t)

    # Place the boxes. A column is one unbroken chain; `bottom` is the lowest used y in each.
    # The first column is wide; columns that hold a fork are narrower, so two still fit a page.
    def width(col):
        return W_MAIN if col == 0 else W_SIDE

    def left(col):
        return 0 if col == 0 else W_MAIN + GAP_X + (col - 1) * (W_SIDE + GAP_X)

    bottom, last = [], []
    for t in tasks:
        p = by_id.get(t["parent"])
        fork = p is not None and last[p["col"]] is not p
        if p is None:
            t["col"] = len(bottom)
        elif not fork:
            t["col"] = p["col"]
            t["so_rows"] = _wrap(t.get("so", ""), width(t["col"]) - ARROW_X - 26 - KEY_W, 16)
        else:  # leave from the parent's side, into the first column that is clear
            t["so_rows"] = _wrap(t.get("so", ""), GAP_X + W_SIDE - 26 - KEY_W, 16)
            line_y = p["y"] + p["h"] // 2
            col = p["col"] + 1
            while col < len(bottom) and bottom[col] > line_y - len(t["so_rows"]) * 20 - 30:
                col += 1
            for c in range(p["col"] + 1, col):
                bottom[c] = max(bottom[c], line_y + 12)
            t["col"], t["fork_y"] = col, line_y
        if t["col"] == len(bottom):
            bottom.append(0)
            last.append(None)
        body_w = width(t["col"]) - 2 * PAD - KEY_W
        t["head"] = _wrap(t["head"], width(t["col"]) - 2 * PAD, 18)
        t["why_rows"] = _wrap(t.get("why", ""), body_w, 16)
        t["found_rows"] = [r for f in t["found"] for r in _wrap(f, body_w, 16)] or [""]
        t["h"] = 2 * PAD + len(t["head"]) * 23 + 8 + (len(t["why_rows"]) + len(t["found_rows"])) * 20 + 10
        if p is None:
            t["y"] = bottom[t["col"]]
        elif fork:
            t["y"] = max(p["y"] + p["h"] + GAP_Y, bottom[t["col"]] + GAP_Y)
        else:
            t["y"] = p["y"] + p["h"] + GAP_Y + len(t["so_rows"]) * 20
        bottom[t["col"]], last[t["col"]] = t["y"] + t["h"], t
    if len(bottom) > MAX_COLS:
        warn.append(f"{len(bottom)} columns; more than {MAX_COLS} makes the text too small to read")

    arrows, boxes, words = [], [], []
    for t in tasks:
        x, y, W = left(t["col"]), t["y"], width(t["col"])
        ends = not t["parent"] or not t["kids"]  # where the work started and where it has got to
        boxes.append(_base("rectangle", f"{t['id']}_box", x, y, W, t["h"], INK, TINT if ends else PAPER, 2))
        words.append(_text(f"{t['id']}_head", x + PAD, y + PAD, t["head"], 18, INK))
        yy = y + PAD + len(t["head"]) * 23 + 8
        yy += _keyed(words, f"{t['id']}_why", x + PAD, yy, "why", t["why_rows"], SLATE) + 4
        _keyed(words, f"{t['id']}_found", x + PAD, yy, "found", t["found_rows"], SIENNA)
        p = by_id.get(t["parent"])
        if p is None:
            continue
        so_h = len(t["so_rows"]) * 20
        if "fork_y" in t:
            px, cx = left(p["col"]) + width(p["col"]), x + W // 2
            arrows.append(_arrow(f"{t['id']}_arrow", [(px, t["fork_y"]), (cx, t["fork_y"]), (cx, y - 4)]))
            _keyed(words, f"{t['id']}_so", px + 16, t["fork_y"] - so_h - 10, "so", t["so_rows"], OLIVE)
        else:
            ax, top = x + ARROW_X, p["y"] + p["h"]
            arrows.append(_arrow(f"{t['id']}_arrow", [(ax, top), (ax, y - 4)]))
            _keyed(words, f"{t['id']}_so", ax + 16, top + (y - top - so_h) // 2, "so", t["so_rows"], OLIVE)

    doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
           "elements": arrows + boxes + words,
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
