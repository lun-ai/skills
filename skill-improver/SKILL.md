---
name: skill-improver
description: >
  DO NOT INVOKE WIHTOUT THE USER PROMPTING EXPLICITLY. Analyze and iteratively improve an existing skill by examining the current session history, spotting failure patterns, edge cases, ambiguous instructions, and inefficiencies in a workflow.
  Use this skill whenever: a skill produced a wrong or suboptimal output just now; the user says
  "this skill isn't working", "improve the skill", "the skill got confused", "fix the skill",
  "the workflow broke", or "update the skill based on what went wrong"; or when the user wants
  to review the last run and make the skill more robust. Also trigger proactively if you notice
  that you just made a mistake while following a skill's instructions — even before the user
  says anything. If a skill was involved in the current session and something went wrong,
  this is the skill to use.
---

# Skill Improver

You are doing **iterative skill surgery** — diagnosing exactly what went wrong in the current
session and writing targeted improvements to make the skill more robust, clear, and effective.

---

## Phase 0 — Orient

Before anything else, establish the situation:

1. **Which skill was involved?** Check `available_skills` in context, or ask the user.
2. **Where is the skill file?** Common paths:
   - `/mnt/skills/user/<name>/SKILL.md`
   - `/mnt/skills/public/<name>/SKILL.md`
   - `/mnt/skills/examples/<name>/SKILL.md`
   - A path the user provides directly
3. **Is the skill file writable?** Installed skills under `/mnt/` are read-only. If so,
   copy to `/tmp/<name>/` before editing:
   ```bash
   cp -r /mnt/skills/user/<name> /tmp/<name>
   ```
4. Read the skill file fully with `view` before touching it.

---

## Phase 1 — Diagnose

### 1a. Mine the session history

Scan **the entire current conversation** — not just the last exchange — and build a structured
fault report. Look for:

| Signal | What to look for |
|---|---|
| **Explicit errors** | Tool call failures, Python tracebacks, file-not-found, wrong output |
| **Correction turns** | User said "no", "wrong", "that's not right", "try again" |
| **Ambiguity confusion** | Claude asked a clarifying question that the skill should have pre-answered |
| **Skipped steps** | A step in the skill was silently omitted or reordered |
| **Assumption failures** | Claude assumed something (file path, format, default) that turned out wrong |
| **Output format drift** | Final output didn't match the format the skill specifies |
| **Trigger mismatch** | Skill triggered when it shouldn't, or didn't trigger when it should |
| **Efficiency waste** | Redundant tool calls, unnecessary back-and-forth, excessive clarifying questions |
| **Edge case blindness** | Input the skill never anticipated (empty file, unusual encoding, nested structure) |

Produce a **Fault List** — a numbered list of distinct issues, each with:
- **Type** (one of the signals above)
- **Evidence** — quote or reference the specific moment in the session
- **Root cause** — which line/section of the skill is responsible, or what is missing

### 1b. Present diagnosis to the user

Show the Fault List clearly. For each item, say what you think caused it and what the
fix strategy is. Ask: _"Does this capture what went wrong? Anything to add or deprioritize?"_

Don't skip this step — the user might have context you don't, and validating the diagnosis
prevents fixing the wrong things.

---

## Phase 2 — Prioritize

Not all faults are equally important. Rank them:

1. **Critical** — causes incorrect or destructive output (fix first)
2. **Major** — causes the workflow to stall, loop, or require repeated correction
3. **Minor** — causes inefficiency, extra turns, or cosmetic issues

Focus improvements on Critical and Major items in the current iteration.
Flag Minor items in a "Future improvements" note at the bottom of the skill.

---

## Phase 3 — Write Improvements

For each Critical/Major fault, make a **targeted edit** to the skill. Follow these principles:

### Editing principles

- **Surgical, not sweeping.** Change only what the fault report identified. Don't rewrite
  sections that weren't broken — you risk breaking them.
- **Add, don't just delete.** Most faults come from insufficient guidance. Add a sentence,
  example, or guard clause rather than just removing something.
- **Be concrete.** Vague guidance like "handle edge cases" is useless. Say exactly what
  the edge case is and how to handle it.
- **Use examples for ambiguous cases.** If a rule is easy to misread, add a one-line
  ✓ / ✗ example pair.
- **Fix triggering in the description.** If the skill triggered at the wrong time,
  update the YAML `description` field — that's the sole trigger mechanism.
- **Preserve the original `name`.** Never change the `name` frontmatter field.

### What good edits look like

| Fault type | Typical fix |
|---|---|
| Skipped step | Add an explicit checklist or "Do not skip" callout |
| Assumption failure | Add a "Defaults and assumptions" section listing them explicitly |
| Ambiguity confusion | Add a decision table or ✓/✗ example |
| Output format drift | Add a concrete output template or example block |
| Edge case blindness | Add an "Edge cases" section with named scenarios |
| Trigger mismatch | Rewrite the `description` with more/fewer trigger phrases |
| Efficiency waste | Add a "When NOT to do X" rule, or consolidate steps |

### Diff format

When presenting changes to the user, show a clear before/after for each edit:

```
CHANGE 1 — Fix skipped validation step
────────────────────────────────────────
BEFORE (line 42):
  Run the transform script.

AFTER:
  Run the transform script.
  ⚠️ Before running: verify the input file is non-empty and UTF-8 encoded.
  If either check fails, stop and tell the user what was wrong.
```

---

## Phase 4 — Apply and Test

1. Apply the edits to the (writable copy of the) skill file using `str_replace`.
2. **Sanity-test the fix**: re-run the exact prompt/input that caused the original failure,
   following the updated skill. Does it now produce the right output?
3. **Regression check**: run 1–2 prompts that worked fine before, to ensure the fix
   didn't break them.
4. Report results to the user: what passed, what still needs work.

---

## Phase 5 — Package and Deliver

Once the user approves the changes:

1. If the skill came from `/mnt/skills/user/`, package it:
   ```bash
   python -m scripts.package_skill /tmp/<name>
   ```
   Then present the `.skill` file to the user.

2. If the user just wants the raw updated SKILL.md, save it to `/mnt/user-data/outputs/`
   and present it.

3. Summarize what changed and why — one sentence per edit — so the user has a record.

---

## Phase 6 — Log for Future Iterations

At the bottom of the skill file (inside an HTML comment so it doesn't affect behavior),
append a brief change log:

```markdown
<!--
CHANGE LOG
v<n> <date>: <one-line summary of changes made>
Outstanding minor issues: <list or "none">
-->
```

This helps future runs of the skill-improver understand what has already been tried.

---

## Edge Cases

- **No skill file found**: Ask the user for the exact path. If they don't know it, list
  `/mnt/skills/user/` and `/mnt/skills/public/` to help them locate it.
- **Multiple skills involved in one session**: Identify which skill is most responsible
  for the fault. Improve that one first; note the others for a follow-up.
- **User wants a full rewrite**: Warn that a full rewrite risks introducing new regressions.
  Offer to do it section-by-section with a test between each section.
- **Fault is actually a Claude bug, not a skill bug**: Some failures happen because Claude
  didn't follow clear instructions — the skill was fine. In that case, consider making the
  instructions more directive ("You MUST…", adding a checklist), but tell the user what
  you're doing and why.
- **Skill description is correct but Claude.ai isn't triggering it**: Remind the user that
  skill triggering works best on complex, multi-step requests. Simple one-shot queries may
  not trigger any skill. Suggest prefacing requests with more context.

---

## Quick Reference: Common Improvement Patterns

```
Problem → Fix pattern
─────────────────────────────────────────────────────────────────────
Skipped step          → Add numbered checklist with explicit ordering
Wrong assumption      → Add "Defaults" table at top of relevant section
Format drift          → Add literal output template with placeholder values
Too many clarifications → Add decision tree or "if X then Y else Z" block
Trigger too broad     → Narrow description with "NOT for: …" clause
Trigger too narrow    → Add more example phrases to description
Efficiency (extra turns) → Add "Before starting, gather: …" preflight section
Edge case crash       → Add named edge-case handler with specific instructions
```
