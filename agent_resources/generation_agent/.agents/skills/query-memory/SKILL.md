---
name: query-memory
description: Retrieve previously saved immediate conclusions, toy examples, counterexamples, failed paths, or branch states from memory. Use when you want to check whether earlier conclusions, examples, counterexamples, failed paths, or brach states can bring insight to the current question, claim, subgoal, or branch decision, or when you want to test a claim against previously saved counterexamples.
---


# Query Memory

Use this skill when you want to check whether earlier conclusions, examples, counterexamples, failed paths, or brach states can bring insight to the current question, claim, subgoal, or branch decision, or when you want to test a claim against previously saved counterexamples.

## Input Contract

Read:

- the current question, claim, subgoal, or branch decision
- the specific type of prior artifact you want to recover
- the most relevant channel list, chosen from:
  - `immediate_conclusions`
  - `toy_examples`
  - `counterexamples`
  - `failed_paths`
  - `branch_states`

## Procedure

1. Form a concrete natural-language query describing the information you want to recover.
2. Choose the smallest relevant list of channels instead of searching everything by default.
3. Read or search the corresponding `{run_dir}/memory/<channel>.md` files directly.
4. Inspect the most relevant entries in each requested channel.
5. Summarize the useful retrieved items and explain how they affect the current proof state.
6. If no useful item is found, say that clearly and then switch to another appropriate skill.

## Output Contract

Append a summary entry to `{run_dir}/memory/events.md`:

```json
{
  "event_type": "query_memory",
  "query": "...",
  "channels": ["counterexamples", "failed_paths"],
  "limit_per_channel": 10,
  "results_summary": ["..."],
  "useful_hits": [
    {
      "channel": "counterexamples",
      "score": 0.0,
      "why_relevant": "...",
      "record_excerpt": "..."
    }
  ],
  "branch_id": "optional",
  "subgoal_id": "optional"
}
```

## Memory Files

- Query memory by reading/searching the selected Markdown files under `{run_dir}/memory/`.
- Append the query summary and usefulness assessment to `events.md`.

## Failure Logging

If the retrieval is not useful, append an `events.md` entry with:

- `event_type="query_memory_stalled"`
- the attempted query
- the channels searched
- the reason the retrieved items were not useful
