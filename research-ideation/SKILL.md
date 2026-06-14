---
name: research-ideation
description: >
  Structured research ideation and planning skill. Use this skill whenever a user wants help
  developing a research idea into a concrete proposal, paper plan, or experimental design.
  Trigger when the user mentions: a research direction they are exploring, a gap they want
  to address, a hypothesis they want to test, a benchmark or dataset they want to work with,
  or phrases like "I want to investigate", "I'm working on", "I have an idea for", "help me
  develop", "turn this into a research plan", "what's novel about", "is this publishable",
  or "how should I structure this study". Also trigger when the user shares a literature
  summary or prior conversation about research and asks for a plan or documentation.
  Always use this skill even if the idea is vague — the skill is designed to elicit the
  missing pieces through structured prompting.
---

# Research Ideation Skill

A structured workflow for turning a research direction into a concrete, publishable proposal.
Modelled on the pattern of expert-researcher dialogue: elicit → situate → decompose → design
→ surface contributions → compile.

---

## Step 0 — Elicit Core Inputs

Before doing anything else, collect three things from the user if they are not already present
in the conversation. Use the elicitation template below. Ask all three in a single message.

**Elicitation template:**

> To help develop your research idea, I need three things:
>
> 1. **The idea** — What is the phenomenon, system, or approach you want to study? (One or two sentences is fine.)
> 2. **The gap** — What does existing work leave unanswered, unsolved, or unstudied? What motivated you to look at this?
> 3. **The aim** — What do you want to achieve or demonstrate? Is this primarily about understanding, improving performance, building a tool, or establishing a benchmark?
>
> You can answer in any order and as briefly or fully as you like. I'll ask follow-up questions
> as we go.

If some inputs are partially present, fill in only what is missing. Do not proceed to Step 1
until you have at least a rough answer to all three.

---

## Step 1 — Situate in the Literature

Once you have the three inputs, do the following in a single response:

### 1a. Map what is already established
Summarise the existing work most directly relevant to the idea. Be specific: name papers,
systems, numbers where you know them. Distinguish between:
- **Existence proofs** — work that shows the phenomenon is real or the approach works at all
- **Mechanism designs** — work that explains *how* or *why* it works
- **Benchmarks and datasets** — existing evaluation infrastructure the user can build on

### 1b. Identify the genuine gap
Make the gap concrete. Frame it as: *"What's missing is a systematic study of X under
condition Y — nobody has done Z."* Avoid vague statements like "this is underexplored."
Decompose the gap into 3–5 specific sub-angles, each of which could be a paper on its own.

### 1c. Ask one focusing question
End with a single question that helps narrow the scope given the user's constraints (compute,
domain expertise, available data, timeline). This keeps the dialogue efficient.

---

## Step 2 — Narrow Based on User Constraints

After the user responds to your focusing question, identify:

- **The primary constraint** (compute, data access, domain, time, collaboration)
- **The most tractable entry point** — which sub-angle can be answered with the least
  resource while still being publishable?
- **The anchor result** — a single number or comparison from existing work that the user
  can beat, extend, or reframe as a baseline

Present these explicitly so the user can confirm or redirect.

---

## Step 3 — Design the Empirical Study

Structure the study in layers. Each layer tests a progressively harder claim and can stand
alone if resources run short.

### Layer 1 — Motivational / diagnostic test
- What is the simplest experiment that shows the problem is real?
- What dataset or benchmark fits here, and why (existing baselines, verifiable outputs,
  domain fit)?
- What failure taxonomy will you collect? (i.e., when it fails, *why* does it fail — this
  is often the key contribution)

### Layer 2 — Core comparison
- What are the conditions (A vs B vs C)?
- What is the independent variable and what is controlled?
- What metric captures success?

### Layer 3 — Extension / scaling
- What happens when you push the finding further (more data, harder tasks, different model
  sizes, different domains)?
- Which of these extensions is most likely to reverse or qualify the core finding?

For each layer, identify the **minimum viable version** (what you need to run to get a
publishable claim) and the **full version** (what would make it a top-venue paper).

---

## Step 4 — Surface Publishable Questions

Generate 3–5 research questions in this format for each:

```
Question: [One sentence, stated as an empirical question]
Expected finding: [What you predict will happen and why, grounded in existing work]
Implication if true: [What changes about how the field thinks or builds systems]
Implication if false: [What you learn from the null result — is it still publishable?]
```

Prioritise questions where the null result is also interesting — these are the most robust
to write into a paper introduction.

---

## Step 5 — Compile the Plan Document

When the user asks for a compiled plan (or when the ideation conversation has converged),
produce a structured document with the following sections. Write it as a `.md` file using
the `create_file` tool so the user can download it.

```
# Research Plan: [Title]

## Core Research Question
[One paragraph: the main question and why it matters now]

### Sub-questions
[Numbered list of 3–5 nested questions]

## Motivation and Gap
[Two paragraphs: what exists, what is missing, why this matters to the field and to
any domain-specific stakeholders]

## Empirical Study Design

### Phase 1 — [Name: e.g., "Motivational diagnostic"]
[Dataset(s), conditions, metrics, failure taxonomy, baseline to beat]

### Phase 2 — [Name: e.g., "Core ablation"]
[Dataset(s), conditions, metrics, minimum viable vs. full version]

### Phase 3 — [Name: e.g., "Scaling / extension"] (optional)
[Dataset(s), conditions, metrics]

## Proposed Pipeline
[Step-by-step technical pipeline with named components, drawing on specific prior work
for each stage. Call out which stage is the novel contribution.]

## Publishable Questions and Implications
[For each question: question, expected finding, implication if true, implication if false]

## Practical and Community Implications
[Who benefits from this beyond the immediate research community? What does a positive
result enable in deployment or practice?]

## Sequencing and Priorities
[Recommended order of experiments given likely constraints. Which result to aim for first
and why.]

## Key References
[Bulleted list of the most important prior works, with one-line summaries of what each
contributes to this proposal]
```

---

## Interaction Principles

- **One question per turn.** Never ask more than one question at a time. If you need multiple
  things, ask the most important one and infer the rest or ask later.
- **Be specific.** Always prefer "Llama-3.1-8B on ALFWorld" over "a small model on an
  agentic benchmark." Vague language is a sign the gap has not been adequately narrowed.
- **Name the contribution explicitly.** In every response after Step 1, state clearly what
  the user's work adds that prior work does not have. Use the phrase "your contribution is..."
  or "the novel element here is..." so the user always knows what they are building.
- **Distinguish phases.** Label clearly what can be published after Phase 1 alone vs. what
  requires Phase 2. This helps users with limited compute plan realistically.
- **Validate against existing baselines.** Whenever you recommend a dataset or benchmark,
  cite a concrete prior result on it so the user knows what they are competing with.
- **Surface the null result.** For every prediction, say explicitly what a negative result
  would mean. Research plans that are not falsifiable are not good research plans.

---

## Worked Pattern (abstract)

The conversation structure that produced this skill followed this pattern:

1. User states idea + gap → Claude maps literature and decomposes gap into sub-angles
2. User narrows aim (e.g., inference-time vs. training-time) → Claude restructures around
   that choice and proposes a pipeline with named stages
3. User introduces domain constraints (compute, domain knowledge) → Claude identifies the
   anchor baseline and the minimum viable experiment
4. User introduces benchmark choices → Claude maps each benchmark to a layer of the study
   and identifies which one provides the cleanest baseline
5. User requests compiled documentation → Claude produces the plan document

The skill reproduces this structure for any research domain by abstracting away the specific
content (ML, bioinformatics, etc.) and preserving the logical shape of the dialogue.
