# Naming and plain language

Write for a collaborator who knows the field but not this codebase. Use short sentences and
everyday words. Expand jargon and internal shorthand on first use in a session. Say what a
config *does* rather than quoting its filename. Filenames, flags and script paths belong in an
artifacts line at the end of a section, not in the sentence carrying the finding.

- **No single-word stand-in for an empirical setting.** Never refer to an arm, condition,
  dataset variant, grading scheme, prompt variant or model configuration by an acronym (`SR`,
  `OC`), a clipped word (`ctx`, `regrade`, `gold`), or a one-word nickname (`oracle`,
  `baseline`, `defeater`). This applies in prose, chat, table keys and dashboard lines. These
  labels look obvious to whoever coined them and are opaque to everyone else, including the
  same user a week later. Say what the setting is, in a phrase: "the run where the model is
  given the gold-standard abstracts as context", not "oracle"; "answers re-scored against the
  SIGNOR curated labels", not "regrade"; "sentence retrieval only, no full-text access", not
  "SR-only".
- **Give every topic, implementation, experiment, arm, condition, run and ablation a
  descriptive name** when it is created: `no-retrieval`, `gold-abstracts-in-context`,
  `shared-step-budget`, `signor-holdout`. The name says what the thing *is*, so it needs no
  lookup. After the first full description in a reply or section, that name carries later
  mentions and serves as the table key.
- **`E###` is the one sanctioned bare symbol**, because the research map's registry defines
  every number in one place and the number is global, so it means the same thing in every
  topic. Even so, pair it with the experiment's subject on first mention in a reply
  (`E003, the SciFact sealed-holdout tree`).
- **Other short codes (`T2`, `C1`, `run4`, `v6`) never travel alone.** A symbolic tag may
  follow the descriptive name once in parentheses, when it is the anchor a reader needs to
  match a table row: `the no-retrieval arm (T2)`. Never write a sentence whose meaning depends
  on remembering what `T2` was. If the codebase already uses a one-word abbreviation,
  translate it into the plain phrase and mention the code at most once, in parentheses. To
  point at an arm from another experiment, combine the two: `E001's frozen tree (v6)`.
- **Table and figure labels use the descriptive name as the row/column key**, with any code as
  a secondary column, not the reverse. The exception is the experiment number, which may lead
  a row because it is the global key.
- **An arm you created mid-run must be registered before it is reported**
  ([work-loop.md](work-loop.md) step 11), with what it varies, what it holds fixed, and why it
  was added. An arm that exists only as a label in one chat message is the main source of the
  tracking problem this rule prevents. Once an experiment has more than about three arms, keep
  the arm table as a glossary and point later reports at it instead of re-explaining the arms.
