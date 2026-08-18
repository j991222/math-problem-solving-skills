# Reference Verifier

Read the standing contract before working. Verify only entries flagged by
`REFERENCE_AUDIT.md`. This is the online half of the reference chain and may run
only when the parent workflow permits retrieval.

## Goal

Check each flagged bibliography entry against an authoritative source, update its
ledger row, and emit a self-contained replacement instruction for the reviser.
Do not edit mathematical prose during verification.

## Scope Discipline

- Do not reopen `verified-by: operator` rows unless asked or an obvious typo is
  under review.
- Do not search for extra references merely to decorate the introduction.
- Confirm the same paper and the cited mathematical use, not only a similar title
  or theorem.
- Tool failure or unreachable sources yield `unverifiable`, never a guess.

## Per-Entry Procedure

1. If the paper itself proves the cited result, return `retarget-internal` and name
   the exact internal paper label. Preserve genuine historical credit separately.
2. For an arXiv source, search by exact title or full statement, then inspect the
   authoritative arXiv abstract page. Confirm authors, title, year, identifier,
   journal reference when present, and that the work supports the cited use.
3. For books or older journal papers, use a publisher page, DOI resolver, zbMATH,
   DBLP, MathSciNet landing page, or another authoritative bibliographic source.
4. When the claimed source exists but metadata is wrong, return `corrected` with
   authoritative values.
5. When no matching work can be confirmed and the claim appears fabricated, return
   `rejected` and record what was checked.
6. When evidence is insufficient, return `unverifiable` and keep the blocker.

## Verdict Format

Write one entry per flagged source in `checks/REFERENCE_VERDICTS.md`:

```yaml
key: <citation or candidate key>
verdict: verified | corrected | rejected | unverifiable | retarget-internal
confirmed_metadata:
  authors: <authoritative full list or blank>
  title: <authoritative title or blank>
  venue: <authoritative venue or blank>
  year: <authoritative year or blank>
  arxiv: <identifier or blank>
  doi: <identifier or blank>
source_url: <exact authoritative URL; required for verified/corrected>
cited_for_check: <how the source supports or fails to support the paper's use>
note: <what was checked>
replacement_instruction: <one located instruction for the reviser>
```

Apply confirmed metadata to `REFERENCE_LEDGER.md` only after the verdict file is
complete. Mark `verified-by: verifier`, exact `source_url`, and current status.
Never update the paper directly; the reviser applies the replacement instruction.

## Self-Check

1. Every audit item has exactly one verdict.
2. Every `verified` or `corrected` verdict has an authoritative `source_url`.
3. Same-paper identity and cited use were both checked.
4. No promotion came from memory.
5. Tool failures became `unverifiable`.
6. Ledger changes match the emitted verdicts exactly.
