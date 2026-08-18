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
- Paper-writing skill: `agent_resources/generation_agent/.agents/skills/write-paper/SKILL.md`
- Selective paper-revision skill: `agent_resources/generation_agent/.agents/skills/revise-paper/SKILL.md`
- Bundled generation subskills: `agent_resources/generation_agent/.agents/skills/`
- Bundled verification subskills: `agent_resources/verify_agent/.agents/skills/`
- arXiv theorem-search API helper: `scripts/search_arxiv_theorems.py`
- Paper compile gate: `agent_resources/generation_agent/.agents/skills/write-paper/scripts/compile_verify.sh`

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
- `best_available_artifacts.md`
- `paper/PROJECT_BRIEF.md`
- `paper/REFERENCE_LEDGER.md`
- `paper/REVISION_LOG.md`
- `paper/VERIFY_LEDGER.md`
- `paper/SOURCE_MAP.json`
- `paper/main.tex`
- `paper/main.pdf`
- `paper/checks/*`
- `memory/*.md`

Never write generated problem artifacts into `agent_resources/`.

Use Markdown files for memory. Do not require external memory tools or a programmatic memory store. Generation and verification agents should append memory entries to `{run_dir}/memory/<channel>.md` and query memory by reading/searching those Markdown files directly. Use the historical channel filenames with `.md`, such as `immediate_conclusions.md`, `big_decisions.md`, `toy_examples.md`, `counterexamples.md`, `subgoals.md`, `proof_steps.md`, `failed_paths.md`, `verification_reports.md`, `branch_states.md`, `events.md`, `statement_checks.md`, and `reference_checks.md`.

## Master Workflow

1. Normalize the user input into a complete problem statement and effort level.
2. Create the run directory and write `problem.md`.
3. Start iteration `0` by spawning a long-running generation agent. Give it:
   - the problem statement
   - the run directory path
   - the current iteration number
   - the current retrieval mode
   - the generation workflow file path
   - the bundled generation skill directory path
4. The generation agent must try to produce or revise `blueprint.md` in the run directory until it either requests verification of a candidate or decides to terminate the current iteration. It should return one of:
   - `candidate_ready`: a full candidate proof blueprint exists
   - `stuck`: it has worked through the current long attempt, made meaningful partial progress, and has decided to terminate this iteration without a verified solution
   - `no_solution`: it has worked through the current long attempt and has decided to terminate this iteration without useful progress
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
   - immediately read and execute the bundled `write-paper` skill with `blueprint_verified.md` as its explicit source and `{run_dir}/paper/` as its workspace
   - require the writing workflow to produce and compile `{run_dir}/paper/main.tex` and `{run_dir}/paper/main.pdf`; do not use the former direct template conversion path
   - immediately return the actual `main.tex` and `main.pdf` files to the user; do not merely print or report their filesystem paths
8. If verification fails, append the verification report to `iteration_log.md`, pass the report back to the same generation agent, and continue the same iteration under the same retrieval mode.
9. If the generation agent returns `stuck` or `no_solution`, append the stuck/no-solution summary to `iteration_log.md`; only then continue to the next iteration if the effort limit permits.
10. If the maximum iteration count is reached without a passing verification, synthesize the best available work into `best_available_artifacts.md`, then immediately read and execute the bundled `write-paper` skill with that file as its explicit `unverified-best-available` source and `{run_dir}/paper/` as its workspace. Require the writing workflow to produce and compile `{run_dir}/paper/main.tex` and `{run_dir}/paper/main.pdf`, with a visible statement that the manuscript is unverified and may contain gaps or errors. Immediately return the actual `main.tex` and `main.pdf` files to the user; do not merely print or report their filesystem paths. Clearly say that the result is not verified.

Do not claim the problem is solved unless the clean-context verification agent passes the blueprint.

## User-Requested Paper After Proof Revisions

Treat a user request to write the paper as an explicit `write-paper` request even
when it arrives after several conversational proof and correction rounds. Before
invoking the writing skill:

1. Reconstruct the latest complete proof state from the current conversation and
   the current run artifacts. Apply proof replacements and corrections in
   chronological order; the user's newest correction overrides older agent text.
2. Materialize that consolidated proof as `{run_dir}/blueprint.md`. Do not pass a
   loose collection of chat fragments to `write-paper`, and do not silently fall
   back to an older complete proof merely because it already exists on disk.
3. Use `blueprint_verified.md` with `source_status: verified-blueprint` only when
   the exact current proof content is the content that received a passing
   clean-context verdict. A later change to a statement, hypothesis, proof step,
   calculation, or conclusion invalidates that inherited status until the changed
   proof is verified again.
4. If the latest proof has not been verified in its exact current form, explicitly
   select `{run_dir}/blueprint.md` with `source_status: unverified-blueprint`. Keep
   any older `blueprint_verified.md` unchanged as historical evidence; never let it
   override the newer proof.
5. Invoke `write-paper` with the selected source path explicitly. Do not rely on
   filename priority or modification time to choose between proof versions.

If the latest corrections are contradictory or insufficient to reconstruct one
complete proof, ask a focused question instead of combining incompatible versions
or writing from a stale proof.

## User-Requested Revision of Existing TeX

When the user supplies or identifies an already-written `.tex` manuscript and asks
to revise it, load and follow the bundled `revise-paper` skill. Do not rerun
`write-paper` or regenerate the manuscript from a blueprint.

On the first revision turn, inspect the current TeX and return selectable, located
suggestions only; do not edit any file. After the user explicitly selects a subset
or gives another exact edit, change only that approved footprint. Treat all
unmentioned text as user-owned and finalized. Every completed revision turn must
pass the revision scope gate and return the actual updated TeX and freshly compiled
PDF files.

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

During `write-paper` finalization, the same verification-agent role may be spawned
in a fresh context for the whole-paper check described by
`agent_resources/generation_agent/.agents/skills/write-paper/references/roles/PAPER_MATH_VERIFIER.md`.
Give that verifier only the final `main.tex`, confirmed reference-ledger rows, the
paper-verifier prompt, and its standing role contract. This remains a verification
agent; it does not create a third agent role.

## Finalization

After successful verification, rename the verified blueprint:

```bash
mv path/to/run/blueprint.md path/to/run/blueprint_verified.md
```

Immediately load and follow:

```text
agent_resources/generation_agent/.agents/skills/write-paper/SKILL.md
```

Invoke it with:

- source: `path/to/run/blueprint_verified.md`
- source status: `verified-blueprint`
- paper workspace: `path/to/run/paper/`

Follow the complete write-paper workflow, including source mapping, reference
ledger, professional paper drafting, static checks, strict compilation, reference
audit, targeted revision, and whole-paper checking. The final manuscript is a new
artifact: upstream blueprint verification does not by itself verify the rewritten
paper. Do not fall back to the old direct template conversion.

Do not finish finalization until `path/to/run/paper/main.tex` exists and the strict
compile gate has produced `path/to/run/paper/main.pdf`. Then immediately return the
actual `main.tex` and `main.pdf` files to the user. Do not only provide paths.

## Failure Return

If no verified blueprint is produced within the allowed number of iterations, create a user-facing best-available artifact:

1. Write `path/to/run/best_available_artifacts.md` from the best current `blueprint.md`, `iteration_log.md`, verifier reports, and relevant memory files.
2. State clearly at the top that the artifact is not verified and may contain gaps or errors.
3. Include the problem statement, the best partial solution or candidate blueprint, known verification failures, remaining gaps, and any useful partial progress.
4. Immediately load and follow the bundled `write-paper` skill with `best_available_artifacts.md` as the explicit source, `source_status: unverified-best-available`, and `path/to/run/paper/` as the workspace.
5. Require the generated `paper/main.tex` to state visibly that it is an unverified draft that may contain gaps or errors. Known failed arguments must remain identified as failures; they must not be rewritten as established results.
6. Run the write-paper static checks and strict compile gate to produce `path/to/run/paper/main.pdf`.
7. Return the actual `paper/main.tex` and `paper/main.pdf` files to the user immediately. Do not only provide their filesystem paths. State clearly that the manuscript is not verified.

If LaTeX tooling is unavailable or PDF compilation fails after reasonable repair attempts, return the actual available source Markdown and `paper/main.tex`, include the compile failure, and state that no PDF was produced. Do not merely print paths when the runtime supports returning files.
