# `update-skills-readme` skill — design

Date: 2026-06-14

## Problem

This repo (`lun-ai/skills`) is a collection of skill packages (one directory
per skill, each with a `SKILL.md`). It started with a single skill
(`ai-paper-writing`) and `README.md` / `README_zh.md` were written to match
— a short "Repository Overview" describing that one package, plus
installation instructions that `cp -R ai-paper-writing` into a target skills
directory.

The repo now has 21 skill directories spanning several distinct areas
(general paper writing/review, a `nature-*` cluster of 9 Nature/CNS-specific
skills, manuscript pipeline tooling, HPC, and meta/skill-tooling). The
READMEs no longer reflect this and will keep drifting every time a skill is
added, renamed, or removed.

## Goal

Create a skill, `update-skills-readme`, that regenerates a categorized
skills-catalog section in both `README.md` and `README_zh.md` from the
current set of skill directories, and run it now to bring both READMEs up to
date.

## Non-goals

- Translating or rewriting the per-skill `SKILL.md` files themselves.
- Enforcing a particular `SKILL.md` frontmatter schema (the skill must cope
  with skills that have no/partial frontmatter).
- Automating the Installation/Credits/License sections beyond the one-time
  generalization described below.

## Design

### 1. Discovery script: `update-skills-readme/scripts/list_skills.py`

Walks the repo root; for each top-level directory containing `SKILL.md`:

- If the file starts with a `---`-delimited YAML frontmatter block, parse it
  with `yaml.safe_load` (PyYAML, confirmed available — 6.0.1) and read
  `name` / `description`.
- Fallbacks for robustness (no frontmatter, or missing/malformed fields):
  - `name` defaults to the directory name.
  - `description` defaults to the first non-empty paragraph of body text
    (with markdown headings stripped).
  - `has_frontmatter: false` is set so the skill's report can flag these for
    manual attention.
- Output: JSON array of `{name, dir, description, has_frontmatter}`,
  sorted by `dir`.

This makes discovery independent of frontmatter quality — a skill with a
broken or missing frontmatter still shows up in the catalog (flagged) rather
than silently disappearing.

### 2. Category map: `update-skills-readme/categories.yaml`

An open-ended, persisted list of categories, each with an ordered list of
skill names:

```yaml
categories:
  - name: "Writing & Polishing"
    skills: [ai-paper-writing, nature-writing, nature-polishing]
  - name: "Reviewing & Feedback"
    skills: [ai-paper-reviewer, nature-reviewer, nature-response]
  - name: "Literature, Reading & Citation"
    skills: [nature-academic-search, nature-reader, paper-summarizer, nature-citation]
  - name: "Manuscript Pipeline & Data"
    skills: [paper-manuscript, programmatic-manuscript-pipeline, nature-data, nature-figure, document-changes]
  - name: "Planning & Ideation"
    skills: [research-ideation, framework-design-alternatives, explain-concept]
  - name: "Presentation"
    skills: [nature-paper2ppt]
  - name: "Skill & Repo Tooling"
    skills: [skill-improver, update-skills-readme]
  - name: "HPC & Infrastructure"
    skills: [slurm]
```

- The number and order of categories is whatever is in this file — not
  hardcoded to two or any fixed count.
- One markdown table is rendered per category, in file order.
- Within a category, skills are sorted alphabetically by name.

### 3. Workflow (`update-skills-readme/SKILL.md`)

1. Run `scripts/list_skills.py` to get the current skill inventory.
2. Load `categories.yaml`. For any skill present in the inventory but absent
   from every category's `skills` list, assign it to the best-fit existing
   category based on its description (using judgment), or — if nothing
   fits — propose a new category. Persist the updated mapping back to
   `categories.yaml`.
3. For any skill name in `categories.yaml` that no longer exists in the
   inventory, remove it from the map (skill was deleted/renamed).
4. For each skill, write a concise (~15–20 word) human-facing one-line
   description for the catalog — English for `README.md`, Chinese for
   `README_zh.md`. (The raw frontmatter descriptions are trigger-keyword
   lists for skill matching, not README prose.)
5. Render one markdown table per category: `| Skill | Description |`, skill
   name linked to `./<dir>/`.
6. In each README, replace everything between
   `<!-- SKILLS-CATALOG:START -->` and `<!-- SKILLS-CATALOG:END -->` inside
   the "Repository Overview" section with the rendered tables (creating the
   markers on first run if absent). Update the overview's intro sentence to
   state the current total skill count.
7. Print a short diff vs. the previous catalog content: skills added,
   removed, or renamed, and any `has_frontmatter: false` flags.

### 4. One-time Installation section update (part of "apply now", not part
of the recurring skill workflow)

Replace the `ai-paper-writing`-specific `cp -R ai-paper-writing ...` examples
in both READMEs with cloning the whole repo into the target skills
directory, e.g.:

```bash
git clone https://github.com/lun-ai/skills.git "$HOME/.claude/skills"
```

(and the project-level / Codex / Gemini equivalents, substituting the target
directory). A short note clarifies that this installs all skills at once;
individual skill directories can still be copied out if only one is wanted.

## Applying the skill now

After creating `update-skills-readme/`:

1. Add it to `categories.yaml` under "Skill & Repo Tooling".
2. Run the skill's workflow to populate the catalog sections of both
   READMEs for the current 22 skills (21 existing + itself).
3. Apply the one-time Installation section generalization.
4. Report the diff (in this case, "added" = all current skills, since this
   is the first run).
