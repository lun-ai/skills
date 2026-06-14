# Number Rules

A paper number is any result-like count, percentage, range, rate, denominator, or summary
statistic that should remain traceable to a source artifact. Every numerical claim in the
manuscript uses `\PaperNumber{MacroName}` rather than a hard-coded value.

---

## Two-Layer Architecture

1. **Source of truth** — `paper_artifacts/numbers/`: definitions, provenance, grouping,
   validation, and collection logic.
2. **Generated output** — `paper/numbers_source/`: LaTeX macros, TSV audit ledger, and
   JSON ledger consumed by the manuscript and checks.

Never edit `numbers_source/` by hand. Change the registry in `paper_artifacts/numbers/`,
then regenerate.

---

## Core Rules

1. Manuscript prose and generated table snippets use `\PaperNumber{MacroName}`, not
   hard-coded values.
2. Every number must carry enough provenance to answer: which input was read, which rows
   were selected, which denominator was used, and what arithmetic produced the displayed
   value.
3. Number collectors read curated artifacts from `paper_artifacts/inputs/` or
   `paper_artifacts/derived/`. Raw experiment files must be promoted into
   `paper_artifacts/` before they can be direct number inputs.
4. `paper/shared/` provides loaders and paths. It must not derive paper-number data.
5. `publishing_artifacts/` TSVs are final handoff copies and must not serve as number
   inputs.

---

## How To Add A Number

### Step 1: Decide whether the claim needs a paper number

Use a macro for result-like values in prose, captions, or generated table cells.
Do NOT use macros for: section labels, figure numbers, model names, literature years,
or other non-result metadata.

### Step 2: Identify the source artifact

Prefer existing curated files under `paper_artifacts/derived/` or `paper_artifacts/inputs/`.
If the data only exists in raw outputs or in a figure/table/publishing TSV, promote
the minimal reusable derived artifact into `paper_artifacts/` first.

### Step 3: Choose or create a number group

Groups live in `paper_artifacts/numbers/groups/`. Add the number to an existing group
when it belongs to the same claim family. Create a new group only when the claim family
has a distinct input set.

Example group module:

```python
"""Paper numbers for the model comparison experiment."""
from __future__ import annotations
from paper_artifacts.numbers.paper_number import PaperNumber

def collect() -> list[PaperNumber]:
    # Load curated data
    import pandas as pd
    df = pd.read_parquet("paper_artifacts/derived/experiment/results.parquet")

    numbers = []

    sample_count = len(df)
    numbers.append(PaperNumber(
        macro_name="ExperimentSampleCount",
        value=sample_count,
        display_value=f"{sample_count:,}".replace(",", "{,}"),
        unit="count",
        source_dataset="paper_artifacts/derived/experiment/results.parquet",
        source_script="paper_artifacts/numbers/build.py",
        source_function_or_query="len(df)",
        upstream_raw_artifacts="data/experiment_raw/run_001.json",
        manuscript_location="Section 3, paragraph 1",
        description="Total number of experiment samples evaluated",
        operation_summary="Count all rows in curated results table",
        derived_inputs=["paper_artifacts/derived/experiment/results.parquet"],
        number_group="model_comparison",
    ))

    accuracy = df["correct"].mean() * 100
    numbers.append(PaperNumber(
        macro_name="ExperimentOverallAccuracy",
        value=accuracy,
        display_value=f"{accuracy:.1f}\\%",
        unit="percent",
        source_dataset="paper_artifacts/derived/experiment/results.parquet",
        source_script="paper_artifacts/numbers/build.py",
        source_function_or_query="df['correct'].mean() * 100",
        upstream_raw_artifacts="data/experiment_raw/run_001.json",
        manuscript_location="Section 3, paragraph 2",
        description="Overall accuracy across all samples",
        operation_summary="Mean of correct column, multiplied by 100",
        derived_inputs=["paper_artifacts/derived/experiment/results.parquet"],
        number_group="model_comparison",
    ))

    return numbers
```

### Step 4: Register the group

In `paper_artifacts/numbers/registry.py`:
```python
from paper_artifacts.numbers.groups import model_comparison
_GROUPS = [model_comparison]
```

### Step 5: Use the macro in the manuscript

```latex
We evaluated \PaperNumber{ExperimentSampleCount} samples, achieving an overall
accuracy of \PaperNumber{ExperimentOverallAccuracy}.
```

For table generators:
```python
def to_latex(data):
    return f"... & \\PaperNumber{{ExperimentOverallAccuracy}} \\\\"
```

### Step 6: Regenerate and verify

```bash
make paper-numbers
make paper-check
```

### Step 7: Audit the generated row

Inspect `paper/numbers_source/paper_numbers.tsv` and confirm value, display value,
inputs, and operation summary are correct.

---

## How To Modify A Number

1. Find the macro in `main_development.tex`, table snippets, or `paper_numbers.tsv`
2. Find the collector in `paper_artifacts/numbers/groups/`
3. Change the upstream artifact or collector logic, not `numbers_source/`
4. Update provenance fields if the input, denominator, filter, or interpretation changed
5. Regenerate: `make paper-numbers && make paper-check`
6. Compare the TSV row before and after. If the displayed value changes, **read every
   sentence or table caption that uses it** and verify the wording still matches

---

## How To Delete A Number

1. Remove `\PaperNumber{...}` from `main_development.tex` or the table generator
2. Remove the `PaperNumber` from its collector in `paper_artifacts/numbers/groups/`
3. If an entire group becomes empty, remove it from `registry.py` and delete the module
4. Regenerate: `make paper-numbers && make paper-check`
5. Confirm the macro is gone from `paper_numbers.tsv` and no `.tex` snippet references it

---

## Display Value Formatting Conventions

| Type | Raw | Display | Notes |
|---|---|---|---|
| Integer | 1234 | `1{,}234` | Use `{,}` for LaTeX thousands separator |
| Percentage | 0.857 | `85.7\%` | Include `\%` in display |
| Percentage points | 30.6 | `30.6 pp` | Use "pp" suffix |
| Signed delta | +7.1 | `+7.1 pp` | Include sign |
| Range | (3, 7) | `3--7` | Use en-dash |
| Large number | 42336 | `42{,}336` | Thousands separator |

---

## Macro Naming Conventions

Use CamelCase with a descriptive prefix matching the number group:

- `ExperimentSampleCount` — not `N` or `n_samples`
- `ModelAAccuracy` — not `acc_a`
- `BaselineMinusProposedLift` — for signed deltas
- `ConfidenceIntervalLow` / `ConfidenceIntervalHigh` — for CI bounds
