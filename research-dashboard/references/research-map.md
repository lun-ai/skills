# Research map and global experiment numbering

The research map is the first section of the dashboard, placed above the experiment list. It
answers the questions the experiment list cannot: what exists, when each piece appeared, what
each experiment was built from, and how one topic's work feeds another's. Think of a
feature map in software development, applied to research: every topic, every implementation
and every experiment is a node, with its timestamp and attributes.

## One numbering system: `E###`

**Every experiment in the effort gets one global number, `E001`, `E002`, ..., from a single
counter shared by all topics.** That number is the experiment's identity everywhere: the
dashboard, its topic file, chat, commit messages, folder names, figure captions. "E007"
means one thing across the whole effort, so nobody needs to know which topic it belongs to
before they can find it.

Rules:

- **Assign at registration, not at completion.** A number is taken when the experiment is
  first written down (status `Planned`), before any design work. That way a planned
  experiment can be cited from the moment it exists.
- **Never reuse, never renumber.** An abandoned experiment keeps its number with status
  `Abandoned` and stays on the map. Gaps are fine; a renumbered experiment breaks every old
  reference to it.
- **Reserve before you build.** Re-read the dashboard, take the `Next experiment number`,
  write the registry row and bump the counter, all before any other work. Two parallel
  sessions that skip this step will both claim the same number. `scripts/check_map.py`
  flags duplicates.
- **Format.** Three digits, zero-padded (`E007`); widen to four only once you pass `E999`.
  If the project already numbers experiment folders (`experiments/007_signor_full/`), the
  folder number *is* the experiment number. Keep the folders and write `E007` in documents.
  If a folder exists, put the number first in its name (`NNN_<descriptive-slug>`).

**What earns a number.** Anything work-loop step 1 counts as a *new experiment*: a test whose
design has not yet been agreed with the user. That covers a new question, dataset, metric,
grading scheme, confound-isolating comparison, or offline re-analysis whose number the user
might act on. **What does not** earn one: arms, seeds, reruns, resumes and bug-fix restarts
of an agreed design. These live *inside* their experiment and are cited as
`E007 / gold-abstracts-in-context` plus job IDs. A follow-up that changes the design gets a
new number and a `from:` link to its parent (see Lineage below). It never gets a suffix like
`E007b`.

**Topics and implementations are named, not numbered.** Only experiments are counted, so
there is exactly one counter to keep honest. Topics and implementations get short slug IDs
for the map (`topic:signor`, `impl:evidence-tree`) and a descriptive name.

`E###` is the one bare symbol a document may use (see [naming.md](naming.md)), because the
registry defines every number in one place. On first mention in a reply, pair it with its
subject: "E004, the first-principles SIGNOR tree".

## What the map section contains

Three parts, in this order, under `## Research map` (full skeleton in
[../templates/dashboard.md](../templates/dashboard.md)):

1. **Counter line.** `Next experiment number: **E009**` and the date the map was last updated.
2. **Map** (`### Map`): a `Format:` line and a link to the map page (or, in the ASCII
   format, the map itself). The whole section is written by `scripts/render_map.py`, never
   by hand.
3. **Registry** (`### Registry`): one row per node, with timestamps and attributes. The map
   is generated *from* this table, so the table is the only place map facts are edited.

### Division of labour with the experiment list

The registry records **identity and provenance**: what an experiment is, when it appeared, what
it was built from, and what it runs on. The experiment list (`## Experiments`, directly below
the map) records **progress**: the question, its status, its effort and its one-line result.
No fact is kept in both. The map page reads status from the experiment list, so it can be
read without the dashboard; `check_map.py` verifies that the page was rendered from the
current registry and statuses.

## The registry

```markdown
### Registry

| ID | Kind | Name | Topic | Created | Updated | Attributes | Links |
|---|---|---|---|---|---|---|---|
| topic:signor | topic | SIGNOR direct-regulation claims | — | 2026-10-20 | 2026-10-22 | data: ProClaim-eval SIGNOR (101 claims), signor_full (400) | [topic file](signor.md) |
| impl:evidence-tree | implementation | Hand-built JEV evidence trees (v-series) | — | 2026-10-20 | 2026-10-22 | code: experiments/001_*/trees.py; current best v6 | [README](experiments/001_signor_evidence_tree/README.md) |
| E007 | experiment | Trees trained on claims from the full SIGNOR database | topic:signor | 2026-10-22 | 2026-10-22 | data: signor_full 400 claims, 5-fold CV · model: JEV typesafe/jev-1.14 · uses: impl:evidence-tree, impl:first-principles-tree · from: E001, E004 · jobs: — | [E007](signor.md#e007) |
```

- **Kind** is `topic`, `implementation` or `experiment`.
- **Topic** is filled for experiments only. An experiment that spans topics lists its main
  topic here and the rest under `also:` in Attributes.
- **Created** is the registration date. **Updated** is the date of the last change to the
  node's facts: a new arm, a new result, a status change. Use absolute dates (`YYYY-MM-DD`),
  never "yesterday".
- **Attributes** are `key: value` pairs separated by ` · `. Use these keys where they apply,
  in this order, and add others only when a reader would filter on them:
  `data` (dataset and split, with n), `model` (backbone or backend), `uses` (implementation
  IDs), `from` (parent experiment IDs, each optionally followed by what changed, in two to
  five words: `from: E001 (reuses tree v6), E004`), `jobs` (approved job IDs only, see
  [background-jobs.md](background-jobs.md)), `cost`, `owner` (only when work streams are
  split between people).
- **Links**: the experiment's stable anchor in its topic file (`topic.md#e007`), its HTML
  report page if it has one (`pages/e007-signor-full.html`), the code folder, or the
  implementation's source file.
- Keep `,`, `:`, `|`, brackets and `*` out of Names: the map page uses Names as node text, and
  `render_map.py` strips those characters.

## The map page

**Default format: `answer-me-with-html`.** `scripts/render_map.py` turns the registry and the
experiment list into a draft (`pages/research-map.am.md`), renders it into
`pages/research-map.html` with the bundled CLI of the `answer-me-with-html` skill, and rewrites
the `### Map` section to link both:

```markdown
### Map

Format: answer-me-with-html · open the map: [pages/research-map.html](pages/research-map.html) · draft: [pages/research-map.am.md](pages/research-map.am.md)

Generated from the registry by `scripts/render_map.py`; do not edit the page or the draft by hand.
```

```bash
python3 <skill-dir>/scripts/render_map.py path/to/DASHBOARD.md              # keeps the declared format
python3 <skill-dir>/scripts/render_map.py path/to/DASHBOARD.md --format ascii
python3 <skill-dir>/scripts/render_map.py path/to/DASHBOARD.md --hide-uses  # fewer crossing arrows
```

The page has three panels:

- **A Map** is a left-to-right flow diagram. Each topic is a box holding its experiments, and
  the implementations sit in their own box. A solid arrow runs from each implementation to
  every experiment that uses it, and a dashed, labelled arrow marks each `from:` link. Each
  experiment node reads `E### · <name> (<status>)`. Open experiments (planned, designing,
  running) are highlighted.
- **B Timeline** lists every experiment by creation date, with its topic and status, and
  highlights the open ones.
- **C Registry** repeats the registry table with status badges (✓ done, ! running,
  ✗ abandoned).

The page header carries `map-source: <hash>`, a hash of the counter, the registry and the
statuses. `check_map.py` recomputes it, so it reports a page that was not re-rendered after a
change as stale. If the solid arrows cross so much that the map is hard to read, render with
`--hide-uses`. The registry's `uses:` attribute still records them, and the dashed lineage
arrows carry more information.

**Where pages live.** Write the map page and every other page made for the effort with `-o`
into `pages/` next to the dashboard, and commit them with it. Never link a page in the CLI's
default location (`~/.answer-me-with-html/pages`): it is outside the repository, other
collaborators cannot open it, and `am clean` deletes it. Name per-experiment pages
`pages/e###-<slug>.html` (see [reporting.md](reporting.md)), and link them from the
experiment's topic-file section and from its registry Links cell. `check_map.py` reports any
linked `.html` file that does not exist.

The CLI needs Node.js 20 or newer. If `node` is missing or older, follow the
`answer-me-with-html` skill's instructions, which ask the user before installing anything.
Otherwise use the ASCII format for that session and say so.

**Other formats.** Choose one with `--format`; later runs keep it:

- **`ascii`** writes the map as a ```` ```text ```` tree directly in the Map section. Topics are
  branches, experiments are leaves, and each leaf shows its `uses:` and `from:` inline. Use it
  when the user reads the dashboard in a terminal or has no Node.js.
- **`excalidraw`** links `pages/research-map.excalidraw` from the Map section. Draw the file
  with the `excalidraw-diagram` skill from the registry, for presentations and meetings.
  `render_map.py` writes only the link, so redraw the file after every registry change.
  `check_map.py` warns when an experiment is missing from the drawing.

## When to update the map

Change the registry and the experiment list in the same edit as the underlying fact, then run
`render_map.py` and `check_map.py`:

| Event | Registry | Experiment list | Counter |
|---|---|---|---|
| New topic | add `topic:` row | — | — |
| New implementation, or one is substantially rewritten | add or update `impl:` row | — | — |
| Experiment registered | add `E###` row (Created = today), with `uses:` and `from:` | add row, status Planned | bump |
| Design agreed, run started, finished, abandoned | bump Updated | change Status | — |
| New arm or rerun inside an experiment | bump Updated; add approved job IDs | — | — |
| New HTML page for an experiment | add it to Links | — | — |
| Experiment moved to another topic | change Topic | change Topic | — |

```bash
python3 <skill-dir>/scripts/render_map.py path/to/DASHBOARD.md
python3 <skill-dir>/scripts/check_map.py path/to/DASHBOARD.md
```

`check_map.py` reports:

- duplicate or missing numbers, and a counter at or below an existing number;
- experiments in the registry but not in the list, or the reverse;
- `uses:` or `from:` references to unregistered IDs;
- a stale or missing map page, and linked HTML pages that do not exist;
- topic-file headings that name an unregistered number.

Dashboards made before global numbering are left as they are. Keep working in their existing
scheme. The numbering and the map apply to dashboards created from these templates.
