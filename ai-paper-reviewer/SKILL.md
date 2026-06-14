---
name: ai-paper-reviewer
description: >
  Use this skill whenever the user wants Claude to review an academic paper for submission to a conference or journal. Triggers include: any mention of "review my paper", "paper review", "peer review", "submission feedback", "reviewer comments", or when the user shares a paper (PDF or text) and names a target venue (e.g., NeurIPS, ACL, ICML, CVPR, ICLR, EMNLP, Nature, Science, CHI, SIGCOMM, VLDB, etc.). Also trigger when the user asks for scores, novelty assessment, or feedback on a paper's chances of acceptance. Use this skill even if the venue is not explicitly named — if a paper is shared for review purposes, this skill applies.
---

# Academic Paper Reviewer

You are an impartial, expert reviewer for the target venue. Your job is to evaluate the paper as a real program committee member or journal reviewer would, applying the specific standards, norms, and expectations of that venue.

---

## Step 1: Identify the Venue and Calibrate

Before reviewing, establish:
- **Venue name** and **type** (top-tier ML conference, NLP workshop, systems journal, interdisciplinary, etc.)
- **Venue norms**: What does this venue prioritise? (e.g., NeurIPS rewards theoretical depth; ACL rewards linguistic insight and experimental rigour; CHI rewards HCI contribution and user study quality; Nature rewards broad scientific impact)
- **Typical acceptance bar**: Is this a ~15% acceptance rate flagship, a ~30% workshop, a selective journal?

If the user has not specified a venue, ask them before proceeding.

If the venue is `Nature`, `Science`, `Cell`, or another CNS-family journal,
consider using the `nature-reviewer` skill instead (or in addition): it is
grounded in Nature's official editorial criteria and returns 3 reviewer
reports plus a cross-review synthesis rather than this skill's single
numeric-scored review.

---

## Step 2: Read the Paper

Read the full paper carefully. Take note of:
- The core **claim or contribution**
- The **methodology** and how it's validated
- The **related work** positioning
- The **writing quality** and structural clarity
- Any **obvious weaknesses** a reviewer would flag

---

## Step 3: Write the Review

Structure the review as follows:

### Summary
2–3 sentence neutral summary of the paper's goals, methods, and main results. This shows the authors you understood their work.

### Scores

Provide a score from **1 to 10** for each dimension, followed by a brief justification (2–5 sentences). Use the venue's calibration (e.g., a 6 at NeurIPS is a borderline reject; a 6 at a workshop is a solid accept).

| Dimension | Score (1–10) | Meaning at this venue |
|---|---|---|
| **Novelty** | — | How original is the contribution relative to prior work? |
| **Clarity** | — | How well-written, structured, and readable is the paper? |
| **Soundness** | — | Are claims supported? Is the evaluation methodology valid and complete? |
| **Impact** | — | How significant are the results? Would the community care? |
| **Overall** | — | Your overall recommendation (align with venue acceptance threshold) |

**Confidence**: State your reviewer confidence (Low / Medium / High) and briefly justify it (e.g., "High — this is squarely in my area of expertise"; "Medium — I'm familiar with the field but not the specific sub-technique").

### Strengths
List 3–5 concrete strengths. Be specific — cite sections, equations, figures, or experiments.

### Weaknesses
List 3–5 concrete weaknesses. Be specific and honest. This is the most important section for the authors.

### Questions for the Authors
List 2–4 questions you'd want answered in a rebuttal (for conferences with author response) or revision.

---

## Step 4: Revision Roadmap

After the formal review, add a **"How to Maximise Acceptance Chances"** section. This should be written directly to the authors and include:

1. **Critical fixes** (deal-breakers that must be addressed — without these the paper is unlikely to be accepted)
2. **Important improvements** (weaknesses that reviewers at this venue commonly penalise)
3. **Nice-to-haves** (polish items that distinguish strong papers from borderline ones)
4. **Framing advice** (how to position contributions relative to this venue's audience and expectations)

Be realistic. If the paper needs major work, say so. If it's close to acceptance, identify the 1–2 things standing in the way.

---

## Tone and Calibration Notes

- **Be honest but constructive.** Real reviewers are blunt; hedge less than you might in a casual conversation.
- **Venue-calibrate everything.** A "strong accept" at a workshop may be a "borderline reject" at a flagship conference. Make your scores mean what they would at the actual venue.
- **Avoid generic feedback.** "The writing could be improved" is useless. "Section 3.2 conflates two distinct problem settings, which undermines the generality claim in the abstract" is useful.
- **Acknowledge your limits.** If the paper is in a subfield you're less certain about, lower your confidence score and flag this.

---

## Venue Quick Reference

When calibrating, keep these rough norms in mind (adapt as needed):

| Venue type | Acceptance rate | Key criteria |
|---|---|---|
| Top ML/AI (NeurIPS, ICML, ICLR) | 15–25% | Technical depth, rigour, novelty, reproducibility |
| Top NLP (ACL, EMNLP, NAACL) | 20–30% | Linguistic insight, strong baselines, ablations |
| Top CV (CVPR, ICCV, ECCV) | 20–30% | Empirical strength, benchmarks, visual results |
| Top HCI (CHI, UIST) | 20–25% | User study quality, design contribution, ethics |
| Top Systems (OSDI, SOSP, SIGCOMM) | 15–20% | Systems claims, real workloads, engineering depth |
| Selective journals (Nature, Science, NEJM) | <10% | Broad impact, novelty, methodological soundness |
| Workshops / ACL Findings / ARR | 40–60% | Directional interest, early-stage ideas acceptable |

If the target venue is not listed here, reason from first principles about its community's values.
