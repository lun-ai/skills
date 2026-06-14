---
name: framework-design-alternatives
description: >
  Brainstorm alternative technical framework design choices. Use this skill whenever a user
  is designing, evaluating, or reconsidering the architecture of a software framework, library,
  SDK, protocol, or system — and wants to explore different design directions. Trigger on:
  "alternative approaches", "trade-offs", "should I use X or Y pattern", "better architecture",
  "rethink this design", "design review", "framework design", "what are my options", "stuck on
  the architecture", "how else could I structure this", competing design patterns, or when the
  user shares code and asks whether there's a better way to structure it. Also trigger when a
  framework isn't working well and the user wants alternatives. Use even when vague — the skill
  elicits missing context through structured questioning.
---

# Framework Design Alternatives

A structured workflow for brainstorming alternative design choices for technical frameworks,
libraries, and systems. The goal is to help the user see the design space clearly, understand
trade-offs, and arrive at a well-reasoned architectural direction — not just list options.

The conversation follows a pattern: **clarify → map the design space → generate alternatives
→ compare trade-offs → recommend a direction**.

---

## Step 0 — Establish Context

Before generating any alternatives, collect five things. If the conversation already contains
some of these, fill in only what is missing. Ask everything that's missing in a single message.

**Elicitation template:**

> To suggest meaningful alternatives, I need to understand what you're building and where the
> pressure is. A few quick questions:
>
> 1. **What are you building?** — Describe the framework, library, or system in a sentence or
>    two. What problem does it solve? Who uses it?
> 2. **What's the current design?** — Sketch the architecture as it stands (or as you're
>    imagining it). Key components, how data flows, what the public API looks like. Code,
>    diagrams, or plain English all work.
> 3. **What's bothering you?** — What's the friction? Performance, ergonomics, extensibility,
>    complexity, coupling, testability, onboarding difficulty? Name the pain even if you can't
>    articulate the cause.
> 4. **What direction are you leaning?** — Do you have a hunch about what kind of improvement
>    you want? For example: "I want it more pluggable", "I think we need to decouple X from Y",
>    "I wonder if an event-driven approach would be simpler." Even a vague hunch helps narrow
>    the space.
> 5. **What's fixed?** — Constraints that alternatives must respect: language/runtime, backward
>    compatibility, team size, performance budget, deployment environment, existing integrations.

**Probing for artifacts.** If the user describes friction but hasn't shared evidence, ask for
the most useful artifact — whichever is most relevant:

- Source code (even partial) of the current design
- Error logs, profiling output, or failure descriptions that illustrate the problem
- API surface or type signatures that show ergonomic issues
- Dependency graphs or module maps that show coupling

These artifacts ground the brainstorm in reality and prevent generic advice. Don't proceed
past Step 1 without at least a rough picture of the current design and the pain point.

---

## Step 1 — Map the Current Design

Once you have enough context, produce a concise design map in a single response:

### 1a. Restate the system's purpose and scope
One paragraph. Confirm you understand what the framework does, who it serves, and what its
boundaries are. This catches misunderstandings early.

### 1b. Identify the core design decisions
List the 3–7 most consequential architectural choices in the current design. For each one,
name:
- **The decision**: e.g., "Middleware is a linear pipeline"
- **The pattern it follows**: e.g., "Chain of Responsibility"
- **What it enables**: e.g., "Simple mental model, easy to add cross-cutting concerns"
- **What it costs**: e.g., "Order-dependent, hard to compose conditionally"

### 1c. Locate the tension
Identify which specific design decision(s) are the primary source of the user's stated pain.
Be precise — "the problem isn't your middleware pattern, it's that your middleware and your
routing are coupled through shared mutable state" is better than "the architecture has some
coupling issues."

### 1d. Name reference frameworks
Mention 2–4 existing frameworks or systems that have faced similar design tensions and
resolved them differently. These serve as concrete prior art for the alternatives in Step 2.
Briefly note how each one approached the same problem.

---

## Step 2 — Generate Alternatives

Produce 3–5 alternative design directions. Each alternative should be a coherent architectural
choice, not a grab-bag of tweaks. Structure each one as:

```
### Alternative N: [Short evocative name]

**Core idea**: [One sentence — the key insight or pattern shift]

**How it works**: [2–4 paragraphs explaining the architecture. Be concrete: describe
components, data flow, API shape. Use pseudocode or type signatures where they clarify.]

**What changes**: [Which of the current design decisions from Step 1 this replaces, and how]

**Enables**: [What becomes easier, faster, or more natural]

**Costs**: [What becomes harder, slower, or breaks. Be honest — every design choice has a cost.]

**Prior art**: [Frameworks, libraries, or systems that use this approach, with a note on
how well it worked for them]

**Fit for your case**: [Why this might or might not suit the user's specific constraints
from Step 0]
```

**Generating good alternatives:**

- Vary the alternatives across different axes of the design space. Don't produce three
  variations on the same idea. One might change the execution model, another the extension
  mechanism, another the data flow topology.
- Include at least one alternative that is a targeted refinement of the current design (not
  a rewrite) — sometimes the best move is surgical.
- Include at least one alternative that challenges a deeply held assumption of the current
  design — something the user might not have considered because it felt "too different."
- Ground every alternative in real prior art. If you can't name a system that has used the
  pattern successfully, flag that — it may mean the idea is novel (exciting) or untested
  (risky).
- If the user provided source code, reference specific modules, functions, or interfaces
  that would change.

---

## Step 3 — Compare Trade-offs

After presenting the alternatives, produce a structured comparison:

### 3a. Trade-off matrix
A concise table or structured comparison across the dimensions that matter most to the user
(taken from their pain points and constraints in Step 0). Common dimensions include:

- Complexity (conceptual, implementation, operational)
- Performance characteristics
- Extensibility / plugin story
- Testability
- Migration effort from current design
- Learning curve for the team
- Long-term maintenance burden

### 3b. Risk assessment
For each alternative, state the biggest risk — the thing most likely to go wrong or to be
underestimated. Be specific: "the event-driven version could introduce subtle ordering bugs
in the billing pipeline" is better than "event-driven systems are harder to debug."

### 3c. Recommendation
Based on everything discussed, offer a clear recommendation with reasoning. Structure it as:

> **If your primary goal is [X]**, go with Alternative N because [reason].
> **If you're more worried about [Y]**, consider Alternative M instead because [reason].

Acknowledge that the user knows their system better than you do. The recommendation is a
starting point for discussion, not a verdict.

---

## Step 4 — Drill Down

After the user reacts to the alternatives, help them go deeper on the direction they find
most promising:

- Sketch out the migration path from the current design
- Identify the riskiest component to prototype first
- Suggest a spike or proof-of-concept that would validate the approach cheaply
- Offer to produce pseudocode, interface definitions, or a module map for the chosen direction

If the user wants to explore a hybrid of multiple alternatives, help them identify which
elements compose well and which conflict.

---

## Interaction Principles

- **Ask before you prescribe.** The brainstorm is only useful if you understand the real
  problem. Don't jump to alternatives before Step 0 is complete.
- **Be concrete.** Prefer "replace the middleware stack with a directed acyclic graph of
  transform nodes, each typed with input/output schemas" over "consider a more modular
  architecture." Vague alternatives waste the user's time.
- **Name trade-offs honestly.** Every design choice has a cost. If you can't name the cost,
  you haven't thought hard enough about the alternative. The user needs to trust that your
  enthusiasm for an idea doesn't blind you to its downsides.
- **Respect the user's constraints.** A beautiful architecture that requires rewriting
  everything in Rust when the team only knows Python is not a useful suggestion. Always tie
  alternatives back to what's feasible given their stated constraints.
- **Use prior art generously.** Real-world examples make alternatives credible and give the
  user something to study independently. When you reference a framework, note what version
  or era you mean — designs evolve.
- **One question per turn.** If you need multiple things, ask the most important one and
  defer the rest.
- **Adapt depth to the user.** If the user is sketching an early idea on a napkin, stay at
  the architectural level. If they've shared 500 lines of code and a profiling trace, get
  into the weeds.
