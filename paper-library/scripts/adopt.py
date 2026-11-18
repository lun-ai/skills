#!/usr/bin/env python3
"""Adopt an existing bibliography into a paper library by writing one note per entry.

Usage:  python3 adopt.py <BIBLIOGRAPHY.md> <library-dir> [--recent-from YYYY-MM-DD]

Reads a bibliography in the layout this skill generates (or the one it was modelled on):

    ## Topic name (N)
    ### [★ ][Title](url)
    Authors (Affiliation), DATE. Full text: `md/<stem>.md`
    **Abstract:**            (or any other bold label ending in a colon)
    > quoted text
    **Summary:** one or two sentences

Writes notes/<stem>.md for each entry that has none, and LIBRARY.md if it is missing. Existing
notes are never overwritten. The Compare section is left empty for the library-keeper to fill.
The source bibliography is not modified; copy any md/ folder into the library yourself.
"""
import datetime
import re
import sys
from pathlib import Path

HEAD = re.compile(r"^### (★ )?\[(.+)\]\((\S+)\)\s*$")
BYLINE = re.compile(r"^(?P<by>.*?),\s*(?P<date>\d{4}(?:-\d{2}){0,2})\.\s*(?:Full text:\s*`(?P<full>[^`]+)`)?")
SECTION = re.compile(r"^## (.+?)(?:\s*\(\d+\))?\s*$")
LABEL = re.compile(r"^\*\*(.+?):\*\*\s*(.*)$")
SKIP_SECTIONS = {"contents"}


def slugify(text, words=4):
    parts = re.findall(r"[a-z0-9]+", text.lower())
    stop = {"and", "of", "the", "a", "an", "in", "on", "for", "to", "with"}
    return "-".join([p for p in parts if p not in stop][:words]) or "unsorted"


def main():
    args = sys.argv[1:]
    recent = ""
    if "--recent-from" in args:
        i = args.index("--recent-from")
        recent = args[i + 1]
        del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    bib, root = Path(args[0]), Path(args[1])
    lines = bib.read_text(encoding="utf-8").splitlines()
    name = next((l[2:].strip() for l in lines if l.startswith("# ")), "Paper library")
    name = re.sub(r"^Bibliography:\s*", "", name)

    topics, entries, cur_topic, cur = [], [], None, None
    untopical = set()

    def close():
        nonlocal cur
        if cur:
            entries.append(cur)
        cur = None

    mode = None
    for line in lines:
        s = SECTION.match(line)
        if s and not line.startswith("### "):
            close()
            title = s.group(1).strip()
            if title.lower() in SKIP_SECTIONS:
                cur_topic = None
                continue
            slug = slugify(title)
            # a short lead-in section (e.g. required reading) repeats entries filed elsewhere
            cur_topic = slug
            topics.append((slug, title))
            continue
        h = HEAD.match(line)
        if h:
            close()
            cur = {"star": bool(h.group(1)), "title": h.group(2), "url": h.group(3), "topic": cur_topic,
                   "by": "", "date": "", "full": "", "abstract": [], "abstract_label": "", "summary": ""}
            mode = "byline"
            continue
        if line.startswith("### "):      # e.g. "Earlier work" divider
            close()
            continue
        if cur is None:
            continue
        if mode == "byline" and line.strip():
            b = BYLINE.match(line.strip())
            if b:
                cur["by"], cur["date"], cur["full"] = b.group("by").strip(), b.group("date"), b.group("full") or ""
            else:
                cur["by"] = line.strip()
            mode = None
            continue
        lab = LABEL.match(line.strip())
        if lab:
            if lab.group(1).strip().lower() == "summary":
                cur["summary"], mode = lab.group(2).strip(), "summary"
            else:
                cur["abstract_label"], mode = lab.group(1).strip(), "abstract"
            continue
        if mode == "abstract" and line.startswith(">"):
            cur["abstract"].append(line[1:].strip() if line[1:].strip() else "")
        elif mode == "summary" and line.strip():
            cur["summary"] += " " + line.strip()
    close()

    (root / "notes").mkdir(parents=True, exist_ok=True)
    seen, written, kept, dup = {}, 0, 0, 0
    for e in entries:
        stem = Path(e["full"]).stem if e["full"] else f"{slugify(e['by'].split(',')[0].split()[-1] if e['by'] else 'anon', 1)}_{slugify(e['title'], 3)}_{e['date'] or 'undated'}"
        if stem in seen:
            dup += 1
            # keep the later, topical filing; remember the star
            seen[stem]["star"] = seen[stem]["star"] or e["star"]
            seen[stem]["topic"] = e["topic"]
            continue
        e["stem"] = stem
        seen[stem] = e
    used_topics = {e["topic"] for e in seen.values()}
    for stem, e in seen.items():
        path = root / "notes" / f"{stem}.md"
        if path.exists():
            kept += 1
            continue
        by, aff = e["by"], ""
        m = re.match(r"^(.*)\s\(([^()]+)\)$", by)
        if m:
            by, aff = m.group(1).strip(), m.group(2).strip()
        out = [f"# {e['title']}", "", f"- **Authors:** {by}"]
        if aff:
            out.append(f"- **Affiliation:** {aff}")
        out += [f"- **Date:** {e['date']}", f"- **Source:** {e['url']}", f"- **Topic:** {e['topic'] or 'unsorted'}",
                f"- **Priority:** {'star' if e['star'] else 'normal'}",
                f"- **Full text:** {'`' + e['full'] + '`' if e['full'] else 'none'}",
                f"- **Fetched:** adopted {datetime.date.today().isoformat()} from {bib.name}", "", "## Abstract", ""]
        if e["abstract_label"] and e["abstract_label"].lower() != "abstract":
            out += [f"*{e['abstract_label']}*", ""]
        out += e["abstract"] + ["", "## Summary", "", e["summary"].strip(), "", "## Compare", "",
                                "- **System:** ", "- **Method:** ", "- **Shows:** ", "- **Does not show:** ", "- **Open:** ", ""]
        path.write_text("\n".join(out), encoding="utf-8")
        written += 1

    cfg = root / "LIBRARY.md"
    if not cfg.exists():
        rows = [f"| `{s}` | {t} | |" for s, t in topics if s in used_topics]
        if any((e["topic"] or "unsorted") == "unsorted" for e in seen.values()):
            rows.append("| `unsorted` | Unsorted | Not yet filed under a topic |")
        cfg.write_text("\n".join([f"# {name}", "", "## Scope", "", "_Adopted library: state what belongs here and what does not._", "",
                                  "## Seed", "", f"Adopted from `{bib}`.", "", "## Settings", "", f"- **Recent from:** {recent}", "",
                                  "## Topics", "", "| Slug | Topic | Covers |", "|---|---|---|"] + rows +
                                 ["", "## Discovery", "", "_How new papers arrive._", "", "## Log", "", "| Date | Change |", "|---|---|",
                                  f"| {datetime.date.today().isoformat()} | Adopted {written} entries from {bib.name} |", ""]), encoding="utf-8")
    print(f"{len(entries)} entries read, {dup} repeated; {written} notes written, {kept} existing notes kept; topics: {len(used_topics)}")


if __name__ == "__main__":
    main()
