---
name: library-keeper
description: >
  Sub-skill of paper-library. Maintains the library: bootstrap a new one, adopt an existing
  bibliography, add papers (fetch, convert to markdown, write the note), fill summaries and
  compare fields, sort into topics, re-fetch revised papers, rebuild and check the index.
  Reached from the paper-library router, or by "add this paper", "import these", "update the
  library", "re-sort the topics", "fill in the notes".
---

# Library keeper

Formats: [../../references/format.md](../../references/format.md). `S` below is the
paper-library skill directory, `L` the library directory.

## Bootstrap

1. Ask for the research area, what is out of scope, and one or two anchor papers.
2. Write `L/LIBRARY.md` from [../../templates/library.md](../../templates/library.md).
   Start with three to seven topics; propose them, do not impose them.
3. Add the anchor papers (below), then offer to add their reference lists as the seed. List
   the candidates and let the user cut before fetching.

## Adopt an existing bibliography

For a folder that already has a `BIBLIOGRAPHY.md` in this layout, with or without `md/`:

```bash
python3 S/scripts/adopt.py <path/to/BIBLIOGRAPHY.md> L --recent-from <YYYY-MM-DD>
```

It writes one note per entry and a starter `LIBRARY.md`, and never overwrites a note. Copy the
`md/` folder into `L` yourself. Compare fields come out empty; fill them as below.

## Add a paper

1. **Deduplicate first.** Search `L/notes/` for the arXiv number, DOI or title. If it is
   there, stop and say so; if it is a new version, go to "Re-fetch".
2. **Assign the stem** and write `L/notes/<stem>.md` from the template with title, authors,
   date, source, verbatim abstract, topic and priority. Take metadata from the source page,
   never from memory.
3. **Convert:** `python3 S/scripts/convert.py L <stem>` (add `--from <file-or-url>` for a PDF
   in `inbox/` or a better URL). Then open `md/<stem>.md` and check it is the paper: the
   title matches, the sections are there, it does not stop early. A paywall or an abstract
   page is a failed conversion; set `Full text: none` and say so.
4. **Read the full text and fill the note:** Summary, then the five Compare fields. `Does not
   show` and `Open` matter most and are the easiest to skip; `Open` carries a line reference.
5. **Rebuild and check** (router, rule 5). Add a line to the Log in `LIBRARY.md`.

Several papers at once: do steps 1-3 for all, then fill notes one paper at a time. One
subagent per paper is fine for step 4; give it the format file and the one full text.

## Fill a backlog

`check_library.py` reports how many notes lack a Summary or Compare fields. Work through
starred papers first, then by topic. Do not fill Compare fields from the abstract alone: an
abstract says what a paper shows, almost never what it does not.

## Topics

- One primary topic per paper; use `Also` for the rest.
- Propose a split when a topic passes about 50 papers, and a merge when one stays under 5.
  Renaming a slug means editing every note that uses it: show the user the plan first.
- The Covers column says what goes in the topic and what goes in its neighbour. Update it
  whenever a filing decision was not obvious.

## Re-fetch

When a paper has a new version: re-run `convert.py`, re-read the changed sections, update
Summary and Compare, and note the version in the Log. The stem does not change.

## Discovery

Only on request, or as the Discovery section of `LIBRARY.md` says. Return candidates as a
list with one line each on why they fit the scope; the user chooses what is added.
