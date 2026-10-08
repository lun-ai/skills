---
name: dataset-card
description: >
  Produce a dataset card — a Datasheets-for-Datasets structured document with a Hugging Face
  metadata header — whose every statistic is computed from the actual data files rather than
  quoted from prose. Use this skill whenever the user wants to document, profile, characterise
  or audit a dataset before training on it: "make a dataset card", "write a datasheet",
  "what are the statistics of this dataset", "profile this data", "summarise the dataset for
  the paper", "build a dataset table for the methods section", "is this data usable for
  training", "how big is this dataset and what's in it", "check this dataset for leakage or
  duplicates", "what's the label noise here", or when they hand over a data directory, a
  supplementary data file, or a paper and ask what its dataset contains. Also trigger when the
  user asks for dataset statistics in a table, a data section for a manuscript, a
  Hugging-Face-publishable card, class-balance or split diagnostics, or train/test leakage
  checks — even if they never say the words "dataset card" or "datasheet". Prefer this skill
  over answering from a paper's own description, since the point is to measure the files.
  Not for writing journal Data Availability statements (that is nature-data) and not for
  plotting the data (that is nature-figure).
---

# Dataset card

A dataset card answers one question for whoever trains on the data next: *what is actually in
these files, and what will bite me?* Papers and READMEs answer the first half and almost never
the second. Duplicated rows, a class with three examples, a measurement error large enough to
cap achievable accuracy, a held-out split drawn from a different distribution than the training
set — these decide whether a modelling result means anything, and none of them appear in a
paper's dataset paragraph.

So the first governing rule of this skill is: **every number in the card comes from running code
over the files.** A statistic copied out of a paper is labelled as quoted, not measured. When the
two disagree, that disagreement is itself a finding worth reporting.

The second matters just as much, and is easier to violate without noticing. **The card describes
the dataset. It is not a plan for one model.** Whoever asked for it has some use in mind, and
that use legitimately shapes *what you check* — but it must not shape *what you claim*. A card
that recommends a particular split, names the best held-out fold, weighs one encoding against
another, advises what to filter or mask, or rules on whether the data suits the asker's project
has stopped describing the data and started designing someone's experiment. It is then useless
to the next reader, whose task is different, and quietly misleading, because its framing looks
like a property of the data rather than a choice someone made.

The discipline that keeps this honest: report **structure**, not **strategy**. Redundancy rate,
group keys and how much of the data sits in repeated groups, class or level imbalance, the
magnitude of distribution differences between strata, measurement noise and the ceiling it
implies, what a fixed window actually contains, how many annotation sources the data mixes —
these are properties of the dataset, they are what makes a card worth reading, and every reader
needs them whatever they are building. Which split to draw, which representation to use, what
to filter and whether to proceed are their decisions, made against a purpose you do not know.
State the structure precisely enough that those decisions become obvious, and then stop.

## Workflow

### 1. Locate the data and establish provenance

Find the actual files before writing anything. Ask the user for a path if the request names a
dataset without one. If the dataset comes from a paper, the usable data is typically in
supplementary files, a repository accession, or a Zenodo/GitHub snapshot rather than the PDF —
read the paper's Data Availability section to find it, then fetch or ask for the files.

Record for the card: the source (citation, DOI, accession, URL), which files you read, and how
they were obtained. Provenance makes the card reproducible; without it the numbers are just
assertions.

**Datasets are usually partly reachable, and that is the interesting case.** A paper whose Data
Availability says "available on request" often still names public inputs and specifies its
method well enough to rebuild the derived dataset. Rebuilding it from an accession plus a
Methods section is a legitimate and preferred move, not a workaround — and it doubles as a check
on the paper, because your reconstruction either reproduces its reported counts or does not.

So treat reachability per dataset, not per paper. A study typically yields two or more: the
public inputs and whatever was derived from them, and the measurements the authors made. Say
which is which, and profile each part you can reach.

When the unreachable part is **the labels**, record that prominently as a property of the
release: which measurements exist in the publication, in what form they were published, and
whether they can be recovered from it. Write the card over what is reachable and name what
obtaining the rest would require. State the absence as a fact about the data — not as a ruling
on what the asker can or cannot now do with it.

Only when nothing at all can be reached should you say so and stop rather than produce a card of
quoted numbers dressed as measurements. A card whose statistics were never computed is worse
than no card, because the next reader trusts it.

### 2. Classify the dataset, because type decides which statistics matter

Dataset type is an attribute recorded in the card, not a different kind of card. Fill the
`modality` and `task` fields early, because they select the statistic set:

| Modality | Typical primary statistics beyond the universal set |
|---|---|
| tabular | per-field cardinality and missingness, numeric distributions, candidate group keys |
| sequence (DNA/RNA/protein) | length distribution, composition (GC, residue frequencies), redundancy at an identity threshold |
| text | token/character length distribution, vocabulary size, language mix, near-duplicate rate |
| image | resolution and aspect distribution, channel statistics, per-class counts, exact/near duplicates |
| graph | node and edge counts, degree distribution, connected components, feature coverage |
| time series | series count and length, sampling interval regularity, gaps, stationarity flags |
| designed / combinatorial | design-space size and the fraction covered, per-factor level balance, replicate structure |

Read `references/modalities.md` for what each of these means concretely and how to compute it.
A dataset is often two of these at once (a table of sequence identifiers with measured
phenotypes is both tabular and sequence) — compute both sets.

### 3. Compute the universal statistics

Every dataset gets these regardless of type, because every training run can be ruined by them.
`references/aspects.md` holds the definition and formula for each; read it before computing so
the card defines its metrics the same way every time.

- **Scale and schema** — instance count, field count, dtypes, storage size.
- **Missingness** — per field, and whether missingness correlates with the label.
- **Duplicates and contradictions** — exact duplicate instances; duplicate *inputs* carrying
  different labels, which bound achievable accuracy and leak across random splits.
- **Group structure** — what repeats across instances (source paper, patient, session, design,
  organism). This decides whether a split may be drawn at random, and it is the single most
  common cause of overstated published accuracy.
- **Label statistics** — for regression: n, mean, standard deviation, range, skew, excess
  kurtosis, coefficient of variation. For classification: per-class counts, imbalance ratio,
  rarest-class count.
- **Label noise and the ceiling it implies** — when the data reports replicate error or has
  repeated measurements, compute the share of label variance that is measurement noise and the
  best score any model could therefore reach. A reported R² of 0.90 means something very
  different against a ceiling of 0.97 than against 0.91.
- **Stratum shift** — when the data ships predefined groups (train/test, library/recommended,
  cohort A/B), compare their label and feature distributions. A held-out set selected to be
  extreme is a covariate-shift test, not a random holdout, and the card should say so.
- **Reference performance** — any published accuracy on this data, with the exact subset and
  metric it was computed on, so a new result is comparable.

Report each of these as a measurement with its definition, in the card's own terms. Resist
appending the consequence: "37.8% of within-paper pairs share an input" is a property of the
data, while "so group your folds by paper" is advice, and the first already tells a careful
reader the second.

**Name the model-input columns explicitly** (`--input-cols`) rather than letting them default to
every non-target column. Duplicate and group checks are computed over whatever you call the
input, and a unique identifier among those columns makes every row look distinct — so a dataset
with 254 duplicate sequences reports zero duplicates. For sequence, text and image data the unit
that repeats is usually one column (the sequence, the document, the file hash), not the row.

Run `scripts/profile_dataset.py` for the tabular backbone of this; it covers scale, schema,
missingness, cardinality, duplicates, candidate group keys, label statistics and target
correlations, and emits both JSON and ready-to-paste Markdown tables:

```bash
python scripts/profile_dataset.py <data-file-or-dir> \
    --target <label-column> [--target <second-label>] \
    --group <group-column> --out <workdir>
```

It handles CSV, TSV, Parquet, JSON Lines and Excel. For anything it does not cover — sequence
composition, image resolutions, graph degree — write a short script, run it, and keep it beside
the card as an artifact. Writing the computation down as code that runs is what makes the card
checkable later; a number derived by eye cannot be re-derived.

### 4. Verify before you believe your own output

Aggregation bugs produce plausible wrong numbers rather than crashes: a regex that silently
matches nothing, a join that drops rows, a glob that mishandles spaces in filenames, a blank
padding block counted as real instances. Three cheap checks catch most of it:

- Confirm the script ran with zero errors, and that its instance count reconciles with the
  file's own row count and with any count the source publication states. An unexplained gap is
  a finding — trailing blank rows, deduplication, or filtered records.
- Spot-check one aggregate by hand against the underlying file. Pick the statistic the card
  most depends on and verify that single number manually.
- Check that per-group counts sum to the total. If they do not, a group key is missing or
  overlapping.
- **Re-derive a second, independent statistic the source reports** — not just the headline
  count. Matching one number can happen by luck or by two errors cancelling; matching a second
  of a different kind is strong evidence the whole reconstruction is right. When the second one
  disagrees, the resolution is usually a convention the source never stated, which is itself
  worth putting in the card.

### 5. Write the card

Copy `references/card-template.md` and fill it. It is a Hugging Face metadata header followed by
the Datasheets-for-Datasets sections (motivation, composition, collection, preprocessing,
uses, distribution, maintenance), with the training-facing statistics tables folded into
composition. The header keeps the card publishable to a dataset hub; the Datasheets sections
keep it answerable by someone deciding whether to use the data at all.

Two conventions that keep the card honest as it is filled:

- **Leave a field blank when the aspect does not apply** to this dataset. An empty cell is
  information: it says this dataset has no held-out split, or no replicate error, or no class
  labels. Do not invent a value and do not pad with "N/A" prose.
- **Write `not determined` when the aspect applies but you could not measure it**, with one
  clause saying why. The distinction between "does not apply" and "applies, unmeasured" is
  exactly what the next reader needs, and collapsing both to a blank hides work still to do.

Mark each statistic's origin: measured here, or quoted from the source. The template carries a
provenance column for this. Anything you quote, attribute.

### 6. Report, context before numbers

Open the reply with what the dataset is, where the files came from, and what the metrics mean
by definition — then the tables. A number with no setting attached is unreadable to anyone who
was not in the session with you, including the same user next week. Name any statistic that
contradicts the source publication, and any finding the source never recorded; those are the
reasons a card is worth producing rather than citing the paper.

Keep interpretation separate. State the measured facts, then offer a read in one line if the
user wants one. Whether a dataset is "good enough" for a purpose is their call, made against
that purpose, and it changes with what they intend to build — so it belongs in the reply if they
ask for it, never in the card, which outlives the conversation that prompted it.

Save the card next to the data or wherever the user keeps documentation, and tell them the path
plus the artifacts (profiling script, JSON output) that produced it.

## Reference files

- `references/aspects.md` — every aspect with its definition, formula, and why it matters.
  Read before computing, so the card's metric definitions stay consistent.
- `references/modalities.md` — per-type statistics: tabular, sequence, text, image, graph,
  time series, designed/combinatorial. Read the sections matching the dataset's modality.
- `references/card-template.md` — the card to copy and fill, with the Hugging Face header and
  the Datasheets sections.
- `scripts/profile_dataset.py` — the tabular profiler described in step 3.
