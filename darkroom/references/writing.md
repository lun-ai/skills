# Writing the prints

Read before drafting and before every edit pass. Every rule here was a correction an author made.

## Story

- **One post per question.** Split a long effort into a series where each post answers one question
  the author actually asked, in the order they asked it. A post's `#` title is that question.
- **Diary order.** Sections run in the order the work happened. Section titles carry dates as a
  progress record: `## 4. Steering the model's internal state (6–12 Sep 2026)`.
- **The author's narrative wins.** If the author states the story ("first I saw X, so I tried Y"),
  restructure to it. Do not impose a thesis they did not choose.
- Unfinished work is marked `status: unfinished`, not padded into a result. A preliminary result
  appears as a teaser: what was built, the numbers, and why it is not a result yet.

## Prose

- **Paragraphs, not bullets**, for anything that explains. Each step: what was set out to test,
  how it was set up, what came out, what led to the next step. Bullets only for true lists, such as
  enumerated traits or three named checks.
- **Setup in the paragraph, not the heading.** Dates in headings; models, sets, judges and
  budgets in the opening sentence.
- **Reasoning is sourced or asked for.** Use the reasons the record gives (plan files, decision
  notes, commit messages). Where only the author knows why, leave an unpublished
  `<!-- YOUR THINKING: … -->` prompt. Never invent a motive.
- **Plain words for settings.** "the run where the agent could search the literature", not an
  internal arm name or dataset code. Internal set names (`failset110`) become descriptions ("the
  hard set").
- Keep the author's voice when editing: change only what was asked or what is factually wrong. Fix
  plain typos when asked, and list every change.

## Numbers

- **Every number traces to a source file.** Re-derive at least one headline number from raw
  outputs before the first draft. When the author edits a number or a claim, check it against the
  source before publishing. If the record contradicts the author's memory, say so with the numbers.
- **One value per table cell.** Flatten composite cells ("0.418 (29/61, 17/38)") into separate
  columns or rows.
- Report what was measured. Interpretation is the author's; when it is added, it is theirs or it is
  a recorded takeaway, clearly worded as such.
- When a source supports a narrower claim than a sentence makes ("best overall" vs "best on one
  set"), narrow the sentence.

## References

- **No code in posts.** No file paths, line numbers, script, plan or job names, "Source:" captions
  or row IDs. One link to the public repo, in the footer and where the project is first named.
- **Citations are checked, never recalled.** Take metadata from the project's own bibliography,
  the DOI or ACL Anthology page, arXiv, or the publisher. If a page cannot be read, keep the
  author's link and leave an unpublished TODO for the title. Do not guess.
- Cite inline as author–year links, and add a `## References` list at the end of the post.
- Keep two findings from two sources apart, even when the author's note merges them.

## Framing for a reader with a purpose

When the posts support an application or a talk, change only framing sentences: name the area the
work already touches, in the reader's vocabulary. Add no claims and no flattery. Re-read every
framing sentence against the results ("tested" vs "began", "only" vs what was actually done).
