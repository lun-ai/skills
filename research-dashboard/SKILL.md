---
name: research-dashboard
description: >
  Manage an ongoing multi-question research or engineering effort as a dashboard: a research
  map of every topic, implementation and experiment (one global experiment number, E001,
  E002, ..., shared across all topics, with timestamps and attributes), an experiment list,
  and one detail file per topic. Covers rebuttals, feature investigations, technical
  probing/testing, or any work where a user has several open questions to answer by building
  something and running it. Use when a user has multiple open research questions to track
  together, asks to "make a plan" or "partition this into topics/areas", asks how much effort
  something would take, wants help deciding an implementation strategy before running an
  experiment, wants results reported back into an existing plan, asks "which experiment was
  that" or wants to see the research map, or is mid-investigation and says things like "check
  on progress", "analyse the results", "update the plan with these numbers". Also trigger for
  "smoke test this before the full run" and similar pre-scale-up validation requests, and for
  any empirical test run against an existing research effort, including offline re-analysis,
  re-scoring stored predictions, resampling and simulation, which are tests, not bookkeeping.
---

# Research Dashboard

A pattern for running a research or engineering effort that spans many sessions and several
open questions at once: paper rebuttals, "why does X underperform" investigations, a batch of
technical probes. The unit of work is not one linear conversation. It is a standing set of
documents that outlive any single session and are updated as experiments are answered.

This file is the router. Each component lives in its own file. Read the ones the situation
needs, listed under Routing below, not all of them.

## The model in one screen

- **Topics** group experiments that share a mechanism, harness or dataset. They are named,
  not numbered.
- **Implementations** are the shared code that experiments are built from (a harness, a tree
  library, a dataset builder). They are named, not numbered.
- **Experiments** are the unit of tracking. **Each one gets a global number `E###` from a
  single counter across all topics**, assigned when it is registered and never reused or
  renumbered. `E007` means one thing everywhere: dashboard, topic file, chat, folder name,
  commit message. Arms, seeds and reruns live inside an experiment. A changed design gets a
  new number linked to its parent.

The documents:

```
DASHBOARD.md
  ## Research map        ← counter line, Mermaid map, registry (timestamps + attributes)
  ## Experiments         ← one row per E###: question, status, effort, one-line result
  ## Topics              ← 2-4 sentences or E###-led bullets per topic, linking its file
  ## Cross-cutting notes
<topic>.md               ← one per topic; one `## E### — <question>` section per experiment
<topic>_e###_detail.md   ← only after the user agrees to a split
```

## Routing

| Situation | Read |
|---|---|
| No dashboard exists yet; user hands over a batch of questions | [references/bootstrap-and-resume.md](references/bootstrap-and-resume.md), [templates/dashboard.md](templates/dashboard.md), [templates/topic-file.md](templates/topic-file.md) |
| A dashboard exists; continue, check progress, update | [references/bootstrap-and-resume.md](references/bootstrap-and-resume.md) (Resume) |
| Registering an experiment, numbering, drawing or updating the map | [references/research-map.md](references/research-map.md) |
| Old dashboard with per-area `Q1, Q2` numbering | [references/research-map.md](references/research-map.md#migrating-an-existing-dashboard), propose only |
| Designing, building, running, analysing one experiment | [references/work-loop.md](references/work-loop.md) |
| About to run any empirical test, including a free re-score | [references/setting-block.md](references/setting-block.md), [templates/setting-block.md](templates/setting-block.md) |
| Steering by a small evaluation set | [references/small-eval-sets.md](references/small-eval-sets.md) |
| Reporting a result in chat or in a document | [references/reporting.md](references/reporting.md), [references/naming.md](references/naming.md) |
| Writing results back; a section is growing | [references/writing-discipline.md](references/writing-discipline.md) (read once per session before the first write-back) |
| Deciding whether to ask the user | [references/judgment-calls.md](references/judgment-calls.md) |
| Slurm or batch jobs; recording job IDs | [references/background-jobs.md](references/background-jobs.md) |

After any edit to the map or the experiment list, run
`python3 <this skill's directory>/scripts/check_map.py <path/to/DASHBOARD.md>` and fix what it
reports. It checks duplicate or missing numbers, the counter, map/registry/list agreement,
status classes, and topic-file sections.

## Non-negotiables

These hold in every situation. Each links to its full rule.

1. **One counter.** Reserve the next `E###` (re-read the dashboard first, write the registry
   row, bump the counter) before designing or building anything. Never reuse or renumber.
   [research-map.md](references/research-map.md)
2. **Map first.** The research map sits above the experiment list and is updated in the same
   edit as the fact it records: registration, status change, new arm, new implementation.
3. **Grill new experiments** with the `grilling` skill before building. A free offline
   re-analysis whose number the user might act on counts. [work-loop.md](references/work-loop.md)
4. **Post the empirical setting block before the first command of any test.**
   [setting-block.md](references/setting-block.md)
5. **Report context first, then numbers in a table, then limitations and what was not
   done.** Do not interpret unless asked. Context and definitions are not interpretation.
   [reporting.md](references/reporting.md)
6. **Descriptive names, never one-word stand-ins.** `E###` is the only bare symbol allowed.
   [naming.md](references/naming.md)
7. **Write back before ending the turn**: topic file, experiment row and map node. An answer
   that only exists in chat is lost. [work-loop.md](references/work-loop.md) step 12
8. **Structural changes are proposed, not made.** This covers partitions, splits, migrations
   and topic moves. [judgment-calls.md](references/judgment-calls.md)

<!--
CHANGE LOG
v2 2026-10-08: Empirical setting block made mandatory; "new experiment" widened to offline
re-analysis; small-evaluation-set floors and budgets; limitations and what-was-not-done owed
unprompted; scratch findings filed.
v3 2026-10-08: Compaction pass, no rules removed.
v4 2026-10-23: Global experiment numbering and research map. Per-area Qn replaced by one
counter E### across all topics (assigned at registration, never reused); "areas" renamed
"topics"; the dashboard opens with a Research map (counter, Mermaid diagram, registry of
topics/implementations/experiments with created/updated dates and attributes) above the
experiment list; stable <a id="e###"> anchors; migration path for per-area dashboards,
proposed rather than applied. Split the monolithic SKILL.md into a router plus one reference
per component (bootstrap-and-resume, research-map, work-loop, setting-block, small-eval-sets,
reporting, naming, judgment-calls, background-jobs, writing-discipline), document templates
under templates/, and scripts/check_map.py for numbering/map consistency. The v3 outstanding
issue (floor and budget invisible on the dashboard) is closed by registry attributes.
-->
