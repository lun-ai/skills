# Figures with little text

A post rarely needs more than one figure per step, and most steps need none: a plain table or a
sentence usually carries the result.

**The rule:** a figure shows; the caption speaks. No chart titles, no subtitles, no source lines,
no axis titles unless the unit is ambiguous (then three words at most), short legend names, labels
of one to four words. If a reader needs a sentence to read the figure, that sentence is the caption.

## Which tool

| Need | Use | Lands in the post as |
|---|---|---|
| Bars, lines, dose curves, small multiples | built-in `chart` block (see AUTHOR_GUIDE.md) | inline SVG; the data stays editable in the markdown |
| Any richer data chart: scatter, heatmap, dumbbell, distribution, waterfall | **lieflat-charts** skill: chart mode, Mono palette unless the series needs colour, a pure-SVG template | extract the `<svg>` into `fig/name.svg`, delete its title, subtitle and source text, then `<!-- svg: fig/name.svg \| caption -->` |
| A mechanism, pipeline, architecture or a before/after concept | **excalidraw-diagram** skill, in its default simple and sparse mode | render to PNG with its renderer into `fig/name.png`, then `![caption](fig/name.png)` |
| A standalone explainer of a mechanism, too large for one figure (rare) | **answer-me-with-html** skill (`am render`) | its own page, published separately and linked from a post |
| An existing result figure from the project | copy into `fig/` | `![caption](fig/name.png)`. Redraw it as a chart block when its own title or annotations are heavy |

## Checks before a figure goes in

- Remove every in-figure title and source line; move the message to the caption.
- One idea per figure. Split a figure making two points.
- Colours follow the post template (`--s1` sienna, `--s2` slate blue, `--s3` olive, `--s0` grey).
  When lieflat-charts produces its own palette, keep one palette per post.
- The numbers in a figure match the text and the tables. A figure is a number too.
- Alt text and caption say what the reader should see, not what the chart type is.
- `fig/` files are committed with the sources. If the repository ignores `*.png`, force-add only
  the blog's figures.
