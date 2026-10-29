---
name: dashboard-checker
description: >
  Sub-skill of research-dashboard. Fact-check one or more experiments' documents against the
  evidence: every value in e###/setup.md against the code, configs and run artifacts it cites
  and the runs actually used; every number in e###/results.md against the script and output
  that produced it; every copy of those facts elsewhere (dashboard, topic summary,
  interpretation, HTML pages, a write-up) against results.md. Reached from the
  research-dashboard router, by the user ("check E002", "fact-check the setup", "verify the
  results", "is the dashboard accurate", "audit the experiment docs") or automatically at the
  trigger points below.
---

# Dashboard checker

Checks the **factual part** of an experiment, its setup and its results, so that a paper,
report or blog post built from `e###/setup.md` and `e###/results.md` describes what was
actually run and what actually came out. It does not judge whether the experiment was well
designed or whether the interpretation is right. It reports; it does not silently fix.

File layout and the rules being checked: [../../references/experiment-files.md](../../references/experiment-files.md).
Report format and the checks log: [report.md](report.md).

## When it runs

**On request:** whenever the user asks, for the experiments they name (default: every
experiment whose status is Running or Done).

**Automatically**, without asking, at these points:

1. **Before a write-up draws on an experiment.** A paper section, report, slide deck or blog
   post (including the `darkroom`, `blog`, `paper-manuscript` and `ai-paper-writing` skills)
   that will describe E###'s setup or quote its results. Skip only when `e###/checks.md`
   already has a check dated on or after the registry's Updated date with no open mismatch.
2. **When an experiment's status becomes Done.**
3. **After a rerun supersedes a run, or a row is added to Changes during execution.** Scope
   the check to the changed run and the setup values the change touches.
4. **When `check_experiments.py` warns "never fact-checked" or "last fact check ... is before
   the last update"** and the user is about to rely on that experiment.

Announce an automatic check in one line ("Fact-checking E002 and E003 before the blog post
draws on them") and proceed.

## Independence

A check by the session that just wrote the documents is anchored on what it believes it
wrote. **If this session wrote or edited the files being checked, run steps 2–5 in a fresh
subagent** (`general-purpose`). Give it this file's path, the dashboard path, the E### list
and the scope, and nothing about what the values are or should be. Then relay its report and
do step 6 yourself. In a session that did not write the files, run the steps inline.

## Steps

### 1. Structural layer

```bash
python3 <research-dashboard dir>/scripts/check_experiments.py path/to/DASHBOARD.md E002 E003
python3 <research-dashboard dir>/scripts/check_map.py path/to/DASHBOARD.md
```

Keep every error and warning; they go in the report. Do not fix anything yet. If `setup.md`
or `results.md` is missing for an experiment in scope, the factual layer for that file is
skipped and the report says so.

**Done when:** both scripts have run and their output is recorded.

### 2. List the claims

Build one list per experiment, numbered, before checking any of it:

- **Setup claims:** every row of every table in `setup.md` with a Source column, plus every
  concrete value in prose (an n, a seed count, a model ID, a threshold, a step in Procedure
  that names a parameter), plus each arm's existence and each row of Changes during execution.
- **Results claims:** every cell of every table in `results.md`, grouped by table, plus every
  number in run-section prose.
- **Copies:** every number or setup value about the experiment that appears in the dashboard
  (experiment row, registry attributes, topic summary), the topic file, `interpretation.md`,
  pages linked from them, and any write-up in scope.

**Done when:** every table row and every number in the files in scope is on the list.

### 3. Check the setup against the evidence

For each setup claim, open its source at the cited location and compare. Then check it
against **what the runs actually used**, which is the stronger evidence: the sbatch script and
log of the job IDs in `results.md`, a config saved into the output folder, the run's metadata
or the command recorded in the log. The current config default is weaker evidence than the
run's own record, because configs change after runs.

Also check, per experiment:

- each arm in `results.md` exists in setup's Arms table, and no arm in Arms marked `run` is
  missing from `results.md`;
- each n in Data matches the n in the results tables (or the difference is explained in a run
  section);
- model IDs, decoding values and seed counts written anywhere in `results.md`, the topic file
  or the dashboard match `setup.md`;
- if a source changed after the runs (`check_experiments.py` warns), compare the value at the
  setup's commit, not at HEAD;
- a `decision:` source is implemented by the code: find where.

### 4. Check the results against the evidence

For each results table:

- Open the `Produced by:` script and output. **Recompute when it is cheap:** re-run the
  analysis script if it is offline, needs no GPU or network, takes a few minutes at most, and
  can write its outputs to a scratch folder. This is re-running an already-reported test
  unchanged, so it needs no setting block (see the research-dashboard `setting-block.md`).
  Otherwise compare each cell against the output file.
- Spot-check at least one aggregate per table against the raw per-item data (one trajectory,
  one prediction file), as in the work loop's aggregation sanity check.
- Check that standard errors, intervals and n follow the definitions in setup's Metrics table.
- Check that the Current results section cites the latest reviewed run, and that no copy
  (step 2) quotes a run marked `superseded by`.

### 5. Give every claim a verdict

| Verdict | Meaning |
|---|---|
| verified | the document matches the evidence; cite the evidence (path:line, job log, recomputed value) |
| mismatch | the document says X, the evidence says Y; cite both |
| stale | true of an earlier run or commit, not of the runs the results come from |
| unverifiable | no source given, or the source is not available here (git-ignored output on another machine, a lost run) |

Do not assume which side of a mismatch is wrong. A doc that says `temperature 0.7` while the
job log says `1.0` may mean the doc is wrong or the run was launched wrongly.

**Done when:** every claim from step 2 has a verdict and, for verified and mismatch, a cited
piece of evidence.

### 6. Report and log

- In chat: lead with the scope and the counts per verdict per experiment, then a table of
  every mismatch, stale and unverifiable claim (see [report.md](report.md)). Verified claims
  are counted, not listed.
- Append a row to each experiment's `e###/checks.md` and write the full claim table under it
  ([report.md](report.md)). Create the file from the format there if it does not exist, and
  link it from the topic-file section's links line.
- **Do not edit `setup.md`, `results.md` or any copy to resolve a mismatch** until the user
  says which side is right. Then fix the document (or record that the run itself was wrong as a
  row in Changes during execution and a note in the run section), and re-run steps 1 and the
  affected part of 3–5.
- When the check was automatic before a write-up, say whether the write-up can proceed: it can
  if no mismatch or stale verdict touches a fact it will use.

**Done when:** the chat report is posted, every experiment in scope has a new `checks.md`
row, and no document was edited without the user's answer.
