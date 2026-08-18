# Whole-Paper Mathematics Verifier

Read this prompt from top to bottom before judging. Verify the finished paper as
one self-contained document: does the complete manuscript, read on its own, prove
its headline result?

Prefer a clean context. Receive only:

- the complete final `main.tex` in reading order;
- confirmed rows of `REFERENCE_LEDGER.md`;
- this verifier prompt and the standing integrity contract.

Do not receive the selected source, source map, generation notes, prior verifier
reports, or intended answer. Those would bias the check. If a clean context is not
available and the same agent performs this pass, record `verification_mode:
same-context`; do not call it independent.

## What to Check

Check every definition, statement, proof, reduction, case split, calculation, and
logical transition sequentially. A result may depend only on earlier paper results
or on confirmed external citations.

The paper is a distinct artifact even when its source was verified upstream. Rewriting
can drop hypotheses, compress pivots, create circular references, misstate a lemma,
or add unsupported glue.

## Citation Policy

A precise external citation to a confirmed ledger row is a valid given. Do not ask
the paper to re-prove established literature. Check that the hypotheses and cited
use match the confirmed `cited_for` field. An unverified citation is not a valid
given.

A result used without proof and without a precise confirmed citation is a finding.
The paper's own combination of internal and external results is always subject to
full scrutiny.

## Classify Every Finding

Use one strict criterion:

- `ignorable`: only when a mathematics undergraduate can fill or follow the step
  unaided from the paper as written, such as a routine computation or standard
  manipulation whose mechanism is clear.
- `must-fix`: every other incomplete, unclear, unsupported, circular, or incorrect
  step. When in doubt, use `must-fix`.

A precise confirmed citation is not a finding. A presentation preference is not a
mathematical finding. Do not invent findings to look thorough.

The paper passes mathematically exactly when there are zero `must-fix` findings.
Ignorable findings remain recorded and surfaced but do not block delivery.

## Output

Write exactly one JSON object to `checks/PAPER_MATH_VERDICT.json`:

```json
{
  "verification_mode": "clean-context|same-context",
  "findings": [
    {
      "location": "exact theorem/proof/paragraph location",
      "issue": "what is missing, unclear, circular, or wrong",
      "class": "ignorable|must-fix"
    }
  ],
  "report": "short justification"
}
```

If the verification run fails, is truncated, or cannot parse the paper, record a
verification error rather than an empty findings list.

## Oversized Papers

First use a verifier with sufficient context if available. Otherwise decompose by
major mathematical result, never by consecutive pages. Each verification unit must
contain:

- the paper's notation and definitions;
- statements of separately verified results it may assume;
- the complete development of one designated result, ending in that result.

Verify every unit and the top-level assembly. This is weaker operationally than one
whole-document check, so record the decomposition and require operator acceptance
before treating it as equivalent to the whole-paper gate.
