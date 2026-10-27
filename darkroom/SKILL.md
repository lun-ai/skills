---
name: darkroom
description: Develop a technical project's notes, plans and results into a blog post or a series of linked posts that the author keeps editing in markdown. Use when the user wants to turn research or engineering work into a blog, write up what they tried, or says "rebuild" on an existing darkroom series.
---

# Darkroom

The project's plan files, logs and results are the **negatives**. The posts are **prints**,
developed from them and never invented. The author edits the markdown by hand: **dodge and burn**.
Claude develops, checks and prints. The author's words stay the author's.

`SKILL_DIR` below is this skill's folder. Build with:

```
uv run --no-project --with markdown==3.7 python "$SKILL_DIR/scripts/build.py" <series>/blog.toml
```

**Resume first.** If a `blog.toml` for this work exists (check memory and the project), skip to
step 6.

## The post

Every print has the same plain shape, in the manner of a research post on anthropic.com: a light
page, a meta line, a question for a title, and prose carrying the results.

- Title: the question the post answers. Above it, the meta line ("Research diary · Part 2 of 3 ·
  date"); below it, the series name when it differs from the title.
- An undated opening section that says why the question matters and ends on the post's
  **question map** (see step 4), then numbered sections in the order the work happened, **each
  with its dates in the heading**:
  `## 4. Steering the model's internal state (6–12 Sep 2026)`.
- Paragraphs, not bullets. Each step's key result sits in **one** plain table or **one** chart,
  with a caption that says what to see. Most sections need neither.
- Unfinished work: `status: unfinished`, and a short closing teaser rather than a result.
- A `## References` list, the series cards, and one link to the public repo in the footer.

The post carries no timeline chart, no boxed findings, no "what went wrong" lists, and no
internal paths. Those belong in the working notes.

## 1. Gather the negatives

Find everything the project tried: dashboards, plan files, result folders, commits, deleted plans.
For a large project, send a read-only subagent to sweep for pieces you have not read. Write
`retrospective.md` in the series folder. It is a **working file, never published**: pieces in date
order, each with its setup, results and plain-words problems, so the author can recall the work.
Re-derive one headline number from raw outputs.

Done when every piece of work has a date, a setup and a result; one number has been re-derived;
and nothing new was run.

## 2. Choose the story

Use the grilling skill. One question at a time, each with a recommendation: audience, where it
opens, which pieces go in, how to cite flawed or superseded results, what to do with unfinished
work. If the author states their own narrative, take it. Split into one post per question the work
asked.

Done when the decisions are recorded as a table in `retrospective.md`, and each post has a question
as its title and an assigned list of sections.

## 3. Develop the drafts

Run `build.py init <series> --series "Series name" --parts N`. Write each post in the shape above,
following [references/writing.md](references/writing.md). Read it now, in full.

Done when every number in the drafts traces to a source, no file path or internal name remains in
published text, every reference was checked against a real source, and each place where only the
author knows the reasoning has a `<!-- YOUR THINKING -->` prompt.

## 4. Make the figures

Follow [references/figures.md](references/figures.md). Every figure is simple and minimal: few
marks, few words, the series palette, nothing decorative.

First, one **question map** per post, drawn with `scripts/mindmap.py`: the post's question in
the centre, 3 to 7 one- or two-word concepts around it, one or two short concrete lines under
each, and an optional "→ what we did" line. It is the post at one glance, one level above the
sections. Then the result figures: built-in chart blocks first, then lieflat-charts,
excalidraw-diagram or answer-me-with-html.

Done when each post opens on a question map whose branches the sections answer, each figure makes
one point, carries no title or source text, has a caption saying what to see, and matches the
numbers in the text.

## 5. Print

Build. Every post must report `ok`. Publish and link the posts as
[references/publishing.md](references/publishing.md) describes, and record the links in
`blog.toml` and in memory.

Done when every post is published, the series cards link to each other, and the author has every
link.

## 6. Dodge and burn

The author edits the markdown and says "rebuild". Run the edit loop in
[references/publishing.md](references/publishing.md): commit the author's edits on their own,
check what they changed, apply only what was asked plus factual fixes, rebuild, republish, commit.

Done when the author's commit and yours are separate, every changed number was checked, and every
change you made is listed in your reply.

## 7. Before sharing

Run the checks in [references/publishing.md](references/publishing.md) (sharing, leaks,
double-blind, collaborators, where the sources live), and give the author anything that is their
call to decide.

<!--
CHANGE LOG
v2 2026-10-27: question map (mindmap.py) as each post's opening figure, abstraction ladder,
  minimal-figure limits; taken from the metacognition-drift series maps the author liked.
Outstanding minor issues: mindmap.py has no top slot (max 7 branches); text widths are estimated.
-->
