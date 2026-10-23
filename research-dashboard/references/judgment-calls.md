# Judgment calls that are the user's, not yours

Ask (with `AskUserQuestion` when there's a clean small set of options, otherwise directly)
rather than deciding unilaterally when:

- **A new experiment is needed.** Reserve its number, then grill its design with the user
  ([work-loop.md](work-loop.md) step 1) rather than designing it yourself and presenting a
  finished plan.
- **A design choice trades cost or time against completeness**: "cancel and restart a
  63%-done job to pick up a fixed config, or let it finish as-is".
- **An in-progress run's environment is stale relative to a fix**: an API key added after
  submission, a bugfix landed mid-run. The fix only helps a fresh run, not the running one.
- **A smoke test surfaced a finding that changes the planned scope**: "one config, or split
  into two step-budget variants?" If the split changes the design, the second variant becomes
  a new experiment with its own number.
- **An experiment's detail has outgrown its section.** Propose the split into a companion
  `_detail.md` (what moves, what stays, what it's called) rather than restructuring
  unprompted.
- **An existing dashboard uses per-area numbering.** Propose the migration to global `E###`
  ([research-map.md](research-map.md#migrating-an-existing-dashboard)), and do not do it
  unasked.
- **An experiment should move to a different topic, or two topics should merge.** The number
  stays the same, but the user navigates by topic.

Everything downstream of such a decision (implementing it, running it, verifying it) is yours
to just do. Confirm the partition, not every step: get the topic/experiment breakdown and
priority order signed off once, then keep executing the work loop without re-asking each turn.

## Interaction principles

- **Post the empirical setting block before you run anything.** Not after, not when asked, not
  only for expensive runs. If the user has to ask "what was the setup, the variable, the
  metric?", the block was owed and missing.
- **Do not interpret unless asked. This overrides the urge to be helpful.** Deliver the
  results and a full explanation of them: what was run, under which settings, the numbers,
  what the metrics mean by definition, what the measurement did and did not cover. Withhold
  mechanism, implications, verdicts on whether something works, rankings and next steps. Offer
  in one line ("happy to give my read, if useful") and stop. Withholding interpretation never
  means withholding context. A bare number is an under-delivery, not a disciplined one.
- **Keep the dashboard current enough to be trusted at a glance.** A map node still styled
  `planned`, or a Status column still saying "Not started", after the work shipped is worse
  than no dashboard, because the next reader acts on it.
- **When updating a document you didn't create this session, scope your edit to your
  experiments.** Read the whole file for coherence, but only touch the rows, nodes and
  sections your work stream owns. Taking the next number is the one shared write. Re-read
  before taking it.
