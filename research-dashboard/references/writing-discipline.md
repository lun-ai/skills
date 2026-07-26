# Writing discipline: facts vs. interpretation, length, redundancy

[← Back to SKILL.md](../SKILL.md)

Apply this before every write-back (work loop step 9) and whenever revisiting a question that
already has content in it.

## Facts vs. interpretation

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
  (the `Takeaways` section in the area-file template, or an area-level synthesis if the
  interpretation spans questions). Don't scatter "this suggests...", "likely because...",
  "probably driven by..." language through the Results section — collect it in Takeaways
  instead, so a reader can find every interpretive claim in one spot and weigh it as such.
- **Use interpretation sparingly.** Takeaways should hold the 1-3 claims a reader actually needs
  in order to act — not a running commentary on every row of a table. If every result seems to
  need its own explanatory sentence, that usually means the table needs a clearer shape, not
  more prose.
- **When genuinely unsure whether something is fact or interpretation, report it as fact and
  let the interpretation section draw the inference explicitly** (labeled as such), rather than
  letting an unmarked "because" slip into the Results prose. An unearned causal claim is exactly
  where a reviewer or collaborator will push back hardest — keeping it isolated and labeled
  makes it easy to find and easy to defend or retract.

## Length and redundancy discipline as areas and questions grow

Area files and the dashboard outlive many sessions. A question answered once often gets
extended later — a new backbone, a new dataset, a rep, a follow-up run answering the same
question under one changed variable. Left unchecked, each extension adds its own subsection
that re-explains the same setup and re-lists the same caveats, and the file stops being
something a reader can skim. This is a routine failure mode, not an edge case — check for it
every time you write results back, not just when a document has visibly become unreadable.

- **Minimize redundancy for comprehensibility — the general rule the other bullets here apply.**
  State each fact once. Don't restate a number that's already in a table as a sentence of prose
  saying the same thing, don't repeat the same caveat or setup context in multiple places in
  the same document, and don't let the dashboard drift into holding content beyond its
  sanctioned one-line compression of the area file. Every repeated fact is one more place a
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
- **Budget roughly one screen per question in the area file** (~30-40 lines): a short setup
  note, one results table, a handful of bullet findings, one caveats list, one
  rebuttal-framing quote if applicable, one artifacts line.
- **When writing back a new result would push a section past that budget, raise it with the
  user before splitting** — don't split unprompted (this is a judgment call, see SKILL.md's
  Judgment calls section). Say what you'd move (e.g. confusion matrices, per-run tables) into a
  companion `<area>_<qN>_detail.md`, what stays (comparison table, compressed findings, a
  one-line pointer to the detail file), and let them confirm or redirect before you restructure
  the document.
- **Before adding to a question you didn't just answer for the first time, read its current
  length first.** If it already reads dense, flag that to the user and propose a consolidation
  (merge duplicate caveats, fold repeated setup paragraphs into one, move numeric detail to a
  companion file) before writing the new result in. Don't wait for the user to flag it as
  dense; treat that feedback, once given, as a standing bar to hold on every future edit — but
  the cleanup itself, if it involves restructuring into new files, is still something to
  propose, not just do.
