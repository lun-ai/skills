---
name: paper-summarizer
description: >
  Summarise academic research papers with precise location references so the user can quickly grasp core ideas,
  methods, and findings — and then navigate directly to the parts that matter most to them.
  Trigger this skill whenever a user shares a PDF or text of a research paper and asks to understand it,
  summarise it, get the key ideas, find the methods, extract results, or says things like "I don't have time
  to read this", "what's this paper about", "can you summarise this for me", "what are the main findings",
  "explain the methodology", "what data did they use", or "give me the key takeaways". Also trigger when
  the user asks for a "reading plan" or "what should I focus on" for a paper. Use this skill even when
  a summary request is phrased casually or very briefly.
---

# Academic Paper Summarizer

Produce structured, location-anchored summaries of research papers so the user can understand the work quickly and navigate to the parts that matter most to them.

---

## 1. Read the Paper

Before summarising:
- Use the `pdf-reading` skill if the paper arrives as a PDF file.
- If the paper is in plain text or already in context, read it fully before writing anything.
- Identify the paper's **structure** (section headings, figure/table labels, numbered equations). Record these as you read — they become your location anchors.

---

## 2. Generate a Session Title

Before writing the summary, extract from the paper:
- **Topic**: 2–4 words capturing the core subject (not the method name — what it's *about*)
- **Authors**: First author's surname + "et al." (use sole author's name if single-author; use both surnames if exactly two authors)
- **Year**: Publication year from the paper header, footer, or metadata

Format: `Topic (Author et al. Year)`

Output this as a plain header line at the very top of your response, before the TL;DR:

```
📄 Session: Fire fact checking (Xie et al. 2025)
```

**Rules:**
- Keep the topic phrase short and human-readable — describe what the paper is *about*, not what it's called
  - ✓ "Transformer language models (Vaswani et al. 2017)"
  - ✗ "Attention is all you need (Vaswani et al. 2017)" — that's the title, not a topic description
- Capitalise only the first word of the topic phrase
- If year cannot be found, omit it: `(Brown et al.)`
- If authors cannot be found, omit the parenthetical entirely

---

## 3. Choose a Summary Mode

Match depth to what the user asked for:

| Mode | When to use | Target length |
|------|-------------|---------------|
| **Flash** | "What's this about?" / "Quick summary" | 5–8 sentences |
| **Standard** | Default — no explicit depth request | Structured sections below |
| **Deep Dive** | "Full breakdown" / "Explain everything" | All sections + every key detail |

If unsure, default to **Standard**.

---

## 4. Standard Summary Structure

Always produce sections in this order. Each claim or fact **must** cite its location using the format `[§ Section Name]`, `[Abstract]`, `[Fig. N]`, `[Table N]`, `[Eq. N]`, or `[p. N]` — whichever is most precise. If multiple locations support a point, list them all.

---

### 🧭 One-Paragraph TL;DR
A single paragraph (4–6 sentences) covering: the problem, the approach, the key result, and the takeaway. No location tags needed here — this is the executive summary.

---

### 🎯 Problem & Motivation
- What gap, limitation, or question does this paper address? `[§ Introduction]` or `[Abstract]`
- Why does it matter? Who cares? `[§ Introduction]`
- Prior work this builds on or challenges `[§ Related Work]` / `[§ Background]`

---

### 🔬 Method / Approach
Describe the core technical contribution in plain language. For each component:
- What it is and how it works
- **Location**: `[§ Method]` / `[§ Model]` / `[§ Approach]` (use the actual section name from the paper)
- Any key equations: `[Eq. N]`
- Any key figures: `[Fig. N]`
- Data used: datasets, sources, size, splits `[§ Experiments]` / `[§ Data]` / `[Table N]`

If the method has sub-components (e.g. encoder, decoder, training procedure), list them as sub-bullets with their own locations.

---

### 📊 Results & Evidence
For each major result or claim:
- The finding in plain English
- The metric/evidence used to support it
- **Location**: `[Table N]` / `[Fig. N]` / `[§ Results]` / `[§ Experiments]`
- Baselines compared against `[Table N]`
- Any ablation studies: what they test and what they show `[§ Ablations]` / `[Table N]`

---

### ⚠️ Limitations & Caveats
- What the paper itself acknowledges as limitations `[§ Limitations]` / `[§ Discussion]` / `[§ Conclusion]`
- Any weaknesses you observe (mark as **[your assessment]**, not the paper's own words)

---

### 💡 Key Takeaway & Impact
- The 1–2 sentence "so what" — what changes if this paper is right?
- Who would benefit from reading this in full (and what section to go to)?

---

## 5. Flash Summary Format

For Flash mode, produce only:
1. **What**: One sentence on the topic.
2. **How**: One sentence on the approach.
3. **Finding**: One–two sentences on the key result, with `[§]` or `[Table/Fig]` anchor.
4. **Worth reading if**: One sentence on who should read the full paper and why.

---

## 6. Deep Dive Additions

For Deep Dive mode, add after the Standard sections:
- **Related Work summary**: Key references and how this paper positions against them `[§ Related Work]`
- **Implementation details**: Architecture sizes, training setup, hyperparameters `[§ Implementation]` / `[Appendix]`
- **Dataset details**: Full breakdown of data sources, preprocessing, splits `[§ Data]` / `[Appendix]`
- **Supplementary findings**: Additional experiments or figures in appendix `[Appendix §]`
- **Reading roadmap**: Ordered list of sections to read if the user wants to go deeper, from highest to lowest priority

---

## 7. Location Anchor Rules

| Source | Tag format | Example |
|--------|-----------|---------|
| Paper section | `[§ Name]` | `[§ 3.2 Encoder]` |
| Abstract | `[Abstract]` | |
| Figure | `[Fig. N]` | `[Fig. 3]` |
| Table | `[Table N]` | `[Table 2]` |
| Equation | `[Eq. N]` | `[Eq. 4]` |
| Page number | `[p. N]` | `[p. 7]` — use when no heading/number is available |
| Appendix | `[Appendix §]` | `[Appendix B]` |

**Rules:**
- Every factual claim needs at least one location anchor.
- Prefer named sections over page numbers.
- If a point spans multiple locations (e.g., introduced in §2, evaluated in §5), cite both: `[§ 2 Method, Table 3]`.
- Never fabricate anchors — if you cannot find the location, write `[location unclear]`.

---

## 8. Tone & Style

- Write for an expert reader who is short on time — precise, no filler.
- Use plain English for method descriptions; don't just re-state jargon from the paper.
- Bullet points for lists of facts; prose for narrative/motivation sections.
- Bold the most surprising or important claim in the Results section.
- If a paper uses unusual notation, define it once on first use.

---

## 9. Follow-Up Prompts

After the summary, always offer these options so the user can go deeper on demand:

> **Want to go deeper?**
> - "Explain the method in more detail"
> - "Walk me through the main results table"
> - "What are the limitations?"
> - "How does this compare to [other paper/approach]?"
> - "Give me a reading plan for this paper"

<!--
CHANGE LOG
v2 2026-03-28: Added §2 "Generate a Session Title" — outputs a concise "Topic (Author et al. Year)" header at the top of every summary. Renumbered subsequent sections 3→4 through 8→9.
Outstanding minor issues: none
-->
