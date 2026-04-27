---
name: construct-toy-examples
description: Generate and analyze simpler examples that satisfy both the assumptions and the conclusion of a theorem statement or subgoal. Use when you are stuck in reasoning and need simpler examples to regain traction, when you need simpler examples that satisfy both assumptions and conclusion, or when you want to see where the assumptions take effect and gain intuition.
---

# Construct Toy Examples

Use this skill when the agent is stuck in reasoning and needs simpler examples that satisfy both the assumptions and the conclusion in order to understand why the statement works.

## Input Contract

Read:

- current statement/subgoal
- relevant `immediate_conclusions`
- relevant `counterexamples` and failed branch notes
- relevant background/results when available

## Procedure

1. Construct simpler cases (low degree, small dimension, special forms, canonical objects).
2. Ensure the toy example satisfies all assumptions of the target statement or subgoal.
3. Check that the conclusion also holds in the toy example.
4. Study where each assumption takes effect and what mechanism makes the conclusion true.
5. Identify repeated patterns, invariants, or proof ideas suggested by the example.
6. Use search/reasoning/decomposition as needed to find examples or simplify the situation.

## Output Contract

Append to `{run_dir}/memory/toy_examples.md`:

```json
{
  "example": "...",
  "why_relevant": "...",
  "assumptions_satisfied": ["..."],
  "conclusion_verified": true,
  "where_assumptions_take_effect": "...",
  "observed_pattern": "...",
  "supports_branch_ids": ["optional"],
  "subgoal_id": "optional"
}
```

## Memory Files and Retrieval

- Query relevant memory by reading/searching Markdown files under `{run_dir}/memory/`.
- Append useful examples to `toy_examples.md`.
- Use `search_arxiv_theorems` through the bundled theorem-search helper for matching examples/known motifs when retrieval is allowed.
- Web search for known example families and standard constructions
- use `$search-math-results` when broader retrieval is needed

## Failure Logging

If generated examples are inconclusive, append an `events.md` entry:

- `event_type="toy_examples_inconclusive"`
- include attempted example families
