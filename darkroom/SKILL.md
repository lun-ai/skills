---
name: darkroom
description: Develop a technical project's notes, plans and results into a blog post or a series of linked posts that the author keeps editing in markdown. Use when the user wants to turn research or engineering work into a blog, write up what they tried and what went wrong, or says "rebuild" on an existing darkroom series.
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

## 1. Gather the negatives

Find everything the project tried: dashboards, plan files, result folders, commits, deleted plans.
For a large project, send a read-only subagent to sweep for pieces you have not read. Write a
**contact sheet**, `retrospective.md` in the series folder: chapters in date order, each with its
setup, results, and "what went wrong" in plain words. Re-derive one headline number from raw
outputs.

Done when every piece of work has a date, a setup, a result and a "what went wrong"; one number
has been re-derived; and nothing new was run. Offer to turn the contact sheet into a page with the
answer-me-with-html skill.

## 2. Choose the story

Use the grilling skill. One question at a time, each with a recommendation: format (a research
diary is the default), audience, where it opens, which pieces go in, how to cite flawed or
superseded results, what to do with unfinished work. If the author states their own narrative,
take it. Split into one post per question the work asked.

Done when the decisions are recorded as a table in `retrospective.md`, and each post has a question
as its title and an assigned list of sections.

## 3. Develop the drafts

Run `build.py init <series> --series "Series name" --parts N`. Write each post in the order agreed,
following [references/writing.md](references/writing.md). Read it now, in full.

Done when every number in the drafts traces to a source, no file path or internal name remains in
published text, every reference was checked against a real source, and each place where only the
author knows the reasoning has a `<!-- YOUR THINKING -->` prompt.

## 4. Make the figures

Follow [references/figures.md](references/figures.md): built-in chart blocks first, then
lieflat-charts, excalidraw-diagram or answer-me-with-html, always with minimal text.

Done when each figure makes one point, carries no title or source text, has a caption saying what
to see, and matches the numbers in the text.

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
