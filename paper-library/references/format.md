# Library layout and formats

```
<library-dir>/            usually papers/
  LIBRARY.md              scope, seed, settings, topics, discovery, log   (hand-edited)
  notes/<stem>.md         one note per paper: metadata, abstract, summary, compare fields
  md/<stem>.md            full text as markdown, standard header          (private)
  BIBLIOGRAPHY.md         generated: every paper by topic
  COMPARE.md              generated: one comparison table per topic
  gaps/<date>-<slug>.md   gap reports written by the gap finder
  inbox/                  PDFs or links dropped by the user, not yet added
```

## Stem

`firstauthor_short-slug_identifier`, lowercase, hyphens inside each part. It is the paper's ID
everywhere and never changes once assigned.

- `firstauthor`: surname of the first author, or the organisation (`anthropic`). Two
  surnames joined by a hyphen when the pair is how the work is known.
- `short-slug`: two to four content words from the title.
- `identifier`: the arXiv number (`2411.02432`), else the date (`2026-07-01` or `2026-07`),
  else the venue or site (`lesswrong`, `preprint`).

Example: `keeling_pain-pleasure-tradeoffs_2411.02432`.

## Note: `notes/<stem>.md`

Template: [../templates/paper-note.md](../templates/paper-note.md).

| Part | Rule |
|---|---|
| `# Title` | The paper's title as published |
| `Authors` | As published. Required |
| `Affiliation` | Optional; shown in brackets in the index |
| `Date` | `YYYY-MM-DD`, `YYYY-MM` or `YYYY`: first public version. Required |
| `Source` | Canonical URL (arXiv abs page, DOI, post). Required; used to detect duplicates |
| `Topic` | One slug from the Topics table in `LIBRARY.md`. Required |
| `Also` | Optional: other slugs the paper bears on, comma-separated |
| `Priority` | `star` for papers a newcomer must read, else `normal`. Required |
| `Full text` | `` `md/<stem>.md` `` or `none`. Required |
| `Fetched` | Date, converter and URL of the copy in `md/`. Written by `convert.py` |
| `## Abstract` | Verbatim from the paper. If there is none, the opening paragraphs, with an italic first line saying so |
| `## Summary` | One or two sentences in your words: method and headline result with its numbers, and how it relates to other papers in the library |
| `## Compare` | Five fields, each one line. See below |

### Compare fields

These make papers comparable and are what gap finding searches first. Fill them from the full
text. Leave a field empty when you have not read enough to fill it; write `none stated` when
you have read it and the paper has nothing.

| Field | Content |
|---|---|
| `System` | What was studied: models, organisms, datasets, populations, with sizes or versions |
| `Method` | What was measured and what was intervened on |
| `Shows` | The main result, with numbers |
| `Does not show` | What the evidence stops short of: missing controls, untested conditions, claims a reader might assume but the paper does not support |
| `Open` | Limitations and future work the authors themselves name, with a line reference |

## Full text: `md/<stem>.md`

Written by `scripts/convert.py`. Starts with a fixed header (title, authors, date, source,
note file, and a notice that the text is machine-extracted with figures removed), then `---`,
then the body. Never edit the body by hand to "fix" content; re-convert instead.

## `LIBRARY.md`

Template: [../templates/library.md](../templates/library.md). The scripts read three things
from it: the `# ` title, `- **Recent from:** <date>` (papers dated on or after it are listed
as recent; leave empty for no split) and the Topics table (`Slug | Topic | Covers`, in display
order). Everything else is for people and agents.

## Generated files

- `BIBLIOGRAPHY.md`: contents list with counts, then per topic the recent papers (starred
  first, newest first), then earlier work. Each entry has title link, authors, date, paths to
  full text and note, abstract and summary.
- `COMPARE.md`: per topic, one row per paper with the five compare fields.
