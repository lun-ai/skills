# Figure Rules

Figures are presentation artifacts. Their code may compute panel-level values needed for
plotting, but reusable datasets and analytical sources of truth belong upstream in
`paper_artifacts/`.

---

## Core Rules

1. Figure source code lives under `figures/fig_<name>/`, `figures/supp/supp_fig_<name>/`,
   or `figures/analyses/<name>/`.
2. Final visual assets live under `figures/outputs/<figure_id>/` and are included from
   `main_development.tex` with `\includegraphics`.
3. Figure code reads curated inputs from `paper_artifacts/` through `paper.shared` loaders.
4. Keep non-visual derived data out of `figures/`. Tracked figure files should be code,
   docs, or visual assets (PDF, SVG, PNG).
5. Figure scripts must not write CSV, TSV, JSON, or parquet files. Editor-facing TSVs are
   generated through `publishing_exports(context)` and written by
   `make paper-publishing-artifacts`.
6. If captions or prose need numerical claims, add paper numbers in
   `paper_artifacts/numbers/` and use `\PaperNumber{...}`.
7. Do not use `publishing_artifacts/` as an input to figures.

---

## How To Add A Figure

### Step 1: Choose the figure class and output ID

Use a semantic name that matches the output directory:
- `figures/fig_<name>/` for main figures
- `figures/supp/supp_fig_<name>/` for supplementary figures
- `figures/analyses/<name>/` for analysis figures

### Step 2: Create the source module

Create `figures/fig_<name>/make.py` with:
- A docstring documenting inputs, outputs, and usage
- `__init__.py` in the same directory
- Panel helpers as separate functions or files if complex

See `references/make-py-patterns.md` for the standard `make.py` template.

### Step 3: Decide where the data comes from

- Use existing curated artifacts when possible
- If a new reusable derived dataset is needed, add an extractor under
  `paper_artifacts/derived/` first
- Presentation-specific computation (aggregation purely for a visual layout) may stay
  in the figure module

### Step 4: Write visual outputs only

```python
from paper.figures.shared.paths import output_dir

OUT_DIR = output_dir("<figure_id>")
PANEL_A = OUT_DIR / "panels" / "panel_a_<description>.pdf"
MAIN_PDF = OUT_DIR / "<figure_id>.pdf"
```

Emit PDF, SVG, and optionally PNG. PDF is the primary format for LaTeX inclusion.

### Step 5: Add publication TSV exports (when editors need plotted data)

Expose a `publishing_exports(context)` function in the same `make.py`:

```python
def publishing_exports(context: PublishingContext) -> list[PublishingExport]:
    return [
        PublishingExport(
            "figures/main/<figure_id>",
            "<descriptive_name>.tsv",
            dataframe,
        ),
    ]
```

### Step 6: Add figure numbers if captions need them

Follow `references/number-rules.md`: add the number to `paper_artifacts/numbers/groups/`,
regenerate `numbers_source/`, and use `\PaperNumber{...}` in the caption.

### Step 7: Wire the Makefile

Add the figure to the root Makefile so it runs with `make paper-figures FIGURE=<name>`.

### Step 8: Include it in the manuscript

```latex
\includegraphics[width=\linewidth]{figures/outputs/<figure_id>/<figure_id>.pdf}
```

### Step 9: Add tests

- Test that output paths are semantic and resolve correctly
- Test panel data preparation when non-trivial
- If publishing TSVs exist, update `publishing/tests/test_publishing_artifacts.py`

### Step 10: Regenerate and verify

```bash
make paper-figures FIGURE=<name>
make paper-publishing-artifacts
make paper-numbers
make paper-check
```

---

## How To Modify A Figure

1. Find the owning source directory and `make.py`
2. Classify the change: visual-only, presentation data prep, or reusable analysis
3. Keep visual changes in the figure module
4. Promote reusable data changes to `paper_artifacts/`
5. Update `publishing_exports(context)` if the plotted data changed
6. If a caption/prose number changed, update the number collector and rerun
   `make paper-numbers`
7. Regenerate: `make paper-figures FIGURE=<name> && make paper-publishing-artifacts && make paper-check`

---

## How To Delete A Figure

1. Remove `\includegraphics` and references from `main_development.tex`
2. Remove from Makefile `paper-figures` target
3. Delete the source directory (if no other figure imports it)
4. Delete visual outputs under `figures/outputs/`
5. Remove `publishing_exports(context)` and update publishing tests
6. Remove unused paper numbers from `paper_artifacts/numbers/groups/`
7. Run: `make paper-publishing-artifacts && make paper-numbers && make paper-check`

---

## Multi-Panel Figures

For composite figures with multiple panels:

```
figures/fig_<name>/
├── __init__.py
├── make.py                          # Main entry: loads data, calls panels, stitches
├── panel_a_<description>.py         # Panel-specific rendering
├── panel_b_<description>.py
└── README.md                        # Documents what each panel shows
```

Output structure:
```
figures/outputs/<figure_id>/
├── <figure_id>.pdf                  # Stitched composite
└── panels/
    ├── panel_a_<description>.pdf
    ├── panel_a_<description>.svg
    └── panel_b_<description>.pdf
```

---

## Boundary Checks

Enforce these in tests:
- Tracked files in `paper/figures/` must not be `.csv`, `.json`, `.parquet`, `.tex`, `.tsv`
- Figure source must not call `to_csv()` or `to_parquet()`
- Generated data handoff belongs under `paper/publishing_artifacts/`
