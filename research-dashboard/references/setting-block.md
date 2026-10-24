# The empirical setting block

**Before running any empirical test, post this block in chat, unprompted, before the first
command.** It is a primer: a reader who was not inside the run should be able to say what is
being measured, what changes, what does not, and what the test could not settle, *before* any
number exists to argue about. Writing it is also the cheapest design review there is. A block
you cannot fill in is a test you have not finished designing.

Template: [../templates/setting-block.md](../templates/setting-block.md). Head it with the
experiment number, `E### / <test name>`, so the block can be matched to its map node.

## What counts as an empirical test

Any procedure whose output is a number, ordering or verdict the user might act on. These are
explicitly included, because they are the ones that get skipped: re-scoring predictions
already on disk; restricting or re-slicing an evaluation set; a bootstrap, permutation or
resampling estimate; a selection-bias, power or noise-floor simulation; a re-grade under a
different rubric; and any "quick check" in a scratch directory. Training nothing, costing
nothing and committing nothing do not exempt a test from the block.

Not included: reading code, inspecting a file, counting rows to orient yourself, or re-running
an already-reported test unchanged to confirm it reproduces.

## Field guidance

- **Provenance.** Say what makes the reuse legitimate: "in cross-validation each item was
  predicted by a model that had not seen it, so narrowing the scoring set afterwards leaks
  nothing". Cite reused outputs by their source experiment number (`predictions from E004`).
- **Populations.** Give each group's outcome distribution when groups will be compared.
  Whether one group lies *beyond* another is usually the crux, and n alone does not show it.
- **Metrics.** Say what each one ignores, for example "ranking ignores whether the values are
  right".
- **Derived quantities.** Define these before the numbers, not in the paragraph that uses
  them. For small evaluation sets this means the floor and the selection inflation from
  [small-eval-sets.md](small-eval-sets.md).
- **Cost and footprint.** "Free: re-scores existing predictions, writes one scratch script" is
  a valid and useful answer.

## Length

Keep only the lines that carry information: a free re-score gets a short block, not a
ceremonial one. But never drop **what varies**, **what is held fixed**, **the metric
definitions** or **what this cannot show**. Those four cannot be reconstructed afterwards, and
they are exactly what users ask for when they were omitted. When one primer covers several
parts, state the shared setting once, then give **one varies/held-fixed pair per part**.
