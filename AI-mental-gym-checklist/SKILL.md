---
name: AI-mental-gym-checklist
description: Generates a CHECKLIST.md progress tracker for an AI-mental-gym build-from-scratch project — phases of atomic, gym-able items plus per-phase depth checkpoints. Use when starting a new mental-gym topic, or when AI-mental-gym finds no checklist file in the project.
---

<AI-mental-gym-checklist-skill>

## Purpose

Companion skill to `AI-mental-gym`. Produces a `CHECKLIST.md` for a new "build X from scratch" topic, structured so the gym loop (concept brief → signature → gap-fill skeleton → critique → depth question → optional tip) has well-scoped items to run reps against. Compatible with the existing LLM-from-scratch `CHECKLIST.md` format — same sections, same conventions.

## When to use

- The user wants to start a new mental-gym topic and has no checklist yet.
- `AI-mental-gym` is invoked on a project with no checklist/progress-tracker file — create one with this skill *first*, before running the first rep.

## Inputs needed from the user

Ask only for what's missing; don't interrogate if the user already gave enough:

1. **Topic / target artifact** — what is being built from scratch (e.g. "a B-tree-backed key-value store", "a regex engine", "an LLM").
2. **Reference material** (optional) — a repo, book, or paper whose structure/scope the checklist should roughly track.
3. **Starting point** (optional) — anything already done, or infrastructure that's fine to copy from a reference rather than build as a rep (becomes a "(Skipped for now, will come back)" phase).

## Required structure

Every generated checklist follows this template — these sections and their order are the contract `AI-mental-gym` relies on:

```markdown
# Mental Gym: <Topic> — Build Checklist

This is a mental gym - the task is to build <topic> from scratch. Use this file as progress tracker.

[Optional, only if a reference implementation exists: note that some sections are
skipped by copying from the reference so the user can focus on building other
sections modularly while keeping the system runnable end-to-end. Annotate those
phases as skipped.]

When starting from any section, AI explanations should provide minimum guide for
the user to gain a deep understanding of the design. The purpose is to train as in
a gym, not to allow the user to answer correctly at the first attempt.

DO NOT provide the answer directly.

[Optional: Reference repo/book: <link>]
[Optional: Target design: <one-line description of the end state>]

---

## Phase 1 — <Name>

- [ ] **1.1** <atomic, gym-able task>
- [ ] **1.2** <atomic, gym-able task>

## Phase 2 — <Name> [(Skipped for now, will come back) if infra-only]

- [ ] **2.1** ...

---

## Depth Checkpoints (answer these before moving on)

| After phase | Question to answer yourself |
|---|---|
| 1 | <conceptual "why" question for phase 1> |
| 2 | <conceptual "why" question for phase 2> |

---

_Use the `AI-mental-gym` skill in Claude Code to get interactive help on any phase._
```

Keep the `DO NOT provide the answer directly` line and the AI-guidance paragraph verbatim (or near-verbatim) — that's the instruction `AI-mental-gym` is built to satisfy.

## Phase and item design rules

- **Phases** = coherent subsystems (e.g. "Parsing", "Storage Engine", "Query Planner"). Aim for 5–9 phases for a project of meaningful scope — enough to show real structure, not so many that phases overlap.
- **Items** = one rep each: one function/class/algorithm/data structure. An item should be small enough that steps 1–3 of the gym loop (concept brief, signature, gap-fill skeleton) produce a single focused skeleton — not a bundle of unrelated pieces.
- **Order by dependency**: sequence phases and items so each builds on something already completed, the way the LLM checklist builds embeddings → attention → transformer block → full model → training → generation before fine-tuning.
- **Skip-and-copy phases**: if a reference implementation exists and a phase is infrastructure that isn't the learning target (e.g. a tokenizer when the goal is the transformer architecture), mark it `(Skipped for now, will come back)` and tell the user to copy it from the reference so the project stays runnable end-to-end while they focus elsewhere.
- **Depth checkpoints**: exactly one per phase, a single conceptual question whose answer requires understanding a design *tradeoff* — not something answerable by re-reading the code (e.g. "why does RoPE generalize better than learned absolute positions?" rather than "what does RoPE stand for?").

## After generating

1. Write the file as `CHECKLIST.md` in the project root (ask where, if the project root is ambiguous).
2. Walk the user through the phase list briefly and confirm scope/ordering before starting reps — getting this wrong means re-deriving the whole plan mid-gym.
3. Once confirmed, hand off to `AI-mental-gym` to start Phase 1, Item 1.

</AI-mental-gym-checklist-skill>
