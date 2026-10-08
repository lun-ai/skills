# Card template

Copy the block below and fill it. Conventions:

- **Blank cell** — the aspect does not apply to this dataset. An empty cell is information.
- **`not determined`** — the aspect applies but was not measured, plus one clause saying why.
- **Provenance column** — one of three values:
  - `measured` — you computed it from files the source distributed.
  - `reconstructed` — you computed it from files *you* rebuilt by reimplementing the source's
    method. Weaker than `measured`, because a reconstruction can be faithful in aggregate and
    wrong in detail, so fill in the Reconciliation subsection whenever this value appears.
  - `quoted` — taken from the source, which is named.
- **Keep every section and its order**, so two cards can be read side by side. When an aspect
  does not apply, leave its cell blank; when a whole subsection does not apply — the label
  sections of an unlabelled corpus, for instance — keep the heading and replace the table with
  one line saying why it is empty. A reader needs to see that the question was asked and
  answered "not applicable", which a deleted section cannot convey.
- Define each metric where it first appears, in one clause. The reader does not have
  `aspects.md`.

The Hugging Face header uses that hub's controlled vocabularies for `license`,
`task_categories` and `size_categories`; leave a field out rather than inventing a value that
is not in the vocabulary. The header is what makes the card publishable as-is; the sections
below it are Datasheets for Datasets (Gebru et al., 2021), trimmed to the questions a training
decision actually turns on.

---

```markdown
---
pretty_name: <human-readable name>
license: <spdx id, or leave out if unknown>
language:
  - <iso code, for text data>
task_categories:
  - <hub vocabulary, e.g. tabular-regression, text-classification>
tags:
  - <free-form, e.g. modality and domain>
size_categories:
  - <n<1K | 1K<n<10K | 10K<n<100K | ...>
configs:
  - config_name: default
    data_files: <path or glob>
---

# Dataset card: <name>

One paragraph, plain language: what one instance is, what is predicted from what, and where the
data came from. Someone who has never seen this dataset should be able to read this paragraph
and know whether it is relevant to them.

| Attribute | Value |
|---|---|
| Modality | <tabular / sequence / text / image / graph / time series / designed> |
| Task | <regression / classification / generation / ...>, <single- or multi-target> |
| Instances | |
| Fields | |
| Targets | |
| Predefined splits | |
| Source, inputs | <accession, repository, DOI for the upstream data> |
| Source, derived | <citation for the work that derived or measured it> |
| Files read | |
| Obtained by | <command, script or route> |
| Reconstructed? | <no / yes, with the script that rebuilds it> |
| Date profiled | |
| Profiled with | <script paths> |

## Motivation

Why the dataset was created, by whom, under what funding, and for what original task. Note
where your intended use diverges from that original purpose — a dataset built to compare two
recommenders is being reused if you train a representation model on it, and the divergence
usually explains the limitations section.

## Composition

### Scale and schema

| Field | Type | Missing | Distinct | Notes | Provenance |
|---|---|---|---|---|---|

State the reconciliation: instance count against raw row count against the count the source
publication reports, and the explanation for any gap.

### Reconciliation

Fill this whenever any number is `reconstructed`, or whenever your instance count differs from
the source's. State each count the source reports against the count you obtain, the agreement,
and the explanation for any gap. Include at least one *second*, independent statistic from the
source as a cross-check on the reconstruction, and record any convention you had to infer to
make it agree — an inferred convention the source never stated is a finding in its own right.

| Quantity | Source reports | This reconstruction | Agreement | Note |
|---|---|---|---|---|

### Strata

| Stratum | n | Role | Label mean ± SD | Label range | Provenance |
|---|---|---|---|---|---|

### Target statistics

| Statistic | <target 1> | <target 2> | Provenance |
|---|---|---|---|
| n / missing | | | |
| Mean ± SD | | | |
| Range | | | |
| Median | | | |
| Coefficient of variation | | | |
| Skew / excess kurtosis | | | |
| Per-class counts | | | |
| Imbalance ratio | | | |
| Rarest class count | | | |

Define every metric used, once, immediately below the table.

### Label noise and achievable ceiling

| Statistic | Value | Provenance |
|---|---|---|
| Replicate error available | | |
| Noise variance fraction | | |
| Implied ceiling on R² | | |
| Reliability (ICC) | | |
| Groups the estimate rests on | | |

State the formula used, so the ceiling is interpretable.

### Multi-target structure

Correlation among targets, with shared variance, and the nuisance-target risk it implies.

### Duplicates, contradictions and group structure

| Check | Value | Provenance |
|---|---|---|
| Exact duplicate instances | | |
| Duplicate inputs, identical label | | |
| Duplicate inputs, differing label | | |
| Within-group disagreement | | |
| Near-duplicates at <threshold> | | |
| Candidate group keys | | |
| Groups / median / max per group | | |
| Random split over instances safe? | | |

### Modality-specific statistics

The table from the relevant section of `modalities.md`.

### Feature diagnostics

Cardinality and rare levels, level balance, constant fields, collinear fields, fields that must
not reach a model because they encode the outcome or the collection order, and the data's native
dimensionality against its instance count.

## Collection

How the data was measured or gathered: instruments, protocol, annotation process and annotator
count, time window, sampling frame. Whether instances are a sample or a census of the frame,
and if a sample, how it was drawn — random, convenience, or model-selected.

## Preprocessing

What was done to the raw data before it became these files, and what you did before profiling:
filtering, deduplication, joins, unit conversion, normalisation. Whether the raw data remains
available. This section is what lets someone reproduce your instance count.

## Uses

This section records what the dataset has been used for and the structure that bears on using
it again. It does not recommend a use. A card is read by people building things you cannot
anticipate, so state the properties and let each of them decide.

### Prior use

What the data has already been used for, by the authors and by others, with citations. This is
the most reliable guide to what it supports, and unlike a recommendation it is checkable.

### Split-relevant structure

The facts a reader needs to choose a split, with no choice made for them: the candidate group
keys and the fraction of instances sitting in groups larger than one; how similar group members
are in the data itself; redundancy at a stated threshold; the magnitude of any distribution
difference between strata; and whether a time axis exists and over what span. Counts, not
counsel.

### Reference performance

| System | Metric | Subset | n | Score | Split protocol | Provenance |
|---|---|---|---|---|---|---|

Published scores are `quoted`. Note any difference between the subset the publication scored on
and the subset a new model would train on, since that difference is what makes the comparison
unfair if unstated.

### Composition effects on future use

Properties of how the data was assembled that will show up in anything fitted on it, each stated
as a measured fact rather than a warning: heterogeneity of sources or annotation vintages, what
a fixed window or crop actually contains, confounding between fields, selection applied to any
stratum. Name the mechanism and give the number; leave the mitigation to the reader.

### Scope

What the data does not cover: populations and conditions absent, proxy measurements standing in
for the quantity of interest, resolution or window choices baked into the files, provenance
mismatches. Scope, not judgement — the boundary of what the files contain, not a verdict on
whether that is enough for a purpose you do not know.

## Distribution and maintenance

License and terms, where the data is hosted and under what identifier, whether it is versioned,
who maintains it, and whether it is expected to change. State the terms for the inputs and for
the derived data separately when they differ — a public-domain reference corpus described in a
copyrighted paper is the normal case, and the two travel under different rules. Note any redistribution restriction that
affects whether derived files can be shared.

## Artifacts

The scripts and outputs that produced every measured number in this card, by path.
```
