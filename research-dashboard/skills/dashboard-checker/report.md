# Checker report and checks log

## Chat report

Open with the scope, then counts, then only the claims that need attention.

```markdown
**Fact check — E002, E003 (setup and results), 2026-10-29, code at `90db748`**
Trigger: before blog part 2 draws on them.

| Experiment | Claims | Verified | Mismatch | Stale | Unverifiable |
|---|---|---|---|---|---|
| E002 | 64 | 58 | 1 | 2 | 3 |
| E003 | 31 | 31 | 0 | 0 | 0 |

| # | Experiment · file · location | Document says | Evidence says | Evidence | Verdict |
|---|---|---|---|---|---|
| 12 | E002 · setup.md · System under test, Decoding | temperature 0.7 | temperature 1.0 | job 13940787 log, line 41 | mismatch |

Structural (check_experiments.py): 0 errors, 2 warnings — <list>.
Not checked: <what was out of scope or skipped, and why>.
Write-up can proceed: <yes / no, because claims # touch facts it uses>.
```

Name arms and settings by their descriptive names, as everywhere in research-dashboard.

## e###/checks.md

One file per experiment, newest entry last. The table row is what
`check_experiments.py` reads (the latest date in the file counts as the last check).

```markdown
# E002 fact checks

[← Setup](setup.md) · [Results](results.md) · [Dashboard](../DASHBOARD.md)

| Date | Scope | Code at | Trigger | Claims | Verified | Mismatch | Stale | Unverifiable | Open |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-29 | setup + results | `90db748` | before blog part 2 | 64 | 58 | 1 | 2 | 3 | #12 |

## 2026-10-29

<the full claim table: #, file and location, document says, evidence says, evidence, verdict.
Verified claims are listed here too, so the next check can start from them.>

Resolved: <later, when the user decides a mismatch: "#12 (2026-10-30): the run used 1.0;
setup.md corrected, Changes during execution row added.">
```

Keep earlier entries; a later check adds a row and a section. Claims marked resolved in an
earlier entry are re-checked, not assumed.
