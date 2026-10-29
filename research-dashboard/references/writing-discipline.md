# Writing discipline: facts vs. interpretation, length, redundancy

[← Back to SKILL.md](../SKILL.md)

Apply this before every write-back (work loop step 12) and whenever revisiting a question that
already has content in it.

## Default: explain results, do not interpret them

**When the user asks for an analysis, a result, an explanation of what was run, or an update on
a question, the deliverable is the results and an explanation of the results — nothing else.
Do not interpret unless interpretation was explicitly requested.** This is a hard default, not
a preference to balance against others. It governs chat replies and document write-backs
equally.

The distinction is operational, not stylistic. Explaining a result describes *what is on the
page*; interpreting it makes a claim about the world beyond the measurement.

**Explaining results — always in scope, and expected:**

- what was run: data, conditions, n, procedure, arms, seeds, folds, and the settings that
  produced them (model, protocol variant, tools, budgets) — always stated before the numbers,
  never on request only
- the numbers themselves, and comparisons/deltas between them
- what a metric means *by definition* ("AUC 0.71 = the model ranks a positive above a negative
  71% of the time")
- the scope of what was measured, and what it did not cover
- discrepancies, verification steps, sanity checks, and errors found in your own work

**Interpreting — withhold unless asked:**

- *why* a result came out that way; any mechanism or causal story
- what it implies for the design, the architecture, the paper, or the research direction
- whether something "works", "is viable", "is the largest lever", "is a dead end"
- recommendations, rankings, priorities, or proposed next steps
- generalization beyond the condition tested
- "this validates / refutes / confirms / retires / rules out <hypothesis>"

**Protocol when interpretation seems necessary.** It usually feels necessary; that feeling is
not the trigger. Deliver the results, then offer in one line — "Happy to give my read on why,
if useful." — and stop. The offer is not a place to smuggle in the interpretation. If the user
asks, give it then, at whatever length the question deserves.

**Do not front-load a verdict.** Opening an analysis with a bolded conclusion ("**The read-out,
not the representation.**", "**Capacity helps in exactly one place.**") is interpretation in
the position of a headline, where it frames every number that follows. Lead with what was run
and what came out.

**Why this is strict.** An interpretation offered alongside a result is not a neutral addition:
it arrives with the authority of the measurement attached, and it pre-empts the reading the
user was in the middle of forming. When they want it, they ask. Withholding costs one round
trip; volunteering costs them the analysis they were doing themselves.

## Context is mandatory, and it is not interpretation

The rule above is frequently over-applied into its opposite failure: a reply or a section that
is *only* numbers, with no statement of what was run, on what, with which settings. That is not
discipline, it is an under-delivered result — and it forces the user to ask for the setting
every single time.

**Every reported result — chat or document — leads with its context, in plain language, before
the first number.** Concretely, and unprompted:

- **What question this answers**, said in words.
- **The settings**: which model, which prompt or protocol variant, which tools were available,
  which dataset and split, how many items, how many seeds or repeats, and any budget or cutoff
  (steps, tokens, wall-clock) that could bound the outcome.
- **The contrast**, if it is a comparison: which single variable changed, and what was held
  fixed across arms.
- **Each metric's definition**, in one clause, the first time it appears in a session — "macro-F1
  = the unweighted mean of per-class F1, so rare classes count as much as common ones".
- **The scope boundary**: what this run does not cover.

All five are descriptions of the measurement, so all five sit squarely in the "explaining
results" column above. None of them makes a claim about the world beyond the run, and none of
them may be dropped on the grounds of avoiding interpretation.

**Plain language is part of the contract.** Write for a competent colleague who has not read
this codebase:

- Use short sentences and everyday words. If a simpler word says the same thing, use it.
- Expand internal shorthand and jargon on first use in a session; don't lean on a config
  filename, a flag, or a class name to carry the meaning of a sentence.
- **Never refer to an empirical setting by a single-word abbreviation.** Arms, conditions,
  dataset variants, grading schemes, prompt variants and model configurations get a
  descriptive phrase, not an acronym (`SR`, `OC`), a clipped word (`ctx`, `regrade`) or a
  one-word nickname (`oracle`, `baseline`). Write "the run where the model is given the
  gold-standard abstracts as context", not "oracle"; "answers re-scored against the SIGNOR
  curated labels", not "regrade". Later mentions may use a multi-word descriptive name
  (`gold-abstracts-in-context`). When the codebase or an existing document already uses the
  abbreviation, translate it and give the code at most once, in parentheses, for matching to
  files.
- Say what a setting *does* ("the arm where the agent had no literature search") rather than
  what it is *called* ("the `--no-retrieval` config").
- Put filenames, script paths, job IDs and commit hashes in a trailing artifacts line, not in
  the sentence carrying the finding.
- A reader should be able to paste any single paragraph into an email and have it stand alone.

## Labels: descriptive names, not symbols

Bare codes — `T2`, `C1`, `A3`, `run7` — are the main reason a multi-arm investigation stops
being followable, especially when arms accumulate across sessions and some were created
autonomously mid-run.

- **Name every arm, condition, run and ablation descriptively when it is created**:
  `no-retrieval`, `shared-step-budget`, `opus5-batchwise`, `signor-holdout`. The name should
  need no lookup, so it is always several words — a single-word abbreviation or nickname does
  not count as descriptive.
- **Prose uses the name.** A code may trail it in parentheses once, as a table-matching anchor
  (`the no-retrieval arm (T2)`), and never stand alone. If a sentence's meaning depends on the
  reader recalling what `T2` meant, rewrite the sentence.
- **`E###` is the one sanctioned bare symbol**, because the research map's registry defines
  each experiment number in exactly one place, the number is global across topics, and every
  topic-summary bullet leads with it. Even so, pair it with the experiment's subject on first
  mention in a reply.
- **Tables key rows by the descriptive name**, with any code as a secondary column — not the
  other way around.
- **Register before you report.** An arm you spun up yourself — a smoke-test variant, a
  confound-isolating third comparison point, a follow-up run — goes into the experiment's
  Arms table in `e###/setup.md` (name, what it varies, what it holds fixed, why it was added) before
  it appears in any result. An arm that exists only as a label in one chat message is exactly
  what makes side arms untrackable.

## Facts vs. interpretation

Once interpretation *has* been requested, it still stays structurally separate from the facts.
Results sections accumulate a mix of measured facts (a number, a direct comparison, an
observed behavior) and interpretation (why it happened, what it implies, whether it
generalizes). When the two blend sentence by sentence, a reader can no longer tell which
claims are load-bearing data and which are a reasoned guess about the data. Keep them
structurally separate, not just stylistically distinct:

- **Results and Findings state facts only.** "Opus 5 scored 0.772 accuracy, Sonnet-4.6 scored
  0.614" is a fact. "Backbone dominates here" or "this shows tool access matters" is
  interpretation — even if true, it doesn't belong in the same bullet as the number. Report the
  measurement plainly; don't wrap it in an evaluative lead-in.
- **Interpretation lives in exactly one place per question: a dedicated section at the end**
  (the experiment's `e###/interpretation.md`, or the topic file's Topic synthesis if the
  interpretation spans experiments) — **and that section is written only when the user has asked
  for interpretation.** Leave it absent otherwise; an absent `interpretation.md` on a question
  whose Results are complete is the correct state, not an unfinished one. Don't scatter "this suggests...", "likely because...",
  "probably driven by..." language through `results.md` — collect it in `interpretation.md`
  instead, so a reader can find every interpretive claim in one spot and weigh it as such.
- **Use interpretation sparingly.** `interpretation.md` should hold the 1-3 claims a reader actually needs
  in order to act — not a running commentary on every row of a table. If every result seems to
  need its own explanatory sentence, that usually means the table needs a clearer shape, not
  more prose.
- **When genuinely unsure whether something is fact or interpretation, report it as fact and
  let the interpretation section draw the inference explicitly** (labeled as such), rather than
  letting an unmarked "because" slip into the Results prose. An unearned causal claim is exactly
  where a reviewer or collaborator will push back hardest — keeping it isolated and labeled
  makes it easy to find and easy to defend or retract.

## Length and redundancy discipline as topics and experiments grow

Topic files and the dashboard outlive many sessions. A question answered once often gets
extended later — a new backbone, a new dataset, a rep, a follow-up run answering the same
question under one changed variable. Left unchecked, each extension adds its own subsection
that re-explains the same setup and re-lists the same caveats, and the file stops being
something a reader can skim. This is a routine failure mode, not an edge case — check for it
every time you write results back, not just when a document has visibly become unreadable.

- **Reach for structure once a paragraph is carrying more than a couple of distinct facts.**
  A topic summary or an interpretation that narrates one finding per done experiment inside a
  single run-on paragraph is the same failure as the caveat/setup duplication below, just at
  the sentence level — the reader has to parse a wall of text to pull out facts that would be
  obvious as a list. Once a paragraph would need more than about 3-4 sentences to say
  everything, split it into a short bulleted list, one bullet per question, run, or distinct
  finding, instead of chaining more clauses onto the same paragraph.
- **Performance numbers go in a markdown table, not a paragraph — this is the default, not a
  judgment call.** Any time a Results section is comparing a metric (accuracy, F1, cost,
  latency, agreement) across two or more things — reps, systems, datasets, backbones,
  ablation variants — that comparison belongs in a table with the things-being-compared as
  rows and metrics as columns, not narrated as "System A scored 0.72 while System B reached
  0.68, and on the other dataset..." A paragraph is for the one-line interpretation of what the
  table shows (see Facts vs. interpretation above), never for carrying the numbers themselves.
  This holds even for a single new row landing in an existing question — extend the table (per
  "Extend the existing table, don't clone the section" below), don't drop the new numbers into
  a sentence next to it. Rule of thumb: if you write two or more numeric comparisons in one
  sentence, or the phrase "vs." more than once in a paragraph, stop and make a table instead.
- **A bulleted breakdown is not license to write fragments.** Every bullet must still be a
  complete, self-contained sentence — subject, verb, and the actual number or claim — not a
  compressed keyword string. "SIGNOR: 0.77 acc, tools help" forces the reader to reconstruct
  what's being compared and why; "On SIGNOR, Claude Science reaches 77% accuracy with Opus 5
  but only 61% with Sonnet-4.6 under the same batch-wise protocol" doesn't. Comprehensibility
  comes before brevity: a slightly longer complete sentence beats a shorter fragment that only
  makes sense with context the reader doesn't have on that bullet alone.
- **Every topic-summary bullet follows the same three-part order: question and status, then
  action, then interpretation — in that order, every time.**
  1. **Lead with `**E### (status)**`** so the reader can match the bullet straight back to its
     experiment row and map node (e.g. `**E003 (done)**`, `**E009–E010 (planned)**`).
  2. **State the action next** — what was actually run, measured, or compared, as fact (see
     Facts vs. interpretation, above). This is where the numbers live.
  3. **Close with the interpretation** — one trailing sentence stating what the result means.
     This is always the *last* clause in the bullet, never the first and never buried before a
     trailing fact. Don't open a bullet with the verdict ("is the plan's biggest finding...")
     before the reader knows what was measured, and don't tack a plain fact onto the end after
     the interpretation has already been stated — the final clause a reader lands on should be
     the takeaway, not a stray implementation detail.
  Apply this order identically across every topic's bullets within the same document,
  including topics whose experiments form one lineage (e.g. `E004`–`E005` carried across two
  datasets): give each experiment its own bullet with its own `E### (status)` lead rather than
  folding them into an unlabeled thematic list. Consistent structure is what lets a reader who
  has learned one topic's pattern skim every other topic the same way, connecting each action
  straight to its interpretation without re-learning the shape of the prose each time.
- **Minimize redundancy for comprehensibility — the general rule the other bullets here apply.**
  State each fact once. Don't restate a number that's already in a table as a sentence of prose
  saying the same thing, don't repeat the same caveat or setup context in multiple places in
  the same document, and don't let the dashboard drift into holding content beyond its
  sanctioned one-line compression of `e###/results.md` (cap the one-line result at about 40
  words; anything longer belongs in `results.md`). Every repeated fact is one more place a
  future edit can drift out of sync with the others.
- **Extend the existing table, don't clone the section.** If a new run answers the same
  question with one more variable held constant (same protocol, new backbone; same protocol,
  new dataset), it belongs as a new row in the existing results table and a fold-in to the
  existing findings list — not a new `### <question> — <variant>` subsection with its own
  Setup/Caveats/Rebuttal-framing paragraphs restating what's already said above.
- **State a caveat once, then point to it.** If a caveat applies to every run in a question
  (e.g., "single pass, no repeats", "batch-wise not independent"), state it once, and reference
  it by name in later findings ("see caveat above") rather than re-writing the paragraph each
  time a new run is added.
- **Keep each topic-file section short** (a links line and a context paragraph): the setup,
  the numbers and the interpretation live in `e###/`, never in the topic file.
- **Keep `results.md` readable**: the Current results table, then one section per run with
  its table and a few bullet findings, one caveats list, one artifacts line. When per-run
  tables, confusion matrices or per-item numbers make it long, move them into a sibling file
  in the same `e###/` folder, linked from the run's section, and say in chat that you did.
- **Before adding to a question you didn't just answer for the first time, read its current
  length first.** If it already reads dense, flag that to the user and propose a consolidation
  (merge duplicate caveats, fold repeated setup paragraphs into `setup.md`, move numeric
  detail to a sibling file in `e###/`) before writing the new result in. Don't wait for the user to flag it as
  dense; treat that feedback, once given, as a standing bar to hold on every future edit — but
  the cleanup itself, if it involves restructuring into new files, is still something to
  propose, not just do.
