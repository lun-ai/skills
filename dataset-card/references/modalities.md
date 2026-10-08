# Per-modality statistics

Read the sections matching the dataset's `modality` field. Many datasets are two modalities at
once — a table of identifiers with measured outcomes is tabular *and* whatever the identifiers
point at — so compute both sets and say in the card that you did.

The universal statistics in `aspects.md` still apply to every modality. What follows is what
each type adds.

## Tabular

`scripts/profile_dataset.py` covers most of this. Beyond its output, judge:

- Which fields are the model **input** and which are **metadata** that must never be fed to it
  (identifiers, timestamps, provenance, anything recorded after the outcome). Record the split
  explicitly; the most common leakage is an index column correlating with a sorted label.
- Units per numeric field, and whether one field mixes units across rows. Mixed units are
  common in text-mined and multi-source tables and silently destroy a regression target; report
  the fraction of rows per unit family rather than converting silently.
- Whether categorical levels are consistently spelled. Count distinct raw strings against
  distinct resolved entities; a gap between them (3,645 product strings resolving to 1,340
  chemicals) is a curation finding, not a detail.

## Sequence — DNA, RNA, protein

- **Length distribution** — n, min, median, max, and the count outside any window the task
  assumes. State the window the data actually uses against the window the source defines; a
  truncation chosen for compute reasons belongs in the card, not in a script's default.
- **Does the window contain what it is named after?** When instances are a fixed span relative
  to some landmark — so many bases upstream of a start codon, so many tokens before a mention,
  a fixed crop around a detection — measure how often that span runs past the feature it claims
  to represent and into neighbouring content. A fixed window is an extraction choice, and the
  overrun rate decides whether a per-instance model learns the named feature or its neighbour.
  Averaged statistics tolerate this; a trained model does not. The same check applies to fixed
  windows in time series and fixed crops in images.
- **Composition** — GC content for nucleotides (range across the set, not just the mean),
  residue frequencies for protein. Composition outliers are often contamination or placeholders.
- **Alphabet validity** — characters outside the expected alphabet, ambiguity codes (`N`, `X`),
  and their per-sequence fraction. Decide and record whether ambiguous sequences are kept.
- **Redundancy at an identity threshold** — cluster at a stated identity (e.g. 90%) and report
  cluster count against sequence count. With no clustering tool installed, a k-mer Jaccard
  proxy (MinHash with locality-sensitive hashing to screen pairs, then exact Jaccard on the
  candidates) is an acceptable substitute as long as the card states the k and the threshold and
  says alignment identity was not used; it finds somewhat less redundancy than alignment would,
  so report it as a lower bound rather than leaving the aspect undetermined. Homologous sequences split at random across folds is
  the standard way sequence models get overrated, and the clustering is what a card needs so a
  later reader can split by cluster instead.
- **Distinct sequences against distinct instances** — when instances reuse a small set of
  sequences combinatorially, say so and give both counts. A dataset of 307 designs built from
  30 reusable fragments has 30 degrees of freedom on the sequence side, however many rows it has.
- **Reference build and organism**, and any mismatch between the genome the sequences were read
  from and the strain or individual actually measured.

## Text

- **Length distribution** in both tokens (naming the tokenizer) and characters.
- **Vocabulary size** and the out-of-vocabulary rate under the intended tokenizer.
- **Language mix**, detected rather than assumed, with per-language counts.
- **Near-duplicate rate** at a stated threshold — MinHash/Jaccard on shingles, or embedding
  cosine. Report both exact and near-duplicate counts; web-derived corpora routinely carry
  double-digit near-duplicate percentages that a random split spreads across train and test.
- **Boilerplate and template share** — the fraction of instances dominated by repeated
  scaffolding, which inflates instance counts without adding information.
- **Contamination against known benchmarks**, when the data will train a model later evaluated
  on public benchmarks. State what you checked against; "not checked" is a legitimate entry.

## Image

- **Resolution distribution** and aspect-ratio distribution, with the count of images below any
  resolution the intended model requires.
- **Channel and bit depth** mix, including greyscale images in a nominally colour set.
- **Per-class counts**, and for detection or segmentation the per-class instance counts and the
  objects-per-image distribution.
- **Exact and perceptual duplicates** — hash for exact, perceptual hash for near. Report the
  cross-split duplicate count when a split already exists.
- **Corrupt or truncated files**, counted by actually decoding every image rather than trusting
  extensions.
- **Capture metadata** where present (device, site, date) — these are group keys, and a model
  that learns the site instead of the condition is the classic failure this surfaces.

## Graph

- **Nodes and edges**, directedness, whether multi-edges and self-loops occur.
- **Degree distribution** — min, median, max, and the isolated-node count.
- **Connected components** — count and the largest component's share. A link-prediction split
  drawn at random over edges leaks through shared neighbourhoods; the card should state the
  component structure so a later reader can split by component or by time.
- **Feature coverage** — the fraction of nodes and edges carrying each feature.
- **Label coverage** — for node or edge classification, the fraction labelled, and whether
  labelled nodes are distributed across components or concentrated.

## Time series

- **Series count** and per-series length distribution.
- **Sampling interval** — nominal against observed, with the fraction of irregular intervals.
- **Gaps** — count and duration distribution of missing stretches, per series.
- **Temporal extent** per series and overall, and whether series overlap in time.
- **Stationarity and seasonality flags** from an explicit test, naming the test.
- **Split protocol** — a time series split at random over timestamps leaks the future into the
  past. Record the intended cutoff and the instance counts either side of it.

## Designed / combinatorial

Experimental libraries, factorial designs, perturbation screens, prompt grids.

- **Design space size** — the product of the level counts across factors — and the **covered
  fraction**, instances ÷ design space. A library covering 3% of its space supports very
  different claims than one covering 80%.
- **Per-factor level balance** — min, median and max instances per level, per factor. Designed
  does not mean balanced; sampled libraries are routinely lopsided.
- **Replicate structure** — how many designs appear more than once, how many instances that
  involves, and the within-design label spread. This is the ceiling estimate in `aspects.md`
  and in designed data it is usually computable, so compute it.
- **Factor interaction coverage** — the fraction of factor *pairs* whose level combinations are
  all observed. Main effects can be estimable while interactions are not, and a model fitted on
  interactions that were never sampled is extrapolating.
- **Selected versus sampled strata** — designs chosen by a prior model or by an experimenter are
  not exchangeable with randomly sampled ones. Keep them as separate strata and run the stratum
  shift comparison from `aspects.md`.
