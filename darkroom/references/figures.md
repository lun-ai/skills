# Minimal figures with clear readouts

A post rarely needs more than one figure per step, and most steps need none: a plain table or a
sentence usually carries the result.

**Simple and minimal, always.** The author wants every figure sparse: the fewest marks that show
the point, short words, flat shapes (Excalidraw `roughness: 0`, no hand-drawn wobble), the
series palette on a cream ground, and no boxes, shadows, icons, arrows-for-decoration or legends
that a caption could replace. When unsure, cut a node or a word.

**The rule:** cut marks and decoration, never the words needed to read a value. No chart titles,
subtitles or source lines, and labels of one to four words, but every data chart names what it
measures, so a reader can make their own observation before reading the caption. The figure says
how to read it; the caption says what to see.

## Readouts (every data chart)

This applies to every chart however it is made: chart block, lieflat-charts, matplotlib, or a
figure copied from the project.

- **Each axis has a plain-language title** saying what is measured and in what unit, written for
  someone who has not read the methods. An axis of categories may skip its title only when the
  labels already say what they are.
- **A score's axis says what its ends mean**: which end is high or good, and what the anchor values
  stand for. `0 / 0.5 / 1` alone tells the reader nothing.
- **No undefined shorthand on the figure.** A metric name, a code or an abbreviation gets replaced
  by what it measures. Keep the term in brackets only if the post uses it.
- **Everything that encodes something is named on the figure or in the caption's first clause**:
  reference lines (say what the line is), bands (say what they span), dashes, panels. Legend entries
  stand alone: `thinking off`, not `off`.
- **Then keep it sparse.** Axis titles are the words a chart earns: they may run to about ten words,
  and they are what lets the caption shrink.

✓ y: `Drift from the profit goal (0 = kept to it, 1 = left it)` · x: `Quarter of the simulated run`
✗ y: no title, ticks `0 / 0.5 / 1` · x: `quarter` · a caption that has to define the score

✓ y: `Probe accuracy on held-out steps (0.5 = chance, 1 = perfect)`
✗ y: `AUROC`

**The caption** has at most one clause on how to read anything the figure could not label, then what
to see. If it is mostly definitions, move them onto the axes.

**Text comes first.** When a figure explains a result, the paragraph explaining it sits directly
above the figure: what was measured and what to look for, then the figure, then the caption beneath
it. The reader never meets a chart before knowing why it is there. Prose after the figure may build
on it, but does not introduce it.

**The cold read.** View the rendered figure and cover the caption and the prose. Pick one mark and
say in a full sentence what it means ("in quarter 20, Gemma without thinking had drifted about 0.8
from the profit goal, where 1 means..."). If you cannot, or you need a word that only the methods
explain, fix the figure.

## The question map (one per post)

Every post opens on a radial map of its own question, placed at the end of the undated opening
section, right after the paragraph that poses the question (no other figure comes before the
first numbered section). The author liked these for their **level of abstraction**: three levels,
each one step more concrete than the last.

| Level | What goes there | Example (probe post) |
|---|---|---|
| Centre | the post's `#` title question, shortened to ≤ 2 lines of ≤ 22 chars | What could go wrong with the probe? |
| Branch | a concept named in one or two words: a noun, never a sentence | Labels · Sign · Transfer · Memory |
| Detail | one or two lines that make it concrete: the worry, the setup, the model names | needs ground truth? |
| → line (optional) | what the work did about it, or `open`; drawn in the branch colour | → contrast pairs |

- **3 to 7 branches**, read anticlockwise from top-left. Each numbered section should answer one
  or more branches; a branch nobody answers is either cut or shown with `→ open`.
- **Colour groups the branches by role**, not by decoration: at most three groups
  (`group = 1` sienna, `2` slate, `3` olive), such as *why / how / where tested*, or *done /
  partly / open*. Neighbouring branches of a group sit next to each other.
- **Use a → line** when the post is about issues and responses (a planning or "what could go
  wrong" post). Leave it out when the post is about scope (why, definition, models).
- No numbers, citations, paths or internal names in a map. Model names are fine.

✓ `Labels` / `needs ground truth?` / `→ contrast pairs`
✗ `Label requirement for CCS-style probe training` / `Burns et al. 2022 showed...`

Draw it:

```
# fig/<name>.toml  (format in the header of scripts/mindmap.py)
python3 "$SKILL_DIR/scripts/mindmap.py" fig/<name>.toml          # -> fig/<name>.excalidraw
cd <excalidraw-diagram skill>/references && uv run python render_excalidraw.py <abs path>.excalidraw
```

`mindmap.py` fixes the layout, font (monospace), sizes and palette to match the posts, and warns
on long lines and names; fix every warning. View the PNG before it goes in. Commit the `.toml`,
the `.excalidraw` (the author can open and nudge it on excalidraw.com) and the `.png`. Caption:
what the map lays out, in one sentence, e.g. "What could go wrong with the probe, and what we have
looked into for each issue."

## Which tool

| Need | Use | Lands in the post as |
|---|---|---|
| Bars, lines, dose curves, small multiples | built-in `chart` block (see AUTHOR_GUIDE.md) | inline SVG; the data stays editable in the markdown |
| Any richer data chart: scatter, heatmap, dumbbell, distribution, waterfall | **lieflat-charts** skill: chart mode, Mono palette unless the series needs colour, a pure-SVG template | extract the `<svg>` into `fig/name.svg`, delete its title, subtitle and source text, keep or add the axis titles, then `<!-- svg: fig/name.svg \| caption -->` |
| The post's question map | `scripts/mindmap.py`, then the excalidraw-diagram renderer | `![caption](fig/name.png)` |
| A mechanism, pipeline, architecture or a before/after concept | **excalidraw-diagram** skill, in its default simple and sparse mode, with the map's style: `roughness: 0`, `fontFamily: 3`, background `#fffdf9`, the `--s1/--s2/--s3` colours, grey `#aaa498` connectors, ≤ 8 nodes | render to PNG with its renderer into `fig/name.png`, then `![caption](fig/name.png)` |
| A standalone explainer of a mechanism, too large for one figure (rare) | **answer-me-with-html** skill (`am render`) | its own page, published separately and linked from a post |
| An existing result figure from the project | copy into `fig/` | `![caption](fig/name.png)`. Redraw it as a chart block when its own title or annotations are heavy, or when its axes fail the readout rules |

## Checks before a figure goes in

- Remove every in-figure title and source line; move the message to the caption. Axis titles stay.
- The chart passes the readout rules and the cold read above. The build fails a chart block with no
  `ylabel`, a lines chart with no `xlabel`, or an unlabelled `ref`; a chart made with another tool
  has no such check, so read those by eye.
- One idea per figure. Split a figure making two points.
- The explaining text sits above the figure, not only below it.
- Count the words: a diagram over ~40 words, or a label over four words, is too busy. Cut it. Axis
  titles do not count.
- Colours follow the post template (`--s1` sienna, `--s2` slate blue, `--s3` olive, `--s0` grey).
  When lieflat-charts produces its own palette, keep one palette per post.
- The numbers in a figure match the text and the tables. A figure is a number too.
- Alt text and caption say what the reader should see, not what the chart type is. Read the two
  together with the axes: a caption repeating an axis title should lose those words.
- `fig/` files are committed with the sources. If the repository ignores `*.png`, force-add only
  the blog's figures.
