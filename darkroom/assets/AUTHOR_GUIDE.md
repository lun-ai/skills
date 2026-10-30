# Editing this blog

You edit the markdown files (`part1.md`, `part2.md`, …). The pages in `site/` are rebuilt from
them; never edit those by hand. When you are done, ask Claude to "rebuild". Your edits are
committed on their own first, any number you changed is checked against its source, and the
posts are republished to the same links.

## What gets published

- The `#` heading is the post title.
- The header block at the top (`part`, `status`, `date`) is not shown. `status: unfinished` adds a
  work-in-progress banner; `date` sets the date in the line above the title.
- Everything between the title and the first `##` heading is working notes: not published.
- `## Important notes …` and `## Open points …` sections are not published. Put requests for the
  next build there.
- Anything inside `<!-- … -->` is not published. Use it for notes to yourself, or to hide a
  paragraph or table without deleting it.
- Every `##` heading appears in the "In this post" list; `###` headings join it when a post has
  fewer than three `##` sections.
- LaTeX-style quotes ``` ``like this'' ``` become curly quotes.

## Charts: data lives in the markdown

Write a fenced block tagged `chart`. Charts carry no titles, but each axis says in plain words what
it measures, and a score's axis says what its ends mean. Say what the reader should see in the
`caption`. The build reports `CHECK` on a chart missing `ylabel`, a lines chart missing `xlabel`, or
a `ref` with no label.

````
```chart
type: bars
ylabel: Share of claims judged correctly (1 = all of them)
xlabel: Type of claim
groups: SUPPORT, REFUTE, all
series: agent alone = 0.80, 0.73, 0.75
series: with objections = 0.87, 0.27, 0.62
y: 0, 1
caption: Objections helped true claims a little and broke false ones.
```
````

| Key | Used by | Meaning |
|---|---|---|
| `type` | all | `bars` or `lines` |
| `series: name = v1, v2, …` | bars, lines | one per series; a legend appears only for two or more |
| `groups: a, b, c` | bars | category labels under the bars |
| `x: a, b, c` | lines | labels along the bottom |
| `panel: name` | lines | starts a small multiple; the `series` lines after it belong to it |
| `y: low, high` | bars, lines | value range; automatic if left out |
| `ref: value label` | bars, lines | dashed reference line, with a label saying what it is |
| `values: off` | bars | hide the numbers above bars |
| `ylabel: text` | bars, lines | required: what the values measure, in plain words, with the meaning of a score's ends; shown above the plot |
| `xlabel: text` | bars, lines | what runs along the bottom; required for lines, and for bars unless the group labels already say it |
| `caption: text` | all | the sentence under the chart |

## Figures

- `![caption](fig/name.png)` on its own line becomes a framed figure with that caption.
- `<!-- svg: fig/name.svg | caption -->` inlines an SVG file, for charts made with another tool.
- Keep text inside figures to a minimum: no titles, short labels, but keep the axis titles. The
  figure says how to read it; the caption says what to see.
- Put the text explaining a result above its figure, with the caption beneath the figure.
- Each post opens on a question map (`fig/<name>.png`). To change it, edit `fig/<name>.toml`
  (question, branches, short lines) and ask for a rebuild, or nudge `fig/<name>.excalidraw` on
  excalidraw.com and export the PNG over the old one.
