---
name: paper-library
description: Keep a local library of research papers as parsed markdown with one comparable note per paper and a generated topic index, and find research gaps in it on demand. Use when the user wants to add, import, re-fetch, summarise, sort or re-index papers in a local collection, asks "what's in my library on X", wants to build a paper database for a research area, or wants to check an idea for novelty, find gaps, or brainstorm directions against the papers they keep. Also when a project has a papers/ folder with BIBLIOGRAPHY.md or LIBRARY.md.
---

# Paper library

A local, private collection of papers that an agent can work on directly: every paper is one
full-text markdown file plus one short note with the same fields as every other note, and
the index is generated from the notes. Plain files and text search; no database.

This file is the router. The skill has two parts, each a sub-skill:

| Part | Use it to | Read |
|---|---|---|
| **Library keeper** | Start a library, add or import papers, convert them to markdown, write and fill notes, sort into topics, rebuild and check the index | [skills/library-keeper/SKILL.md](skills/library-keeper/SKILL.md) |
| **Gap finder** | Sharpen an idea, then find what the library has and has not done about it; or turn a set of topics into candidate ideas | [skills/gap-finder/SKILL.md](skills/gap-finder/SKILL.md) |

Both parts depend on the file layout and note format in
[references/format.md](references/format.md). Read it before writing any library file.

## Locating the library

Look for `LIBRARY.md` in `papers/`, then the project root, then where the user says. If there
is none, ask where it should live (default `papers/` in the current project) and bootstrap it
with the library keeper. A folder that has `BIBLIOGRAPHY.md` and `md/` but no `LIBRARY.md` is
a library made elsewhere: adopt it (library keeper, "Adopt").

## Rules that hold in both parts

1. **Notes are the source of truth.** `BIBLIOGRAPHY.md` and `COMPARE.md` are generated. Edit
   `notes/<stem>.md` or `LIBRARY.md`, then rebuild. Never edit a generated file.
2. **Claims about a paper come from its full text**, with the file and line. A summary or an
   abstract is a pointer to where to read, not evidence.
3. **Say what the library does not cover.** It holds what was added to it, up to the date it
   was last updated. "Not in the library" is never reported as "not done".
4. **Full texts stay private.** Do not publish or push `md/`; papers are other people's work.
5. **After any change to notes, topics or full texts**, run both scripts and fix what the
   checker reports:

```bash
python3 <skill-dir>/scripts/build_index.py <library-dir>
python3 <skill-dir>/scripts/check_library.py <library-dir>
```
