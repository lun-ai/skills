---
name: slides
description: >
  Sub-skill of darkroom. Build or revise a presentation as a web deck the author edits in the
  browser (a Slides artifact on claude.ai), taking its look and content from an existing
  PowerPoint or Google Slides deck when there is one, and exported to .pptx or PDF by the author
  at the end. Reached from the darkroom router, or by the user ("make slides", "a talk from
  this", "use this template", "update the deck", "turn this pptx into something I can edit").
---

# Slides

A deck is another **print**, and it lives in the browser. Claude builds it as a Slides artifact;
the author opens the link from any machine, edits text and layout in place, and asks Claude for
the rest. PowerPoint is a final export, never the working format.

**The browser deck is the source.** The author changes it without telling you. Read a slide
before you change it, every time. The files on disk are a mirror, stale the moment the author
edits.

`SKILL_DIR` below is this sub-skill's folder.

**Resume first.** If the presentation folder has a `LINK.txt`, the deck exists: read its README,
then go to step 4.

## The slide

Every slide is minimal.

- **One message per slide**, stated by the title as a short sentence ("Accuracy falls after
  step 20"), not a topic label ("Results").
- **At most 3 points of at most 12 words**, 40 words below the title, one level of nesting. A
  slide whose title says it all carries no points.
- **One figure per slide, one panel per figure.** A multi-panel paper figure is re-plotted or
  cropped to the panel the title is about. Few marks, readable axes, no figure title (the slide
  title is the title). [../../references/figures.md](../../references/figures.md) applies.
- A figure and text share a slide only when the text is 1 to 3 short points about that figure.
- Detail, caveats and what to say go in the **speaker notes**; backup material goes after the
  closing slide.

When a slide you write breaks a limit, cut it or split it; never shrink the type to fit. A slide
the author designed, or brought from an existing deck, is theirs: carry it over as it is and
mention the limit it breaks rather than rewriting it.

## The presentation folder

Talks live together in one slides repository, one folder per presentation. That repository holds
presentation artefacts only. The project's code, data, papers and figures stay in their own
repositories and are read from there.

```
<slides repo>/<presentation>/
  README.md           the talk, the deck's link, and where every source lives
  LINK.txt            the deck's link
  project/            mirror of the deck: deck.json, deck.css, slides/<id>.html
  img/                every picture uploaded to the deck, and blob-ids.txt mapping
                      each uploaded id to its file name (preview.py needs it)
  <original>.pptx     the author's own deck or template, never modified
```

**Write only inside the presentation folder.** Never create, change or delete a file in a source
repository, in another presentation's folder, or at the slides repository's top level. A source
is read where it lives and is not copied in; only what the deck shows (a picture, cropped or
converted for a slide) is saved, under `img/`.

**README.md is the map to the sources.** Keep it current in the same turn as any change that
adds or drops a source:

```markdown
# <Talk title> · <venue> · <date>

Deck: <link>

## Sources (read-only, in their own repositories)

| What | Where it lives | Used for |
|---|---|---|
| Paper, submitted version | <absolute path or repo URL>, <commit or date> | slides 4 to 14 |
| Figure 3 | <path>, made by <script> | "Context" slide |

## Files here

<one line per file or folder in this presentation folder>
```

Each row gives enough to find the source again: a path or URL, and a commit, version or date
when the source changes over time.

The Artifact tool publishes only from under the working directory or the scratchpad. When the
session's working directory is the slides repository, publish straight from the presentation
folder. Otherwise write and publish from a scratch folder, then copy `project/` into the
presentation folder after every publish.

## 1. Gather

Find what the talk is made from: an existing deck or template, a darkroom series
(`retrospective.md`, posts, figures), a paper, the project's results. A Google Slides deck is
downloaded by the author as .pptx (File → Download) and put in the presentation folder. Write the
README's sources table now, before building.

Read an existing deck with

```
uv run --no-project --with python-pptx==1.0.2 --with pillow \
    python "$SKILL_DIR/scripts/read_pptx.py" <deck.pptx> <scratch folder>
```

It reports the look (fonts, theme colours, title and body sizes, backgrounds) and each slide's
shapes in pixels on the deck's 1920-wide canvas, and saves every picture already cropped as the
slide shows it. It never writes to the .pptx.

Done when every source has a row in the README with where it lives, an existing deck's dump and
pictures are on disk, and nothing outside the presentation folder was written.

## 2. Create the deck

Call the Artifact tool's `quickstart` with intent `slides`, then create the deck from the Slides
type it names. **The create result carries the type's own instructions for the file format and
the calls. They are the authority on format; follow them over anything remembered from an
earlier deck.**

- **The look comes from the existing deck when there is one**: its background, fonts, colours
  and sizes go into `project/deck.css`. This overrides the type's default palette and typeface
  advice. With no existing deck, design one plain look: light background, one typeface, one
  accent.
- **Adopting a deck**: rebuild each slide from the dump at the same positions and sizes (1 pt is
  2 px), in the dump's order, so later shapes paint over earlier ones. Keep the author's wording
  exactly. A hidden slide stays hidden. Speaker notes go in each slide's notes.
- **Upload the pictures** from `img/` and record each returned id in `img/blob-ids.txt`.
- Where the original has an empty box the author will fill, leave a bracketed grey placeholder
  such as `[Content to add]`, so there is something to click in the browser. List every
  placeholder you added in your reply.

Write `LINK.txt`, put the link in the README, and give the author the link as soon as the cover
is up. The deck is private; sharing it is the author's choice, made from the page.

Done when every slide of the outline or the original is published, the link is in `LINK.txt`
and the README, and `project/` is mirrored in the presentation folder.

## 3. Look

```
uv run --no-project --with pillow \
    python "$SKILL_DIR/scripts/preview.py" <presentation folder> <scratch folder>
```

It draws each slide with a local headless Chromium, four to a sheet, and prints each slide's
points and word counts against the limits. Read the sheets: a title wrapping into a figure, text
overflowing or hidden behind a picture, a figure too small to read, pictures stacked in the
wrong order. Fix what is clearly wrong in one pass and say what you changed.

The preview is an approximation: the machine may lack the deck's fonts, so line breaks differ.
If no Chromium is found, say plainly that the deck was not looked at.

Done when every slide was looked at or the author was told it was not, and each slide marked
OVER is either yours and fixed, or the author's and reported.

## 4. Edit loop

The author edits in the browser and asks for changes in chat or in a comment on the deck.

1. Read the deck's index and each slide you will touch, then change only those.
2. A publish refused because the author saved meanwhile: read their version, reapply your change
   onto it, publish again. Never resend your earlier copy.
3. A slide the author is working on right now (it changed during this turn) is left alone: tell
   them what you would have changed.
4. After each publish, mirror `project/` into the presentation folder, update the README if a
   source was added or dropped, and list what you changed.

New content for a slide still follows **The slide**. Every number traces to a source, as in the
posts.

Done when the author's edits are intact, every change you made is listed in your reply, and the
mirror matches what you last published.

## 5. Export

The author exports from the page (Share › Export) to .pptx or PDF when the talk is final; Claude
cannot do this step. Before they do, run step 3 once more and remind them that fonts the other
machine lacks will be substituted in PowerPoint, and that a hidden slide and any bracketed
placeholder left in the deck go into the export as they are.

<!--
CHANGE LOG
v5 2026-11-19: dropped the tell-before-upload step at the author's request: a deck is private
  by default, so no warning is needed.
v4 2026-11-19: one slides repository of presentation folders; README.md maps the sources, which
  stay in their own repositories; writes are confined to the presentation folder.
v3 2026-11-19: rewritten around the Slides artifact: the deck is edited in the browser and
  exported to .pptx at the end. Removed the markdown -> .pptx build (slides.py, style.toml, keep
  mode, pull) and the Google Slides reference. New read_pptx.py and preview.py. The author
  preferred this after trying both on one talk.
v2 2026-11-18: kept slides and pull --adopt.
v1 2026-11-18: first version, markdown source built into a template's placeholders.
Outstanding: the exported .pptx has not been inspected; preview.py cannot draw connectors or
  icons and uses whatever fonts the machine has.
-->
