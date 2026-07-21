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
   call they may want to redirect.

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

| # | Area | Q | Question | Status | Effort | One-line takeaway |
|---|---|---|---|---|---|---|
| 1 | [Area Name](area_file.md#q1-anchor) | Q1 | <question> | Not started / In progress / Done | ~X days | <finding, once done> |

Sequencing: <which areas are independent, which are blocked, which goes last>

## Areas

### [Area Name →](area_file.md)
<2-4 sentences: what this area investigates, current state, headline finding if done>

## Cross-cutting notes
- <shared invariants: "all areas reuse X untouched", "no core-library changes except...">
- <any exception to those invariants, stated explicitly, with a link to where it's detailed>
```

**Area file** (one per area):

```markdown
# <Area Name>

## Q1: <question>

### Context / motivation
<why this question, what's already known, what's missing>

### Implementation plan
<mechanism: what gets built or instrumented, what stays untouched, effort estimate>

### Infra notes (found during execution, not anticipated at plan time)
<rate limits, bugs, environment quirks hit along the way — these are often as valuable
as the headline result; don't drop them once the question is answered>

### Results
<tables, numbers, links to notebooks/scripts that produced them>

### Takeaways
<the finding, stated as a claim a reader can act on, not just a data dump>
```

Keep the dashboard's one-line takeaway and the area file's Takeaways section consistent —
the dashboard line is the compressed version, not a different claim.

## The work loop, per question

1. **Decide implementation strategy with the user before building.** If there's more than one
   reasonable way to instrument or measure something, say so and let them pick — especially
   when one option adds a new schema field / structural change and another doesn't. Prefer the
   option that reuses an existing artifact (a log file, an existing table) over inventing a new
   parallel one, unless the user wants otherwise.
2. **Smoke test before scaling up.** Before committing real wall-clock or API cost to a full
   run, run the smallest version that can surface a design flaw — one item, one seed. This is
   especially important when a design choice is a hypothesis about system behavior (e.g. "will
   a shared step budget across two tools starve the agent before it can answer?") — a cheap
   smoke test turns that hypothesis into a fact before you pay for the full run, and often
   changes the plan (e.g. splitting one run into two step-budget variants).
3. **Implement the minimal instrumentation.** Don't add fields, flags, or abstractions beyond
   what the question needs. If the user steers toward "simpler, non-redundant" over "more
   structured," take it — a log-only capture beats a new schema field when nothing downstream
   needs to query it structurally.
4. **Run it**, respecting shared infrastructure limits (rate limits on shared egress IPs,
   cluster off-peak windows) rather than assuming your process is the only consumer.
5. **Analyze with verification, not assertion.** Build the analysis as an executable artifact
   (notebook, script) and actually run it — check it executes with zero errors — rather than
   hand-computing or eyeballing numbers into prose. Regenerate and re-run it every time new
   data lands, don't hand-edit stale output.
6. **Sanity-check aggregation before trusting it.** A bad regex, a shell glob that mishandles
   spaces in filenames, an off-by-one in a join key — these produce plausible-looking wrong
   numbers, not crashes. Spot-check one aggregated data point against a manual read of the
   underlying file before reporting the aggregate.
7. **Isolate confounded variables with a third comparison point**, not just two. If a result
   could be explained by either of two factors (e.g. "less source access" vs. "worse
   architecture"), don't guess — add a comparison arm that holds one factor fixed while
   varying the other, so the write-up can say which one actually moved the number.
8. **Report dual metrics when a comparison isn't apples-to-apples.** If two systems produce
   results in different identity spaces (e.g. one returns structured paper IDs, another
   returns arbitrary URLs), don't collapse to one number — report both the raw count and the
   resolved/comparable count, with the resolution rate stated alongside so the gap is visible
   rather than silently baked in.
9. **Write the result back** into the area file (Results + Takeaways) and update the
   dashboard row (Status, Effort actuals if they moved, One-line takeaway). Disclose any
   exception to a stated cross-cutting invariant explicitly, in the Cross-cutting notes
   section — don't let a necessary core-library fix pass silently just because the plan said
   "no core-library changes."

## Judgment calls that are the user's, not yours

Ask (with `AskUserQuestion` when there's a clean small set of options, otherwise directly)
rather than deciding unilaterally when:

- A design choice trades off cost/time against completeness (e.g., "cancel and restart a
  63%-done job to pick up a fixed config, or let it finish as-is").
- An in-progress run's environment is stale relative to a fix (an API key added after
  submission, a bugfix landed mid-run) — the fix only helps a fresh run, not the running one.
- A cheap smoke test surfaced a real behavioral finding that changes the planned scope (e.g.,
  "should we run one config or split into two step-budget variants?").

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

## Interaction principles

- **Confirm the partition, not every step.** Get the area/question breakdown and priority
  order signed off once; after that, keep executing the work loop without re-asking at every
  turn, unless you hit one of the judgment calls above.
- **State findings as claims, not data dumps.** "Source access explains ~4.6x of the overlap
  gap; step budget explains almost none of the remainder" is a takeaway. A table of eight
  numbers without that sentence is not.
- **Keep the dashboard current enough to be trusted at a glance.** A stale Status column
  (says "Not started" after the work shipped) is worse than no dashboard — the next reader
  acts on it.
- **When updating a document you didn't create this session, scope your edit to your area.**
  Read the whole file for coherence, but only touch the rows/sections your work stream owns.
