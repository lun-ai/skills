# The work loop, per experiment

1. **When a new experiment is needed, register it and invoke the `grilling` skill before
   building anything.** A new experiment is any *test* whose design has not yet been agreed
   with the user, not just any new *training run*: a new question, arm or condition, a new
   dataset or split, a new metric or grading scheme, a confound-isolating comparison (step 9),
   a scope change surfaced by a smoke test, or an offline analysis producing a number the user
   might act on (re-scoring stored predictions on a different subset, a resampling estimate, a
   selection-bias or power simulation). Costing nothing and training nothing does not make a
   test exempt: a free re-score that changes which arm looks best is a new experiment. First
   reserve its `E###` and add it to the map as `planned`
   ([research-map.md](research-map.md)). A new *arm* inside an already-agreed experiment is
   grilled the same way but does not take a new number. Let grilling interview the user about
   the hypothesis, the arms and what each holds fixed, the dataset, the metric, the budget and
   the stopping point. Then write the agreed design into the experiment's "Setup and arms" and
   "Implementation plan" before implementing. Reruns, resumes and bug-fix restarts of an
   already-agreed design need neither grilling nor a number.
2. **Decide implementation strategy with the user before building.** If there's more than one
   reasonable way to instrument or measure something, say so and let them pick, especially
   when one option adds a schema field or structural change and another doesn't. Prefer the
   option that reuses an existing artifact (a log file, an existing table, an `impl:` node
   already on the map) over inventing a parallel one, unless the user wants otherwise.
3. **Post the empirical setting block, then execute.** Before the first command of any
   empirical test, including a free offline re-analysis, post the block
   ([setting-block.md](setting-block.md)) in chat, unprompted, every time. Then proceed
   without waiting, with three exceptions: the test is a new experiment still being grilled
   (step 1), it spends real money or shared wall-clock, or the block itself surfaced a design
   problem. In those cases stop on the block and let the user answer.
4. **Smoke test before scaling up.** Before committing real wall-clock or API cost, run the
   smallest version that can surface a design flaw: one item, one seed. This matters most when
   a design choice is itself a hypothesis about system behavior ("will a shared step budget
   across two tools starve the agent before it can answer?"). A cheap test turns that into a
   fact before you pay for the full run, and often changes the plan.
5. **Implement the minimal instrumentation.** No fields, flags or abstractions beyond what the
   experiment needs. If the user steers toward "simpler, non-redundant" over "more
   structured", take it. A log-only capture beats a new schema field when nothing downstream
   queries it.
6. **Run it**, respecting shared infrastructure limits (rate limits on shared egress IPs,
   cluster off-peak windows) rather than assuming your process is the only consumer. Set the
   map node to `running`.
7. **Analyze with verification, not assertion.** Build the analysis as an executable artifact
   (notebook, script) and actually run it, confirming zero errors, rather than hand-computing or
   eyeballing numbers into prose. Regenerate and re-run it whenever new data lands; never
   hand-edit stale output.
8. **Sanity-check aggregation before trusting it.** A bad regex, a glob that mishandles spaces
   in filenames, an off-by-one in a join key: these produce plausible wrong numbers, not
   crashes. Spot-check one aggregated data point against a manual read of the underlying file
   before reporting the aggregate.
9. **Isolate confounded variables with a third comparison point**, not just two. If a result
   could be explained by either of two factors ("less source access" vs. "worse
   architecture"), add an arm that holds one fixed while varying the other. The write-up can
   then say which one actually moved the number.
10. **Report dual metrics when a comparison isn't apples-to-apples.** If two systems produce
   results in different identity spaces (one returns structured paper IDs, another arbitrary
   URLs), don't collapse to one number. Report the raw count and the resolved or comparable
   count, with the resolution rate alongside, so the gap is visible rather than baked in.
11. **Name and register any arm you added**, including ones created autonomously during a
   smoke test or a confound-isolating comparison, in the experiment's arm table with a
   descriptive name, *before* reporting anything about it.
12. **Write the result back** in three places: the topic file (Results, and Limitations and
   what was not done; Takeaways only if interpretation was asked for), the experiment row
   (Status, Effort actuals if they moved, and the one-line column, which states *what was
   measured* unless interpretation was requested), and the map (status class, Updated date,
   approved job IDs). Append the producing job's ID to the experiment heading once that job
   has finished and the user has approved its results. Run `scripts/check_map.py`. Disclose
   any exception to a stated cross-cutting invariant in Cross-cutting notes. Don't let a
   necessary core-library fix pass silently because the plan said "no core-library changes".
13. **A finding from a scratch analysis is written back like any other.** A test run from a
   scratch directory with nothing committed still produced a number the user may act on, so it
   gets a home: its own `E###` if its design was new, otherwise a named subsection under the
   experiment it re-analyses, with its setting block, its limitations and the path to the
   scratch script. Never end a turn offering to record it "if useful". Offer the
   *interpretation*, never the record. If you genuinely cannot place it, say where the script
   lives and that it is unfiled, so it stays findable.
