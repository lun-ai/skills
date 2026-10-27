# Figures with little text

A post rarely needs more than one figure per step, and most steps need none: a plain table or a
sentence usually carries the result.

**Simple and minimal, always.** The author wants every figure sparse: the fewest marks that show
the point, short words, flat shapes (Excalidraw `roughness: 0`, no hand-drawn wobble), the
series palette on a cream ground, and no boxes, shadows, icons, arrows-for-decoration or legends
that a caption could replace. When unsure, cut a node or a word.

**The rule:** a figure shows; the caption speaks. No chart titles, no subtitles, no source lines,
no axis titles unless the unit is ambiguous (then three words at most), short legend names, labels
of one to four words. If a reader needs a sentence to read the figure, that sentence is the caption.

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
| Any richer data chart: scatter, heatmap, dumbbell, distribution, waterfall | **lieflat-charts** skill: chart mode, Mono palette unless the series needs colour, a pure-SVG template | extract the `<svg>` into `fig/name.svg`, delete its title, subtitle and source text, then `<!-- svg: fig/name.svg \| caption -->` |
| The post's question map | `scripts/mindmap.py`, then the excalidraw-diagram renderer | `![caption](fig/name.png)` |
| A mechanism, pipeline, architecture or a before/after concept | **excalidraw-diagram** skill, in its default simple and sparse mode, with the map's style: `roughness: 0`, `fontFamily: 3`, background `#fffdf9`, the `--s1/--s2/--s3` colours, grey `#aaa498` connectors, ≤ 8 nodes | render to PNG with its renderer into `fig/name.png`, then `![caption](fig/name.png)` |
| A standalone explainer of a mechanism, too large for one figure (rare) | **answer-me-with-html** skill (`am render`) | its own page, published separately and linked from a post |
| An existing result figure from the project | copy into `fig/` | `![caption](fig/name.png)`. Redraw it as a chart block when its own title or annotations are heavy |

## Checks before a figure goes in

- Remove every in-figure title and source line; move the message to the caption.
- One idea per figure. Split a figure making two points.
- Count the words: a diagram over ~40 words, or a label over four words, is too busy. Cut it.
- Colours follow the post template (`--s1` sienna, `--s2` slate blue, `--s3` olive, `--s0` grey).
  When lieflat-charts produces its own palette, keep one palette per post.
- The numbers in a figure match the text and the tables. A figure is a number too.
- Alt text and caption say what the reader should see, not what the chart type is.
- `fig/` files are committed with the sources. If the repository ignores `*.png`, force-add only
  the blog's figures.
