#!/usr/bin/env python3
"""Check a paper library for consistency.

Usage:  python3 check_library.py <library-dir>

Errors (exit 1): missing required fields, unknown topic, bad stem or date, a note whose full
text is missing, a full text with no note, duplicate sources, stale generated files.
Warnings: notes with no summary or an unfilled Compare section, full texts that look too short.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paperlib import COMPARE_FIELDS, DATE, REQUIRED_FIELDS, STEM, load_library  # noqa: E402
from build_index import render_bibliography, render_compare  # noqa: E402

ARXIV = re.compile(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    lib = load_library(Path(sys.argv[1]))
    errors, warnings = list(lib.problems), []
    slugs = {s for s, _, _ in lib.topics}
    if not lib.topics:
        errors.append("LIBRARY.md has no rows in its Topics table")
    by_source = defaultdict(list)
    unsummarised = uncompared = 0
    for stem, n in lib.notes.items():
        where = f"notes/{stem}.md"
        if not STEM.match(stem):
            errors.append(f"{where}: stem is not firstauthor_short-slug_identifier (lowercase, digits, hyphens)")
        if not n.title:
            errors.append(f"{where}: no '# Title' line")
        for f in REQUIRED_FIELDS:
            if not n.fields.get(f):
                errors.append(f"{where}: missing field '{f}'")
        if n.date and not DATE.match(n.date):
            errors.append(f"{where}: Date '{n.date}' is not YYYY, YYYY-MM or YYYY-MM-DD")
        if n.topic and n.topic not in slugs:
            errors.append(f"{where}: Topic '{n.topic}' is not a slug in LIBRARY.md")
        if n.fields.get("Priority", "").lower() not in ("star", "normal", ""):
            errors.append(f"{where}: Priority must be 'star' or 'normal'")
        full = n.fields.get("Full text", "")
        if full and full != "none":
            fp = lib.root / full.strip("`")
            if not fp.exists():
                errors.append(f"{where}: Full text '{full}' does not exist")
            elif len(fp.read_text(encoding="utf-8", errors="replace").split()) < 500:
                warnings.append(f"{full}: under 500 words; the conversion may have failed")
        src = n.fields.get("Source", "")
        m = ARXIV.search(src)
        by_source[m.group(1) if m else src.rstrip("/").lower()].append(stem)
        if not n.sections.get("Summary", "").strip():
            unsummarised += 1
        if not all(n.compare.get(f) for f in COMPARE_FIELDS):
            uncompared += 1
    for key, stems in by_source.items():
        if key and len(stems) > 1:
            errors.append(f"duplicate source {key}: {', '.join(stems)}")
    md = lib.root / "md"
    if md.is_dir():
        for p in sorted(md.glob("*.md")):
            if p.stem not in lib.notes:
                errors.append(f"md/{p.name}: full text with no note")
    if not lib.problems:
        for name, render in (("BIBLIOGRAPHY.md", render_bibliography), ("COMPARE.md", render_compare)):
            f = lib.root / name
            if not f.exists() or f.read_text(encoding="utf-8") != render(lib):
                errors.append(f"{name} is missing or stale: run build_index.py")
    if unsummarised:
        warnings.append(f"{unsummarised} note(s) have no Summary")
    if uncompared:
        warnings.append(f"{uncompared} note(s) have an incomplete Compare section; gap finding is weaker for them")
    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("warning", w)
    with_text = sum(1 for n in lib.notes.values() if n.fields.get("Full text", "none") != "none")
    print(f"{len(lib.notes)} papers ({with_text} with full text), {len(lib.topics)} topics; {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
