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
  validation requests.
---

# Research Dashboard

A pattern for running a research or engineering effort that spans many sessions and several
open questions at once: paper rebuttals, "why does X underperform" investigations, a batch of
technical probes. The unit of work is not one linear conversation — it's a standing set of
documents that outlive any single session, updated as questions get answered.

Two files types, always:

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
3. **Estimate effort per question**, not per area — one question in an area might be "done, a
   synthesis of existing numbers, 0.5 day" while another needs a new harness and real
   GPU/API cost. Be concrete: wall-clock, $ cost, and whether it depends on another
   question's harness ("shares 70% of code with Q1").
4. **Sequence, don't just list.** State which areas/questions can run in parallel, which are
   blocked on another's output, and which should go last because they can absorb whatever the
   others produce along the way (a failure-mode taxonomy that wants to see traces from
   everything else, for instance).
5. Write the dashboard and one file per area (structures below). Confirm the partition and
   priority order with the user before doing any implementation — the grouping is a judgment
   call they may want to redirect. Every question that needs a new experiment then goes
   through the grilling step (work loop step 1) before anything is built for it.

## Resume: continue existing plan files

Before acting, **read the dashboard in full and the specific area file(s) relevant to the
request** — don't assume your last-known structure still holds. These documents may have been
reorganized, split, or edited by the user or a parallel work stream between sessions. If the
dashboard now links to files you don't recognize, or an area file covers ground you don't
remember touching, that's someone else's parallel stream — read enough to not collide with it,
but don't touch sections outside the area you were asked about.

Then do one iteration of the work loop below, and write results back into the relevant area
file and the dashboard row before ending the turn. A question is not "done" until both are
updated — an answer that only exists in chat is lost the moment the session ends.

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
<what this area investigates, current state, and what its questions measured. A short paragraph
(2-4 sentences) if the area has one main result so far; a short bulleted list — one
complete-sentence bullet per done question, each leading with "**Qn (status)**" then what was
done then what came out — once the area covers several done questions each with their own
number. "What it means" belongs here only if interpretation was requested. Use the same three-part bullet order and the same paragraph-vs-list threshold in every
area's summary within one document; a reader who has learned one area's pattern should be able
to skim every other area the same way. See references/writing-discipline.md for the full
format and why the order matters>

## Cross-cutting notes
- <shared invariants: "all areas reuse X untouched", "no core-library changes except...">
- <any exception to those invariants, stated explicitly, with a link to where it's detailed>
```

**Area file** (one per area):

Below is a general template that can be instantiated/extended depending on the actual task.

```markdown
# <Area Name>

## Q1: <question> (job <id>)
<!-- job ID(s) appended only once the job finished and the user approved its results;
     see "Background job discipline" in SKILL.md -->

### Context / motivation
<why this question, what's already known, what's missing>

### Setup and arms
<the settings a reader needs before any number, in plain words: which model, which prompt or
protocol variant, which tools the system could use, which dataset and split, how many items,
how many seeds or repeats, any step or token budget, and what the run does not cover.
Once an area has more than ~3 arms, make this a table keyed by the arm's descriptive name —
name | plain-language description | what it varies | what it holds fixed | status — and
register every arm created mid-investigation here before reporting it. See "Naming" in
SKILL.md>

### Implementation plan
<mechanism: what gets built or instrumented, what stays untouched, effort estimate>

### Infra notes (found during execution, not anticipated at plan time)
<rate limits, bugs, environment quirks hit along the way — these are often as valuable
as the headline result; don't drop them once the question is answered>

### Results
<facts only, but never context-free: open with a plain-language line naming what was run and
under which settings (or point at Setup and arms above), define each metric once, then the
numbers. Markdown tables for any metric compared across arms/systems/datasets/variants — not
narrated in prose — with arms keyed by their descriptive names, plus links to the
notebooks/scripts that produced them. No causal language ("because", "suggests", "likely
driven by") here — see references/writing-discipline.md>

### Takeaways — WRITE ONLY IF THE USER ASKED FOR INTERPRETATION
<omit this section entirely otherwise. When asked: interpretation only, and sparse — the 1-3
claims a reader needs to act on, not a running commentary on every row above>

...
```

Keep the dashboard's one-line result and the area file consistent — the dashboard line is the
compressed version of the question's Results (or of its Takeaways, where interpretation was
requested), not a different claim. This one pairing is a
sanctioned duplication (a summary is supposed to restate the detail, compressed); it's not an
exception to the redundancy rules below, which target *unintentional* restatement.

**When a question's own detail outgrows its section** (many per-run tables, confusion
matrices, per-class breakdowns, raw per-item numbers), a companion detail file —
`<area>_<qN>_detail.md`, linked from the question section ("Full numbers: [...]") and linking
back up to the area file at its own top — is the usual fix. **Propose the split to the user
rather than doing it unprompted** (see Judgment calls, below): it changes the document
structure they navigate, and they may prefer a different split point, a different file, or no
split at all. See [references/writing-discipline.md](references/writing-discipline.md) for
when a split is warranted and what stays vs. moves once agreed.

## The work loop, per question

1. **When a new experiment is needed, invoke the `grilling` skill before building anything.**
   A new experiment is any run whose design has not yet been agreed with the user: a new
   question, a new arm or condition, a new dataset or split, a new metric or grading scheme, a
   confound-isolating comparison (step 8), or a scope change surfaced by a smoke test. Call it
   with the Skill tool and let it interview the user, one question at a time, about the
   hypothesis, the arms and what each holds fixed, the dataset, the metric, the budget, and the
   stopping point. Write the agreed design into the question's "Setup and arms" and
   "Implementation plan" sections before implementing. Reruns, resumes, or bug-fix restarts of
   a design the user already agreed do not need grilling.
2. **Decide implementation strategy with the user before building.** If there's more than one
   reasonable way to instrument or measure something, say so and let them pick — especially
   when one option adds a new schema field / structural change and another doesn't. Prefer the
   option that reuses an existing artifact (a log file, an existing table) over inventing a new
   parallel one, unless the user wants otherwise.
3. **Smoke test before scaling up.** Before committing real wall-clock or API cost to a full
   run, run the smallest version that can surface a design flaw — one item, one seed. This is
   especially important when a design choice is a hypothesis about system behavior (e.g. "will
   a shared step budget across two tools starve the agent before it can answer?") — a cheap
   smoke test turns that hypothesis into a fact before you pay for the full run, and often
   changes the plan (e.g. splitting one run into two step-budget variants).
4. **Implement the minimal instrumentation.** Don't add fields, flags, or abstractions beyond
   what the question needs. If the user steers toward "simpler, non-redundant" over "more
   structured," take it — a log-only capture beats a new schema field when nothing downstream
   needs to query it structurally.
5. **Run it**, respecting shared infrastructure limits (rate limits on shared egress IPs,
   cluster off-peak windows) rather than assuming your process is the only consumer.
6. **Analyze with verification, not assertion.** Build the analysis as an executable artifact
   (notebook, script) and actually run it — check it executes with zero errors — rather than
   hand-computing or eyeballing numbers into prose. Regenerate and re-run it every time new
   data lands, don't hand-edit stale output.
7. **Sanity-check aggregation before trusting it.** A bad regex, a shell glob that mishandles
   spaces in filenames, an off-by-one in a join key — these produce plausible-looking wrong
   numbers, not crashes. Spot-check one aggregated data point against a manual read of the
   underlying file before reporting the aggregate.
8. **Isolate confounded variables with a third comparison point**, not just two. If a result
   could be explained by either of two factors (e.g. "less source access" vs. "worse
   architecture"), don't guess — add a comparison arm that holds one factor fixed while
   varying the other, so the write-up can say which one actually moved the number.
9. **Report dual metrics when a comparison isn't apples-to-apples.** If two systems produce
   results in different identity spaces (e.g. one returns structured paper IDs, another
   returns arbitrary URLs), don't collapse to one number — report both the raw count and the
   resolved/comparable count, with the resolution rate stated alongside so the gap is visible
   rather than silently baked in.
10. **Name and register any arm you added** (including ones created autonomously during a
   smoke test or a confound-isolating comparison) in the area file's Setup and arms table,
   with a descriptive name — before reporting anything about it. See "Naming", below.
11. **Write the result back** into the area file (Results; Takeaways only if the user asked for
   interpretation) and update the dashboard row (Status, Effort actuals if they moved, and the
   one-line column — which states *what was measured* unless an interpretation was requested).
   Once the producing job has finished and the user has approved its results, append its job
   ID to the question/section title (see "Background job discipline", below). Disclose any
   exception to a stated cross-cutting invariant explicitly, in the Cross-cutting notes
   section — don't let a necessary core-library fix pass silently just because the plan said
   "no core-library changes." Before appending, apply
   [references/writing-discipline.md](references/writing-discipline.md) — check whether this
   is new content or a restatement of something already written, and whether it's a fact or an
   interpretation dressed up as one.

## Reporting contract: context first, in plain language

**Every report of a result — in chat and in a document — opens with the context of that result
before any number appears.** This is not optional, not "when it seems useful", and not
something to wait for the user to ask for. A number with no setting attached is unreadable to
anyone who wasn't inside the run with you, including the same user three days later.

Before the first number, state, in a few plain sentences (or a small setup table when there are
several arms):

1. **The question this run was answering**, in words, not by its label.
2. **The system and settings**: which model, which prompt or protocol variant, which tools
   were available, which dataset and split, how many items, how many seeds or repeats, and any
   budget or cutoff (step budget, token budget, timeout) that could bound the result.
3. **What differs from the comparison point**, if this is a comparison — name the one variable
   that changed, and confirm what was held fixed.
4. **What each metric means by definition**, in one clause, the first time it appears in a
   session ("agreement = fraction of items where the two verdicts match").
5. **What the run did not cover** — the scope boundary.

Then the numbers (in a table, per the writing discipline), then nothing else unless
interpretation was requested.

**Context and definitions are not interpretation.** The "do not interpret unless asked" default
below restricts *why* a number came out that way and *what it implies*; it never licenses
dropping bare numbers on the user. Explaining the context, the settings, and the metric is
required by that same default, not in tension with it. If a report could be pasted into a
stranger's inbox and leave them asking "on what, with what?", it is not finished.

**Plain language, always.** Write for a collaborator who knows the field but not this
codebase. Use short sentences and everyday words; expand jargon and internal shorthand on first
use in a session; prefer "the run where the agent could search the literature" over an internal
flag name; and say what a config *does* rather than quoting its filename. Filenames, flags and
script paths belong in an artifacts line at the end of the section, not in the sentence
carrying the finding.

**No single-word abbreviations for empirical settings.** An arm, condition, dataset variant,
grading scheme, prompt variant or model configuration is never referred to by a one-word
stand-in — an acronym (`SR`, `OC`), a clipped word (`ctx`, `regrade`, `gold`), or a one-word
nickname (`oracle`, `baseline`, `defeater`) — in prose, chat, table keys, or dashboard lines.
These read as obvious to whoever coined them and are opaque to everyone else, including the
same user a week later. Say what the setting is, in a phrase: "the run where the model is given
the gold-standard abstracts as context", not "oracle"; "answers re-scored against the SIGNOR
curated labels", not "regrade"; "sentence retrieval only, no full-text access", not "SR-only".
After the first full description in a reply or section, a short multi-word descriptive name
(`gold-abstracts-in-context`, `signor-curated-labels`) may carry later mentions and serve as
the table key. If the codebase or an existing plan file already uses a one-word abbreviation,
translate it into the plain phrase when writing, and at most mention the code once in
parentheses so the reader can match it to files.

## Naming: descriptive labels, never bare symbols

Short codes (`T2`, `C1`, `A3`, `run4`) are unreadable the moment there is more than a handful
of them, and they are worst exactly when they matter most — when side arms have accumulated
over sessions, several of them created autonomously mid-investigation.

- **Give every area, question, arm, condition, run and ablation a short descriptive name** at
  the moment it is created: `no-retrieval`, `opus5-batchwise`, `shared-step-budget`,
  `signor-holdout`. The name says what the thing *is*, so it needs no lookup. It is always
  several words, never a single-word abbreviation or nickname (see "No single-word
  abbreviations for empirical settings", above), and the arm table pairs it with a
  one-sentence plain-language description.
- **In prose and in chat, use the descriptive name.** A symbolic tag may follow it once in
  parentheses when it is the anchor a reader needs to match a table row or a Dashboard entry —
  `the no-retrieval arm (T2)` — and never on its own. Never write a sentence whose meaning
  depends on the reader remembering what `T2` was.
- **`Qn` is the one sanctioned bare symbol**, because the Dashboard defines every `Qn` in one
  place and the area-summary bullets lead with it. Even then, pair it with the question's
  subject on first mention in a reply (`Q3, the retrieval-comparison question`).
- **Table and figure labels use the descriptive name as the row/column key**, with any code as a
  secondary column — not the reverse.
- **An arm you created yourself mid-run must be registered before it is reported.** If a smoke
  test, a confound-isolating third comparison point (work loop step 8), or a follow-up variant
  produced an arm that is not yet in the plan, add it to the area file's arm table — name,
  one-line description of what it holds fixed and what it varies, and why it was added — and
  reference it by that name from then on. An arm that exists only as a label in one chat
  message is the main source of the tracking problem this rule exists to prevent.
- **Keep an arm glossary in the area file** once an area has more than about three arms: a small
  table of name, what changed, what was held fixed, and status. Every later report points at
  that table instead of re-explaining the arms.

## Writing discipline: facts vs. interpretation, length, redundancy

Full rules: [references/writing-discipline.md](references/writing-discipline.md). Read it
before the first report or write-back in a session, and re-check it whenever a question's section is
growing (new run, new backbone, new dataset) rather than being answered for the first time.
**The governing rule is the first two sections there: when asked for an analysis or a result,
explain the results — always leading with the settings they came from, in plain language — and
do not interpret unless interpretation was explicitly requested.**
Beyond that it covers: the mandatory context-and-settings preamble and descriptive naming of
arms (the two sections above), keeping measured facts and interpretation structurally separate once
interpretation *has* been asked for (facts in Results/Findings, interpretation confined to
Takeaways), and keeping documents non-redundant as they grow (extend existing tables/caveats instead of cloning subsections;
propose — don't unilaterally do — a split into a companion `_detail.md` file once a question's
section outgrows roughly one screen).

## Judgment calls that are the user's, not yours

Ask (with `AskUserQuestion` when there's a clean small set of options, otherwise directly)
rather than deciding unilaterally when:

- **A new experiment is needed** — invoke the `grilling` skill to settle its design with the
  user (work loop step 1), rather than designing it yourself and presenting a finished plan.

- A design choice trades off cost/time against completeness (e.g., "cancel and restart a
  63%-done job to pick up a fixed config, or let it finish as-is").
- An in-progress run's environment is stale relative to a fix (an API key added after
  submission, a bugfix landed mid-run) — the fix only helps a fresh run, not the running one.
- A cheap smoke test surfaced a real behavioral finding that changes the planned scope (e.g.,
  "should we run one config or split into two step-budget variants?").
- **A question's detail has outgrown its section and needs restructuring** — splitting into a
  companion `<area>_<qN>_detail.md`, or any other reshuffle of what lives where. This changes
  the document structure the user navigates and reads from; propose the split (what moves,
  what stays, what the new file is called) rather than doing it unprompted.

Everything downstream of that decision — implementing it, running it, verifying it — is yours
to just do.

## Background job discipline

For long-running work (Slurm jobs, batch API calls), prefer resumable harnesses: a run that
loads already-completed results and skips them on restart makes "cancel and resubmit to pick
up a fix" lossless instead of throwing away partial progress. Verify a resume actually skipped
existing work (grep the restart log for a "loaded N already-completed" line) rather than
assuming the resume flag did what it says.

If a job-monitoring mechanism reports it lost track of a job ("no completion record found, it
may have stopped"), that is a statement about the monitor, not the job. Check the job's actual
state directly (queue status, output file, log tail) before reporting anything as failed —
monitoring infrastructure and job infrastructure fail independently.

**Record the job ID next to the title once a job is finished and approved.** For record
keeping, when a job (Slurm job, batch API run, any scheduler-issued run) has finished *and* the
user has approved its results, append its ID to the title of the question or section that
reports those results — `## Q2: Does retrieval help on SIGNOR? (job 41873920)`; several jobs as
`(jobs 41873920, 41874115)`. This makes every reported number traceable back to its logs and
outputs without a separate lookup table. Do not add the ID while the job is still running or
before approval — a title ID means "these are the accepted results of this job". If an approved
result is later superseded by a rerun, replace the ID with the new one once that rerun is
approved, rather than accumulating stale IDs.

## Interaction principles

- **Confirm the partition, not every step.** Get the area/question breakdown and priority
  order signed off once; after that, keep executing the work loop without re-asking at every
  turn, unless you hit one of the judgment calls above. A new experiment is always one of
  them: grill it (work loop step 1) before building.
- **Plain language, no one-word shorthand for settings.** Describe every arm, dataset variant
  and grading scheme in words a newcomer would follow. See "Reporting contract", above.
- **Always give the context and settings first, unprompted, in plain language.** The user
  should never have to ask "on what data? which model? what does that metric mean?" after a
  report. See "Reporting contract", above — this is a standing requirement on every result you
  report, and it is not in tension with the no-interpretation default.
- **Refer to things by descriptive name, not by code.** No sentence should depend on the reader
  remembering what `T2` or `C1` stands for. See "Naming", above.
- **Do not interpret unless asked — this overrides the urge to be helpful.** When the user
  asks for an analysis, deliver the results and a full explanation of the results: what was
  run, under which settings, the numbers, what the metrics mean by definition, what the
  measurement did and did not cover. Withholding interpretation never means withholding
  context — a bare number is an under-delivery, not a disciplined one. Withhold mechanism, implications, verdicts on whether something works, rankings and
  next steps. Offer in one line ("happy to give my read, if useful") and stop. If they ask,
  interpretation goes in Takeaways — see
  [references/writing-discipline.md](references/writing-discipline.md), first section.
- **When interpretation *has* been requested, state it as claims, not a data dump.**
  "Source access explains ~4.6x of the overlap gap; step budget explains almost none of the
  remainder" is a takeaway. This lives in Takeaways, not Results.
- **Keep the dashboard current enough to be trusted at a glance.** A stale Status column
  (says "Not started" after the work shipped) is worse than no dashboard — the next reader
  acts on it.
- **Keep documents skimmable, not just current.** Being up to date and being dense are
  independent failures — a document can be fully current and still unreadable because every
  update appended instead of consolidating. Apply
  [references/writing-discipline.md](references/writing-discipline.md) on every write-back,
  not only when asked to.
- **When updating a document you didn't create this session, scope your edit to your area.**
  Read the whole file for coherence, but only touch the rows/sections your work stream owns.
