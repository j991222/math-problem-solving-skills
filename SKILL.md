---
name: math-problem-solving-skills
description: "Use when a user gives a mathematics problem. Execute the dual-agent workflow: a generation agent builds a proof blueprint, a clean-context verification agent checks it, and the master agent iterates according to low, medium, or high reasoning effort. Default effort is high."
metadata:
  short-description: Dual-agent math proof workflow
---

# Math Problem Solving Skills

This skill is the master-agent wrapper for a dual-agent mathematics problem-solving system. It accepts:

- a mathematics problem statement
- optional reasoning effort: `low`, `medium`, or `high`

If effort is omitted, use `high`.

## Bundled Resources

Resolve paths relative to this skill directory.

- Generation agent workflow: `references/generation-agent-workflow.md`
- Verification agent workflow: `references/verification-agent-workflow.md`
- Bundled generation subskills: `agent_resources/generation_agent/.agents/skills/`
- Bundled verification subskills: `agent_resources/verify_agent/.agents/skills/`
- arXiv theorem-search API helper: `scripts/search_arxiv_theorems.py`
- Markdown-to-LaTeX helper: `scripts/blueprint_to_latex.py`
- LaTeX compiler helper: `scripts/compile_latex.sh`



## Effort Policy

Map reasoning effort to the maximum number of generation iterations:

| Effort | Max Iterations |
| --- | ---: |
| `low` | 1 |
| `medium` | 5 |
| `high` | 10 |

If the user gives an unrecognized effort, default to `high` and note that assumption.

## Run Directory

Create one local run directory outside the skill package, for example:

```text
math_problem_runs/{run_id}/
```

Use a stable `run_id` such as a timestamp plus a short problem hash. Store all run artifacts there:

- `problem.md`
- `iteration_log.md`
- `blueprint.md`
- `blueprint_verified.md`
- `verification_iter_{n}.json`
- `blueprint_verified.tex`
- `blueprint_verified.pdf`

Never write generated problem artifacts into `agent_resources/`.

## Master Workflow

1. Normalize the user input into a complete problem statement and effort level.
2. Create the run directory and write `problem.md`.
3. Start iteration `0` by spawning a generation agent. Give it:
   - the problem statement
   - the run directory path
   - the current iteration number
   - the current retrieval mode
   - the generation workflow file path
   - the bundled generation skill directory path
4. The generation agent must try to produce or revise `blueprint.md` in the run directory. It should return one of:
   - `candidate_ready`: a full candidate proof blueprint exists
   - `stuck`: meaningful partial progress exists but no full candidate is ready
   - `no_solution`: no useful progress was made in the allowed iteration
5. Whenever `candidate_ready` is returned, spawn a verification agent with clean context. Give it only:
   - the problem statement
   - the candidate `blueprint.md` content or path
   - the run directory path
   - the current iteration number
   - the verification workflow file path
   - the bundled verification skill directory path
6. Treat verification as passing only when the verification verdict is `correct` and both `critical_errors` and `gaps` are empty.
7. If verification passes:
   - rename `blueprint.md` to `blueprint_verified.md`
   - generate `blueprint_verified.tex`
   - compile `blueprint_verified.pdf`
   - return the PDF path and the verified blueprint path to the user
8. If verification fails or generation is stuck, append the verification report or stuck summary to `iteration_log.md`, then continue to the next iteration if the effort limit permits.
9. If the maximum iteration count is reached without a passing verification, return the best available artifacts and clearly say that the result is not verified.

Do not claim the problem is solved unless the clean-context verification agent passes the blueprint.

## Retrieval Alternation

Use this retrieval policy for generation iterations:

- iteration `0`: retrieval allowed
- odd iterations after that: retrieval forbidden
- even iterations after that: retrieval allowed

When retrieval is forbidden, the generation agent must not use web search, theorem search, arXiv search, or other external retrieval. It may use its current local notes, the problem statement, local memory artifacts, and the non-retrieval bundled generation subskills.

When retrieval is allowed, the generation agent may use the bundled retrieval-oriented subskill `search-math-results`, the arXiv theorem-search API helper hosted at `leansearch.net`, and any browser/search tools already available in the active runtime.

The retrieval mode instruction in this root skill overrides any search preference in the bundled generation subskills during no-retrieval iterations.

If a bundled subskill mentions `search_arxiv_theorems`, implement that action by running:

```bash
python3 path/to/scripts/search_arxiv_theorems.py --query "complete mathematical statement" --num-results 10
```

Do this only when retrieval is allowed. If the API call fails, record the failure and continue with local reasoning and available OpenClaw search/browser tools.

## Agent Spawning

Spawn subagents only for the two roles below.

### Generation Agent

Use the workflow in `references/generation-agent-workflow.md`. The generation agent should consult the bundled generation `SKILL.md` files in `agent_resources/generation_agent/.agents/skills/` as needed and write `blueprint.md` in the run directory.

When continuing after a failed or stuck iteration, pass the previous `iteration_log.md`, any verification report, and the current `blueprint.md` if it exists. Tell the generation agent whether retrieval is currently allowed.

### Verification Agent

Use a clean context for verification. Do not fork the generation agent context. Use the workflow in `references/verification-agent-workflow.md` and the bundled verification `SKILL.md` files in `agent_resources/verify_agent/.agents/skills/`.

The verifier must be strict: `correct` iff there are no critical errors and no gaps.

## Finalization

After successful verification, run:

```bash
python3 path/to/scripts/blueprint_to_latex.py path/to/run/blueprint_verified.md --output path/to/run/blueprint_verified.tex
path/to/scripts/compile_latex.sh path/to/run/blueprint_verified.tex path/to/run
```

If LaTeX tooling is unavailable or compilation fails, still return `blueprint_verified.md` and `blueprint_verified.tex`, and state that PDF compilation failed.
