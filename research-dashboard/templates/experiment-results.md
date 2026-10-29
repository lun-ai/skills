<!--
Results file for one experiment: <dashboard dir>/e###/results.md. Facts only, no causal
language. Arms and metrics are named as defined in setup.md and not redefined here. Every
table is followed by a "Produced by:" line. Rules: references/experiment-files.md. Keep the
Current results, Execution notes and Limitations headings verbatim: scripts/check_experiments.py
looks for them.
-->
# E### results — <descriptive name>

[← E### in <Topic name>](../<topic>.md#e###) · [Setup](setup.md) · [Interpretation](interpretation.md) · [Checks](checks.md) · [Dashboard](../DASHBOARD.md)

What was run, on what, with which settings: [setup.md](setup.md). Report page, if one was
made: [../pages/e###-<slug>.html](../pages/e###-<slug>.html).

## Current results

From <run name(s)>. <One sentence on what the table compares.>

| Arm | <metric> | <metric> | n |
|---|---|---|---|
| <arm name from setup.md> | | | |

Produced by: `<script>` → `<output file>` @ `<commit>`

## <Run name> (<YYYY-MM-DD>), jobs <ids> — <reviewed by the user YYYY-MM-DD | not yet reviewed | superseded by <run name>>

<What differs from setup.md for this run, citing its Changes during execution row; otherwise
"As in setup.md.">

| Arm | <metric> | <metric> | n |
|---|---|---|---|
| | | | |

Produced by: `<script>` → `<output file>` @ `<commit>`

## Execution notes

<Rate limits, bugs, lost outputs, environment quirks found while running, not anticipated at
design time.>

## Limitations and what was not done

- <what would bias these numbers high or low>
- <which reported differences sit inside their own floor, and are claimed in neither direction>
- <what the test did not cover; the adjacent question still unmeasured, by E### if registered>
