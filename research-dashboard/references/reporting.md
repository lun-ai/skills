# Reporting results

**Every report of a result, in chat or in a document, mirrors the setting block: context
first, before any number appears.** This is not optional, not "when it seems useful", and not
something to wait for the user to ask for. A number with no setting attached is unreadable to
anyone who wasn't inside the run, including the same user three days later.

Lead every report with the experiment number and its subject ("E007, trees trained on the
full SIGNOR database"), then report in this order, per part:

1. **The setting block's content.** Give the question in words, the provenance, the
   populations, **what varies and what is held fixed** (as a named pair, for every test, not
   only ones that feel like comparisons), the procedure, the metric and derived-quantity
   definitions, and the scope boundary. Add anything that changed during execution and the
   system settings a reader needs: which model, which prompt or protocol variant, which tools
   were available, which dataset and split, how many items, how many seeds or repeats, and any
   budget or cutoff (step, token, timeout) that could bound the result.
2. **The numbers**, in a table.
3. **Limitations of the estimate**: what would bias it high or low, and which of its
   differences sit inside their own floor and are therefore claimed in neither direction.
4. **What was not done**: parts of the question left untested, what was not committed, and the
   cheapest unanswered measurement still on the board (by E# if it is registered).

Steps 3 and 4 are facts about the measurement, so they are owed unprompted. Nothing beyond them
unless interpretation was requested.

**Context and definitions are not interpretation.** The "do not interpret unless asked"
default restricts *why* a number came out that way and *what it implies*. It never licenses
dropping bare numbers on the user. If a report could be pasted into a stranger's inbox and
leave them asking "on what, with what?", it is not finished.

**When interpretation *has* been requested, state it as claims, not a data dump.** "Source
access explains ~4.6x of the overlap gap; step budget explains almost none of the remainder"
is a takeaway, and it lives in Takeaways, not Results.

## HTML pages

When a result, a comparison or an explanation for an experiment is better read as a page than
as chat (several arms, a flow, a ranked list of findings), make it with the
`answer-me-with-html` skill. The reporting order above applies to the page as well: the
setting first, then the numbers in a table, then limitations and what was not done. Then:

- Render it into the effort's `pages/` folder with `-o`, named after the experiment:
  `-o "<dashboard dir>/pages/e007-signor-full.html"`. To change one panel later, use
  `am patch` on that same file; to rebuild it, reuse the same `-o` path. A page left in the
  CLI's default folder (`~/.answer-me-with-html/pages`) is outside the repository and is
  deleted by `am clean`, so never link one.
- Link the page from the experiment's section in its topic file, with a path relative to
  that file (`Report page: [pages/e007-signor-full.html](pages/e007-signor-full.html)`), and
  add it to the experiment's Links cell in the registry.
- Run `scripts/render_map.py` and `scripts/check_map.py`. `check_map.py` reports any linked
  page that does not exist.
- In chat, give the conclusion in two or three lines plus the page link, as the
  `answer-me-with-html` skill asks. The topic file still holds the Results table; the page
  presents it, it does not replace it.
