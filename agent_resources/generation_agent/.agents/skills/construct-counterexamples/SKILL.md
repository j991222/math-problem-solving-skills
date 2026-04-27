---
name: construct-counterexamples
description: Construct candidate counterexamples to test a proposed conjecture, lemma, or intermediate claim by keeping the assumptions true while making the claimed conclusion fail. Use when you are stuck in reasoning and want to see where the assumptions take effect and gain intuition, when a proposed conjecture/claim feels fragile or unproved, or when you want to test whether the assumptions can hold while the claimed conclusion fails.
---

# Construct Counterexamples

Actively falsify proposed conjectures or intermediate claims by finding examples that satisfy the assumptions but violate the claimed conclusion.

## Input Contract

Read:

- the specific conjecture/claim to test
- active branch assumptions
- candidate lemmas/proof steps
- current `immediate_conclusions` and `toy_examples`
- previously found counterexamples that can be reused against new claims

## Procedure

1. Identify the assumptions that must hold and the conclusion to fail.
2. Use reasoning, decomposition, and retrieval to search for standard obstructions, pathological constructions, or previously known counterexamples.
3. Decide status:
   - `refuted`: assumptions hold and the claim fails
   - `not_refuted`: no counterexample found yet
   - `inconclusive`: search space unclear or partially explored
4. If the search produces a concrete example that is informative but is not actually a counterexample, save that example as well in `toy_examples`.
5. If refuted, store the counterexample for reuse against future claims and mark impacted branches/lemmas as invalid.
6. If no counterexample is found, treat that only as evidence that the claim may be correct, not as a proof.

## Output Contract

Append to `{run_dir}/memory/counterexamples.md`:

```json
{
  "target_claim": "...",
  "candidate_counterexample": "...",
  "status": "refuted|not_refuted|inconclusive",
  "assumptions_satisfied": ["..."],
  "failed_conclusion": "...",
  "impact": "...",
  "branch_id": "optional",
  "subgoal_id": "optional"
}
```

If `status="refuted"`, also append to `{run_dir}/memory/failed_paths.md` when it kills a branch.

If the search produced a concrete non-refuting example, also append a record to `{run_dir}/memory/toy_examples.md`:

```json
{
  "example": "...",
  "why_relevant": "constructed while testing the claim ...",
  "assumptions_satisfied": ["..."],
  "conclusion_verified": true,
  "where_assumptions_take_effect": "...",
  "observed_pattern": "...",
  "supports_branch_ids": ["optional"],
  "subgoal_id": "optional"
}
```

Do this whenever the constructed example is useful enough to test future claims or clarify the current branch, even if it did not refute the target claim.

## Memory Files and Retrieval

- Query relevant memory by reading/searching Markdown files under `{run_dir}/memory/`.
- Append counterexamples to `counterexamples.md`.
- Append killed branches or invalidated plans to `failed_paths.md` and `branch_states.md`.
- Web search and `search_arxiv_theorems` to find standard counterexample patterns
- reuse stored counterexamples to test future conjectures/claims

## Failure Logging

If no meaningful counterexample space is identified, append to `{run_dir}/memory/events.md`:

- `events.event_type="counterexample_space_unclear"`
