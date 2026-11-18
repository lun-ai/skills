---
name: gap-finder
description: >
  Sub-skill of paper-library. On demand, checks an idea against the library: sharpens the idea
  into a testable claim first, then finds the closest work, what it left undone, and whether
  the idea is new. With only topics and no idea, proposes a few candidate ideas from tensions
  in the library instead of listing gaps. Reached from the paper-library router, or by "is
  this novel", "find the gap", "what hasn't been done on X", "brainstorm directions".
---

# Gap finder

A library has more gaps than anyone can use. Most are uninteresting: nobody did X on model Y
because nobody would care. The interesting ones appear only once there is a sharp idea to
measure the library against. So the idea is sharpened first, and the search comes second.

Formats: [../../references/format.md](../../references/format.md). Report template:
[../../templates/gap-report.md](../../templates/gap-report.md).

## 1. Sharpen

Get the idea into this form before searching anything:

> In **system**, **measure or intervention** will show **result**, which would mean
> **consequence**.

If the user's idea does not fill all four slots, ask for the missing ones, one question at a
time, each with your recommended answer (the `grilling` skill's manner). Stop when the four
slots are filled; this is a few questions, not a design review. For the full design, hand
over to `grill-experiment` afterwards.

**If the user has topics but no idea,** do not list gaps. Read `COMPARE.md` for those topics
and offer three candidate claims in the form above, each built from a tension you can point
to:

- two papers whose `Shows` disagree;
- an `Open` item that several papers name and none has done;
- a `Method` used in one topic and never in a neighbouring one;
- a `Does not show` that a later paper's argument quietly depends on.

The user picks or rewrites one. Then continue with it.

## 2. Search

Split the claim into its components (system, measure, intervention, claim) and list search
terms for each, including the names other authors would use.

1. **Notes first:** search `notes/` and `COMPARE.md` for each component. This finds
   candidates quickly.
2. **Full text second:** search `md/` for the same terms. Notes miss side experiments and
   single paragraphs; full texts do not.
3. **Read the passages.** For every candidate, open the full text at the hits and read the
   surrounding section. A paper counts as having done something only when you can cite the
   line.

Look hardest at the papers the idea cites or builds on: the closest prior work is often a
secondary experiment inside a paper already known for something else.

## 3. Classify

For each close paper, one of:

| Relation | Meaning |
|---|---|
| done | Tests the same claim on a comparable system. The idea is not new as stated |
| half | Covers some components and not others. Say which |
| named, not done | The authors list it as future work or a limitation |
| contradicts | Reports a result that makes the idea's premise doubtful |

## 4. Report

Write `gaps/<date>-<slug>.md` from the template and give the user the same content in chat,
closest work first:

- the sharpened claim;
- the closest papers with relation, what each did and left, and a file-and-line reference;
- the gap in one or two sentences, stated as a comparison between what exists and what the
  idea adds;
- what would close or kill it: the finding that would make it not new, and the cheapest
  check that the idea can work at all;
- what was not searched: thin topics, papers with no full text, everything outside the
  library, and the date the library was last updated.

If a "done" paper turns up, say so first and plainly. Then offer the nearest variation that
is still open; that is usually the more useful result.

## 5. Feed the library

- A paper whose note was wrong or empty where it mattered: fix the Compare fields now.
- Close work that the search suggests exists but is not in the library (cited by several
  hits, for example): list it for the library keeper to add, then re-run the search.
