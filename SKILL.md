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
- Verified blueprint LaTeX template: `references/verified-blueprint-template.tex`
- Bundled generation subskills: `agent_resources/generation_agent/.agents/skills/`
- Bundled verification subskills: `agent_resources/verify_agent/.agents/skills/`
- arXiv theorem-search API helper: `scripts/search_arxiv_theorems.py`
- LaTeX compiler helper: `scripts/compile_latex.sh`


## Runtime Notes

Before doing anything else for this skill, initialize the shell environment by running:

```bash
source /root/root/bashrc
```

If the runtime launches a fresh shell for each command, make sure commands that depend on that environment are run from a shell where `/root/root/bashrc` has been sourced. Tell spawned generation and verification agents to source `/root/root/bashrc` before their own work begins.

## Effort Policy

Map reasoning effort to the maximum number of generation iterations:

| Effort | Max Iterations |
| --- | ---: |
| `low` | 1 |
| `medium` | 5 |
| `high` | 10 |

If the user gives an unrecognized effort, default to `high` and note that assumption.

## Iteration Definition

One iteration is one long generation phase under a fixed retrieval mode.

During one iteration, the generation agent may work for a long time, revise `blueprint.md` repeatedly, and request verification multiple times. Each time it produces a candidate blueprint, the master agent may spawn a clean-context verification agent and return the verifier's report to the same generation agent inside the same iteration. Failed verification attempts do not by themselves consume a new iteration.

An iteration ends only when one of these happens:

- a candidate blueprint passes clean-context verification
- the generation agent itself decides to stop the current long attempt and returns `stuck` or `no_solution`
- the master agent must stop for an external runtime/tooling failure

The maximum iteration count limits these long generation phases, not the number of candidate blueprints or verification checks. Retrieval mode is fixed for the entire iteration: iteration `0` allows retrieval; odd-numbered later iterations forbid retrieval; even-numbered later iterations allow retrieval.

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
- `memory/*.md`

Never write generated problem artifacts into `agent_resources/`.

Use Markdown files for memory. Do not require external memory tools or a programmatic memory store. Generation and verification agents should append memory entries to `{run_dir}/memory/<channel>.md` and query memory by reading/searching those Markdown files directly. Use the historical channel filenames with `.md`, such as `immediate_conclusions.md`, `big_decisions.md`, `toy_examples.md`, `counterexamples.md`, `subgoals.md`, `proof_steps.md`, `failed_paths.md`, `verification_reports.md`, `branch_states.md`, `events.md`, `statement_checks.md`, and `reference_checks.md`.

## Master Workflow

1. Source `/root/root/bashrc` before any other action.
2. Normalize the user input into a complete problem statement and effort level.
3. Create the run directory and write `problem.md`.
4. Start iteration `0` by spawning a long-running generation agent. Give it:
   - the problem statement
   - the run directory path
   - the current iteration number
   - the current retrieval mode
   - the generation workflow file path
   - the bundled generation skill directory path
   - the instruction to source `/root/root/bashrc` before doing anything else
5. The generation agent must try to produce or revise `blueprint.md` in the run directory until it either requests verification of a candidate or decides to terminate the current iteration. It should return one of:
   - `candidate_ready`: a full candidate proof blueprint exists
   - `stuck`: it has worked through the current long attempt, made meaningful partial progress, and has decided to terminate this iteration without a verified solution
   - `no_solution`: it has worked through the current long attempt and has decided to terminate this iteration without useful progress
6. Whenever `candidate_ready` is returned, spawn a verification agent with clean context. Give it only:
   - the problem statement
   - the candidate `blueprint.md` content or path
   - the run directory path
   - the current iteration number
   - the verification workflow file path
   - the bundled verification skill directory path
   - the instruction to source `/root/root/bashrc` before doing anything else
7. Treat verification as passing only when the verification verdict is `correct` and both `critical_errors` and `gaps` are empty.
8. If verification passes:
   - rename `blueprint.md` to `blueprint_verified.md`
   - author `blueprint_verified.tex` by hand from `blueprint_verified.md` using `references/verified-blueprint-template.tex` as the starting structure
   - compile `blueprint_verified.pdf`
   - return the PDF path and the verified blueprint path to the user
9. If verification fails, append the verification report to `iteration_log.md`, pass the report back to the same generation agent, and continue the same iteration under the same retrieval mode.
10. If the generation agent returns `stuck` or `no_solution`, append the stuck/no-solution summary to `iteration_log.md`; only then continue to the next iteration if the effort limit permits.
11. If the maximum iteration count is reached without a passing verification, return the best available artifacts and clearly say that the result is not verified.

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

After successful verification, rename the verified blueprint:

```bash
mv path/to/run/blueprint.md path/to/run/blueprint_verified.md
```

Then author `path/to/run/blueprint_verified.tex` directly from `blueprint_verified.md`.

- Use `references/verified-blueprint-template.tex` as the starting structure unless a better paper-style preamble is clearly needed.
- Do not use a programmatic Markdown-to-LaTeX converter.
- Write valid LaTeX that reads like a professional mathematics paper, not a line-by-line rendering of Markdown.
- Preserve the verified blueprint's mathematical content, theorem statement, definitions, lemmas, propositions, proof structure, labels, hypotheses, and logical dependencies.
- Convert blueprint sections into LaTeX sections and theorem/proof environments.
- Keep formulas as real LaTeX math; do not leave escaped Markdown artifacts such as `\#`, raw `#` headings, or escaped dollar signs in running text.
- Do not introduce new mathematical claims that were not in the verified blueprint unless they are purely expository and do not affect correctness.

After writing `blueprint_verified.tex`, compile it:

```bash
path/to/scripts/compile_latex.sh path/to/run/blueprint_verified.tex path/to/run
```

Before returning, inspect `blueprint_verified.tex`. If it is not valid professional LaTeX, if it looks like raw Markdown, or if it compresses or omits essential proof content from `blueprint_verified.md`, rewrite it from the template and recompile.

If LaTeX tooling is unavailable or compilation fails after reasonable repair attempts, still return `blueprint_verified.md` and `blueprint_verified.tex`, and state that PDF compilation failed.
