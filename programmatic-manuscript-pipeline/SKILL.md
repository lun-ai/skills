---
name: programmatic-manuscript-pipeline
description: >
  Programmatic research manuscript pipeline — automates figure/table regeneration and
  number traceability for LaTeX papers. Use when the user wants to: set up a reproducible
  paper build system, add or update figures/tables/numbers programmatically, wire data
  artifacts to LaTeX, create a "make paper" pipeline, connect experiment results to
  manuscript prose, ensure all numbers trace to source data, regenerate outputs from
  upstream changes, or automate any data-to-PDF paper workflow. Trigger on "update the
  paper with new results", "regenerate figures", "add a paper number", "wire this data
  to the manuscript", "make the paper reproducible", or structuring a paper repo so
  changing one data file updates everything downstream. Covers the full pipeline: raw
  data → curated artifacts → figures → tables → number macros → PDF. Does NOT cover
  prose drafting — use academic-paper-writer for that.
---

# Manuscript Pipeline

A skill for building and maintaining programmatic, reproducible research manuscript
pipelines. The core idea: every number, figure, and table in the paper is generated from
code that reads curated data artifacts, and the entire manuscript can be regenerated
end-to-end from a single command.

This skill is about **infrastructure**, not prose. It covers repository layout, data flow
conventions, figure/table/number wiring, Makefile orchestration, and the iterative
update cycle. For help writing actual paper text, prompt the user to use a writing skill or use an appropriate writing skill from the skill repo.

---

## When To Use This Skill

Before starting any task, determine what the user needs:

- **Scaffolding a new paper repo** → read `references/repo-scaffold.md`, then follow it
- **Adding/modifying/deleting a figure** → read `references/figure-rules.md`
- **Adding/modifying/deleting a table** → read `references/table-rules.md`
- **Adding/modifying/deleting a paper number** → read `references/number-rules.md`
- **Updating the pipeline after new results** → read `references/update-cycle.md`
- **Understanding the data flow** → read the Architecture section below
- **Final pre-submission audit (typos, numerical claims, cross-references)** → after `make paper-check` passes, use the `paper-manuscript` skill (see Complementary Skills below)

---

## Architecture: The Unidirectional Data Flow

The single most important principle is **unidirectional data flow**. Data moves in one
direction only, from raw inputs to final PDF, and no downstream layer feeds back upstream.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Layer 1: RAW DATA                                                     │
│  Experiment outputs, external datasets, API dumps                      │
│  Location: data/ or external storage                                   │
└─────────────┬───────────────────────────────────────────────────────────┘
              │  curate / extract / validate
              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Layer 2: CURATED ARTIFACTS                                            │
│  Cleaned, validated, canonical datasets ready for paper use            │
│  Location: paper_artifacts/derived/                                    │
└──────┬──────────────┬──────────────┬────────────────────────────────────┘
       │              │              │
       ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────────┐
│ Figures    │ │ Tables     │ │ Numbers        │
│ make.py   │ │ make.py    │ │ collectors     │
│ → PDF/SVG │ │ → .tex     │ │ → macros .tex  │
└─────┬──────┘ └─────┬──────┘ └───────┬────────┘
      │              │                │
      ▼              ▼                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Layer 3: MANUSCRIPT                                                   │
│  main.tex consumes only: figures/outputs/, tables/outputs/,            │
│  numbers_source/paper_numbers.tex, bibliography files                  │
└─────────────┬───────────────────────────────────────────────────────────┘
              │  pdflatex + bibtex
              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Layer 4: FINAL PDF                                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

**Never reverse the flow.** Figures must not read from table outputs. Tables must not
read from publishing exports. Number collectors must not read from figure outputs.
Analysis code must not depend on the paper directory.

---

## Repository Structure

Read `references/repo-scaffold.md` for the full scaffolding guide. Summary:

```
project-root/
├── Makefile                         # Orchestrates all paper targets
├── paper/
│   ├── main.tex                     # Generated readable source (do not edit)
│   ├── main_development.tex         # Editable manuscript source
│   ├── references.bib               # Bibliography
│   ├── figures/
│   │   ├── fig_<name>/make.py       # One module per main figure
│   │   ├── supp/supp_fig_<name>/    # Supplementary figures
│   │   ├── analyses/<name>/         # Analysis figures
│   │   ├── shared/                  # Plotting style, output paths
│   │   ├── outputs/                 # Generated visual assets (PDF/SVG/PNG)
│   │   └── tests/                   # Figure boundary and data tests
│   ├── tables/
│   │   ├── supp/supp_table_<name>/make.py
│   │   ├── shared/                  # Table output paths
│   │   ├── outputs/                 # Generated .tex snippets
│   │   └── tests/
│   ├── numbers_source/
│   │   ├── paper_numbers.tex        # LaTeX macros consumed by main.tex
│   │   ├── paper_numbers.tsv        # Human-readable audit ledger
│   │   └── paper_numbers.json       # Machine-readable ledger
│   ├── shared/                      # Non-visual loaders, paths, metadata
│   ├── publishing/                  # TSV export discovery and writing
│   └── publishing_artifacts/        # Final editor-facing TSV exports
├── paper_artifacts/
│   ├── inputs/                      # Canonical external inputs
│   ├── derived/                     # Curated datasets for paper use
│   └── numbers/
│       ├── build.py                 # Number builder entry point
│       ├── registry.py              # Group registration
│       └── groups/                  # One module per number family
└── data/                            # Raw experiment outputs
```

---

## The Three Artifact Types

Every claim in the manuscript traces to one of three programmatic artifact types. Each
has its own rules file with add/modify/delete procedures. Read the relevant one before
any operation.

### 1. Figures → `references/figure-rules.md`

- Source code in `figures/fig_<name>/make.py`
- Reads curated data from `paper_artifacts/`
- Writes visual outputs (PDF, SVG, PNG) to `figures/outputs/<figure_id>/`
- Optionally exposes `publishing_exports(context)` for editor TSV handoff
- Referenced in manuscript via `\includegraphics{figures/outputs/...}`

### 2. Tables → `references/table-rules.md`

- Source code in `tables/supp/supp_table_<name>/make.py`
- Reads curated data from `paper_artifacts/`
- Writes `.tex` snippets to `tables/outputs/`
- Numeric cells use `\PaperNumber{MacroName}`, never hard-coded values
- Referenced in manuscript via `\input{tables/outputs/...}`

### 3. Numbers → `references/number-rules.md`

- Definitions in `paper_artifacts/numbers/groups/`
- Built by `paper_artifacts/numbers/build.py`
- Output to `numbers_source/paper_numbers.tex` (LaTeX macros)
- Used in manuscript and table snippets as `\PaperNumber{MacroName}`
- Every number carries full provenance: source dataset, filter, denominator, arithmetic

---

## Makefile Targets

The Makefile is the single entry point for all regeneration. Targets run in dependency
order and can be scoped to individual artifacts.

```makefile
# Full pipeline — curate, render, compile, check
make paper-reproduce

# Individual stages
make paper-artifacts                          # Curate raw → derived datasets
make paper-artifacts DATASET=<name>           # One dataset only

make paper-figures                            # All figures
make paper-figures FIGURE=<name>              # One figure only

make paper-tables                             # All table snippets
make paper-tables TABLE=<name>                # One table only

make paper-numbers                            # Regenerate number macros + audit ledger

make paper-publishing-artifacts               # Editor-facing TSV exports

make paper-readable                           # Generate readable main.tex from development source

make paper-pdf                                # Compile PDF (pdflatex + bibtex)

make paper-check                              # Run all reproducibility checks and tests
```

---

## The Iterative Update Cycle

Read `references/update-cycle.md` for the full procedure. Summary:

When new results arrive or existing analysis changes:

1. **Identify what changed** — raw data, analysis logic, or presentation only?
2. **Update at the right layer** — push changes as far upstream as they belong
3. **Regenerate downstream** — run the appropriate make targets in order
4. **Verify prose** — check that every sentence using affected `\PaperNumber{...}` macros still reads correctly with the new values
5. **Run checks** — `make paper-check` validates consistency

The key discipline: never patch a displayed number by editing `main_development.tex`.
Change the upstream collector, regenerate, and let the macro system propagate.

---

## Quick Reference: Common Operations

| Task | Do This |
|---|---|
| New experiment data arrived | Add to `paper_artifacts/inputs/` or `derived/`, regenerate |
| A figure looks wrong | Fix the `make.py`, run `make paper-figures FIGURE=<name>` |
| Need a new number in prose | Add collector in `numbers/groups/`, `make paper-numbers` |
| Table cell is wrong | Fix the collector or curated data, `make paper-tables TABLE=<name>` |
| Caption needs a stat | Add paper number, use `\PaperNumber{...}` in caption |
| Remove a figure | Delete from tex, Makefile, source dir, outputs, numbers, run checks |
| Full rebuild | `make paper-reproduce` |
| Verify everything | `make paper-check` |

---

## Complementary Skills

This skill covers infrastructure, not correctness auditing or prose. Once the
pipeline is set up and `make paper-check` passes, use the `paper-manuscript`
skill for a final pass: it audits numerical claims in prose, checks
typos/formatting/spelling consistency, and verifies cross-references (its
Steps 2–4).

Because every figure, table, and number here already carries provenance in
`numbers_source/paper_numbers.tsv` / `.json`, point `paper-manuscript`'s Step
2a ("trace each number to its source") at that ledger as the "Expected
source" instead of re-deriving values from table fragments or script output.

---

## Reference Files

Read these when performing specific operations:

- `references/repo-scaffold.md` — How to set up a new manuscript pipeline from scratch
- `references/figure-rules.md` — Add / modify / delete figures
- `references/table-rules.md` — Add / modify / delete tables
- `references/number-rules.md` — Add / modify / delete paper numbers
- `references/update-cycle.md` — Step-by-step procedure for incorporating new results
- `references/make-py-patterns.md` — Templates and conventions for figure/table make.py files
- `references/publishing-exports.md` — How the publishing artifact export system works
