# Bootstrap and resume

## The document set

- **One dashboard** ([template](../templates/dashboard.md)), usually `DASHBOARD.md`: the
  research map, then the experiment list, then a short summary per topic. This is what the
  user reads to get oriented in five seconds.
- **One topic file per topic** ([template](../templates/topic-file.md)): the detail
  (mechanism, effort, results, limitations) for every experiment under that topic, in E#
  order. Linked from the dashboard, never duplicated into it.
- **Optional detail files** ([template](../templates/experiment-detail.md)), only once a split
  has been agreed (see below).

The dashboard's one-line result and the topic file must agree. The one-line result is the
compressed version of the experiment's Results (or of its Takeaways, where interpretation was
requested), not a different claim. This is the one sanctioned duplication. It is not an
exception to the redundancy rules, which target *unintentional* restatement.

## Bootstrap: partition questions into topics

When a user hands you a batch of open questions (reviewer comments, a backlog of "why does
this happen" investigations, a list of things to probe), don't start implementing right away.

1. **Group into topics.** A topic is a cluster of questions answerable with one shared
   mechanism or harness. If two questions would need the same instrumentation or the same
   comparison infrastructure, they belong to the same topic. Topics are usually nouns
   ("Retrieval comparison", "Sufficiency classifier"), not verbs. A topic can also be a
   dataset when the same methods are carried across datasets (JevMaster's SIGNOR /
   connectomeDB / SciFact).
2. **Register each question as an experiment with a global number** (`E001`, `E002`, ...,
   one counter across all topics; see [research-map.md](research-map.md)). Number in the
   order you plan to start them, not grouped by topic.
3. **Name the shared implementations.** Any harness, model wrapper, dataset builder or tree
   library that more than one experiment will use becomes an `impl:` node on the map.
4. **Estimate effort per experiment**, not per topic. One experiment might be "a synthesis of
   existing numbers, 0.5 day" while another needs a new harness and real GPU or API cost. Be
   concrete: wall-clock, $ cost, and dependencies ("shares 70% of code with E001").
5. **Sequence, don't just list.** State which experiments can run in parallel, which are
   blocked on another's output (by E#), and which should go last because they can absorb what
   the others produce (a failure-mode taxonomy that wants traces from everything else, for
   instance).
6. **Write the dashboard (map first) and one file per topic**, then run
   `scripts/render_map.py` to build the map page and `scripts/check_map.py`. Confirm the partition, the numbering and the priority order with
   the user before any implementation. The grouping is a judgment call they may want to
   redirect. Every experiment then goes through grilling ([work-loop.md](work-loop.md) step 1)
   before anything is built for it.

## Resume: continue existing documents

Before acting, **read the dashboard in full, including the research map, and the topic
file(s) relevant to the request.** Don't assume your last-known structure still holds. These
documents may have been reorganized, split or edited by the user or a parallel work stream
between sessions. If the map shows experiments or implementations you don't recognize, that is
someone else's stream: read enough to avoid colliding with it, but don't touch rows or
sections outside the experiments you were asked about.

If the dashboard predates global numbering (per-area `Q1, Q2...`, no research map), leave it
as it is and keep working in its existing scheme.

Then do one iteration of the work loop, and write results back into the topic file, the
experiment row and the registry (Updated date, approved job IDs), and re-render the map page,
before ending the turn. An experiment
is not "done" until all three are updated. An answer that only exists in chat is lost the
moment the session ends.

## When an experiment's detail outgrows its section

When an experiment's own detail outgrows its section (many per-run tables, confusion matrices,
per-class breakdowns, raw per-item numbers), the usual fix is a companion
`<topic>_e###_detail.md`. Link it from the experiment's section ("Full numbers: [...]") and
link back up from the top of the companion file. **Propose the split rather than doing it
unprompted.** It changes the structure the user navigates, and they may prefer a different
split point, a different file, or no split at all.
[writing-discipline.md](writing-discipline.md) covers when a split is warranted and what moves
once agreed.
