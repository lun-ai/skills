#!/usr/bin/env python3
"""Check a research-dashboard DASHBOARD.md for numbering and map consistency.

Usage: python3 check_map.py path/to/DASHBOARD.md

Checks that the global experiment numbers (E###) agree across the counter line, the map
diagram, the registry, the experiment list and the topic files linked from the dashboard.
Exits 1 if any error is found; warnings alone exit 0.
"""
import re
import sys
from pathlib import Path

EID = re.compile(r"\bE(\d{3,})\b")
# Experiment-list status (first word) -> map class.
STATUS_CLASS = {"planned": "planned", "designing": "planned", "running": "running",
                "done": "done", "abandoned": "abandoned"}


def section(text, heading):
    """Body of the section starting at `heading`, up to the next heading of equal or higher level."""
    level = heading.split()[0]
    m = re.search(rf"^{re.escape(heading)}\s*$", text, re.M)
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


def main(path):
    dash = Path(path)
    text = dash.read_text()
    errors, warnings = [], []

    rmap = section(text, "## Research map")
    if rmap is None:
        print(f"ERROR: no '## Research map' section in {dash}")
        return 1

    counter = re.search(r"Next experiment number:\s*\**E(\d+)", rmap)
    if not counter:
        errors.append("no 'Next experiment number: **E###**' line in the Research map")

    # Registry
    _, reg_rows = table_rows(section(text, "### Registry"))
    registry, topics = {}, set()
    for row in reg_rows:
        rid = row[0]
        if rid.startswith("topic:"):
            topics.add(rid)
        if re.fullmatch(r"E\d{3,}", rid):
            if rid in registry:
                errors.append(f"{rid} appears twice in the registry")
            registry[rid] = row
    for rid, row in registry.items():
        topic = row[3] if len(row) > 3 else ""
        if topic not in topics:
            errors.append(f"{rid}: registry topic '{topic}' is not a registered 'topic:' row")

    # Map diagram: Mermaid preferred, ASCII text block accepted.
    map_body = section(text, "### Map") or ""
    mermaid = re.search(r"```mermaid\n(.*?)```", map_body, re.S)
    ascii_ = re.search(r"```text\n(.*?)```", map_body, re.S)
    map_ids, map_class = set(), {}
    if mermaid:
        body = mermaid.group(1)
        map_ids = set(re.findall(r"\b(E\d{3,})\s*[\[\(\{>]", body))
        for ids, cls in re.findall(r"^\s*class\s+([\w,\s]+?)\s+(\w+)\s*$", body, re.M):
            for i in re.split(r"[,\s]+", ids):
                if i:
                    map_class[i] = cls
    elif ascii_:
        map_ids = {f"E{n}" for n in EID.findall(ascii_.group(1))}
    else:
        errors.append("no ```mermaid or ```text block under '### Map'")

    # Experiment list
    head, exp_rows = table_rows(section(text, "## Experiments"))
    status_col = head.index("status") if "status" in head else None
    listed = {}
    for row in exp_rows:
        m = EID.search(row[0])
        if not m:
            continue
        eid = f"E{m.group(1)}"
        if eid in listed:
            errors.append(f"{eid} appears twice in the experiment list")
        listed[eid] = row[status_col] if status_col is not None and status_col < len(row) else ""

    # Cross-part agreement
    reg_ids = set(registry)
    for name, ids in (("map", map_ids), ("experiment list", set(listed))):
        for eid in sorted(reg_ids - ids):
            errors.append(f"{eid} is in the registry but not in the {name}")
        for eid in sorted(ids - reg_ids):
            errors.append(f"{eid} is in the {name} but not in the registry")

    if counter and reg_ids:
        top = max(int(e[1:]) for e in reg_ids)
        nxt = int(counter.group(1))
        if nxt <= top:
            errors.append(f"counter says next is E{nxt:03d} but E{top:03d} is already registered")
        missing = sorted(set(range(1, top + 1)) - {int(e[1:]) for e in reg_ids})
        if missing:
            warnings.append("unregistered numbers below the counter (fine if never assigned): "
                            + ", ".join(f"E{n:03d}" for n in missing))

    if mermaid:
        for eid, status in listed.items():
            word = status.strip("* ").split(" ")[0].lower() if status else ""
            want = STATUS_CLASS.get(word)
            if want is None:
                warnings.append(f"{eid}: status '{status}' does not start with "
                                "Planned/Designing/Running/Done/Abandoned")
            elif map_class.get(eid) != want:
                errors.append(f"{eid}: list status '{word}' but map class "
                              f"'{map_class.get(eid, 'none')}' (expected '{want}')")

    # Topic files linked from the dashboard
    seen_in = {}
    links = {l.split("#")[0] for l in re.findall(r"\]\(([^)\s]+\.md)(?:#[^)]*)?\)", text)}
    for link in sorted(links):
        f = (dash.parent / link).resolve()
        if not f.exists() or f == dash.resolve() or f.name.endswith("_detail.md"):
            continue
        for n in re.findall(r"^##\s+E(\d{3,})\b", f.read_text(), re.M):
            seen_in.setdefault(f"E{n}", []).append(link)
    for eid, files in sorted(seen_in.items()):
        if eid not in reg_ids:
            errors.append(f"{eid} has a section in {files[0]} but is not registered")
        if len(files) > 1:
            errors.append(f"{eid} has sections in several topic files: {', '.join(files)}")
    for eid in sorted(reg_ids - set(seen_in)):
        if seen_in or links:
            warnings.append(f"{eid} has no '## {eid} ...' section in any linked topic file")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print(f"{len(reg_ids)} experiments, {len(topics)} topics; "
          f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
