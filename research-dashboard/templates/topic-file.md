<!--
Topic file template: one per topic, holding the detail of every experiment registered under
that topic. Experiments appear in E# order. The <a id> anchor is the stable link target;
the dashboard links to <topic>.md#e###, so rewording a question never breaks a link.
Instantiate or extend per task. Drop sections that would be empty, except Limitations.
-->
# <Topic name>

<One line: what this topic covers. Link back to the dashboard: [← Dashboard](DASHBOARD.md)>

<a id="e007"></a>
## E007 — <question, as a question> (job <id>)
<!-- job ID(s) appended only once the job finished and the user approved its results.
     Lineage, if any: "From E001 (reuses its frozen v6 tree)." -->

<Report page, only if one was made: [pages/e007-<slug>.html](pages/e007-<slug>.html), rendered
with the answer-me-with-html skill into pages/ (references/reporting.md#html-pages)>

### Context / motivation
<why this question, what's already known, what's missing>

### Setup and arms
<the agreed empirical setting block for this experiment, kept as written at design time, plus
anything that changed during execution. Once there are more than ~3 arms, make the arms a
table keyed by descriptive name: name | plain-language description | what it varies | what
it holds fixed | status. Register every arm created mid-investigation here before reporting
anything about it>

### Implementation plan
<mechanism: what gets built or instrumented (name the impl: node from the map), what stays
untouched, effort estimate>

### Infra notes (found during execution, not anticipated at plan time)
<rate limits, bugs, environment quirks hit along the way. These are often as valuable as the
headline result, so keep them once the question is answered>

### Results
<facts only, never context-free. Open by naming what was run under which settings (or point
at Setup and arms), then the numbers. Use Markdown tables for any metric compared across
arms, systems, datasets or variants, not prose, keyed by the arms' descriptive names, plus links
to the notebooks/scripts that produced them. No causal language ("because", "suggests",
"likely driven by") here>

### Limitations and what was not done
<facts about the measurement, so always written: what would bias these numbers high or low,
which reported differences sit inside their own floor (and are therefore claimed in neither
direction), what the test did not cover, and which adjacent question remains unmeasured>

### Takeaways — WRITE ONLY IF THE USER ASKED FOR INTERPRETATION
<omit entirely otherwise. When asked: interpretation only, and sparse. Give the 1-3 claims a
reader needs to act on, not a running commentary on every row above>
