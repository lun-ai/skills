#!/usr/bin/env python3
"""Check a research-dashboard DASHBOARD.md for numbering, map and page-link consistency.

Usage: python3 check_map.py path/to/DASHBOARD.md

Checks that the global experiment numbers (E###) agree across the counter line, the
registry, the experiment list, the map (HTML page, ASCII block or Excalidraw file) and the
topic files linked from the dashboard, and that every linked HTML page exists.
Exits 1 if any error is found; warnings alone exit 0.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

EID = re.compile(r"\bE(\d{3,})\b")
STATUSES = ("planned", "designing", "running", "done", "abandoned")
HTML_LINK = re.compile(r"\]\(<?([^)>\s]+\.html)>?(?:#[^)]*)?\)")


def section(text, heading):
    """Body of the section starting at `heading`, up to the next heading of equal or higher level."""
    level = heading.split()[0]
    m = re.search(rf"^{re.escape(heading)}[ \t]*$", text, re.M)
    if not m:
        return None
    rest = text[m.end():]
    stop = re.search(rf"^#{{1,{len(level)}}} ", rest, re.M)
    return rest[: stop.start()] if stop else rest


def table_rows(body):
    """Header cells and data rows of the first Markdown table in `body`."""
    lines = [l.strip() for l in (body or "").splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return [], []
    split = lambda l: [c.strip() for c in l.strip("|").split("|")]
    return [h.lower() for h in split(lines[0])], [split(l) for l in lines[2:]]


def status_word(status):
    return status.strip("* ").split(" ")[0].lower() if status else ""


def parse(text):
    """The dashboard's counter, registry rows (by ID) and experiment statuses (by E###)."""
    rmap = section(text, "## Research map") or ""
    counter = re.search(r"Next experiment number:\s*\**E(\d+)", rmap)
    _, reg_rows = table_rows(section(text, "### Registry"))
    registry, duplicates = {}, []
    for row in reg_rows:
        if row[0] in registry:
            duplicates.append(row[0])
        registry[row[0]] = row
    head, exp_rows = table_rows(section(text, "## Experiments"))
    col = head.index("status") if "status" in head else None
    listed, list_dupes = {}, []
    for row in exp_rows:
        m = EID.search(row[0])
        if not m:
            continue
        eid = f"E{m.group(1)}"
        if eid in listed:
            list_dupes.append(eid)
        listed[eid] = row[col] if col is not None and col < len(row) else ""
    return {"counter": int(counter.group(1)) if counter else None, "registry": registry,
            "listed": listed, "duplicates": duplicates, "list_duplicates": list_dupes}


def map_source(d):
    """Hash of everything the map is drawn from; stamped on the page as `map-source`."""
    payload = [d["counter"], sorted(d["registry"].values()),
               sorted((e, status_word(s)) for e, s in d["listed"].items())]
    return hashlib.sha256(json.dumps(payload).encode()).hexdigest()[:12]


def map_format(map_body):
    m = re.search(r"^Format:\s*([\w-]+)", map_body or "", re.M)
    return m.group(1).lower() if m else None


def main(path):
    dash = Path(path)
    text = dash.read_text()
    errors, warnings = [], []

    if section(text, "## Research map") is None:
        print(f"ERROR: no '## Research map' section in {dash}")
        return 1
    d = parse(text)
    registry, listed = d["registry"], d["listed"]
    if d["counter"] is None:
        errors.append("no 'Next experiment number: **E###**' line in the Research map")
    for rid in d["duplicates"]:
        errors.append(f"{rid} appears twice in the registry")
    for eid in d["list_duplicates"]:
        errors.append(f"{eid} appears twice in the experiment list")

    topics = {r for r in registry if r.startswith("topic:")}
    impls = {r for r in registry if r.startswith("impl:")}
    reg_ids = {r for r in registry if re.fullmatch(r"E\d{3,}", r)}
    for rid in sorted(reg_ids):
        row = registry[rid]
        topic = row[3] if len(row) > 3 else ""
        if topic not in topics:
            errors.append(f"{rid}: registry topic '{topic}' is not a registered 'topic:' row")
        attrs = row[6] if len(row) > 6 else ""
        for key, known in (("uses", impls), ("from", reg_ids)):
            m = re.search(rf"\b{key}:\s*([^·]*)", attrs)
            for ref in re.findall(r"impl:[\w-]+|E\d{3,}", m.group(1) if m else ""):
                if ref not in known:
                    errors.append(f"{rid}: '{key}: {ref}' is not registered")

    # Registry and experiment list agree; counter is ahead of every number.
    for eid in sorted(reg_ids - set(listed)):
        errors.append(f"{eid} is in the registry but not in the experiment list")
    for eid in sorted(set(listed) - reg_ids):
        errors.append(f"{eid} is in the experiment list but not in the registry")
    for eid, status in sorted(listed.items()):
        if status_word(status) not in STATUSES:
            warnings.append(f"{eid}: status '{status}' does not start with "
                            "Planned/Designing/Running/Done/Abandoned")
    if d["counter"] is not None and reg_ids:
        top = max(int(e[1:]) for e in reg_ids)
        if d["counter"] <= top:
            errors.append(f"counter says next is E{d['counter']:03d} "
                          f"but E{top:03d} is already registered")
        missing = sorted(set(range(1, top + 1)) - {int(e[1:]) for e in reg_ids})
        if missing:
            warnings.append("unregistered numbers below the counter (fine if never assigned): "
                            + ", ".join(f"E{n:03d}" for n in missing))

    # The map, in whichever format the Map section declares.
    map_body = section(text, "### Map") or ""
    fmt = map_format(map_body)
    if fmt == "answer-me-with-html":
        link = HTML_LINK.search(map_body)
        page = dash.parent / link.group(1) if link else None
        if not page:
            errors.append("Map section declares answer-me-with-html but links no .html page")
        elif page.exists():
            if f"map-source: {map_source(d)}" not in page.read_text(errors="replace"):
                errors.append(f"{link.group(1)} is stale (registry or statuses changed since it "
                              "was rendered); run scripts/render_map.py")
    elif fmt == "ascii":
        block = re.search(r"```text\n(.*?)```", map_body, re.S)
        ids = {f"E{n}" for n in EID.findall(block.group(1))} if block else set()
        for eid in sorted(reg_ids - ids):
            errors.append(f"{eid} is in the registry but not in the ASCII map; "
                          "run scripts/render_map.py")
        for eid in sorted(ids - reg_ids):
            errors.append(f"{eid} is in the ASCII map but not in the registry")
    elif fmt == "excalidraw":
        link = re.search(r"\]\(<?([^)>\s]+\.excalidraw)>?\)", map_body)
        drawing = dash.parent / link.group(1) if link else None
        if not drawing or not drawing.exists():
            errors.append("Map section declares excalidraw but its .excalidraw file is missing")
        else:
            ids = {f"E{n}" for n in EID.findall(drawing.read_text(errors="replace"))}
            for eid in sorted(reg_ids - ids):
                warnings.append(f"{eid} is not in {link.group(1)}; redraw it from the registry")
    else:
        errors.append("Map section has no 'Format: answer-me-with-html|ascii|excalidraw' line; "
                      "run scripts/render_map.py")

    # Topic files, and every HTML page linked from the dashboard or a topic file.
    seen_in = {}
    md_links = {l.split("#")[0] for l in re.findall(r"\]\(([^)\s]+\.md)(?:#[^)]*)?\)", text)}
    pages = {(dash.name, l) for l in HTML_LINK.findall(text)}
    for link in sorted(md_links):
        f = (dash.parent / link).resolve()
        if not f.exists() or f == dash.resolve() or f.parent.name == "pages":
            continue
        body = f.read_text()
        pages |= {(link, str(Path(link).parent / l)) for l in HTML_LINK.findall(body)}
        if f.name.endswith("_detail.md") or re.fullmatch(r"e\d{3,}", f.parent.name):
            continue
        for n in re.findall(r"^##\s+E(\d{3,})\b", body, re.M):
            seen_in.setdefault(f"E{n}", []).append(link)
    for source, link in sorted(pages):
        if not re.match(r"[a-z]+:", link) and not (dash.parent / link).exists():
            errors.append(f"{source} links {link}, which does not exist")
    for eid, files in sorted(seen_in.items()):
        if eid not in reg_ids:
            errors.append(f"{eid} has a section in {files[0]} but is not registered")
        if len(files) > 1:
            errors.append(f"{eid} has sections in several topic files: {', '.join(files)}")
    for eid in sorted(reg_ids - set(seen_in)):
        warnings.append(f"{eid} has no '## {eid} ...' section in any linked topic file")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print(f"{len(reg_ids)} experiments, {len(topics)} topics, {len(impls)} implementations; "
          f"map format {fmt or 'none'}; {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
