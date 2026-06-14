# Table Rules

Tables are presentation artifacts. Their LaTeX snippets belong in `tables/outputs/`,
while reusable data processing and number provenance belong upstream in `paper_artifacts/`.

---

## Core Rules

1. Table source code lives under `tables/supp/supp_table_<name>/`.
2. Final `.tex` snippets live under `tables/outputs/` and are included from
   `main_development.tex` with `\input{tables/outputs/...}`.
3. Numeric cells in generated `.tex` snippets use `\PaperNumber{...}` macros.
   The rendered values live in `numbers_source/`, generated from `paper_artifacts/numbers/`.
4. Table code reads curated inputs from `paper_artifacts/` or `paper/shared` loaders,
   never from `publishing_artifacts/`.
5. Tables must not import `paper.figures.shared`; shared non-visual helpers belong in
   `paper/shared/`.
6. Editor-facing TSVs are generated through `publishing_exports(context)` and written by
   `make paper-publishing-artifacts`.

---

## How To Add A Table

### Step 1: Choose the table ID and output path

Use a semantic path:
- Source: `tables/supp/supp_table_<name>/make.py`
- Output: `tables/outputs/supplementary/<name>/<name>.tex`

### Step 2: Create the table module

```
tables/supp/supp_table_<name>/
├── __init__.py
├── make.py      # Data builder + to_latex() renderer
└── README.md    # Documents what the table shows
```

The `make.py` must implement:
- A data loading function that reads from curated artifacts
- A `to_latex(data)` function that returns a LaTeX string with `\PaperNumber{...}` macros
- A `main()` entry point that writes the `.tex` snippet
- Optionally, `publishing_exports(context)` for TSV export

### Step 3: Decide where the data comes from

Read existing curated artifacts when possible. If the table needs a new reusable summary,
create or extend an extractor in `paper_artifacts/`. Do not create source TSVs inside
`paper/tables/`.

### Step 4: Add paper-number macros for numeric cells

Follow `references/number-rules.md`. Add cell macros to `paper_artifacts/numbers/groups/`.
Render `\PaperNumber{...}` in the table snippet, never raw numbers.

For systematic cell macros, create a helper:
```python
def table_cell_macro(model: str, metric: str) -> str:
    """Generate a deterministic macro name for a table cell."""
    return f"Table{model.title()}{metric.title()}"
```

### Step 5: Add publication TSV exports

```python
def publishing_exports(_context: PublishingContext) -> list[PublishingExport]:
    return [
        PublishingExport(
            "tables/supplementary/<name>",
            "<name>.tsv",
            pd.DataFrame(load_data()),
        )
    ]
```

### Step 6: Wire the Makefile

Add to the root Makefile `paper-tables` target.

### Step 7: Include in the manuscript

```latex
\input{tables/outputs/supplementary/<name>/<name>.tex}
```

Do not put inline `tabular` blocks in the main manuscript for supplementary tables.

### Step 8: Add tests

Test table-building logic, boundary constraints, and publishing inventory.

### Step 9: Regenerate and verify

```bash
make paper-tables TABLE=<name>
make paper-publishing-artifacts
make paper-numbers
make paper-check
```

---

## How To Modify A Table

1. Find the owning directory under `tables/supp/`
2. Classify: layout, presentation-specific calculation, or reusable data
3. Keep layout in the table module; promote reusable summaries to `paper_artifacts/`
4. If numeric cells changed, update matching paper-number collectors
5. Keep TSV export aligned with rendered table data
6. Run: `make paper-tables TABLE=<name> && make paper-publishing-artifacts && make paper-numbers && make paper-check`
7. Inspect the generated `.tex` snippet — numeric cells must use `\PaperNumber{...}`,
   never rendered literals

---

## How To Delete A Table

1. Remove `\input{tables/outputs/...}` from `main_development.tex`
2. Remove from Makefile `paper-tables` target
3. Delete the source directory under `tables/supp/`
4. Delete the generated `.tex` snippet under `tables/outputs/`
5. Remove `publishing_exports(context)` and update publishing tests
6. Remove unused table cell macros from `paper_artifacts/numbers/groups/`
7. Run: `make paper-publishing-artifacts && make paper-numbers && make paper-check`

---

## Boundary Checks

- Supplementary tables in `main_development.tex` are included as generated snippets,
  not inline `tabular` blocks
- Generated supplementary table snippets should use `\PaperNumber{...}`
- Table sources should not import `paper.figures.shared`
- Table and figure output directories should not store TSV/CSV/JSON/parquet sidecars
