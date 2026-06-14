# Figure and Table make.py Patterns

Standard templates and conventions for artifact `make.py` files. Every figure and table
module follows the same structural pattern so the pipeline can discover, execute, and
export them uniformly.

---

## Figure make.py Template

```python
"""Render <figure description>.

Inputs (curated derived artifacts):
- ``paper_artifacts/derived/<dataset>/<file>``

Outputs (written under ``paper/figures/outputs/<figure_id>/``):
- ``<figure_id>.pdf`` — main composite figure
- ``panels/panel_a_<description>.pdf`` — panel A
- ``panels/panel_b_<description>.pdf`` — panel B

Usage:
    python paper/figures/fig_<name>/make.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Resolve project root for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from paper.figures.shared.paths import output_dir, REPO_ROOT
from paper.publishing.shared.exports import PublishingContext, PublishingExport


# ── Paths ────────────────────────────────────────────────────────────────
INPUT_PATH = Path(__file__).resolve().parents[3] / "paper_artifacts" / "derived" / "<dataset>" / "<file>"
OUT_DIR = output_dir("<figure_id>")
PANEL_DIR = OUT_DIR / "panels"
PANEL_A_PDF = PANEL_DIR / "panel_a_<description>.pdf"
MAIN_PDF = OUT_DIR / "<figure_id>.pdf"


# ── Data loading ─────────────────────────────────────────────────────────
def _load_data() -> pd.DataFrame:
    """Load the curated input artifact."""
    return pd.read_parquet(INPUT_PATH)


# ── Panel rendering ──────────────────────────────────────────────────────
def render_panel_a(df: pd.DataFrame, path: Path) -> None:
    """Render panel A: <description>."""
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    # ... plotting code ...
    ax.set_xlabel("X label")
    ax.set_ylabel("Y label")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=300)
    plt.close(fig)


# ── Publishing exports ───────────────────────────────────────────────────
def publishing_exports(_context: PublishingContext) -> list[PublishingExport]:
    """Return editor-facing TSV exports for this figure."""
    df = _load_data()
    return [
        PublishingExport(
            "figures/main/<figure_id>",
            "<descriptive_name>.tsv",
            df[["col_a", "col_b", "col_c"]],  # Select relevant columns
        ),
    ]


# ── Main entry point ────────────────────────────────────────────────────
def main() -> int:
    if not INPUT_PATH.exists():
        print(f"Missing input: {INPUT_PATH}")
        return 1

    PANEL_DIR.mkdir(parents=True, exist_ok=True)

    df = _load_data()
    render_panel_a(df, PANEL_A_PDF)

    # If multi-panel, stitch panels here into MAIN_PDF
    # For single-panel figures, the panel IS the main output

    for p in (PANEL_A_PDF,):
        print(f"  -> {p.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

---

## Table make.py Template

```python
"""Build supplementary <table description> from curated artifacts.

Inputs:
- ``paper_artifacts/derived/<dataset>/<file>``

Outputs:
- ``paper/tables/outputs/supplementary/<name>/<name>.tex``
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from paper.publishing.shared.exports import PublishingContext, PublishingExport
from paper.tables.shared.paths import output_dir

logger = logging.getLogger(__name__)
OUT_DIR = output_dir("supplementary/<name>")
INPUT_PATH = Path(__file__).resolve().parents[4] / "paper_artifacts" / "derived" / "<dataset>" / "<file>"


def load_data() -> pd.DataFrame:
    """Load the curated input artifact."""
    return pd.read_csv(INPUT_PATH, sep="\t")


def to_latex(df: pd.DataFrame) -> str:
    """Render the table as a LaTeX tabular with PaperNumber macros."""
    rows = [
        r"\begin{tabular}{@{}lrrr@{}}",
        r"\toprule",
        r"Category & Metric A & Metric B & Total \\",
        r"\midrule",
    ]
    for _, row in df.iterrows():
        # Use \PaperNumber{MacroName} for every numeric cell
        macro_prefix = f"Table{row['category'].title()}"
        rows.append(
            f"{row['category']} & "
            f"\\PaperNumber{{{macro_prefix}MetricA}} & "
            f"\\PaperNumber{{{macro_prefix}MetricB}} & "
            f"\\PaperNumber{{{macro_prefix}Total}} \\\\"
        )
    rows.extend([r"\bottomrule", r"\end{tabular}"])
    return "\n".join(rows)


def publishing_exports(_context: PublishingContext) -> list[PublishingExport]:
    """Return editor-facing TSV exports for this table."""
    return [
        PublishingExport(
            "tables/supplementary/<name>",
            "<name>.tsv",
            load_data(),
        )
    ]


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    df = load_data()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_tex = OUT_DIR / "<name>.tex"
    out_tex.write_text(to_latex(df), encoding="utf-8")
    logger.info("Wrote %s", out_tex)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## Key Conventions

### Import resolution

Figure `make.py` files are typically 3 levels deep from the repo root. Table files are
4 levels deep. Use `sys.path.insert(0, str(Path(__file__).resolve().parents[N]))` where
N gets you to the repo root.

### Input validation

Always check that input files exist before proceeding. Print a clear message pointing
to the missing file and which pipeline stage should produce it.

### Output paths

Use the `output_dir()` helper from `figures/shared/paths.py` or `tables/shared/paths.py`.
This ensures consistent directory creation and path resolution.

### Panel naming

Use descriptive panel names: `panel_a_heatmap.pdf`, not `panel_a.pdf`. This makes the
outputs self-documenting.

### Idempotency

Running `make.py` twice should produce identical outputs. Avoid timestamps, random seeds
without fixing, or order-dependent operations.

### Multi-format output

For figures, emit PDF (for LaTeX), SVG (for web/editing), and optionally PNG (for
documentation). PDF is always the primary format referenced from `main_development.tex`.

### Publishing exports contract

The `publishing_exports(context)` function is optional but recommended. It:
- Takes a `PublishingContext` (shared data available to all exporters)
- Returns a list of `PublishingExport` objects
- Each export has a semantic `artifact_id` and a `.tsv` filename
- The `frame` must be a pandas DataFrame
- The function is discovered automatically by the publishing runner

### README.md

Every figure and table module should have a `README.md` documenting:
- What the artifact shows
- Which curated inputs it reads
- Which outputs it produces
- Any non-obvious design decisions
