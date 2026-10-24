#!/usr/bin/env python3
"""Draw the research map from a DASHBOARD.md registry and rewrite its '### Map' section.

Usage: python3 render_map.py path/to/DASHBOARD.md [--format answer-me-with-html|ascii|excalidraw]
                             [--hide-uses] [--am path/to/am.mjs] [--open]

answer-me-with-html (default): writes pages/research-map.am.md next to the dashboard, renders
  pages/research-map.html with the answer-me-with-html CLI, and links both from the Map section.
ascii: writes the map as a ```text block into the Map section.
excalidraw: links pages/research-map.excalidraw from the Map section; draw or redraw that file
  with the excalidraw-diagram skill from the registry.
Without --format, the format already declared in the Map section is kept.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_map import map_format, map_source, parse, section, status_word  # noqa: E402

DEFAULT_AM = Path(__file__).resolve().parents[2] / "answer-me-with-html" / "scripts" / "am.mjs"
OPEN = {"planned", "designing", "running"}
BADGE = {"done": "ok done", "running": "warn running", "abandoned": "no abandoned"}


def clean(s):
    """Node text for the flow component: no characters it reads as syntax."""
    return re.sub(r"\s+", " ", re.sub(r"[\[\]{}()*,:|]", " ", s)).strip()


def attr(row, key):
    m = re.search(rf"\b{key}:\s*([^·]*)", row[6] if len(row) > 6 else "")
    return m.group(1).strip() if m else ""


def model(text):
    """Topics, implementations and experiments, in registry order, with what the map needs."""
    d = parse(text)
    reg = d["registry"]
    name = lambda rid: reg[rid][2] if rid in reg and len(reg[rid]) > 2 else rid
    exps = []
    for rid, row in reg.items():
        if not re.fullmatch(r"E\d{3,}", rid):
            continue
        status = status_word(d["listed"].get(rid, "")) or "planned"
        exps.append({
            "id": rid, "name": row[2], "topic": row[3], "created": row[4], "updated": row[5],
            "status": status, "uses": re.findall(r"impl:[\w-]+", attr(row, "uses")),
            "from": re.findall(r"(E\d{3,})(?:\s*\(([^)]*)\))?", attr(row, "from")),
            "node": f"{rid} · {clean(row[2])} ({status})",
        })
    return d, reg, name, exps


def html_draft(title, d, reg, name, exps, hide_uses=False):
    impl_node = {r: f"impl · {clean(name(r))}" for r in reg if r.startswith("impl:")}
    node = {e["id"]: e["node"] for e in exps}
    open_n = sum(e["status"] in OPEN for e in exps)
    topics = [r for r in reg if r.startswith("topic:")]
    lines = [
        "---", f"title: {title} research map",
        f"subtitle: Next experiment number E{d['counter']:03d}",
        f"map-source: {map_source(d)}", "cols: 3", "---",
        f"{len(exps)} experiments in {len(topics)} topics. {open_n} are open. "
        "The registry in the dashboard is the source of this page.", "",
        "## A Map {span=3}", "```flow LR",
    ]
    for e in exps:
        star = "*" if e["status"] in OPEN else ""
        drawn = False
        for u in [] if hide_uses else e["uses"]:
            if u in impl_node:
                lines.append(f"[{impl_node[u]}] -> {star}[{e['node']}]")
                drawn = True
        for parent, why in e["from"]:
            if parent in node:
                label = f": {clean(why)}" if why else ""
                lines.append(f"[{node[parent]}] --> {star}[{e['node']}]{label}")
                drawn = True
        if not drawn:
            lines.append(f"{star}[{e['node']}]")
    for t in topics:
        members = [e["node"] for e in exps if e["topic"] == t]
        if members:
            lines.append(f"group {clean(name(t))}: " + ", ".join(members))
    used = [impl_node[u] for u in impl_node if any(u in e["uses"] for e in exps)]
    if used and not hide_uses:
        lines.append("group Implementations: " + ", ".join(used))
    lines += ["```", "", "## B Timeline {span=1}", "```timeline v"]
    for e in sorted(exps, key=lambda e: (e["created"], e["id"])):
        star = "*" if e["status"] in OPEN else ""
        lines.append(f"{star}{e['created']} | {e['id']} · {clean(e['name'])} | "
                     f"{clean(name(e['topic']))} · {e['status']}")
    lines += ["```", "", "## C Registry {span=2}",
              "| ID | Kind | Name | Topic | Created | Updated | Status | Attributes |",
              "|---|---|---|---|---|---|---|---|"]
    status = {e["id"]: BADGE.get(e["status"], e["status"]) for e in exps}
    for rid, row in reg.items():
        cells = (row + [""] * 8)[:8]
        lines.append(f"| {rid} | {cells[1]} | {cells[2]} | {cells[3]} | {cells[4]} | "
                     f"{cells[5]} | {status.get(rid, '—')} | {cells[6]} |")
    return "\n".join(lines) + "\n"


def ascii_map(reg, name, exps):
    out = []
    for t in [r for r in reg if r.startswith("topic:")]:
        out.append(f"{name(t)} ({t})")
        mine = [e for e in exps if e["topic"] == t]
        for i, e in enumerate(mine):
            branch = "└──" if i == len(mine) - 1 else "├──"
            extra = "".join([f"  uses: {', '.join(e['uses'])}" if e["uses"] else "",
                             "  from: " + ", ".join(f"{p} ({w})" if w else p for p, w in e["from"])
                             if e["from"] else ""])
            out.append(f"{branch} {e['id']} · {e['name']} [{e['status']}] {e['created']}{extra}")
    impls = [r for r in reg if r.startswith("impl:")]
    if impls:
        out.append("Implementations")
        for i, r in enumerate(impls):
            out.append(f"{'└──' if i == len(impls) - 1 else '├──'} {r} · {name(r)}")
    return "\n".join(out)


def replace_map(text, body):
    m = re.search(r"^### Map[ \t]*$", text, re.M)
    if not m:
        sys.exit("no '### Map' heading in the dashboard")
    rest = text[m.end():]
    stop = re.search(r"^#{1,3} ", rest, re.M)
    end = m.end() + (stop.start() if stop else len(rest))
    return text[: m.end()] + "\n\n" + body.strip() + "\n\n" + text[end:]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("dashboard")
    ap.add_argument("--format", choices=["answer-me-with-html", "ascii", "excalidraw"])
    ap.add_argument("--am", default=os.environ.get("AM_MJS", str(DEFAULT_AM)))
    ap.add_argument("--hide-uses", action="store_true",
                    help="leave implementation arrows out of the HTML map (registry keeps them)")
    ap.add_argument("--open", action="store_true", help="let am open the page in a browser")
    a = ap.parse_args()

    dash = Path(a.dashboard).resolve()
    text = dash.read_text()
    fmt = a.format or map_format(section(text, "### Map")) or "answer-me-with-html"
    d, reg, name, exps = model(text)
    if d["counter"] is None:
        sys.exit("no 'Next experiment number: **E###**' line in the Research map")
    title = re.sub(r"\s*[—-]\s*Dashboard\s*$", "", re.search(r"^# (.+)$", text, re.M).group(1))

    if fmt == "answer-me-with-html":
        pages = dash.parent / "pages"
        pages.mkdir(exist_ok=True)
        draft, page = pages / "research-map.am.md", pages / "research-map.html"
        draft.write_text(html_draft(title, d, reg, name, exps, a.hide_uses))
        cmd = ["node", a.am, "render", str(draft), "-o", str(page)]
        if not a.open:
            cmd.append("--no-open")
        r = subprocess.run(cmd, capture_output=True, text=True)
        sys.stdout.write(r.stdout + r.stderr)
        if r.returncode or not page.exists():
            sys.exit(f"am render failed; fix {draft} or the registry and run again")
        body = ("Format: answer-me-with-html · open the map: "
                "[pages/research-map.html](pages/research-map.html) · draft: "
                "[pages/research-map.am.md](pages/research-map.am.md)\n\n"
                "Generated from the registry by `scripts/render_map.py`; do not edit the page "
                "or the draft by hand.")
    elif fmt == "ascii":
        body = ("Format: ascii · generated from the registry by `scripts/render_map.py`\n\n"
                "```text\n" + ascii_map(reg, name, exps) + "\n```")
    else:
        body = ("Format: excalidraw · open the map: "
                "[pages/research-map.excalidraw](pages/research-map.excalidraw)\n\n"
                "Drawn with the excalidraw-diagram skill from the registry; redraw it after "
                "every registry change.")
        if not (dash.parent / "pages" / "research-map.excalidraw").exists():
            print("! pages/research-map.excalidraw does not exist yet: draw it with the "
                  "excalidraw-diagram skill from the registry")
    dash.write_text(replace_map(text, body))
    print(f"Map section of {dash.name} now uses format {fmt}")


if __name__ == "__main__":
    main()
