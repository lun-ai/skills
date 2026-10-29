<!--
Dashboard template. One per effort, usually DASHBOARD.md. Section order is fixed:
map first, then the experiment list, then topic summaries. render_map.py and check_map.py
locate the sections by these exact headings, so keep them verbatim. Fill in the registry and
the experiment list, then run render_map.py: it writes the ### Map section and the pages/
files it links to. HTML pages for the effort live in pages/ beside this file. Each experiment's
setup, results and interpretation live in e###/ beside this file
(references/experiment-files.md); link every one that exists from the registry's Links cell.
-->
# <Effort name> — Dashboard

<One paragraph: what this effort is for, what it deliberately does not track, and where the
reference results it extends live.>

## Research map

Next experiment number: **E001** · map updated <YYYY-MM-DD>

### Map

Format: answer-me-with-html · open the map: [pages/research-map.html](pages/research-map.html) · draft: [pages/research-map.am.md](pages/research-map.am.md)

Generated from the registry by `scripts/render_map.py`; do not edit the page or the draft by hand.

### Registry

| ID | Kind | Name | Topic | Created | Updated | Attributes | Links |
|---|---|---|---|---|---|---|---|
| topic:<slug> | topic | <Topic name> | — | <date> | <date> | data: <datasets, n> | [topic file](<topic>.md) |
| impl:<slug> | implementation | <what it is> | — | <date> | <date> | code: <path> | [source](<path>) |
| E001 | experiment | <descriptive name> | topic:<slug> | <date> | <date> | data: <set, split, n> · model: <backbone> · uses: impl:<slug> · from: — · jobs: — | [topic](<topic>.md#e001) · [setup](e001/setup.md) · [results](e001/results.md) |

## Experiments

| E# | Topic | Question | Status | Effort | One-line result |
|---|---|---|---|---|---|
| [E001](<topic>.md#e001) | <Topic name> | <question, as a question> | Planned / Designing / Running / Done / Abandoned | ~X days, $Y (actuals once known) | <what was measured, in at most ~40 words; a verdict only if interpretation was requested> |

Sequencing: <which experiments are independent, which are blocked on which (by E#), which
go last because they absorb what the others produce>

## Topics

### [<Topic name> →](<topic>.md)
<2-4 sentences while the topic has one main result. Once it has several, use one bullet per
finished experiment, each starting with **E### (status)**, then what was done, then what came
out. Use the same format in every topic of this document. See
references/writing-discipline.md.>

## Cross-cutting notes
- <shared invariants: "all experiments reuse X untouched", "no core-library changes except...">
- <any exception to those invariants, stated explicitly, with a link to where it's detailed>
