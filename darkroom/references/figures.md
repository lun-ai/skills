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

## The idea map (one per post)

Every post opens on a map that places it in the series, at the end of the undated opening section,
right after the paragraph that poses the question (no other figure comes before the first numbered
section). The author wants it for **continuity**: a reader coming from the previous post should see
at once how this one follows from it, instead of having to load a new mental context. This matters
most when explaining the work to people.

**It is a graph, not a list.** Think of the commit graph of a codebase. Time runs left to right,
one band per post, and the current post's band is tinted. Each node is one idea or experiment, and
a lane is a thread of work. The shape tells the story, so a reader sees it before reading a word:

| What happened | How it is drawn | In the spec |
|---|---|---|
| One idea led to the next | a line along a lane | `after = ["id"]` |
| The work split into two threads | a line stepping to another lane | `after` plus a different `lane` |
| Two threads fed one experiment | two lines meeting at a node | `after = ["a", "b"]` |
| An idea held up | a filled node with a tick | `status = "held"` |
| An idea was refuted, a dead end | a filled node with a cross, and no line onward | `status = "refuted"` |
| An idea was replaced by a better version | a dashed ring, and a dashed arrow into the idea that replaced it | `status = "revised"`, and `revises = "id"` on the new idea |
| A question is not settled yet | a ring with a question mark | `status = "open"` |
| A result sent the work back to an earlier idea | a dashed arrow arcing back | `back_to = "id"` |
| The ideas this post is about | a dark ring around each node, inside the tinted band | nodes of the last `[[page]]` |
| How belief moved | a meter filled to the credence now, with a tick at the credence before | `credence`, `credence_was` |

**Show first, write last**, the way a paper's abstract gives an easy way in with very little text.
Before writing any words on a map, ask whether a mark, a line or the position already says it:

- **A node carries a name, never a sentence**: one to four words, in the words the posts use for
  it (`Linear probe`, `Long run`). The earlier posts already explained it, and the mark shows how
  it turned out.
- **A node carries its experiment number** (`exp = "E004"`) whenever the project numbers its
  experiments, as the research-dashboard skill does. The author wants it as a callback to the
  experiment they remember and as a tracker across posts. Use the project's own number exactly,
  give a range for a node that covers several runs (`E004-E006`), leave it off an idea that was
  never run, and never invent a number. The same number appears where the post's section reports
  that experiment, so the map and the text point at each other.
- **Full sentences are kept for the two things no mark can say**, both about the current post
  only: the question it asks (1 or 2) and the result that would refute it (1 or 2). Each is one
  complete, short sentence of at most 110 characters, never a fragment or a noun label.
- Nothing else is written: no "what this post does" line (the tinted band and the lines into it
  say that), no list of focuses (they are the ringed nodes), no reason for the credence (the post
  gives it), no numbers besides the credence and the experiment numbers, no citations, paths or
  other internal names.

✓ node `Steer middle layers` with a tick · question `Does the steered goal still hold at the end of a long run?`
✗ node `Steering along the probe direction changed what the model chose` · question `Long-run stability`

What goes in:

- **Only the ideas the current post builds on or answers**, plus the dead ends and revisions that
  explain why the work took this path. At most 12 nodes, 7 columns and 3 lanes; an earlier post
  usually shrinks to one to three nodes. The map stops at the current post: nothing from later
  posts.
- **The same idea keeps the same id, name and lane in every post's map**, so the series reads as
  one growing graph. Each map is the previous one plus this post's band, with older detail trimmed.
  A node's status is what the reader knows by the end of the current post, so an idea shown open
  in its own post turns to held or refuted in the next one's map.
- **A map with no branch, dead end, revision or loop is suspect.** Work rarely runs in a straight
  line; go back to the retrospective for what was tried and dropped before accepting one lane.
  Never invent a branch to make a map look richer: every node and line traces to the record.
- The first post may open with a band labelled `Before`, holding the one or two ideas the work
  started from.
- **A refuting condition is a result that could have come out**, stated so a reader could check it
  against the post's own figures. "The idea fails if the results are bad" refutes nothing.
- **Credence belongs to the author**, like the refuting conditions: take them from the record (a
  plan file, a decision note) or ask. Never guess. A percentage draws the meter; a word such as
  `likely` is shown as text.

Draw it:

```
# fig/<name>.toml  (format in the header of scripts/ideamap.py)
python3 "$SKILL_DIR/scripts/ideamap.py" fig/<name>.toml          # -> fig/<name>.excalidraw
cd <excalidraw-diagram skill>/references && uv run python render_excalidraw.py <abs path>.excalidraw
```

`ideamap.py` places the nodes, routes the lines, fixes the font (monospace), sizes and palette to
match the posts, and adds a key for the marks used. It warns on a line running through a node
(move one to another lane), names that are sentences, experiment numbers that wrap, sentences that are labels, too many nodes
and a missing credence; fix every warning. Then view the PNG and give it the cold read: cover the
text strip and say, from the drawing alone, what was tried, what failed, what was revised and what
this post takes on. If you cannot, fix the lanes or the statuses, not the wording. Commit the
`.toml`, the `.excalidraw` (the author can open and nudge it on excalidraw.com) and the `.png`.
Caption: one sentence on what the map shows, e.g. "How the long-run test follows from the first
two posts, and what would prove it wrong."

## The work history (one per post)

Every post closes on a diagram of the work it reports, in a last section titled
`## How the work unfolded`, after the last numbered section and before any teaser and the
references. The author asked for it in these words: for each task, why the work was done, what it
found, and why that prompted follow-up work, in a connected diagram. They like it because it
summarises the actions taken to complete the investigation, so a reader can check and recall them.

It pairs with the idea map and does a different job:

| | Idea map (opens the post) | Work history (closes the post) |
|---|---|---|
| Scope | the series up to this post | this post only |
| A node is | an idea: a name and a status mark | a task: why it was done and what it found |
| An arrow says | this followed from that | why that finding prompted this task |
| Text | minimal, marks first | three short lines per task, by design |
| The reader uses it to | orient before reading | check and recall what was done |

Each task is a numbered box with three kinds of line, each in its own colour:

| Line | Colour | Says | Example |
|---|---|---|---|
| title | ink | the action, as a verb phrase, then its experiment number and date | `4  Compare two halves of the texts · E023 · 20 Nov` |
| `why` | slate | the reason the task was done | `a lens should not depend on which texts it saw` |
| `found` | sienna | what was measured: one finding, or two when they differ by model or setting | `Gemma: none below layer 27; one text 9,000x too large` |
| `so`, on the arrow | olive | why that finding prompted the next task | `Gemma: is that one text the cause?` |

- **One box per task the post reports**, numbered in the order of the post's sections, at most 12.
  Join steps that share one finding. A task the post does not report has no box.
- **Every task but the first hangs from the finding that prompted it** (`after`), and its arrow
  says why (`so`). When one finding prompted two tasks the chain forks; the script keeps the first
  follow-up in the column and moves the others to the right. The boxes where the work started
  and where it has got to are tinted.
- **Lines are short and plain, not full sentences**: a clause of at most 90 characters, lower
  case, no full stop, in the words of the post. A `so` line is often the question the finding
  raised.
- **`found` reports what was measured**, with the numbers the section gives. Numbers are welcome
  here and must match the text and tables exactly.
- **`why` and `so` are reasons, so they are sourced or asked for.** Take them from the plan files,
  decision notes and commit messages gathered in the retrospective. Where the record does not say
  why a task was done or why it led to the next, ask the author. Never invent a motive to make the
  chain connect.
- **It agrees with the idea map.** The tasks carry the same experiment numbers as the map's nodes
  for this post, and a branch on one appears on the other.
- This figure is exempt from the word count and the no-boxes rule in this file. It keeps the
  others: no title or source line, the series palette, no paths or internal names besides the
  experiment number.

✓ why `know the cost before a full fit` · found `about two minutes per text` · so `1,000 texts is about 35 GPU-hours: try 100 first`
✗ why `Timing` · found `The results were informative` · so `next step`

Above the figure goes one short paragraph saying how to read it: what a box is, what the three
colours mean, and where the chain forks. Caption: what the chain shows as a whole, in one or two
sentences, e.g. "Each finding is the reason for the next task. Gemma needed three further checks
before a first reading; Qwen needed only more text."

Draw it:

```
# fig/<name>-history.toml  (format in the header of scripts/history.py)
python3 "$SKILL_DIR/scripts/history.py" fig/<name>-history.toml  # -> fig/<name>-history.excalidraw
cd <excalidraw-diagram skill>/references && uv run python render_excalidraw.py <abs path>.excalidraw
```

`history.py` numbers and places the boxes, wraps the lines, routes the forks and warns on a task
with no `why`, no `after` or no `so`, on long lines, and on more than two columns; fix every
warning. View the PNG, then read it against the post: every box has a section, every number
matches, and every `why` and `so` traces to the record or the author. Commit the `.toml`, the
`.excalidraw` and the `.png`.

## Which tool

| Need | Use | Lands in the post as |
|---|---|---|
| Bars, lines, dose curves, small multiples | built-in `chart` block (see AUTHOR_GUIDE.md) | inline SVG; the data stays editable in the markdown |
| Any richer data chart: scatter, heatmap, dumbbell, distribution, waterfall | **lieflat-charts** skill: chart mode, Mono palette unless the series needs colour, a pure-SVG template | extract the `<svg>` into `fig/name.svg`, delete its title, subtitle and source text, keep or add the axis titles, then `<!-- svg: fig/name.svg \| caption -->` |
| The post's idea map | `scripts/ideamap.py`, then the excalidraw-diagram renderer | `![caption](fig/name.png)` |
| The post's work history | `scripts/history.py`, then the excalidraw-diagram renderer | `![caption](fig/name-history.png)` |
| A mechanism, pipeline, architecture or a before/after concept | **excalidraw-diagram** skill, in its default simple and sparse mode, with the idea map's style: `roughness: 0`, `fontFamily: 3`, background `#fffdf9`, the `--s1/--s2/--s3` colours, grey `#aaa498` connectors, ≤ 8 nodes | render to PNG with its renderer into `fig/name.png`, then `![caption](fig/name.png)` |
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
  titles do not count, and the idea map and the work history follow their own limits above.
- Colours follow the post template (`--s1` sienna, `--s2` slate blue, `--s3` olive, `--s0` grey).
  When lieflat-charts produces its own palette, keep one palette per post.
- The numbers in a figure match the text and the tables. A figure is a number too.
- Alt text and caption say what the reader should see, not what the chart type is. Read the two
  together with the axes: a caption repeating an axis title should lose those words.
- `fig/` files are committed with the sources. If the repository ignores `*.png`, force-add only
  the blog's figures.
