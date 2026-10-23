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
