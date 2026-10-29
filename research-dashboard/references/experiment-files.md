# Experiment files: setup, results, interpretation

Every registered experiment gets its own folder beside the dashboard, named by its number
alone, holding up to four files:

```
e007/
  setup.md            ← what was run, as run, with a source for every value
  results.md          ← every run's numbers, each table with the script that produced it
  interpretation.md   ← only once the user asks for interpretation
  checks.md           ← log of fact checks (written by the dashboard-checker sub-skill)
```

The folder is named `e###` with no slug, like the `<a id="e###">` anchors, so renaming the
experiment never breaks a link. If the project also has a code folder
(`experiments/007_signor_full/`), that folder holds code and outputs; `e007/` holds the
documents. Link one from the other.

**Why three files.** A paper, a report or a blog post must be able to rebuild the methods
section from `setup.md` alone, the numbers from `results.md` alone, and the claims from
`interpretation.md` alone, without picking facts out of a topic file where setup, numbers and
commentary from several runs are interleaved. Each file has one kind of content, so each can
be checked on its own, and a write-up that cites `e007/setup.md` cites one place.

## Where each fact lives

| Fact | File |
|---|---|
| Question, hypothesis, lineage, what is reused | `setup.md` |
| Data, models, decoding, prompts, seeds, hardware, budgets | `setup.md` |
| Arms (the glossary every later file refers to), what is held fixed | `setup.md` |
| Procedure, metric and derived-quantity definitions, decision rules | `setup.md` |
| What the test cannot show (written before the results) | `setup.md` |
| Implementation plan, entry points, the command that reproduces a run | `setup.md` |
| Anything that changed after the design was agreed | `setup.md`, Changes during execution |
| Per-run numbers, which run is current, which were superseded | `results.md` |
| Execution notes (rate limits, bugs, lost outputs, environment quirks) | `results.md` |
| Limitations and what was not done | `results.md` |
| Why it came out that way, what it implies | `interpretation.md` |
| Why the question was asked, how it relates to the topic's other experiments | the topic file's section |
| Status, effort, one-line result | the dashboard's experiment list |
| Identity, dates, attributes, links to all of the above | the dashboard's registry |

Each fact is written once. Other files point at it.

## setup.md

Template: [../templates/experiment-setup.md](../templates/experiment-setup.md).

- **It describes the experiment as run, not as planned.** Write it from the agreed setting
  block at design time (work loop step 1). When something changes during execution (a
  hyperparameter, a filter, a dropped arm, a new arm), change the value in place *and* add a
  dated row to **Changes during execution** naming the old value, the new value, why, and which
  runs each value applies to. A write-up then describes what was actually run, and the design
  history is still recoverable from the log.
- **Every concrete value has a source.** Tables of parameters, populations and metrics carry a
  `Source` column. A source is one of:
  - a repository path, optionally with a line, flag or commit: `configs/qwen.yaml:12`,
    `scripts/run.py --temperature`, `prompts/system.txt@a1b2c3d`;
  - a run artifact: a job ID, a log path, a saved config in an output folder;
  - a decision: `decision: grilling 2026-10-27`, for a design choice that does not live in
    code (the checker then verifies the code implements it);
  - a paper or external release: `Menon et al. 2025, Sec. 3.2`.
  A value with no source is reported by the checker as unverifiable.
- **Values a write-up will quote must be exact.** Model IDs with revision, decoding
  parameters, n per population, seed list, number of repeats, how the standard error is
  computed. "~10 runs" or "default settings" cannot be rebuilt into a methods section.
- **Shared setups.** When two experiments share most of a setup (same jobs, same environment),
  the second may open a section with `Inherits: [E002 setup § Environment](../e002/setup.md#environment)`
  and list only its differences. Never copy the shared text: two copies drift.
- **Arms are defined here once.** `results.md`, `interpretation.md`, pages and write-ups name
  arms by the descriptive names in this table and do not redefine them. An arm created
  mid-investigation is added here before anything is reported about it.

## results.md

Template: [../templates/experiment-results.md](../templates/experiment-results.md).

- **It opens by pointing at `setup.md`**, not by restating it. Each run section says only what
  differs from the setup (and cites the Changes during execution row).
- **One section per run** (smoke test, full run, rerun, re-analysis), in date order, headed
  with its descriptive name, date, job IDs and review state: `reviewed by the user
  <date>`, `not yet reviewed`, or `superseded by <run name>`. Superseded runs stay, marked,
  so a write-up never quotes them by accident and the history is not lost.
- **A Current results section at the top** names which run(s) its table comes from. The
  dashboard's one-line result compresses this table and nothing else.
- **Every table is followed by a `Produced by:` line**: the script or notebook, the output file
  it read or wrote, and the commit. This is what lets a number be recomputed.
- **Facts only.** No causal language ("because", "suggests", "likely driven by"). Limitations
  and what was not done are facts about the measurement, so they live here and are always
  written.
- **A large file stays one file** while it is readable. When per-item tables, confusion
  matrices or per-class breakdowns make it long, put them in another file *inside the same
  folder* (`e007/per-item.md`) linked from the run's section. Say in chat that you did it; it
  does not change the structure the user navigates, so it needs no prior agreement.

## interpretation.md

Template: [../templates/experiment-interpretation.md](../templates/experiment-interpretation.md).

- **Created only when the user asks for interpretation** (see
  [writing-discipline.md](writing-discipline.md)). Its absence is the correct state otherwise.
- It records **when and what was asked**, and which state of `results.md` it rests on.
- **Each claim cites the result it rests on** with a link into `results.md`. A number quoted in
  a claim must match the number in `results.md`.
- When a result it rests on is superseded or corrected, the claim is not silently edited: move
  it to **Retracted or superseded claims** with the date and the reason, then write the new
  claim if the user still wants one.

## Links

- The registry's Links cell for the experiment links its topic section and every file that
  exists: `[topic](goal_drift.md#e002) · [setup](e002/setup.md) · [results](e002/results.md) · [interpretation](e002/interpretation.md)`.
- The topic-file section carries the same links on its first line.
- Each file opens with links to its siblings, its topic section and the dashboard.
- HTML pages for the experiment stay in `pages/`; link them from `results.md` with
  `../pages/e007-<slug>.html`.

## When each file must exist

| Status | Required |
|---|---|
| Planned | nothing beyond the registry row and the topic-file section |
| Designing | `setup.md` (filled in as grilling settles each part) |
| Running | `setup.md` complete, `results.md` with at least the run section and its job IDs |
| Done | both complete, a Current results section, and a fact check in `checks.md` dated on or after the registry's Updated date |
| Abandoned | whatever exists; `results.md` says why it was abandoned |

`scripts/check_experiments.py` enforces this table and the structural rules above.

## Dashboards that keep setup and results in topic files

Dashboards created before this layout keep everything in the topic-file sections (`Setup and
arms`, `Results`, `Takeaways`, optional `<topic>_e###_detail.md`). Moving them is a structural
change, so **propose it, do not do it** ([judgment-calls.md](judgment-calls.md)). Once agreed,
per experiment:

1. Create `e###/` and move the text verbatim: Setup and arms and Implementation plan to
   `setup.md`; Results, Infra notes and Limitations to `results.md`; Takeaways to
   `interpretation.md`; the detail file's content to `results.md` or a sibling file in the
   folder.
2. Reshape only what the templates require (tables with a Source column, one section per run
   with its review state, `Produced by:` lines). Leave a Source cell as `?` where you do not
   know it; do not guess.
3. Leave the topic-file section with its anchor, heading, links line and Context / motivation.
4. Update the registry Links cell, re-render the map, and run both check scripts.
5. Run the dashboard-checker on the migrated experiments. The `?` sources come back as
   unverifiable; filling them in is the first fact check.
