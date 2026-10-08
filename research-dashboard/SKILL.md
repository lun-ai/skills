---
name: research-dashboard
description: >
  Manage an ongoing multi-question research or engineering effort as a dashboard of areas,
  each with its own effort-scoped plan file — for rebuttals, feature investigations, technical
  probing/testing, or any work where a user has several open questions to answer by building
  something and running it. Use when a user has multiple open research questions to track
  together, asks to "make a plan" or "partition this into areas", asks how much effort
  something would take, wants help deciding an implementation strategy before running an
  experiment, wants results reported back into an existing plan, or is mid-investigation and
  says things like "check on progress", "analyse the results", "update the plan with these
  numbers". Also trigger for "smoke test this before the full run" and similar pre-scale-up
  validation requests, and for any empirical test run against an existing research effort —
  including offline re-analysis, re-scoring stored predictions, resampling and simulation,
  which are tests, not bookkeeping.
---

# Research Dashboard

A pattern for running a research or engineering effort that spans many sessions and several
open questions at once: paper rebuttals, "why does X underperform" investigations, a batch of
technical probes. The unit of work is not one linear conversation — it's a standing set of
documents that outlive any single session, updated as questions get answered.

Two file types, always:

- **One dashboard** — an index. A table of every open question across every area, plus a
  couple of paragraphs per area. This is what the user reads to get oriented in five seconds.
- **One plan file per area** — the detail. Mechanism, effort, results, takeaways for that
  area's questions. Linked from the dashboard, never duplicated into it.

If no such documents exist yet, this skill **bootstraps** them from the user's questions. If
they exist, this skill **resumes** — reads current state, does the next piece of work, writes
results back, keeps the dashboard in sync.

## Bootstrap: partition questions into areas

When a user hands you a batch of open questions (reviewer comments, a backlog of "why does
this happen" investigations, a list of things to probe), don't start implementing immediately.

1. **Group into areas.** An area is a cluster of questions answerable with one shared
   mechanism/harness — if two questions would need the same instrumentation or the same
   comparison infrastructure, they're the same area. Areas are usually nouns ("Retrieval
   comparison", "Sufficiency classifier", "Model scaling"), not verbs.
2. **Number the questions within each area** (Q1, Q2, ...) — this gives every question a
   stable, linkable identity across both the dashboard and its own file.
3. **Estimate effort per question**, not per area — one question might be "a synthesis of
   existing numbers, 0.5 day" while another needs a new harness and real GPU/API cost. Be
   concrete: wall-clock, $ cost, and dependencies ("shares 70% of code with Q1").
4. **Sequence, don't just list.** State which areas/questions can run in parallel, which are
   blocked on another's output, and which should go last because they can absorb whatever the
   others produce along the way (a failure-mode taxonomy that wants traces from everything
   else, for instance).
5. Write the dashboard and one file per area (structures below). Confirm the partition and
   priority order with the user before any implementation — the grouping is a judgment call
   they may want to redirect. Every question needing a new experiment then goes through
   grilling (work loop step 1) before anything is built for it.

## Resume: continue existing plan files

Before acting, **read the dashboard in full and the area file(s) relevant to the request** —
don't assume your last-known structure still holds. These documents may have been reorganized,
split, or edited by the user or a parallel work stream between sessions. If the dashboard links
to files you don't recognize, or an area file covers ground you don't remember touching, that's
someone else's stream: read enough to not collide with it, but don't touch sections outside the
area you were asked about.

Then do one iteration of the work loop, and write results back into the relevant area file and
the dashboard row before ending the turn. A question is not "done" until both are updated — an
answer that only exists in chat is lost the moment the session ends.

## Document structure

**Dashboard** (one file, e.g. `PLAN.md`):

```markdown
## Dashboard

| # | Area | Q | Question | Status | Effort | One-line result |
|---|---|---|---|---|---|---|
| 1 | [Area Name](area_file.md#q1-anchor) | Q1 | <question> | Not started / In progress / Done | ~X days | <what was measured, once done — a verdict here only if interpretation was requested> |

Sequencing: <which areas are independent, which are blocked, which goes last>

## Areas

### [Area Name →](area_file.md)
<what this area investigates, its current state, and what its questions measured. One short
paragraph (2-4 sentences) while the area has a single main result; a bulleted list — one
complete-sentence bullet per done question, each leading with "**Qn (status)**", then what was
done, then what came out — once it covers several. Use the same bullet order and the same
paragraph-vs-list threshold in every area of one document, so a reader who has learned one
area can skim the rest the same way. "What it means" appears only if interpretation was
requested. Format rationale: references/writing-discipline.md>

## Cross-cutting notes
- <shared invariants: "all areas reuse X untouched", "no core-library changes except...">
- <any exception to those invariants, stated explicitly, with a link to where it's detailed>
```

**Area file** (one per area) — a general template, to be instantiated or extended per task:

```markdown
# <Area Name>

## Q1: <question> (job <id>)
<!-- job ID(s) appended only once the job finished and the user approved its results -->

### Context / motivation
<why this question, what's already known, what's missing>

### Setup and arms
<the agreed empirical setting block for this question, kept as written at design time, plus
anything that changed during execution. Once an area has more than ~3 arms, make the arms a
table keyed by descriptive name — name | plain-language description | what it varies | what it
holds fixed | status — and register every arm created mid-investigation here before reporting
anything about it>

### Implementation plan
<mechanism: what gets built or instrumented, what stays untouched, effort estimate>

### Infra notes (found during execution, not anticipated at plan time)
<rate limits, bugs, environment quirks hit along the way — often as valuable as the headline
result; don't drop them once the question is answered>

### Results
<facts only, never context-free: open by naming what was run under which settings (or point at
Setup and arms), then the numbers. Markdown tables for any metric compared across
arms/systems/datasets/variants — not narrated in prose — keyed by the arms' descriptive names,
plus links to the notebooks/scripts that produced them. No causal language ("because",
"suggests", "likely driven by") here>

### Limitations and what was not done
<facts about the measurement, so always written: what would bias these numbers high or low,
which reported differences sit inside their own floor (and are therefore claimed in neither
direction), what the test did not cover, and which adjacent question remains unmeasured. Not
interpretation — never gate this on being asked>

### Takeaways — WRITE ONLY IF THE USER ASKED FOR INTERPRETATION
<omit entirely otherwise. When asked: interpretation only, and sparse — the 1-3 claims a reader
needs to act on, not a running commentary on every row above>

...
```

Keep the dashboard's one-line result and the area file consistent — the dashboard line is the
compressed version of the question's Results (or of its Takeaways, where interpretation was
requested), not a different claim. That one pairing is a sanctioned duplication; it is not an
exception to the redundancy rules, which target *unintentional* restatement.

**When a question's own detail outgrows its section** (many per-run tables, confusion matrices,
per-class breakdowns, raw per-item numbers), a companion `<area>_<qN>_detail.md` — linked from
the question section ("Full numbers: [...]") and linking back up at its own top — is the usual
fix. **Propose the split rather than doing it unprompted**: it changes the structure the user
navigates, and they may prefer a different split point, a different file, or no split at all.
[references/writing-discipline.md](references/writing-discipline.md) covers when a split is
warranted and what moves once agreed.

## The work loop, per question

1. **When a new experiment is needed, invoke the `grilling` skill before building anything.**
   A new experiment is any *test* whose design has not yet been agreed with the user — not just
   any new *training run*: a new question, arm or condition, a new dataset or split, a new
   metric or grading scheme, a confound-isolating comparison (step 9), a scope change surfaced
   by a smoke test, or an offline analysis producing a number the user might act on (re-scoring
   stored predictions on a different subset, a resampling estimate, a selection-bias or power
   simulation). Costing nothing and training nothing does not make a test exempt: a free
   re-score that changes which arm looks best is a new experiment. Let grilling interview the
   user — hypothesis, arms and what each holds fixed, dataset, metric, budget, stopping point —
   then write the agreed design into the question's "Setup and arms" and "Implementation plan"
   before implementing. Reruns, resumes and bug-fix restarts of an already-agreed design do not
   need grilling.
2. **Decide implementation strategy with the user before building.** If there's more than one
   reasonable way to instrument or measure something, say so and let them pick — especially
   when one option adds a schema field or structural change and another doesn't. Prefer the
   option that reuses an existing artifact (a log file, an existing table) over inventing a
   parallel one, unless the user wants otherwise.
3. **Post the empirical setting block, then execute.** Before the first command of any
   empirical test — including a free offline re-analysis — post the block defined below, in
   chat, unprompted, every time. Then proceed without waiting, unless the test is a new
   experiment still being grilled (step 1), spends real money or shared wall-clock, or the
   block itself surfaced a design problem; in those cases stop on the block and let the user
   answer.
4. **Smoke test before scaling up.** Before committing real wall-clock or API cost, run the
   smallest version that can surface a design flaw — one item, one seed. This matters most when
   a design choice is itself a hypothesis about system behavior ("will a shared step budget
   across two tools starve the agent before it can answer?"): a cheap test turns that into a
   fact before you pay for the full run, and often changes the plan.
5. **Implement the minimal instrumentation.** No fields, flags or abstractions beyond what the
   question needs. If the user steers toward "simpler, non-redundant" over "more structured",
   take it — a log-only capture beats a new schema field when nothing downstream queries it.
6. **Run it**, respecting shared infrastructure limits (rate limits on shared egress IPs,
   cluster off-peak windows) rather than assuming your process is the only consumer.
7. **Analyze with verification, not assertion.** Build the analysis as an executable artifact
   (notebook, script) and actually run it — confirm zero errors — rather than hand-computing or
   eyeballing numbers into prose. Regenerate and re-run it whenever new data lands; never
   hand-edit stale output.
8. **Sanity-check aggregation before trusting it.** A bad regex, a glob that mishandles spaces
   in filenames, an off-by-one in a join key: these produce plausible wrong numbers, not
   crashes. Spot-check one aggregated data point against a manual read of the underlying file
   before reporting the aggregate.
9. **Isolate confounded variables with a third comparison point**, not just two. If a result
   could be explained by either of two factors ("less source access" vs. "worse architecture"),
   add an arm holding one fixed while varying the other, so the write-up can say which one
   actually moved the number.
10. **Report dual metrics when a comparison isn't apples-to-apples.** If two systems produce
   results in different identity spaces (one returns structured paper IDs, another arbitrary
   URLs), don't collapse to one number — report the raw count and the resolved/comparable
   count, with the resolution rate alongside, so the gap is visible rather than baked in.
11. **Name and register any arm you added** — including ones created autonomously during a
   smoke test or a confound-isolating comparison — in the area file's arm table, with a
   descriptive name, *before* reporting anything about it.
12. **Write the result back** into the area file (Results, and Limitations and what was not
   done; Takeaways only if interpretation was asked for) and update the dashboard row (Status,
   Effort actuals if they moved, and the one-line column — which states *what was measured*
   unless interpretation was requested). Append the producing job's ID to the question title
   once that job has finished and the user has approved its results. Disclose any exception to
   a stated cross-cutting invariant in Cross-cutting notes — don't let a necessary core-library
   fix pass silently because the plan said "no core-library changes".
13. **A finding from a scratch analysis is written back like any other.** A test run from a
   scratch directory with nothing committed still produced a number the user may act on, so it
   gets a home in the area file — its own `Qn` if it answers a standing question, otherwise a
   named subsection under the nearest area — with its setting block, its limitations and the
   path to the scratch script. Never end a turn offering to record it "if useful": offer the
   *interpretation*, never the record. If you genuinely cannot place it, say where the script
   lives and that it is unfiled, so it stays findable.

## The empirical setting block

**Before running any empirical test, post this block — in chat, unprompted, before the first
command.** Its job is to be a primer: a reader who was not inside the run should be able to say
what is being measured, what changes, what does not, and what the test could not settle —
*before* any number exists to argue about. Writing it is also the cheapest design review there
is; a block you cannot fill in is a test you have not finished designing.

**What counts as an empirical test.** Any procedure whose output is a number, ordering or
verdict the user might act on. Explicitly included, because these are the ones that get
skipped: re-scoring predictions already on disk; restricting or re-slicing an evaluation set; a
bootstrap, permutation or resampling estimate; a selection-bias, power or noise-floor
simulation; a re-grade under a different rubric; and any "quick check" in a scratch directory.
Training nothing, costing nothing and committing nothing do not exempt a test from the block.
Not included: reading code, inspecting a file, counting rows to orient yourself, or re-running
an already-reported test unchanged to confirm it reproduces.

```markdown
**Empirical setting — <short descriptive name of the test>**

- **Question in words** — what this test is meant to settle, as a question, not as a label.
- **Provenance** — what is reused exactly as-is (predictions from an earlier run, stored
  outputs, a published table), what is newly computed, and whether anything is trained or
  re-trained. State "nothing new is trained" explicitly when true, and say what makes the reuse
  legitimate ("in cross-validation each item was predicted by a model that had not seen it, so
  narrowing the scoring set afterwards leaks nothing").
- **Populations** — every group of items scored over: name, n, one plain sentence of what it is
  and where it came from; a table once there is more than one. Give each group's outcome
  distribution (mean and range) when groups will be compared — whether one group lies *beyond*
  another is usually the crux, and it is invisible from n alone.
- **What varies** — the one thing this test changes, named, with its levels.
- **What is held fixed** — listed explicitly, not left implied.
- **Procedure** — the steps in order, in plain words, including any resampling or simulation
  and its repeat count.
- **Metrics** — each defined in one clause, with units and direction (higher/lower is better)
  and what it ignores ("ranking ignores whether the values are right").
- **Derived quantities and decision rules** — any threshold a verdict will hinge on, defined
  with its computation: a discrimination floor, a smallest difference you would believe, a pass
  mark. Define these before the numbers, not in the paragraph that uses them.
- **What this cannot show** — the inference boundary, written before the result exists.
- **Cost and footprint** — wall-clock, $, shared infrastructure touched, scratch vs. repo,
  which files are created or changed, whether anything is committed. "Free — re-scores existing
  predictions, writes one scratch script" is a valid and useful answer.
```

Keep it to the lines that carry information: a free re-score is a short block, not a ceremonial
one. But never drop **what varies**, **what is held fixed**, **the metric definitions** or
**what this cannot show** — those four cannot be reconstructed afterwards, and they are exactly
what users ask for when they were omitted. When one primer covers several parts, state the
shared setting once, then give **one varies/held-fixed pair per part**.

## Small evaluation sets: floors, and a budget for how often you may look

Any set you *steer by* needs two numbers before it can decide anything, and both belong in the
setting block:

- **Its discrimination floor** — the smallest difference between two candidates the set can
  tell apart from luck. Estimate it by resampling the set from itself, re-scoring both
  candidates on each draw, and taking 1.96 standard deviations of how much their difference
  bounces. A difference smaller than the floor is not a result, whichever way it points.
- **Its selection inflation** — how much apparent improvement comes from keeping the best of
  *k* candidates that are not genuinely different. Simulate it with candidates you believe are
  equivalent (repeats of one method under different random seeds): score them all, then
  repeatedly draw *k* at random and keep the best. Report the inflation at the *k* you actually
  intend to try.

When inflation at your intended *k* approaches the floor, that set cannot referee your
iteration — selection alone manufactures a difference the size of the smallest one you would
believe. Say so plainly and propose a split: iterate on a larger in-distribution view, and
**spend the small set once, at the end**, under an explicit consultation budget written into
the plan file ("this set may inform zero decisions before the final comparison"). A budget that
is not written down erodes one glance at a time.

Also say when a cheap proxy *cannot* be manufactured. A subset matched on surface features is
still drawn from the same distribution, so it cannot stand in for a set whose difficulty comes
from lying beyond that distribution. Name which kind of hardness is in play — a different mix
of the same ingredients, or genuine extrapolation — because only the first can be proxied, and
a sharper-but-in-distribution view is a reported lens, not a decider.

## Reporting results

**Every report of a result — chat or document — mirrors the setting block, context first,
before any number appears.** Not optional, not "when it seems useful", not something to wait
for the user to ask for. A number with no setting attached is unreadable to anyone who wasn't
inside the run, including the same user three days later.

Report in this order, per part:

1. The setting block's content — the question in words, provenance, populations, **what varies
   and what is held fixed** (as a named pair, for every test, not only ones that feel like
   comparisons), the procedure, the metric and derived-quantity definitions, and the scope
   boundary — plus anything that changed during execution, and the system settings a reader
   needs: which model, which prompt or protocol variant, which tools were available, which
   dataset and split, how many items, how many seeds or repeats, any budget or cutoff (step,
   token, timeout) that could bound the result.
2. The numbers, in a table.
3. **Limitations of the estimate** — what would bias it high or low, and which of its
   differences sit inside their own floor and are therefore claimed in neither direction.
4. **What was not done** — parts of the question left untested, what was not committed, and
   the cheapest unanswered measurement still on the board.

Steps 3 and 4 are facts about the measurement, so they are owed unprompted. Nothing beyond them
unless interpretation was requested.

**Context and definitions are not interpretation.** The "do not interpret unless asked" default
restricts *why* a number came out that way and *what it implies*; it never licenses dropping
bare numbers on the user. If a report could be pasted into a stranger's inbox and leave them
asking "on what, with what?", it is not finished.

## Naming and plain language

Write for a collaborator who knows the field but not this codebase. Short sentences, everyday
words; expand jargon and internal shorthand on first use in a session; say what a config *does*
rather than quoting its filename. Filenames, flags and script paths belong in an artifacts line
at the end of a section, not in the sentence carrying the finding.

- **No single-word stand-in for an empirical setting.** An arm, condition, dataset variant,
  grading scheme, prompt variant or model configuration is never referred to by an acronym
  (`SR`, `OC`), a clipped word (`ctx`, `regrade`, `gold`), or a one-word nickname (`oracle`,
  `baseline`, `defeater`) — in prose, chat, table keys or dashboard lines. These read as obvious
  to whoever coined them and are opaque to everyone else, including the same user a week later.
  Say what the setting is, in a phrase: "the run where the model is given the gold-standard
  abstracts as context", not "oracle"; "answers re-scored against the SIGNOR curated labels",
  not "regrade"; "sentence retrieval only, no full-text access", not "SR-only".
- **Give every area, question, arm, condition, run and ablation a descriptive name** at the
  moment it is created — `no-retrieval`, `gold-abstracts-in-context`, `shared-step-budget`,
  `signor-holdout`. The name says what the thing *is*, so it needs no lookup. After the first
  full description in a reply or section, that name carries later mentions and serves as the
  table key.
- **Short codes (`T2`, `C1`, `run4`) never travel alone.** A symbolic tag may follow the
  descriptive name once in parentheses, when it is the anchor a reader needs to match a table
  row or dashboard entry — `the no-retrieval arm (T2)`. Never write a sentence whose meaning
  depends on remembering what `T2` was. If the codebase already uses a one-word abbreviation,
  translate it into the plain phrase and mention the code at most once, parenthetically.
- **`Qn` is the one sanctioned bare symbol**, because the dashboard defines every `Qn` in one
  place. Even then, pair it with the question's subject on first mention in a reply (`Q3, the
  retrieval-comparison question`).
- **Table and figure labels use the descriptive name as the row/column key**, with any code as
  a secondary column — not the reverse.
- **An arm you created mid-run must be registered before it is reported** (work loop step 11),
  with what it varies, what it holds fixed, and why it was added. An arm that exists only as a
  label in one chat message is the main source of the tracking problem this rule prevents. Keep
  the arm table as a glossary once an area has more than about three arms, and point later
  reports at it instead of re-explaining the arms.

## Writing discipline: facts vs. interpretation, length, redundancy

Full rules: [references/writing-discipline.md](references/writing-discipline.md). Read it
before the first report or write-back in a session, apply it on *every* write-back, and
re-check it whenever a question's section is growing (new run, new backbone, new dataset)
rather than being answered for the first time. **Its governing rule: when asked for an analysis
or a result, explain the results — leading with the settings they came from, in plain language
— and do not interpret unless interpretation was explicitly requested.** Beyond that it covers
keeping measured facts and interpretation structurally separate once interpretation *has* been
asked for (facts in Results, interpretation confined to Takeaways), and keeping documents
non-redundant as they grow — extend existing tables and caveats instead of cloning subsections,
because being current and being dense are independent failures: a document can be fully
up to date and still unreadable because every update appended instead of consolidating.

## Judgment calls that are the user's, not yours

Ask (with `AskUserQuestion` when there's a clean small set of options, otherwise directly)
rather than deciding unilaterally when:

- **A new experiment is needed** — grill its design with the user (step 1) rather than
  designing it yourself and presenting a finished plan.
- **A design choice trades cost or time against completeness** — "cancel and restart a 63%-done
  job to pick up a fixed config, or let it finish as-is".
- **An in-progress run's environment is stale relative to a fix** — an API key added after
  submission, a bugfix landed mid-run: the fix only helps a fresh run, not the running one.
- **A smoke test surfaced a finding that changes the planned scope** — "one config, or split
  into two step-budget variants?".
- **A question's detail has outgrown its section** — propose the split into a companion
  `_detail.md` (what moves, what stays, what it's called) rather than restructuring unprompted.

Everything downstream of such a decision — implementing it, running it, verifying it — is yours
to just do. Confirm the partition, not every step: get the area/question breakdown and priority
order signed off once, then keep executing the work loop without re-asking each turn.

## Background job discipline

For long-running work (Slurm jobs, batch API calls), prefer resumable harnesses: a run that
loads already-completed results and skips them on restart makes "cancel and resubmit to pick up
a fix" lossless instead of throwing away partial progress. Verify a resume actually skipped
existing work (grep the restart log for a "loaded N already-completed" line) rather than
assuming the resume flag did what it says.

If a job-monitoring mechanism reports it lost track of a job ("no completion record found, it
may have stopped"), that is a statement about the monitor, not the job. Check the job's actual
state directly — queue status, output file, log tail — before reporting anything as failed;
monitoring infrastructure and job infrastructure fail independently.

**Record the job ID next to the title once a job is finished and approved.** When a job (Slurm,
batch API, any scheduler-issued run) has finished *and* the user has approved its results,
append its ID to the title of the question or section reporting those results — `## Q2: Does
retrieval help on SIGNOR? (job 41873920)`, or `(jobs 41873920, 41874115)`. This makes every
reported number traceable to its logs without a separate lookup table. Do not add an ID while
the job is still running or before approval — a title ID means "these are the accepted results
of this job". If an approved result is later superseded by a rerun, replace the ID once that
rerun is approved rather than accumulating stale IDs.

## Interaction principles

- **Post the empirical setting block before you run anything.** Not after, not when asked, not
  only for expensive runs. If the user has to ask "what was the setup, the variable, the
  metric?", the block was owed and missing.
- **Do not interpret unless asked — this overrides the urge to be helpful.** Deliver the
  results and a full explanation of them: what was run, under which settings, the numbers, what
  the metrics mean by definition, what the measurement did and did not cover. Withhold
  mechanism, implications, verdicts on whether something works, rankings and next steps. Offer
  in one line ("happy to give my read, if useful") and stop. Withholding interpretation never
  means withholding context — a bare number is an under-delivery, not a disciplined one.
- **When interpretation *has* been requested, state it as claims, not a data dump.** "Source
  access explains ~4.6x of the overlap gap; step budget explains almost none of the remainder"
  is a takeaway, and it lives in Takeaways, not Results.
- **Keep the dashboard current enough to be trusted at a glance.** A Status column that still
  says "Not started" after the work shipped is worse than no dashboard — the next reader acts
  on it.
- **When updating a document you didn't create this session, scope your edit to your area.**
  Read the whole file for coherence, but only touch the rows and sections your work stream owns.

<!--
CHANGE LOG
v2 2026-10-08: Added "The empirical setting block" (mandatory pre-execution primer: question,
provenance, populations, what varies / held fixed, procedure, metrics, derived decision
quantities, what it cannot show, cost, footprint) and made it work-loop step 3; widened step 1's
"new experiment" to cover offline re-analysis, re-scoring, resampling and simulation, so free
tests are no longer exempt from design agreement; added "Small evaluation sets" (discrimination
floor, selection inflation at intended k, written consultation budget, why an in-distribution
subset cannot proxy extrapolation); made what-varies/held-fixed, provenance, derived
quantities, limitations and what-was-not-done unprompted obligations when reporting; added a
"Limitations and what was not done" section to the area-file template; added step 13 so
scratch-directory findings are filed rather than offered.
v3 2026-10-08: Compaction pass, no rules removed. Merged the old "Reporting contract" into
"Reporting results" (its numbered context list was a second copy of the setting block's
fields); merged "Plain language"/"No single-word abbreviations" into "Naming and plain
language"; folded the skimmability rule into "Writing discipline" and the confirm-the-partition
rule into "Judgment calls"; cut "Interaction principles" from ten bullets to five by deleting
the ones that only pointed at a section above. 549 -> ~400 lines.
Outstanding minor issues: the dashboard table has no column for a question's floor or
consultation budget — it lives in the area file's prose only.
-->
