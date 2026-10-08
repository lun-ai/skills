# Aspects, with definitions and formulas

Read this before computing, so the card defines each metric the same way every time. Every
definition here is written to be quotable directly into the card — the card should define a
metric the first time it uses it, in one clause, because the reader will not have this file.

## Contents

- [Provenance](#provenance)
- [Scale and schema](#scale-and-schema)
- [Missingness](#missingness)
- [Duplicates and label contradictions](#duplicates-and-label-contradictions)
- [Group structure and split safety](#group-structure-and-split-safety)
- [Label statistics, regression](#label-statistics-regression)
- [Label statistics, classification](#label-statistics-classification)
- [Label noise and the achievable ceiling](#label-noise-and-the-achievable-ceiling)
- [Multi-target structure](#multi-target-structure)
- [Stratum shift](#stratum-shift)
- [Feature diagnostics](#feature-diagnostics)
- [Reference performance](#reference-performance)
- [Limitations](#limitations)

## Provenance

Source citation, DOI, accession number or URL; the exact files read, with sizes; how they were
obtained (download command, script, manual export); the date read. A card without provenance
cannot be reproduced or audited, which defeats the point of computing the numbers.

Note the distinction between the *source* dataset and *your* reading of it. If you filtered,
deduplicated or joined before profiling, the card describes the result of those steps and must
say what they were.

## Scale and schema

- **Instances** — rows, examples, records. State what one instance *is* in a sentence; it is
  rarely obvious and the whole card depends on it.
- **Fields** — count and dtypes. Flag fields that look numeric but parse as text, a common
  source of silent breakage.
- **Storage size** — on disk, and in memory once loaded if that gap matters.
- **Reconciliation** — the instance count against the file's row count and against any count
  the source publication states. Trailing blank rows, header rows counted as data, and
  multi-sheet workbooks all cause gaps. An unexplained gap goes in the card as a finding.

## Missingness

Per field: the count and fraction of instances with no value. Treat empty strings, sentinel
values (`-999`, `NA`, `unknown`) and whitespace as missing, since loaders often do not.

Then the question that matters more than the rate: **is missingness related to the label?**
Compare the label distribution between instances missing a field and instances carrying it. If
they differ, dropping incomplete rows biases the training set, and imputation choices become
part of the result rather than a preprocessing detail.

## Duplicates and label contradictions

First decide **what the input actually is**, because every count below is computed over it. If
the comparison includes an identifier, a timestamp or any per-instance unique field, every
instance is trivially distinct and the duplicate rate comes back as zero no matter how much
redundancy the data holds. For sequence, text and image data the input is typically a single
column; for tabular data it is the feature set minus metadata. Name it, and say in the card
which fields it comprised.

Three distinct things, often conflated:

- **Exact duplicate instances** — identical in every field. Usually a data-handling artifact.
- **Duplicate inputs with identical labels** — the same input repeated. Harmless for
  correctness, but they inflate the effective dataset size and land on both sides of a split
  drawn at random, producing optimistic held-out scores.
- **Duplicate inputs with differing labels** — the same input measured twice with different
  outcomes. These are the informative case. They are replicates, and the spread between them
  is a direct estimate of irreducible error: no model can predict both values. Report how many
  such groups exist, how many instances they involve, and the distribution of within-group
  disagreement.

For text, sequence and image data, add **near-duplicates** at a stated threshold (edit distance,
sequence identity, embedding cosine, perceptual hash), since exact matching misses most real
redundancy. Always state the threshold — a near-duplicate rate without one is uninterpretable.

## Group structure and split safety

Look for any field, or any derivable key, along which instances repeat: source publication,
patient, subject, session, site, batch, device, design, organism, time window, parent document.

For each candidate group key report: number of groups, median and maximum instances per group,
and the fraction of instances in groups larger than one. Then quantify how much group members
resemble each other in the data itself — the fraction of within-group instance pairs whose
values are identical, or whose similarity exceeds the threshold you used for near-duplicates.

That similarity figure is the measurement a reader needs, and it is the one almost always
missing. Report it and stop there: do not prescribe a split. Which key to group on, or whether
to group at all, depends on what the reader is estimating and on how much leakage they are
willing to accept, and a card that answers for them is making a decision it cannot see the
inputs to. "100% of instances sit in groups larger than one, and 37.8% of within-group pairs
have identical inputs" is complete; adding "so split by group" is not more informative, only
less neutral.

## Label statistics, regression

Per target: n, missing count, mean, standard deviation, minimum, maximum, median, skew, excess
kurtosis, and coefficient of variation.

- **Coefficient of variation** = standard deviation ÷ mean. Scale-free spread; it makes two
  targets in different units comparable.
- **Skew** near zero and **excess kurtosis** near zero indicate a roughly normal target. Report
  these because they decide whether a transform helps. If you test a transform, report the
  statistics after it too — a log transform applied reflexively to a left-skewed target makes
  the skew worse, and the card should record that rather than the habit.

## Label statistics, classification

Per class: count and fraction. Then:

- **Imbalance ratio** = largest class count ÷ smallest class count.
- **Rarest-class count** — the absolute number, not just the fraction. A class at 0.4% of a
  million instances is 4,000 examples and fine; at 0.4% of 700 it is three examples and cannot
  support a held-out estimate at all.
- **Effective instances per class under the intended split** — the rarest class's count divided
  by the number of folds. This is what a per-class held-out metric is actually computed on, and
  it is routinely one or two instances for the tail classes.

For multi-label data, add label cardinality (mean labels per instance) and the co-occurrence of
the most frequent pairs.

## Label noise and the achievable ceiling

The most useful statistic a card can carry, and the one almost always absent. It answers: *what
score would a perfect model get?*

**When the data reports a standard error per measurement** (common in experimental data, where
each instance is a mean over replicates):

```
noise variance fraction = (mean reported standard error)² ÷ variance(target)
implied ceiling on R²   = 1 − noise variance fraction
```

State both, and state the definition in the card, because the number is meaningless without it.
A dataset with a ceiling of 0.91 on which a model reaches 0.88 is nearly solved; the same 0.88
against a ceiling of 0.99 is not.

**When the data has replicate measurements of the same input** (the duplicate-inputs-with-
differing-labels case above), decompose the variance instead:

```
within-group variance  = mean over groups of the variance among that group's labels
between-group variance = variance of the per-group means
reliability (ICC)      = between ÷ (between + within)
```

Reliability is the ceiling on squared correlation. Report the number of groups it rests on; an
ICC from nine replicate pairs is an estimate with wide uncertainty, and the card should say so
rather than presenting it as a fact.

**When both are available, compute both and reconcile them.** They answer slightly different
questions — the reported standard error describes the precision of each instance's own
measurement, while the ICC describes how reproducibly the whole pipeline returns the same value
for the same input, and so absorbs build-to-build and batch variation that a within-instance
standard error never sees. A large gap between them is therefore a finding, not an error to
pick a winner from: on one experimental library the standard errors imply a ceiling of 0.977
while nine replicate pairs give an ICC of 0.787, because a single discordant pair dominates the
within-group variance. Report both with their n, say which is the looser bound, and check
whether a handful of outlying replicate groups drive the lower estimate before treating it as
the ceiling.

**When neither is available**, leave the aspect blank and say replicate information is absent.
Do not substitute a guess — an invented ceiling is worse than an acknowledged gap, because
every later result gets judged against it.

## Multi-target structure

When a dataset carries several labels, report the correlation matrix among them (Pearson and
Spearman), and the shared variance (r²) for any pair.

This matters because the targets are not independent problems. If production rate correlates
with growth rate at r = 0.64, then 41% of the headline target's variance is shared with
fitness. Report the coupling and name both quantities plainly; what a reader should therefore
measure or report is their call.

## Stratum shift

When the data ships predefined groups — train/test, cohorts, library versus selected,
pre/post — do not assume they are exchangeable. For each stratum report n and the label
distribution (mean, standard deviation, range), then quantify the gap:

```
standardised mean difference = (mean_A − mean_B) ÷ pooled standard deviation
```

Report the magnitude; the reader draws the consequence. A standardised mean difference past
roughly half a pooled standard deviation means the strata are not exchangeable, which is a
property of how the data was assembled — often because one stratum was selected rather than
sampled. Say which stratum was selected and how, since that is the fact behind the number.

## Feature diagnostics

- **Cardinality** per categorical field, with the rarest level's count. Rare levels cannot be
  learned and cannot be held out.
- **Level balance** per factor, for designed data: the minimum, median and maximum count across
  levels. A factor with levels at 3 and 88 instances is not a balanced factor.
- **Constant and near-constant fields** — zero variance, or a single value in over ~99% of
  instances. They carry no signal and often indicate a collection problem.
- **Duplicate and perfectly collinear fields** — the same information under two names.
- **Target leakage candidates** — any field correlating with the label far more strongly than
  domain knowledge allows, or any field computed after the label was known. Flag these
  explicitly; they are the mechanism behind most too-good-to-be-true results.
- **Native dimensionality** against the instance count — the number of fields for tabular data,
  sequence length, image pixel count, vocabulary size. Report what the data *is*. Do not score
  candidate encodings or recommend one: which representation to build, and what
  instance-to-feature ratio is acceptable, belongs to whoever is fitting the model.

## Reference performance

Any published score on this data: the system, the metric, the exact subset and its n, and the
split protocol. Subset matters as much as the number — a published R² on 260 instances including
controls is not comparable to one on 254 library instances, and a card that records only the
number invites exactly that comparison.

Record the reference as quoted, not measured, and note any difference between the subset the
publication used and the subset a new model would train on.

## Limitations

Close with what the data cannot support, stated as scope rather than judgement: populations or
conditions not represented, measurement proxies standing in for the quantity of interest,
window or resolution choices baked into the files, known provenance mismatches (a reference
genome differing from the strain actually assayed, annotations from a different build, labels
transferred from a related task).

These are the facts that stop a later reader from asking the data a question it cannot answer.
