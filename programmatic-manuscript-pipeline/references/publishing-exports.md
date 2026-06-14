# Publishing Export System

The publishing export system generates final editor-facing TSV files from figure and table
computations. These TSVs are **downstream mirrors** — they contain the exact data behind
each visual or table, formatted for handoff to journal editors or reviewers. They are
never used as inputs to analysis, figures, tables, or paper numbers.

---

## Architecture

```
figures/fig_*/make.py  ──┐
                         ├── each optionally exposes publishing_exports(context)
tables/supp/*/make.py  ──┘
                              │
                              ▼
                    publishing/make.py
                    (discovers providers, calls them, writes TSVs)
                              │
                              ▼
                    publishing_artifacts/
                    ├── figures/main/<figure_id>/<name>.tsv
                    ├── figures/supplementary/<figure_id>/<name>.tsv
                    ├── figures/analyses/<analysis_id>/<name>.tsv
                    └── tables/supplementary/<table_id>/<name>.tsv
```

---

## How It Works

### 1. Provider functions

Each figure or table `make.py` optionally exposes a function:

```python
def publishing_exports(context: PublishingContext) -> list[PublishingExport]:
    ...
```

This function is not called during normal figure/table rendering. It is only called by
`make paper-publishing-artifacts`.

### 2. Discovery

`publishing/shared/exports.py` contains `discover_export_modules()`, which:
- Walks `paper/figures/` and `paper/tables/` recursively
- Finds every `make.py` (excluding `outputs/`, `tests/`, `__pycache__/`)
- Imports each module
- Extracts any `publishing_exports` attribute

### 3. Collection

`collect_exports()` calls each provider with a shared `PublishingContext` and aggregates
the results. It validates:
- Every return value is a `PublishingExport`
- No two exports share the same output path (rejects duplicates)

### 4. Writing

`publishing/make.py` writes each export as a TSV to
`publishing_artifacts/<artifact_id>/<filename>`.

---

## The PublishingContext

```python
@dataclass(frozen=True)
class PublishingContext:
    """Inputs shared by publication export providers."""
    df: pd.DataFrame     # Primary dataset (if applicable)
    meta: pd.DataFrame   # Metadata (if applicable)
```

Extend this dataclass with project-specific shared data. The context is constructed once
in `publishing/make.py` and passed to every provider.

If a provider doesn't need the shared context, it can ignore it:

```python
def publishing_exports(_context: PublishingContext) -> list[PublishingExport]:
    # Load data directly from curated artifacts
    df = pd.read_csv(CELLS_PATH, sep="\t")
    return [PublishingExport("figures/main/my_figure", "my_data.tsv", df)]
```

---

## The PublishingExport

```python
@dataclass(frozen=True)
class PublishingExport:
    artifact_id: str        # Semantic path, e.g. "figures/main/model_comparison"
    filename: str           # Must end in .tsv
    frame: pd.DataFrame     # The data to write
    float_format: str | None = None  # Optional pandas float format
```

Rules:
- `artifact_id` must be a clean relative path (no `.`, `..`, absolute paths)
- `filename` must be a single filename ending in `.tsv`
- `frame` must be a pandas DataFrame

### Semantic artifact_id conventions

| Figure type | artifact_id pattern |
|---|---|
| Main figure | `figures/main/<figure_id>` |
| Supplementary figure | `figures/supplementary/<figure_id>` |
| Analysis figure | `figures/analyses/<analysis_id>` |
| Supplementary table | `tables/supplementary/<table_id>` |

---

## Adding a Publishing Export

1. Add `publishing_exports(context)` to the owning figure or table `make.py`
2. Return `PublishingExport` objects with semantic paths
3. Update `publishing/tests/test_publishing_artifacts.py` to expect the new TSV
4. Run: `make paper-publishing-artifacts`
5. Verify the output under `publishing_artifacts/`

---

## Testing

`publishing/tests/test_publishing_artifacts.py` should:
- Import all figure and table modules
- Call `publishing_exports()` on a test context
- Verify the expected TSV paths are produced
- Verify no unexpected TSV paths appear
- Verify the DataFrame is non-empty and has expected columns

---

## Critical Rule

Publishing artifacts are **write-only outputs**. Nothing in the pipeline — figures,
tables, numbers, analysis code — should ever read from `publishing_artifacts/`. If a
value needs to change, update the upstream artifact or owning computation, then
regenerate.
