<!--
Dashboard template. One per effort, usually DASHBOARD.md. Section order is fixed:
map first, then the experiment list, then topic summaries. check_map.py locates the
sections by these exact headings, so keep them verbatim.
-->
# <Effort name> — Dashboard

<One paragraph: what this effort is for, what it deliberately does not track, and where the
reference results it extends live.>

## Research map

Next experiment number: **E001** · map updated <YYYY-MM-DD>

### Map

```mermaid
flowchart LR
  subgraph topic_<slug>["<Topic name>"]
    E001["E001 · <descriptive name><br/><YYYY-MM-DD>"]
  end
  impl_<slug>{{"impl:<slug><br/><what it is>"}}
  impl_<slug> --> E001

  classDef planned stroke-dasharray:4 3
  classDef running stroke-width:3px
  classDef done fill:#e6f4ea,stroke:#2e7d32
  classDef abandoned fill:#eeeeee,stroke:#9e9e9e,color:#757575
  class E001 planned
```

### Registry

| ID | Kind | Name | Topic | Created | Updated | Attributes | Links |
|---|---|---|---|---|---|---|---|
| topic:<slug> | topic | <Topic name> | — | <date> | <date> | data: <datasets, n> | [topic file](<topic>.md) |
| impl:<slug> | implementation | <what it is> | — | <date> | <date> | code: <path> | [source](<path>) |
| E001 | experiment | <descriptive name> | topic:<slug> | <date> | <date> | data: <set, split, n> · model: <backbone> · uses: impl:<slug> · from: — · jobs: — | [E001](<topic>.md#e001) |

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
