<!--
Setup file for one experiment: <dashboard dir>/e###/setup.md. The as-run description a
methods section is rebuilt from. Rules: references/experiment-files.md. Every concrete value
has a Source (repo path[:line|@commit], job ID or log, "decision: <where> <date>", or a paper).
Keep the headings verbatim: scripts/check_experiments.py looks for them. Write "—" under a
heading that does not apply rather than deleting it.
-->
# E### setup — <descriptive name>

[← E### in <Topic name>](../<topic>.md#e###) · [Results](results.md) · [Interpretation](interpretation.md) · [Checks](checks.md) · [Dashboard](../DASHBOARD.md)

Design agreed <YYYY-MM-DD> (grilling). Describes the runs up to and including <run name>.
Code at `<commit>`.

## Question

<What this experiment is meant to settle, as a question in words. The hypothesis, if one was
stated before the run.>

## Lineage and provenance

- **From:** <E### and what is reused from it, or —>
- **Reused as-is:** <predictions, trajectories, a published table; cite the source E### or
  paper, and say what makes the reuse legitimate>
- **Newly computed:** <what this experiment produces>
- **Trained:** <what is trained or re-trained, or "nothing new is trained">

## Data

| Population | n | What it is and where it came from | Outcome distribution | Source |
|---|---|---|---|---|
| <descriptive name> | <n> | <one plain sentence> | <mean, range> | <path or release> |

## System under test

| Parameter | Value | Source |
|---|---|---|
| Model | <exact ID and revision> | <path:line> |
| Decoding | <temperature, top-p, max new tokens, stop rules> | <path:line> |
| Prompt | <name; verbatim text lives in the source file> | <path@commit> |
| Tools and budgets | <tools available; step, token, wall-clock limits> | <path:line> |
| Seeds and repeats | <seed list; repeats per arm> | <path or job IDs> |
| Hardware | <GPU type and count, per job> | <sbatch path or job ID> |

## Arms

| Arm (descriptive name) | Description | Varies | Holds fixed | Status | Source |
|---|---|---|---|---|---|
| <name> | <plain-language description> | <the one thing it changes> | <what it keeps> | planned / run / dropped | <config or decision> |

## Held fixed across all arms

- <listed explicitly, not left implied>

## Procedure

1. <steps in order, in plain words, including any resampling or simulation and its repeat
   count>

## Metrics and derived quantities

| Name | Definition | Unit, direction | Ignores | Source |
|---|---|---|---|---|
| <name> | <formula or one-clause definition; how the standard error is computed> | <unit; higher/lower is better> | <what it does not see> | <path:function> |

## Decision rules

<Any threshold a verdict hinges on (a discrimination floor, a smallest difference you would
believe, a pass mark), with its computation. "None: the experiment reports measurements only"
is a valid entry.>

## What this cannot show

<The inference boundary, written before the results existed.>

## Implementation

- **Built or instrumented:** <impl: nodes from the map, what is new, what is untouched>
- **Entry points:** <scripts and configs>
- **Reproduce a run:**

```bash
<the exact command or sbatch line>
```

- **Effort estimate:** <at design time; actuals go in the experiment list>

## Changes during execution

| Date | What changed (old → new) | Why | Applies to runs | Source |
|---|---|---|---|---|
| — | | | | |
