# Math Problem Solving Skills

`math-problem-solving-skills` packages a dual-agent math research workflow as an installable OpenClaw skill.

The skill coordinates:

- a generation agent that attempts to build a proof blueprint
- a clean-context verification agent that checks the blueprint
- an iteration controller that alternates retrieval and no-retrieval proof attempts
- final source Markdown plus manuscript LaTeX and PDF artifacts produced by the
  bundled `write-paper` skill

## Package Layout

```text
math-problem-solving-skills/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── generation-agent-workflow.md
│   └── verification-agent-workflow.md
├── agent_resources/
│   ├── generation_agent/
│   │   └── .agents/skills/
│   │       ├── revise-paper/
│   │       └── write-paper/
│   └── verify_agent/
│       └── .agents/skills/
└── scripts/
    └── search_arxiv_theorems.py
```

The generation and verification subskills are bundled under `agent_resources/*/.agents/skills/`. The generation-side `verify-proof` subskill is intentionally excluded because verification is handled by a separate clean-context subagent. Datasets, old setup scripts, API wrappers, verification services, and computation experiments are intentionally excluded.

## Installation

Install by copying the whole `math-problem-solving-skills` directory into an OpenClaw skills directory.

Workspace installation, highest precedence:

```bash
mkdir -p /path/to/workspace/skills
cp -R math-problem-solving-skills /path/to/workspace/skills/
```

Project-agent installation:

```bash
mkdir -p /path/to/workspace/.agents/skills
cp -R math-problem-solving-skills /path/to/workspace/.agents/skills/
```

Shared local installation:

```bash
mkdir -p "$HOME/.openclaw/skills"
cp -R math-problem-solving-skills "$HOME/.openclaw/skills/"
```

Restart the OpenClaw session, or run `/new`, so the skill registry reloads. Verify with:

```bash
openclaw skills list
```

## Usage

Invoke the skill with a math problem and optional effort.

```text
Use $math_problem_solving_skills to solve the following problem.
Reasoning effort: high.

Problem:
Every finite group of prime order is cyclic.
```

If reasoning effort is omitted, the skill uses `high`.

## Reasoning Effort

| Effort | Maximum Iterations | Behavior |
| --- | ---: | --- |
| `low` | 1 | One long generation phase, with verification cycles if candidates appear |
| `medium` | 5 | Up to five long generation phases |
| `high` | 10 | Up to ten long generation phases |

One iteration means the generation agent works for a long time under one fixed retrieval mode. During that iteration it may produce several candidate blueprints, receive clean-context verification reports through the master agent, and continue repairing the same blueprint. Failed verification does not consume a new iteration. The iteration ends only when a candidate verifies or when the generation agent itself decides to stop the current long attempt and returns `stuck` or `no_solution`.

Generation iteration `0` allows retrieval. After that, odd iterations forbid web search and theorem search, while even iterations allow retrieval again.

## Workflow

1. The master agent creates a local run directory such as `math_problem_runs/{run_id}/`.
2. The generation agent uses the bundled generation skills to write or revise `blueprint.md` during a long iteration.
3. When a candidate blueprint exists, the master agent starts a clean-context verification agent.
4. The verification agent uses the bundled verification skills and writes `verification_iter_{n}.json`.
5. If verification fails, the report is sent back to the same generation agent inside the same iteration.
6. If the generation agent itself stops without a verified solution, the master agent starts the next iteration if the effort limit permits.
7. If verification passes, `blueprint.md` is renamed to `blueprint_verified.md`.
8. The master agent immediately invokes the bundled `write-paper` skill with
   `blueprint_verified.md` as the sole mathematical source. The writing workflow
   authors `paper/main.tex`, compiles `paper/main.pdf`, and runs its static,
   reference, mathematical, and whole-paper checks.
9. The master agent returns the actual `paper/main.tex` and `paper/main.pdf` files
   to the user.
10. If the maximum iteration count is reached without passing verification, the
    master agent first synthesizes `best_available_artifacts.md`, then explicitly
    invokes `write-paper` on that file. The resulting manuscript remains visibly
    marked as an unverified draft, preserves known failures and open gaps, and is
    compiled to `paper/main.pdf`; the actual TeX and PDF files are returned to the
    user.

If the user asks for a paper after one or more conversational proof-correction
rounds, the master first consolidates the newest complete proof into
`blueprint.md`. Newer user corrections override older agent proofs. The master then
passes that exact source path to `write-paper`; it does not prefer an older
`blueprint_verified.md` merely because of its filename. Verification status is
retained only when the exact latest proof was the version that passed verification.

For an existing TeX manuscript, revision uses the bundled `revise-paper` skill
instead of regenerating the article. Its first response contains selectable,
located suggestions and makes no file changes. After the user chooses a subset,
only those approved locations may change; each completed revision returns the
actual revised TeX and a freshly compiled PDF.

The skill never treats an attempt as solved unless the clean-context verifier returns `correct` with no critical errors and no gaps.

The old memory-tool behavior is implemented with plain Markdown files. Agents append memories to `math_problem_runs/{run_id}/memory/*.md` and query memory by reading or searching those files. Examples include `immediate_conclusions.md`, `big_decisions.md`, `toy_examples.md`, `counterexamples.md`, `subgoals.md`, `proof_steps.md`, `failed_paths.md`, `verification_reports.md`, `branch_states.md`, `events.md`, `statement_checks.md`, and `reference_checks.md`. No external memory service or programmatic memory database is required.

## Outputs

A successful run produces:

```text
math_problem_runs/{run_id}/blueprint_verified.md
math_problem_runs/{run_id}/paper/main.tex
math_problem_runs/{run_id}/paper/main.pdf
math_problem_runs/{run_id}/paper/PROJECT_BRIEF.md
math_problem_runs/{run_id}/paper/REFERENCE_LEDGER.md
math_problem_runs/{run_id}/paper/REVISION_LOG.md
math_problem_runs/{run_id}/paper/VERIFY_LEDGER.md
math_problem_runs/{run_id}/paper/SOURCE_MAP.json
math_problem_runs/{run_id}/memory/*.md
```

Unsuccessful runs keep the best available working artifacts:

```text
math_problem_runs/{run_id}/blueprint.md
math_problem_runs/{run_id}/best_available_artifacts.md
math_problem_runs/{run_id}/iteration_log.md
math_problem_runs/{run_id}/verification_iter_{n}.json
math_problem_runs/{run_id}/paper/main.tex
math_problem_runs/{run_id}/paper/main.pdf
```

The unsuccessful-run PDF is a readable record of the strongest supported partial
work, not a verified solution. If the TeX toolchain remains unavailable or
compilation still fails after the repair cycle, the skill returns the source
Markdown and `paper/main.tex`, reports the exact failure, and does not claim that a
PDF was produced.

## Tooling

For theorem search during retrieval-allowed iterations, the skill includes a stdlib Python helper for the arXiv theorem-search API hosted at `leansearch.net`:

```bash
python3 scripts/search_arxiv_theorems.py --query "complete mathematical statement" --num-results 10
```

The helper posts to `https://leansearch.net/thm/search` and returns normalized JSON with `title`, `theorem`, `arxiv_id`, and `theorem_id` fields.

For PDF generation, install a supported TeX engine: `pdflatex`, `xelatex`,
`lualatex`, or `tectonic`. The compile gate auto-detects `pdflatex` or `tectonic`;
set `TEX_ENGINE=xelatex` or `TEX_ENGINE=lualatex` to select either of those
engines. The bundled `write-paper` skill authors the manuscript in a dedicated
`paper/` workspace and compiles it through its strict
compile gate. It accepts `blueprint_verified.md` after successful verification and
accepts `best_available_artifacts.md` only when the master explicitly supplies it
after the iteration limit. It does not use a programmatic Markdown-to-LaTeX
converter for the manuscript.
