# The Iterative Update Cycle

This guide covers the step-by-step procedure for incorporating new results, fixing
errors, or changing analysis logic — and propagating those changes correctly through the
entire pipeline.

---

## Principle: Push Changes Upstream, Regenerate Downstream

Never patch a displayed number by editing `main_development.tex`. Never fix a figure by
hand-editing a PDF. Never correct a table cell by changing the `.tex` snippet directly.

Instead: fix the problem at its source layer, then regenerate everything downstream.

---

## Identifying the Change Layer

| What Changed | Source Layer | Downstream to Regenerate |
|---|---|---|
| Raw experiment data | `data/` | artifacts → figures → tables → numbers → PDF |
| Curation/extraction logic | `paper_artifacts/derived/` | figures → tables → numbers → PDF |
| Analysis interpretation | `paper_artifacts/numbers/groups/` | numbers → PDF |
| Figure visual design | `paper/figures/fig_*/make.py` | figures → publishing → PDF |
| Table layout | `paper/tables/supp/*/make.py` | tables → publishing → PDF |
| Prose wording only | `paper/main_development.tex` | readable → PDF |
| Bibliography | `paper/references.bib` | PDF |

---

## Full Update Procedure

### Scenario A: New or Updated Raw Data

1. **Place or replace** the raw data files in `data/` or external storage
2. **Update curated artifacts**:
   ```bash
   make paper-artifacts DATASET=<affected_dataset>
   ```
3. **Regenerate figures** that read from the affected artifact:
   ```bash
   make paper-figures FIGURE=<name>   # for each affected figure
   # or: make paper-figures           # all figures
   ```
4. **Regenerate tables**:
   ```bash
   make paper-tables TABLE=<name>     # for each affected table
   ```
5. **Regenerate numbers**:
   ```bash
   make paper-numbers
   ```
6. **Regenerate publishing exports**:
   ```bash
   make paper-publishing-artifacts
   ```
7. **Review prose** — Open `main_development.tex` and read every sentence that uses
   `\PaperNumber{...}` macros from the affected number groups. Verify:
   - Comparative claims ("X is higher than Y") still hold
   - Orderings ("from lowest to highest: A, B, C") are still correct
   - Qualitative descriptors ("substantially", "nearly", "marginal") match the new magnitudes
   - Confidence intervals still support the stated conclusions
8. **Compile and check**:
   ```bash
   make paper-pdf
   make paper-check
   ```

### Scenario B: Changed Analysis Logic

Same as Scenario A, but starting at step 2. If only the number collector logic changed
(not the curated data), you can skip to step 5.

### Scenario C: Visual-Only Figure Change

1. Edit the `make.py` in the figure module
2. Regenerate the figure: `make paper-figures FIGURE=<name>`
3. Update publishing exports if the plotted data changed: `make paper-publishing-artifacts`
4. Compile: `make paper-pdf`

### Scenario D: Prose-Only Change

1. Edit `main_development.tex`
2. Regenerate readable source: `make paper-readable`
3. Compile: `make paper-pdf`

### Scenario E: Adding a New Claim to Prose

1. Check if a paper number already exists in `paper_numbers.tsv`
2. If not, follow `references/number-rules.md` to add one
3. Use `\PaperNumber{MacroName}` in the manuscript
4. Regenerate: `make paper-numbers && make paper-pdf`

---

## The Prose Review Step (Critical)

After any regeneration that changes displayed values, you must review the prose.
This is the step most commonly skipped, and it produces the most embarrassing errors.

### What to check:

**Comparative statements**: "Model A outperforms Model B" — does it still? Check the
new values.

**Orderings and rankings**: "from worst to best: Haiku, Sonnet, Opus" — is the ordering
still correct?

**Magnitude descriptors**: "a substantial improvement of \PaperNumber{Lift}" — is 2 pp
still "substantial"? Would "modest" be more accurate now?

**Confidence interval claims**: "the 95% CI excludes unity" — does it still?

**Denominator references**: "of \PaperNumber{Total} instances" — is the denominator
still the right one?

**Cross-references**: "consistent with Figure X" — does the figure still show what the
prose claims?

### Systematic approach:

```bash
# Find all PaperNumber uses in the manuscript
grep -n 'PaperNumber{' paper/main_development.tex | head -50

# Find all PaperNumber uses in generated table snippets
grep -rn 'PaperNumber{' paper/tables/outputs/

# Cross-reference with the audit ledger
cat paper/numbers_source/paper_numbers.tsv | cut -f1,3 | head -50
```

---

## Dependency Tracking

When you change something, trace the dependency chain:

```
Raw data file X
  └── Curated artifact Y (reads X)
       ├── Figure A (reads Y)
       │    └── Publishing export A.1
       ├── Table B (reads Y)
       │    └── Publishing export B.1
       └── Number group C (reads Y)
            ├── Macro C1 (used in Section 3, paragraph 1)
            ├── Macro C2 (used in Table B, cell [2,3])
            └── Macro C3 (used in Figure A caption)
```

If you change X, everything below it must regenerate. If you change only Number group C's
logic, only the macros and downstream prose/tables need updating.

---

## Safety Checklist Before Submitting

- [ ] `make paper-reproduce` completes without errors
- [ ] `make paper-check` passes all tests
- [ ] Every `\PaperNumber{...}` in `main_development.tex` has a matching macro in
      `paper_numbers.tex`
- [ ] No hard-coded numbers appear in prose where a `\PaperNumber{...}` should be used
- [ ] Prose has been re-read for consistency with new values
- [ ] Figure captions match what the figures actually show
- [ ] Table captions match the table content
- [ ] Bibliography compiles without warnings
- [ ] The generated `paper_numbers.tsv` audit ledger has been inspected
