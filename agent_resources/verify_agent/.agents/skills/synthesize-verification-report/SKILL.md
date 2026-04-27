---
name: synthesize-verification-report
description: Aggregate all detected errors and gaps into the final verification report, apply strict accept/reject logic, and produce repair hints when rejected.
---

# Synthesize Verification Report

Produce the final verification output JSON and verdict.

## Input Contract

Read all findings from:

- `{run_dir}/memory/statement_checks.md`
- `{run_dir}/memory/reference_checks.md`

Each issue must include `location` and `issue`.

## Procedure

1. Collect all critical errors and all gaps from previous checks.
2. Build a complete `verification_report` object with:
   - `summary`
   - `critical_errors`
   - `gaps`
3. Apply strict verdict rule:
   - `correct` iff `critical_errors=[]` and `gaps=[]`.
   - otherwise `wrong`.
4. If verdict is `wrong`, produce concrete non-empty `repair_hints`.
5. Validate the output by checking it against the output contract below.
6. Write the final JSON to `{run_dir}/verification_iter_{iteration}.json`.
7. Append a short summary of the verdict to `{run_dir}/memory/verification_reports.md`.

## Output Contract

Final output JSON:

```json
{
  "verification_report": {
    "summary": "string",
    "critical_errors": [],
    "gaps": []
  },
  "verdict": "correct",
  "repair_hints": ""
}
```

If there is any error or gap, verdict must be `"wrong"` and `repair_hints` must be non-empty.

## Memory Files

- Query checks by reading/searching `statement_checks.md` and `reference_checks.md`.
- Append the final verdict summary to `verification_reports.md`.
- Write the required final JSON directly to `{run_dir}/verification_iter_{iteration}.json`.
