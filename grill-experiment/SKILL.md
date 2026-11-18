---
name: grill-experiment
description: Interview the user about an experimental design, one aspect at a time, until every aspect is either settled or named as open. Use when the user wants to stress-test, clarify or refine a research or experiment design before running it, or says "grill my experiment" or "grill this design".
---

Run a `/grilling` session on my experimental design: one question at a time, each with your
recommended answer, waiting for my reply before the next. If a question can be answered from
the repository, my notes or the literature I point you to, look it up instead of asking.

Cover the aspects below in order, because later ones depend on earlier ones. Skip an aspect
only when I have already settled it, and say that you skipped it. Do not move on while my
answer is vague: ask for the number, the example or the definition.

| # | Aspect | Settled when I can state |
|---|---|---|
| 1 | Prior beliefs | What I believe now and how confident I am in each belief, as a number |
| 2 | Subject | Exactly what system, population or object is studied, and why this one |
| 3 | Contrast | A similar case I expect to behave differently, and the reason |
| 4 | Theory and prediction | The theory behind the design and a prediction from it that could turn out false |
| 5 | Method | The experiment end to end, in a form I could draw as one figure |
| 6 | Measures and interventions | What is read and what is changed, each with an operational definition |
| 7 | Controls and confounds | Each other explanation of the expected result, and the control that rules it out |
| 8 | Outcomes | Every plausible outcome, with a credence for each, summing to 100% |
| 9 | Updates | How far each outcome would move each belief from aspect 1, and in which direction |
| 10 | Construct validity | Why the measure captures the concept I care about, and where it might not |
| 11 | Novelty | The closest prior work and what this design adds to it |
| 12 | Feasibility | Data, tools, compute, time and cost, each with a number or a named unknown |
| 13 | Ethics | Who or what could be harmed by running it, and the mitigation |
| 14 | Decision rules | Which result counts as which outcome, plus stopping and exclusion rules, fixed in advance |

Check for consistency as you go, and raise any conflict as the next question:

- The outcome credences (8) must agree with the prior beliefs (1).
- Every outcome (8) must move at least one belief (9). If no outcome would change my mind,
  say that the experiment is not worth running as designed.
- Every measure (6) must be used by a decision rule (14), and every rule must use a defined
  measure.

End with a table of the fourteen aspects, each marked settled (with my answer in one line) or
open (with what is missing). Do not fill in an open aspect yourself.
