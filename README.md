# Skills: Research Paper Writing

[中文介绍](./README_zh.md).

> Some skills in this repository came from Prof. Peng Sida (彭思达)'s notes:
> https://pengsida.notion.site/c1a22465a0fa4b15a12985223916048e
> Prof. Peng's original repository:
> https://github.com/pengsida/learning_research
> I sincerely thank Prof. Peng for openly sharing these valuable experiences.
> My contribution is organization, structured adaptation, and packaging as reusable Skills.

## Repository Overview

This repository currently provides **37 skills**, organized into the
following groups. Each skill is a self-contained package: its directory
contains a `SKILL.md` with the core workflow and usage rules, plus any
supporting `references/`.

<!-- SKILLS-CATALOG:START -->
### Learning & Skill-Building

| Skill | Description |
|---|---|
| [AI-mental-gym](./AI-mental-gym/) | Guide hands-on coding reps for any build-from-scratch topic via concept briefs, gap-fill skeletons, and critique — without giving away solutions. |
| [AI-mental-gym-checklist](./AI-mental-gym-checklist/) | Generate a phased CHECKLIST.md of gym-able build items and depth-checkpoint questions for a new build-from-scratch learning project. |

### Writing & Polishing

| Skill | Description |
|---|---|
| [ai-paper-writing](./ai-paper-writing/) | Rewrite ML/CV/NLP papers section-by-section for clarity, flow, and reviewer-facing presentation, with claim-evidence checks. |
| [nature-polishing](./nature-polishing/) | Polish, restructure, or translate academic prose into Nature-leaning English, plus LaTeX layout/typesetting fixes. |
| [nature-writing](./nature-writing/) | Draft or restructure Nature-style manuscript sections (abstract, intro, methods, etc.) from claims, results, and notes. |

### Reviewing & Feedback

| Skill | Description |
|---|---|
| [ai-paper-reviewer](./ai-paper-reviewer/) | Simulate a venue-calibrated peer reviewer: numeric scores (novelty/clarity/soundness/impact), strengths/weaknesses, and a revision roadmap. |
| [nature-response](./nature-response/) | Draft, audit, or revise point-by-point reviewer response letters and rebuttals for Nature-family manuscript revisions. |
| [nature-reviewer](./nature-reviewer/) | Simulate 3 Nature-style referee reports plus a cross-review synthesis, grounded in Nature's official editorial criteria. |

### Literature, Reading & Citation

| Skill | Description |
|---|---|
| [nature-academic-search](./nature-academic-search/) | Multi-source literature search, citation verification, and reference management (PubMed, CrossRef, arXiv, Scopus, BibTeX/RIS conversion). |
| [nature-citation](./nature-citation/) | Add strict Nature/CNS-family citations to manuscript text, splitting passages into segments and exporting reference-manager files. |
| [nature-reader](./nature-reader/) | Build full-paper Chinese-English side-by-side, figure/table-aware Markdown readers from a paper's PDF, DOI, or text. |
| [paper-summarizer](./paper-summarizer/) | Summarize research papers with precise location references so readers can quickly find core ideas and navigate to relevant parts. |

### Manuscript Pipeline & Data

| Skill | Description |
|---|---|
| [document-changes](./document-changes/) | Create a timestamped markdown note documenting recent implementation changes, derived from the codebase and git state. |
| [nature-data](./nature-data/) | Prepare or audit Nature-ready Data Availability statements, repository plans, dataset citations, and FAIR metadata checklists. |
| [nature-figure](./nature-figure/) | Create, audit, or polish submission-grade Nature-style multi-panel figures in Python (matplotlib/seaborn) or R (ggplot2). |
| [paper-manuscript](./paper-manuscript/) | Generic LaTeX manuscript pipeline: regenerate tables/figures, audit numerical claims, check formatting, and verify cross-references. |
| [programmatic-manuscript-pipeline](./programmatic-manuscript-pipeline/) | Set up a reproducible LaTeX paper pipeline where every figure, table, and number traces to curated source data. |

### Planning & Ideation

| Skill | Description |
|---|---|
| [decision-mapping](./decision-mapping/) | Turn a loose idea into a sequenced map of investigation tickets, then drive them to resolution one at a time. |
| [explain-concept](./explain-concept/) | Explain a complex or technical concept in an easy-to-understand way using a fable or toy story. |
| [framework-design-alternatives](./framework-design-alternatives/) | Brainstorm alternative architectures for a software framework, library, SDK, or protocol, with trade-offs for each option. |
| [grill-me](./grill-me/) | Stress-test a plan or design through a relentless structured interview. |
| [grill-with-docs](./grill-with-docs/) | Stress-test a plan through a relentless interview while producing ADRs and a glossary along the way. |
| [grilling](./grilling/) | Interview the user relentlessly about a plan or design before building starts. |
| [reflect](./reflect/) | Pause mid-task and offer a menu of reflection lenses — pivotal question, failure backtrace, real problem, standard-answer critique, contradicting variables, fact/interpretation/test split, act-as-me. |
| [research-ideation](./research-ideation/) | Develop a research idea into a concrete proposal, paper plan, or experimental design through structured questioning. |
| [research-dashboard](./research-dashboard/) | Track a multi-question research/engineering effort as a dashboard of areas, each with its own effort-scoped plan file, updated as work lands. |

### Presentation

| Skill | Description |
|---|---|
| [nature-paper2ppt](./nature-paper2ppt/) | Turn a paper, preprint, or reading notes into a Chinese PPTX deck for journal clubs, group meetings, or talks. |

### Engineering & Prototyping

| Skill | Description |
|---|---|
| [improve-codebase-architecture](./improve-codebase-architecture/) | Scan a codebase for architecture-deepening opportunities, presented as a visual HTML report with guided follow-up. |
| [prototype](./prototype/) | Build a throwaway prototype — a runnable terminal app for logic questions or multiple toggleable UI variations. |
| [setup-matt-pocock-skills](./setup-matt-pocock-skills/) | One-time repo setup for the engineering skills: issue tracker, triage labels, and domain doc layout. |

### Notes & Knowledge

| Skill | Description |
|---|---|
| [obsidian-vault](./obsidian-vault/) | Search, create, and organize notes in an Obsidian vault with wikilinks and index notes. |

### Skill & Repo Tooling

| Skill | Description |
|---|---|
| [find-skills](./find-skills/) | Discover and install agent skills matching a capability the user is looking for. |
| [handoff](./handoff/) | Compact the current conversation into a handoff document another agent can pick up. |
| [skill-improver](./skill-improver/) | Analyze a session where a skill misfired and iteratively improve that skill's instructions. Use only when explicitly requested. |
| [update-skills-readme](./update-skills-readme/) | Regenerate the categorized skills catalog in README.md and README_zh.md from the current skill directories in this repo. |
| [writing-great-skills](./writing-great-skills/) | Reference for writing and editing skills well — the vocabulary and principles that make a skill predictable. |

### HPC & Infrastructure

| Skill | Description |
|---|---|
| [slurm](./slurm/) | General strategies for orchestrating HPC work through Slurm: job submission, resource requests, and lifecycle management. |
| [slurm-gpu-probe](./slurm-gpu-probe/) | Probe Slurm GPU availability by type and node — free/used counts, start-time estimates — to plan GPU-heavy jobs. |
<!-- SKILLS-CATALOG:END -->

## Installation

Cloning this repository directly into a tool's skills directory installs
all skills at once. If you only want specific skills, clone anywhere and
copy out the directories you need (each skill is self-contained).

### 1) Codex

```bash
git clone https://github.com/lun-ai/skills.git "$CODEX_HOME/skills"
```

> If `$CODEX_HOME/skills` already exists, clone to a temporary location and
> merge instead: `git clone https://github.com/lun-ai/skills.git /tmp/skills && cp -R /tmp/skills/. "$CODEX_HOME/skills/"`.

Usage example:

```text
Use $ai-paper-writing to improve my paper's Introduction.
```

### 2) CC (Claude Code)

Use either a global or project-level installation.

Global:

```bash
git clone https://github.com/lun-ai/skills.git "$HOME/.claude/skills"
```

Project-level:

```bash
mkdir -p .claude
git clone https://github.com/lun-ai/skills.git .claude/skills
```

> If the target directory already exists, clone to a temporary location and
> merge instead: `git clone https://github.com/lun-ai/skills.git /tmp/skills && cp -R /tmp/skills/. "$HOME/.claude/skills/"`.

In prompts, explicitly request a skill by name, for example: `Please use the ai-paper-writing skill`.

### 3) Gemini

```bash
git clone https://github.com/lun-ai/skills.git "$HOME/.gemini/skills"
```

> If `$HOME/.gemini/skills` already exists, clone to a temporary location and
> merge instead: `git clone https://github.com/lun-ai/skills.git /tmp/skills && cp -R /tmp/skills/. "$HOME/.gemini/skills/"`.

Then ask concrete tasks in Gemini (for example, rewriting an Abstract with claim-evidence checks).

## Credits

Again, this repository is primarily based on Prof. Peng Sida (彭思达)'s open notes, while my work focuses on curation and Skills adaptation.
Prof. Peng's original repository: https://github.com/pengsida/learning_research

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE).
