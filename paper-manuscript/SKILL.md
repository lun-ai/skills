---
name: paper-manuscript
description: >
  Generic pipeline for updating a LaTeX manuscript from source code: regenerate
  tables and figures, audit numerical claims against generated data, check for
  typos and formatting inconsistencies, and verify cross-references. Designed to
  work on any research paper repository. A repo-specific skill may extend this
  one by supplying paths, pipeline commands, and paper-specific prose passages.
version: 1.0.0
---

# Paper Manuscript Pipeline

This skill has five steps:

1. **Discover** — locate the manuscript structure (skip if a repo-specific skill already provides paths)
2. **Regenerate** — run analysis scripts to update tables and figures
3. **Audit** — verify every numerical claim in prose against its data source
4. **Format** — check for typos, LaTeX formatting issues, and terminology inconsistencies
5. **Report** — produce a structured findings report

A repo-specific skill should override Steps 1–2 with exact paths and commands,
and extend Step 3 with paper-specific prose passages and their expected values.
If no repo-specific skill exists, follow the discovery protocol in Step 0.

---

## Step 0 — Discovery (skip if repo-specific skill provides paths)

Run these commands from the repository root to locate the manuscript structure:

```bash
# Find the LaTeX entry point
find . -name "main.tex" -o -name "*.tex" | grep -v ".git" | head -20

# Find generated table fragments (\input{} targets)
grep -r "\\\\input{" <ENTRY_POINT>.tex | grep -v "^%" | sed 's/.*\\input{\([^}]*\)}.*/\1/'

# Find figure includes
grep -r "\\\\includegraphics" <ENTRY_POINT>.tex | grep -v "^%" | sed 's/.*{\([^}]*\)}.*/\1/'

# Find analysis/plotting scripts
find . -path "./.git" -prune -o \( -name "*.py" -o -name "*.R" \) -print | \
  xargs grep -l "savefig\|to_latex\|write_text\|output" 2>/dev/null

# Check for an existing pipeline script
find . -name "update_manuscript*" -o -name "Makefile" | grep -v ".git"
```

From this, establish:
```
MANUSCRIPT = <directory containing the .tex entry point>
REPO       = <repository root>
TABLES     = <directory where .tex table fragments are written>
FIGS       = <directory where figures included by the .tex are stored>
PIPELINE   = <script or Makefile target that regenerates tables and figures>
```

---

## Step 1 — Regenerate tables and figures

If a pipeline script exists, run it:
```bash
bash <PIPELINE>          # e.g. bash update_manuscript.sh
# or
make manuscript
```

If no pipeline exists, identify which scripts produce which outputs and run them
individually. After running, confirm that:
- All `\input{}` target `.tex` files exist and have a recent modification timestamp
- All `\includegraphics{}` target files exist and have a recent modification timestamp

Capture any accuracy / metric values printed to stdout — these will be needed in Step 3.

---

## Step 2 — Audit numerical claims

Read the full `.tex` entry point. For every number appearing in prose (not inside
a table or equation), record:

| Location (line) | Quoted text | Value | Expected source |
|---|---|---|---|
| … | … | … | … |

### 2a — Trace each number to its source

For numbers that should come from generated tables:
```python
# Generic: extract all numbers from a .tex table fragment
import re
tex = open("<TABLE_FILE>.tex").read()
# Strip LaTeX commands, find floats and percentages
numbers = re.findall(r'(?<![\\{])\b(\d+\.?\d*)\b', tex)
print(sorted(set(numbers)))
```

For numbers printed to stdout during Step 1, compare against the prose claim.

For numbers in inline (non-generated) tables, read each cell directly.

### 2b — Arithmetic checks

For any sum, percentage, or derived value stated in prose:
- Compute it explicitly and compare to the stated value
- Flag any discrepancy greater than rounding (typically ±1 in the last stated digit)

### 2c — Inequality language

Check that inequality language matches the data:
- "over X%" / "more than X%" — the actual value must be strictly greater than X
- "at least X%" — the actual value must be ≥ X (use this when the gap is exactly X)
- "up to X%" — the actual value must be ≤ X
- "approximately X" / "~X" — acceptable within ±5% of X

---

## Step 3 — Formatting and typo checklist

Read the full `.tex` and scan for each of the following. Report every occurrence
with line number.

### 3a — LaTeX formatting

| Pattern | Issue | Fix |
|---|---|---|
| `  ` (double space in prose) | Typographic error | Single space |
| ` \cite{` (space before `\cite`) | Non-breaking space missing | `~\cite{` |
| `[0-9]-[0-9]` numeric range with hyphen | Should use en-dash | `--` in LaTeX |
| Unicode `–` or `—` in source | Inconsistent with LaTeX convention | `--` or `---` |
| Commented-out `\caption` | Figure renders without caption | Uncomment or remove figure |
| `\textsuperscript{N}Word` (no space) | Runs into following word | `\textsuperscript{N} Word` |
| `\label{X}` with no `\ref{X}` anywhere | Orphan label | Add cross-reference or remove |
| `\ref{X}` with no `\label{X}` anywhere | Missing label | Add label or fix reference key |

Run this cross-reference check from the manuscript directory:
```python
import re
tex = open("<ENTRY_POINT>.tex").read()
labels  = set(re.findall(r'\\label\{([^}]+)\}', tex))
refs    = set(re.findall(r'\\(?:eq)?ref\{([^}]+)\}', tex))
citerefs = set(re.findall(r'\\cite[tp]?\{([^}]+)\}', tex))
print("=== \\ref without \\label ===")
for r in sorted(refs - labels): print(f"  \\ref{{{r}}}")
print("\n=== \\label without \\ref ===")
for l in sorted(labels - refs): print(f"  \\label{{{l}}}")
```

### 3b — Spelling consistency

Check that the paper does not mix British and American English. Pick one and flag
every deviation:

| British | American |
|---|---|
| organis/ation/ing | organiz/ation/ing |
| behaviour/al | behavior/al |
| modelling / labelling | modeling / labeling |
| colour | color |
| analyse | analyze |

Scan with:
```bash
grep -in "organi[sz]\|behaviou\|behavior\|modell\|labell\|colour\|analy[sz]" <ENTRY_POINT>.tex
```

### 3c — Proper noun and terminology consistency

Build a terminology table at the start of any repo-specific skill. At minimum,
check that model names, dataset names, and system names are capitalised and
hyphenated consistently throughout. Common patterns to enforce:

- Model names: use the official capitalisation (e.g. "GPT-4o", "Claude Sonnet 4.6",
  "Gemini 2.5 Flash") — no hyphens where spaces are canonical, no lowercase
- Dataset names: consistent hyphenation and capitalisation throughout
- System/method names introduced in the paper: one canonical form, used everywhere
- "in-the-wild": hyphenated when used as a modifier, two words otherwise

Scan for lowercase variants of any proper noun introduced in the paper.

### 3d — Sentence-level issues

- Sentences beginning with a numeral: rewrite to start with a word
- Undefined acronyms: every acronym must be expanded on first use
- Dangling abbreviations: "i.e." and "e.g." should be followed by a comma;
  inside parentheses only (or use "that is" / "for example" in running text)
- Hedged causal language: flag "which is why", "because X therefore Y",
  "this is due to" — verify each is supported by a direct measurement, not
  a post-hoc interpretation

---

## Step 4 — Report

Produce a structured report with these sections. Write "✓ No issues found." for
any section with nothing to flag.

```
### 1. Pipeline
List each regenerated file with its modification timestamp.

### 2. Numerical claims
For each number in prose: quoted text | stated value | source value | status (✓/✗)

### 3. Arithmetic checks
Any sum, percentage, or derived value: expression | expected | actual | status

### 4. Inequality language
Any "over / at least / up to" phrasing: quoted text | actual gap | correct phrasing

### 5. Cross-references
Missing \label and orphan \label entries.

### 6. LaTeX formatting
Each issue with line number: double spaces, missing ~\cite, range dashes,
uncaptioned figures, \textsuperscript spacing.

### 7. Spelling and terminology
Each inconsistency with line number and the canonical form.

### 8. Sentence-level issues
Undefined acronyms, causal language without supporting measurement.
```

---

## Extension guide — writing a repo-specific skill

Create `.claude/skills/<name>/SKILL.md` inside the repository. At minimum, provide:

```markdown
# <Paper Title> Manuscript Pipeline

Extends the generic `paper-manuscript` skill.

## Paths
MANUSCRIPT = <absolute path>
REPO       = <absolute path>
TABLES     = <absolute path>
FIGS       = <absolute path>

## Step 1 override — Pipeline command
\`\`\`bash
bash <MANUSCRIPT>/update_manuscript.sh
\`\`\`

Confirm these files are updated after running:
- <list each generated .tex and .pdf>

## Step 2 additions — Paper-specific prose passages

For each section of the paper that contains numerical claims, add a block:

### Section: <section name>  *(~line NNN)*
> "<exact quoted sentence>"
→ Source: <table file / script stdout / inline table> column "<column name>"
   Expected: <value or formula>

## Step 3 additions — Terminology table
| Term | Canonical form |
|---|---|
| <term> | <correct form> |
```
