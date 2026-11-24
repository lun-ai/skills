"""darkroom: draw a post's idea map as an Excalidraw file, in the series' style.

    python ideamap.py fig/name.toml            # writes fig/name.excalidraw, prints checks

The map is a graph in the manner of a commit graph. Time runs left to right, one band per post,
the current post's band tinted. Each node is one idea or experiment; lanes are threads of work.
The drawing carries the story: a branch is a line leaving its lane, a dead end is a cross, a
revision is a dashed arrow into the idea that replaced it, a loop is a dashed arrow going back.
Text is kept for what a drawing cannot say: a short name under each node and, for the current
post only, its question, what would refute it, and a credence meter.

Spec (TOML). Top-level keys come first, then the posts in order, each with its nodes:

    here = "Part 3"                  # label of the current post, the last [[page]]
    questions = ["Does the steered goal still hold at the end of a long run?"]     # 1 or 2
    refuted_if = ["The idea fails if steered and unsteered runs drift equally."]   # 1 or 2
    credence = "70%"                 # a percentage, a 0-1 number, or a word such as "likely"
    credence_was = "40%"             # optional: the credence before this post, marked on the meter

    [[page]]
    label = "Part 1"                 # the first post may open with a page labelled "Before"
    [[page.node]]
    id = "probe"
    label = "Linear probe"           # the idea's name: one to four words
    exp = "E004"                     # optional: its experiment number, or a list of numbers;
                                     # drawn under the node as a callback and a tracker
    status = "held"                  # held | refuted | revised | open
    lane = 0                         # optional row, 0 at the top; default is the parent's lane
    after = []                       # ids this idea followed from; two ids draw a merge
    revises = "other_id"             # optional: this idea replaced that one (dashed arrow)
    back_to = "other_id"             # optional: this result sent the work back to that idea

Render with the excalidraw-diagram skill's render_excalidraw.py, then view the PNG.
"""
import json
import math
import re
import sys
import textwrap
import tomllib
from pathlib import Path

INK, MUTED, RULE, TINT, PAPER = "#1e1d1a", "#6b675f", "#aaa498", "#f3efe6", "#fffdf9"
SIENNA, SLATE, OLIVE = "#a9502c", "#3e6a88", "#6f7f38"
STATUS = {"held": OLIVE, "refuted": SIENNA, "revised": RULE, "open": SLATE}
MIN_W, LANE0, LANE_H, R = 1000, 104, 128, 13
MAX_NODES, MAX_COLS, MAX_LANES, MAX_WORDS, MAX_CHARS, MAX_POINTS = 12, 7, 3, 4, 110, 2

_seed = [1000]


def _base(kind, eid, x, y, w, h, stroke, bg="transparent", sw=1, style="solid"):
    _seed[0] += 1
    return {"type": kind, "id": eid, "x": x, "y": y, "width": w, "height": h,
            "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid",
            "strokeWidth": sw, "strokeStyle": style, "roughness": 0, "opacity": 100,
            "angle": 0, "seed": _seed[0], "version": 1, "versionNonce": 1, "isDeleted": False,
            "groupIds": [], "boundElements": None, "link": None, "locked": False}


def _text(eid, x, y, s, size, color, width, align="left"):
    """Text wrapped to `width` pixels; x is the left edge, or the centre for align="center"."""
    rows = textwrap.wrap(s, max(6, int(width / (size * 0.6)))) or [""]
    w = math.ceil(max(map(len, rows)) * size * 0.6) + 10
    e = _base("text", eid, x - w / 2 if align == "center" else x, y, w,
              round(len(rows) * size * 1.25), color)
    s = "\n".join(rows)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=3, textAlign=align,
             verticalAlign="top", containerId=None, lineHeight=1.25)
    return e, len(rows)


def _path(eid, pts, color, sw=2, style="solid", arrow=False, curved=False):
    """A line or arrow through absolute points."""
    (x0, y0), xs, ys = pts[0], [p[0] for p in pts], [p[1] for p in pts]
    e = _base("arrow" if arrow else "line", eid, x0, y0, max(xs) - min(xs), max(ys) - min(ys),
              color, sw=sw, style=style)
    e["points"] = [[x - x0, y - y0] for x, y in pts]
    if curved:
        e["roundness"] = {"type": 2}
    if arrow:
        e.update(startArrowhead=None, endArrowhead="arrow", startBinding=None, endBinding=None,
                 lastCommittedPoint=None)
    return e


def _glyph(key, cx, cy, status, r=R):
    """A node's mark: a tick for held, a cross for refuted, '?' for open, dashed ring for revised."""
    col, k = STATUS[status], r / R
    if status in ("held", "refuted"):
        out = [_base("ellipse", f"{key}_disc", cx - r, cy - r, 2 * r, 2 * r, col, col, 2)]
        strokes = ([[(-6, 0), (-2, 5), (6, -5)]] if status == "held"
                   else [[(-5, -5), (5, 5)], [(-5, 5), (5, -5)]])
        for i, st in enumerate(strokes):
            out.append(_path(f"{key}_mark{i}", [(cx + k * a, cy + k * b) for a, b in st], PAPER, sw=2))
        return out
    out = [_base("ellipse", f"{key}_disc", cx - r, cy - r, 2 * r, 2 * r, col, PAPER, 2,
                 "dashed" if status == "revised" else "solid")]
    if status == "open":
        size = round(17 * k)
        out.append(_text(f"{key}_mark", cx, cy - size * 0.625, "?", size, col, 40, "center")[0])
    return out


def _sentence(warn, where, s, question=False):
    s = s.strip()
    if len(s.split()) < 4 or not s[:1].isupper() and not s[:1].isdigit():
        warn.append(f"{where}: write a full sentence, not a label")
    elif question and not s.endswith("?"):
        warn.append(f"{where}: a question ends with '?'")
    elif not question and s[-1] not in ".?!":
        warn.append(f"{where}: a full sentence ends with a full stop")
    if len(s) > MAX_CHARS:
        warn.append(f"{where}: {len(s)} chars; keep each sentence to <= {MAX_CHARS}")


def _level(s):
    """A credence as a 0-1 fraction, or None when it is a word or missing."""
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*%\s*", s or "")
    if m:
        return min(float(m.group(1)) / 100, 1.0)
    m = re.fullmatch(r"\s*(0?\.\d+|[01](?:\.0+)?)\s*", s or "")
    return float(m.group(1)) if m else None


def _place(spec, warn):
    """Give every node a column and a lane. Each post owns a run of columns."""
    pages, nodes = spec.get("page", []), {}
    if not pages:
        sys.exit("ideamap: no [[page]] tables")
    start = 0
    for pi, pg in enumerate(pages):
        pg["c0"], end = start, start
        for n in pg.get("node", []):
            if n["id"] in nodes:
                sys.exit(f"ideamap: node id {n['id']} is used twice")
            if n.get("status") not in STATUS:
                sys.exit(f"ideamap: node {n['id']}: status must be one of {', '.join(STATUS)}")
            parents = list(n.get("after", []))
            if n.get("revises") and n["revises"] not in parents:
                parents.append(n["revises"])
            for p in parents:
                if p not in nodes:
                    sys.exit(f"ideamap: node {n['id']} follows {p}, which is not defined before it")
            n.update(parents=parents, page=pi,
                     col=max([start] + [nodes[p]["col"] + 1 for p in parents]),
                     lane=n.get("lane", nodes[parents[0]]["lane"] if parents else 0))
            if any(m["col"] == n["col"] and m["lane"] == n["lane"] for m in nodes.values()):
                sys.exit(f"ideamap: node {n['id']} lands on another node; give it its own lane")
            if len(n["label"].split()) > MAX_WORDS:
                warn.append(f"{n['id']}: name over {MAX_WORDS} words; a node carries a name, not a sentence")
            nodes[n["id"]] = n
            end = max(end, n["col"])
        if not pg.get("node"):
            sys.exit(f"ideamap: page {pg['label']} has no nodes")
        pg["c1"], start = end, end + 1
    for n in nodes.values():
        if n.get("back_to") and n["back_to"] not in nodes:
            sys.exit(f"ideamap: node {n['id']} goes back to {n['back_to']}, which is not defined")
        n["route"] = {}
        for p in n["parents"]:
            a = nodes[p]
            busy = {m["lane"] for m in nodes.values() if a["col"] < m["col"] < n["col"]}
            # Run along the parent's lane and step over just before the child, or step first.
            n["route"][p] = "late" if a["lane"] not in busy else "early"
            if a["lane"] in busy and (n["lane"] in busy or n["lane"] == a["lane"]):
                warn.append(f"{p} -> {n['id']}: the line runs through another node; move one to another lane")
    if len(nodes) > MAX_NODES:
        warn.append(f"{len(nodes)} nodes; keep to <= {MAX_NODES} by leaving out ideas this post does not build on")
    if start > MAX_COLS:
        warn.append(f"{start} columns; keep to <= {MAX_COLS} so the names stay readable")
    if max(n["lane"] for n in nodes.values()) >= MAX_LANES:
        warn.append(f"more than {MAX_LANES} lanes; merge threads or drop one")
    if not any(n.get("after") or n.get("revises") for n in nodes.values()):
        warn.append("no node follows another: this is a list, not a map")
    return pages, nodes, start


def build(spec):
    warn = []
    pages, nodes, ncols = _place(spec, warn)
    here = spec.get("here")
    if here != pages[-1]["label"]:
        warn.append("here: must name the last [[page]]; the map stops at the current post")
    pitch = min(300, max(150, MIN_W // ncols))
    width = max(MIN_W, ncols * pitch)
    lanes = max(n["lane"] for n in nodes.values()) + 1
    bottom = LANE0 + (lanes - 1) * LANE_H + 100
    for n in nodes.values():
        n["x"], n["y"] = n["col"] * pitch + pitch // 2, LANE0 + n["lane"] * LANE_H
        n["now"] = n["page"] == len(pages) - 1
        n["r"] = R + (7 if n["now"] else 0)  # the clearance a line keeps from the node

    for n in nodes.values():
        e = n.get("exp", "")
        n["exp"] = ", ".join(map(str, e)) if isinstance(e, list) else str(e).strip()
    tag_h = 19 if any(n["exp"] for n in nodes.values()) else 0  # one shift for all, names stay aligned
    bottom += tag_h

    bands, edges, marks, words = [], [], [], []
    for i, pg in enumerate(pages):
        x0, x1 = pg["c0"] * pitch, (pg["c1"] + 1) * pitch
        now = i == len(pages) - 1
        if now:
            bands.append(_base("rectangle", "band_now", x0, -14, max(x1, width) - x0, bottom + 14, TINT, TINT))
        elif i:
            bands.append(_path(f"band{i}", [(x0, -14), (x0, bottom)], RULE, sw=1, style="dotted"))
        words.append(_text(f"page{i}", x0 + 14, 0, pg["label"] + (" · this page" if now else ""),
                           15, INK if now else MUTED, 400)[0])

    for n in nodes.values():
        for p in n["parents"]:
            a, revision = nodes[p], p == n.get("revises")
            xa, xb = a["x"] + a["r"] + 3, n["x"] - n["r"] - (8 if revision else 3)
            # The step between lanes sits on a column boundary, clear of the names under the nodes.
            mid = (n["col"] if n["route"][p] == "late" else a["col"] + 1) * pitch
            pts = ([(xa, a["y"]), (xb, n["y"])] if a["y"] == n["y"] else
                   [(xa, a["y"]), (mid - 0.1 * pitch, a["y"]), (mid + 0.1 * pitch, n["y"]), (xb, n["y"])])
            edges.append(_path(f"edge_{p}_{n['id']}", pts, RULE, style="dashed" if revision else "solid",
                               arrow=revision))
        if n.get("back_to"):
            b = nodes[n["back_to"]]
            top = min(n["y"], b["y"]) - 62
            edges.append(_path(f"loop_{n['id']}", [(n["x"] - 6, n["y"] - n["r"] - 4),
                                                   ((n["x"] + b["x"]) / 2, top),
                                                   (b["x"] + 6, b["y"] - b["r"] - 9)],
                               MUTED, style="dashed", arrow=True, curved=True))
        if n["now"]:
            marks.append(_base("ellipse", f"{n['id']}_ring", n["x"] - R - 6, n["y"] - R - 6,
                               2 * R + 12, 2 * R + 12, INK, PAPER, 2))
        marks += _glyph(n["id"], n["x"], n["y"], n["status"])
        if n["exp"]:
            e, rows = _text(f"{n['id']}_exp", n["x"], n["y"] + R + 13, n["exp"], 13,
                            STATUS[n["status"]] if n["status"] != "revised" else MUTED,
                            pitch - 22, "center")
            words.append(e)
            if rows > 1:
                warn.append(f"{n['id']}: experiment numbers wrap; give a range such as E004-E006")
        e, rows = _text(f"{n['id']}_name", n["x"], n["y"] + R + 14 + tag_h, n["label"], 15,
                        INK if n["now"] else MUTED, pitch - 22, "center")
        words.append(e)
        if rows > 3:
            warn.append(f"{n['id']}: the name wraps to {rows} lines; shorten it")

    # What a drawing cannot say, for the current post only: the question, the refuter, the credence.
    y, gap, cred_w = bottom + 30, 36, 190
    col_w = (width - cred_w - 2 * gap) // 2
    heights = []
    for k, (key, head, status, x) in enumerate((("questions", "This page asks", "open", 0),
                                                ("refuted_if", "Refuted if", "refuted", col_w + gap))):
        pts = spec.get(key, [])
        if not 1 <= len(pts) <= MAX_POINTS:
            warn.append(f"{key}: {len(pts)} sentences; use 1 to {MAX_POINTS}")
        words.append(_text(f"{key}_head", x, y, head, 14, MUTED, col_w)[0])
        yy = y + 30
        for i, s in enumerate(pts):
            _sentence(warn, f"{key} {i + 1}", s, question=key == "questions")
            marks += _glyph(f"{key}{i}", x + 10, yy + 11, status, r=9)
            e, rows = _text(f"{key}_{i}", x + 30, yy, s, 16, INK, col_w - 40)
            words.append(e)
            yy += rows * 20 + 12
        heights.append(yy)

    x = width - cred_w
    cred, was = str(spec.get("credence", "")).strip(), str(spec.get("credence_was", "")).strip()
    words.append(_text("credence_head", x, y, "Credence", 14, MUTED, cred_w)[0])
    if not cred:
        warn.append("credence: give the author's credence; ask, never guess")
    p, q = _level(cred), _level(was)
    words.append(_text("credence_level", x, y + 26, f"{was} → {cred}" if was else cred or "not stated",
                       20, OLIVE, cred_w + 60)[0])
    if p is not None:
        marks.append(_base("rectangle", "credence_track", x, y + 62, 160, 10, RULE, PAPER))
        if p > 0:
            marks.append(_base("rectangle", "credence_fill", x, y + 62, round(160 * p), 10, OLIVE, OLIVE))
        if q is not None:
            marks.append(_path("credence_was", [(x + round(160 * q), y + 56), (x + round(160 * q), y + 78)], INK))
    heights.append(y + 84)

    # A key for the marks this map uses that do not explain themselves.
    used = {n["status"] for n in nodes.values()}
    key = [(s, w) for s, w in (("held", "held up"), ("refuted", "refuted"), ("revised", "revised"),
                               ("open", "still open")) if s in used]
    y, x = max(heights) + 18, 0
    for s, w in key:
        marks += _glyph(f"key_{s}", x + 8, y + 8, s, r=7)
        e, _ = _text(f"key_{s}_word", x + 22, y, w, 13, MUTED, 200)
        words.append(e)
        x += 22 + e["width"] + 16
    if any(n.get("back_to") for n in nodes.values()):
        edges.append(_path("key_loop", [(x + 34, y + 9), (x, y + 9)], MUTED, style="dashed", arrow=True))
        words.append(_text("key_loop_word", x + 42, y, "went back to", 13, MUTED, 200)[0])

    doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
           "elements": bands + edges + marks + words,
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
