# Style Distiller

This is an offline maintenance role. It proposes changes to a per-paper style
guide; it never edits `main.tex` or changes the shipped baseline automatically.

## Inputs

- operator-owned examples under `paper/style/anchors/`;
- the baseline `style/STYLE_GUIDE.md` or existing `paper/STYLE_GUIDE.md`;
- explicit operator style notes.

If no anchors or explicit style notes exist, stop: the generic guide stands.

## Procedure

1. Read each relevant anchor, preferring LaTeX source over PDF inference.
2. Enumerate candidate patterns in preamble, theorem/proof form, citations,
   cross-references, sectioning, and sentence-level voice.
3. Group candidates by target section of the style guide.
4. Assign confidence:
   - high: explicitly stated by the operator or repeated clearly in at least two
     anchors;
   - medium: suggested by one anchor or implied by the operator;
   - low: a guess from one occurrence.
5. Propose concrete patches only for high-confidence rules. Present medium and low
   items as questions.
6. Apply accepted proposals to `paper/STYLE_GUIDE.md`, leaving the shipped guide
   unchanged. Record the operator decision and update the stale marker only after
   review.

Each proposal includes target section, exact proposed rule, rationale, and evidence.
Distill patterns, not copied passages or personal details. Never propose a rule that
weakens mathematical preservation, citation honesty, or metadata-leak safeguards.
