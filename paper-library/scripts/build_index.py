#!/usr/bin/env python3
"""Rebuild BIBLIOGRAPHY.md and COMPARE.md from notes/ and LIBRARY.md.

Usage:  python3 build_index.py <library-dir>

BIBLIOGRAPHY.md  one entry per paper, grouped by topic, recent before earlier, starred first.
COMPARE.md       one table per topic: system, method, shows, does not show, open.
Both are generated. Edit notes/<stem>.md or LIBRARY.md and rebuild; never edit them by hand.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paperlib import COMPARE_FIELDS, GENERATED, is_recent, load_library, oneline, sort_key  # noqa: E402


def groups(lib):
    """Yield (slug, name, recent_notes, earlier_notes) in LIBRARY.md order, then unknown topics."""
    known = [s for s, _, _ in lib.topics]
    extra = sorted({n.topic or "unsorted" for n in lib.notes.values()} - set(known))
    for slug in known + extra:
        notes = sorted((n for n in lib.notes.values() if (n.topic or "unsorted") == slug), key=sort_key)
        if notes or slug in known:
            yield slug, lib.topic_name(slug), [n for n in notes if is_recent(lib, n)], [n for n in notes if not is_recent(lib, n)]


def stars(notes):
    return sum(1 for n in notes if n.starred)


def entry(n):
    star = "★ " if n.starred else ""
    src = n.fields.get("Source", "")
    head = f"### {star}[{n.title}]({src})" if src else f"### {star}{n.title}"
    authors = n.fields.get("Authors", "")
    aff = n.fields.get("Affiliation", "")
    by = authors + (f" ({aff})" if aff else "")
    full = n.fields.get("Full text", "none")
    where = f"Full text: `{full}`" if full and full != "none" else "Full text: none"
    out = [head, "", f"{by}, {n.date}. {where} · Notes: `notes/{n.stem}.md`", ""]
    abstract = n.sections.get("Abstract", "").strip()
    if abstract:
        out += ["**Abstract:**", ""] + [("> " + l) if l.strip() else ">" for l in abstract.splitlines()] + [""]
    summary = oneline(n.sections.get("Summary", "")).replace("\\|", "|")
    out += [f"**Summary:** {summary or '_not yet summarised_'}", ""]
    return out


def render_bibliography(lib):
    gs = list(groups(lib))
    out = [GENERATED, "", f"# Bibliography: {lib.name}", "", f"{len(lib.notes)} papers. Comparison tables: [COMPARE.md](COMPARE.md). Scope and topics: [LIBRARY.md](LIBRARY.md).", "", "## Contents", ""]
    for slug, name, rec, ear in gs:
        total = len(rec) + len(ear)
        detail = f"{len(rec)} recent, {stars(rec)} ★; {len(ear)} earlier, {stars(ear)} ★" if lib.recent_from else f"{stars(rec)} ★"
        out.append(f"- [{name}](#{slug}) ({total}: {detail})")
    out.append("")
    for slug, name, rec, ear in gs:
        out += [f'<a id="{slug}"></a>', "", f"## {name} ({len(rec) + len(ear)})", ""]
        for n in rec:
            out += entry(n)
        if ear:
            out += [f"### Earlier work (before {lib.recent_from})", ""]
            for n in ear:
                out += entry(n)
    return "\n".join(out).rstrip() + "\n"


def render_compare(lib):
    out = [GENERATED, "", f"# Comparison tables: {lib.name}", "",
           "One row per paper, from the Compare section of its note. An empty cell means the note has not been filled in, not that the paper has nothing to say.", ""]
    for slug, name, rec, ear in groups(lib):
        notes = rec + ear
        if not notes:
            continue
        out += [f"## {name} ({len(notes)})", "", "| Paper | Date | " + " | ".join(COMPARE_FIELDS) + " |", "|---|---|" + "---|" * len(COMPARE_FIELDS)]
        for n in notes:
            star = "★ " if n.starred else ""
            cells = [oneline(n.compare.get(f, "")) for f in COMPARE_FIELDS]
            out.append(f"| {star}[{n.stem}](notes/{n.stem}.md) | {n.date} | " + " | ".join(cells) + " |")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    lib = load_library(Path(sys.argv[1]))
    for p in lib.problems:
        sys.exit(p)
    (lib.root / "BIBLIOGRAPHY.md").write_text(render_bibliography(lib), encoding="utf-8")
    (lib.root / "COMPARE.md").write_text(render_compare(lib), encoding="utf-8")
    print(f"built BIBLIOGRAPHY.md and COMPARE.md: {len(lib.notes)} papers, {len(lib.topics)} topics")


if __name__ == "__main__":
    main()
