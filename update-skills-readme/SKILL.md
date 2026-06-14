---
name: update-skills-readme
description: >
  Regenerate the categorized skills catalog in README.md and README_zh.md
  from the current set of skill directories in this repo. Use whenever a
  skill is added, removed, renamed, or its SKILL.md description changes —
  to keep the bilingual skills catalog in both READMEs in sync with the
  repo's actual contents.
---

# Update Skills README

Keeps the "Repository Overview" skills-catalog tables in `README.md` and
`README_zh.md` synchronized with the skill directories that actually exist
in this repo.

## Workflow

1. Run the discovery script from the repo root:

   ```bash
   python3 update-skills-readme/scripts/list_skills.py
   ```

   This prints a JSON array of `{name, dir, description, has_frontmatter}`
   for every top-level directory containing a `SKILL.md`. Entries with
   `"has_frontmatter": false` are missing a usable `name`/`description` in
   their frontmatter — flag these in your final report for manual attention.

2. Open `update-skills-readme/categories.yaml`. For every skill `dir` from
   step 1 that does not appear in any category's `skills` list, decide which
   existing category fits best based on its description, or — if none fit —
   add a new category. Append the skill to the chosen category's `skills`
   list. For every skill name in `categories.yaml` that no longer appears in
   the step-1 output, remove it (the skill was deleted or renamed).

3. For each skill, write one concise (~15-20 word) human-facing description
   for the catalog: English for `README.md`, Chinese for `README_zh.md`. Do
   not reuse the raw frontmatter `description` verbatim — those are
   trigger-keyword lists for skill matching, not README prose.

4. Render one markdown table per category, in the order categories appear in
   `categories.yaml`, with skills sorted alphabetically within each category:

   ```markdown
   ### <Category Name>

   | Skill | Description |
   |---|---|
   | [<dir>](./<dir>/) | <one-line description> |
   ```

5. In each README, replace everything between
   `<!-- SKILLS-CATALOG:START -->` and `<!-- SKILLS-CATALOG:END -->` (inside
   "## Repository Overview" / "## 仓库介绍") with the rendered tables. Update
   the sentence immediately above the markers to state the current total
   skill count.

6. Report a short diff vs. the previous catalog: skills added, removed, or
   renamed, plus any `has_frontmatter: false` flags from step 1.

## Notes

- This workflow does not touch Installation/Credits/License — if those need
  updating, do it separately.
- `categories.yaml` is the source of truth for grouping and ordering. Keep it
  in this skill's directory (`update-skills-readme/categories.yaml`).
