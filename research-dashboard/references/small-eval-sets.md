# Small evaluation sets: floors, and a budget for how often you may look

Any set you *steer by* needs two numbers before it can decide anything, and both belong in the
setting block:

- **Its discrimination floor**: the smallest difference between two candidates that the set
  can tell apart from luck. To estimate it, resample the set from itself, re-score both
  candidates on each draw, and take 1.96 standard deviations of how much their difference
  bounces. A difference smaller than the floor is not a result, whichever way it points.
- **Its selection inflation**: how much apparent improvement comes from keeping the best of
  *k* candidates that are not genuinely different. Simulate it with candidates you believe are
  equivalent (repeats of one method under different random seeds): score them all, then
  repeatedly draw *k* at random and keep the best. Report the inflation at the *k* you actually
  intend to try.

When inflation at your intended *k* approaches the floor, the set cannot referee your
iteration: selection alone manufactures a difference the size of the smallest one you would
believe. Say so plainly and propose a split. Iterate on a larger in-distribution view, and
**spend the small set once, at the end**, under an explicit consultation budget written into
the experiment's section of the topic file ("this set may inform zero decisions before the
final comparison"). A budget that is not written down erodes one glance at a time. Record the
floor and budget in the registry's Attributes as well (`floor: 0.08 · budget: 1 look`), so
they are visible on the dashboard.

Also say when a cheap proxy *cannot* be manufactured. A subset matched on surface features is
still drawn from the same distribution, so it cannot stand in for a set whose difficulty comes
from lying beyond that distribution. Name which kind of hardness is in play: a different mix of
the same ingredients, or genuine extrapolation. Only the first can be proxied, and a
sharper-but-in-distribution view is a reported lens, not a decider.
