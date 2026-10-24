<!--
The empirical setting block: posted in chat before the first command of any empirical test,
and kept in the experiment's "Setup and arms" section. Rules: references/setting-block.md.
-->
**Empirical setting — E### / <short descriptive name of the test>**

- **Question in words** — what this test is meant to settle, as a question, not as a label.
- **Provenance** — what is reused exactly as-is (predictions from an earlier run, stored
  outputs, a published table; cite the source experiment by E#), what is newly computed, and
  whether anything is trained or re-trained. State "nothing new is trained" explicitly when
  true, and say what makes the reuse legitimate.
- **Populations** — every group of items scored over: name, n, one plain sentence of what it
  is and where it came from; a table once there is more than one. Give each group's outcome
  distribution (mean and range) when groups will be compared.
- **What varies** — the one thing this test changes, named, with its levels.
- **What is held fixed** — listed explicitly, not left implied.
- **Procedure** — the steps in order, in plain words, including any resampling or simulation
  and its repeat count.
- **Metrics** — each defined in one clause, with units and direction (higher/lower is better)
  and what it ignores.
- **Derived quantities and decision rules** — any threshold a verdict will hinge on (a
  discrimination floor, a smallest difference you would believe, a pass mark), defined with
  its computation, before the numbers.
- **What this cannot show** — the inference boundary, written before the result exists.
- **Cost and footprint** — wall-clock, $, shared infrastructure touched, scratch vs. repo,
  which files are created or changed, whether anything is committed.
