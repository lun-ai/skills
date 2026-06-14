---
name: document-changes
description: >
  Create a timestamped markdown note in doc/ documenting recent implementation
  changes: new files, modified files, architecture, design decisions, and bug
  fixes. Derives all content from the codebase and git state.
  Use when asked to document a feature, branch, or implementation.
version: 1.0.0
argument-hint: A short description of the feature or branch name to document
---

# Document Changes

Create a markdown file in `doc/` that records what was implemented.

---

## Step 1 — Gather facts from git

```bash
# Current branch name
git branch --show-current

# Files added since diverging from main
git diff --name-status main...HEAD

# Commit messages on this branch
git log main...HEAD --oneline
```

Read any new or heavily modified files to understand their purpose. Do not use
placeholders — derive every section from actual code and git state.

---

## Step 2 — Write the note

**Filename:** `doc/YYYY-MM-DD_<slug>.md`

- `YYYY-MM-DD` is today's date
- `<slug>` is a lowercase-hyphenated summary of the feature or the branch name

**Required sections (omit a section if it has no content):**

### Title
Feature name and date as a top-level heading.

### Branch
The current git branch name.

### Summary
A concise paragraph (3–5 sentences) describing what was done and why.

### New Files
A table of newly created files:

| File | Purpose |
|------|---------|
| path/to/file.py | One-line description |

### Modified Files
A table of changed files:

| File | Changes |
|------|---------|
| path/to/file.py | One-line summary of what changed |

### Architecture
An ASCII diagram or prose description of the system design, if the change
introduced new components, data flows, or inter-module relationships.

### Key Design Decisions
Bullet list of important choices and their rationale. Focus on non-obvious
trade-offs, constraints that shaped the approach, or alternatives that were
considered and rejected.

### Bug Fixes
Issues discovered and resolved during implementation, with a brief explanation
of the root cause and fix.

---

## Step 3 — Create the file

Write the completed document to `doc/<filename>.md`.
Create the `doc/` directory first if it does not exist.

Keep descriptions concise. Every claim must be grounded in the actual codebase
or conversation context — no invented details, no placeholders.
