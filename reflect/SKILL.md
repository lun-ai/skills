---
name: reflect
description: Pause mid-task and offer the user a menu of reflection lenses (pivotal question, failure backtrace, real problem, standard-answer critique, contradicting variables, fact/interpretation/test split, act-as-me), then run the chosen ones against the current work.
---

Use this when the current task has enough substance to be wrong — a plan is
about to be executed, a result is about to be interpreted, a judgement is
about to be acted on. It does not do the task. It interrupts it.

## Step 1 — Prompt the user

Always prompt first. Never pick lenses on the user's behalf, and never run
all seven unprompted.

Ask with `AskUserQuestion`, two questions in **one** call, both
`multiSelect: true` (the tool caps options at 4 per question, so the seven
lenses are split across two). Header for both: `Lenses`.

Question 1 — *"Which reflection lenses should I apply? (pick any)"*

| Label | Description |
|---|---|
| Pivotal question | Ask you the one question whose answer would change the result or its interpretation |
| Failure backtrace | Assume the task has already failed; give the three most likely reasons |
| Real problem | Name the problems actually worth solving, behind the stated one |
| Standard answer critique | Predict the obvious answer, name three flaws in it, propose a better one |

Question 2 — *"…and from this group? (pick any, or none)"*

| Label | Description |
|---|---|
| Contradicting variables | Assume your judgement is wrong — which uncovered variables would most likely contradict it |
| Fact / interpretation / test | Split what is known, what is interpreted, and what still needs an empirical or field test |
| Act as me | Given your goals, constraints, and affordable trade-offs, what I would do in your position |
| None from this group | Skip this group |

If `AskUserQuestion` is unavailable, print the seven as a numbered list and
ask the user to reply with numbers.

## Step 2 — Run the selected lenses

One section per selected lens, in the order listed above. Ground every lens
in the *actual* current task — the files, numbers, and decisions in this
session. A lens that could have been written before seeing the work is a
failed lens.

| Lens | Output contract |
|---|---|
| Pivotal question | Exactly **one** question, plus one line on how each plausible answer would change the outcome. Then stop and wait for the answer. |
| Failure backtrace | Three causes, ranked by likelihood; each with the observable signal that would confirm it. |
| Real problem | 2–4 candidate real problems; for each, what makes the stated problem a symptom of it. Mechanisms, not verdicts on feasibility. |
| Standard answer critique | The predicted default answer in 1–2 sentences → three specific flaws → one better version. The better version must survive all three flaws. |
| Contradicting variables | Variables *not yet covered* in this session, ranked by how hard they'd hit the judgement; each with the cheapest check that would surface it. |
| Fact / interpretation / test | Three short lists: **Known** (with source), **Interpretation** (with the assumption it rests on), **Untested** (with the test that would settle it). Anything unsourced is an interpretation, not a fact. |
| Act as me | A concrete next action stated in the first person, plus the trade-off being accepted and the one it refuses. No menus, no "it depends". |

## Rules

- **Terse.** Bullets and short tables. No restated preamble, no summary of
  what the task was — the user was there.
- **Adversarial, not agreeable.** If a lens produces nothing damaging, say
  so explicitly rather than manufacturing filler.
- **Cite the session.** Reference file paths, run IDs, and numbers already
  on screen instead of speaking in generalities.
- **Pivotal question blocks.** If that lens is selected, deliver it and
  stop; do not answer it yourself or continue the task.
- After all lenses are delivered, ask once whether to resume the task, and
  resume only on a yes.
