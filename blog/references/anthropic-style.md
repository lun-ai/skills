# Anthropic research-post style

A house style for technical posts that report work the authors did themselves: assessments,
incident write-ups, evaluations, engineering results. Derived from Anthropic's
*Alignment assessment of four cybersecurity incidents*
(<https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents>, read
2026-10-20), which is the reference example to imitate.

Use when the user asks for "Anthropic blog style", "Anthropic research style", or a measured
first-person technical report. It composes with the 6 pillars; where it conflicts with generic
blog advice, this file wins for the voice and the structure, and the delivery contract still
governs gates.

## The shape

1. **Open with the finding, not the background.** The first sentence states what was done and
   what came of it. The reference opens "We present an alignment assessment of four incidents."
   Scope and method come next; context and narrative come after that, not before.
2. **Section order**: finding → scope and definitions → method → results, one section per case
   or dimension → replication or cross-checks → limitations → what follows.
3. **Close with a synthesis, not a flourish.** Sections and the post end with a short
   "Taken together, …" judgement, then open problems or next steps.

## The voice

- **First person plural throughout.** "We identified", "we believe", "we are releasing". The
  authors are visible and accountable.
- **Own the errors in the same voice.** Self-correction is a feature of the style:
  "In retrospect, we should have avoided making such strong claims about what Claude believed."
  If an earlier claim was wrong, say so in the body rather than quietly fixing it.
- **Assertive about severity, hedged about mechanism.** State plainly how bad or good a result
  is; hedge on *why* it happened. "Taken together, our assessment is that these incidents are
  serious" sits comfortably beside "weakly suggestive" and "not decisive" a paragraph later.
- **Dense paragraphs, varied sentences.** Five to eight sentences per paragraph, long sentences
  carrying embedded clauses and parentheticals, with short plain sentences reserved for
  transitions and conclusions. Do not chop everything into two-line paragraphs.
- **Technical, not popularised.** Accessible framing, dense detail. No marketing adjectives, no
  rhetorical questions, no second-person exhortation.

## Evidence

- **Every number carries its denominator and its conditions.** Not "most runs failed" but the
  count, the total, and the subset the percentage is over.
- **Figures are the main visual device**, interleaved with prose and placed immediately after
  the paragraph that introduces them. Label each in bold — `**Figure 3:**` — with a
  one-sentence caption, and refer back to it in the text. Use "(left)" and "(right)" for
  side-by-side comparisons.
- **Bullets sparingly**, mainly to define terms or enumerate scenarios. The reference post uses
  no tables at all; use one only when the table *is* the deliverable, such as a per-item result
  listing, and keep it to one or two.
- **Separate what was observed from what it means.** The reference keeps "what the model said"
  apart from "what the model did"; the general rule is that description and interpretation do
  not share a paragraph.

## Limitations

- **A dedicated limitations paragraph per method or result section**, not one disclaimer at the
  end. Label it in italics — *Limitations:* — and state what would bias the result, what the
  method could not see, and which differences are too small to claim.
- **Explain why a result may be weaker than it looks.** The style actively argues against its
  own strongest reading.

## Headings

- **Top-level headings are short and sentence case.**
- **Subheadings may be full assertive claims**, including the subject: "Claude disregarded
  evidence of realism in favour of continuing its course of action". A subheading that states
  the finding is preferred over a label like "Results".

## Recurring habits worth copying

`Taken together, …` · `We note that …` · `To be clear about …` · `Overall, …` · italic
*Limitations:* labels · numbered footnotes for asides that would break the sentence.

## Checklist before shipping

- [ ] First sentence states the finding, not the setting
- [ ] Every statistic has a denominator and the condition it was measured under
- [ ] Each figure is numbered, bold-labelled, captioned in one sentence, referenced in prose
- [ ] At least one italic *Limitations:* paragraph, placed with the result it qualifies
- [ ] Any earlier claim now known to be wrong is corrected in the body, in the same voice
- [ ] A "Taken together" synthesis before the close
- [ ] No marketing adjectives, no rhetorical questions, no second person
