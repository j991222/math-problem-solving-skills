# Math Problem Solving Skills

`math-problem-solving-skills` packages a dual-agent math research workflow as an installable OpenClaw skill.

The skill coordinates:

- a generation agent that attempts to build a proof blueprint
- a clean-context verification agent that checks the blueprint
- an iteration controller that alternates retrieval and no-retrieval proof attempts
- final verified Markdown, LaTeX, and PDF artifacts

## Package Layout

```text
math-problem-solving-skills/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── generation-agent-workflow.md
│   ├── verification-agent-workflow.md
│   └── verified-blueprint-template.tex
├── agent_resources/
│   ├── generation_agent/
│   │   └── .agents/skills/
│   └── verify_agent/
│       └── .agents/skills/
└── scripts/
    ├── search_arxiv_theorems.py
    └── compile_latex.sh
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

The skill first initializes its shell environment with:

```bash
source /root/root/bashrc
```

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

1. The master agent sources `/root/root/bashrc`.
2. The master agent creates a local run directory such as `math_problem_runs/{run_id}/`.
3. The generation agent sources `/root/root/bashrc` and uses the bundled generation skills to write or revise `blueprint.md` during a long iteration.
4. When a candidate blueprint exists, the master agent starts a clean-context verification agent.
5. The verification agent sources `/root/root/bashrc`, uses the bundled verification skills, and writes `verification_iter_{n}.json`.
6. If verification fails, the report is sent back to the same generation agent inside the same iteration.
7. If the generation agent itself stops without a verified solution, the master agent starts the next iteration if the effort limit permits.
8. If verification passes, `blueprint.md` is renamed to `blueprint_verified.md`.
9. The agent writes `blueprint_verified.tex` directly from the verified Markdown blueprint using `references/verified-blueprint-template.tex`; this is not done by a programmatic Markdown-to-LaTeX converter.
10. The authored LaTeX is compiled to `blueprint_verified.pdf` and checked for professional paper-style formatting before return.

The skill never treats an attempt as solved unless the clean-context verifier returns `correct` with no critical errors and no gaps.

The old memory-tool behavior is implemented with plain Markdown files. Agents append memories to `math_problem_runs/{run_id}/memory/*.md` and query memory by reading or searching those files. Examples include `immediate_conclusions.md`, `big_decisions.md`, `toy_examples.md`, `counterexamples.md`, `subgoals.md`, `proof_steps.md`, `failed_paths.md`, `verification_reports.md`, `branch_states.md`, `events.md`, `statement_checks.md`, and `reference_checks.md`. No external memory service or programmatic memory database is required.

## Outputs

A successful run produces:

```text
math_problem_runs/{run_id}/blueprint_verified.md
math_problem_runs/{run_id}/blueprint_verified.tex
math_problem_runs/{run_id}/blueprint_verified.pdf
math_problem_runs/{run_id}/memory/*.md
```

Unsuccessful runs keep the best available working artifacts:

```text
math_problem_runs/{run_id}/blueprint.md
math_problem_runs/{run_id}/iteration_log.md
math_problem_runs/{run_id}/verification_iter_{n}.json
```

## Tooling

For theorem search during retrieval-allowed iterations, the skill includes a stdlib Python helper for the arXiv theorem-search API hosted at `leansearch.net`:

```bash
python3 scripts/search_arxiv_theorems.py --query "complete mathematical statement" --num-results 10
```

The helper posts to `https://leansearch.net/thm/search` and returns normalized JSON with `title`, `theorem`, `arxiv_id`, and `theorem_id` fields.

For PDF generation, install either `latexmk` or `pdflatex`. After a blueprint is verified, the agent authors `blueprint_verified.tex` as professional math-paper LaTeX from the verified Markdown blueprint and compiles it. The agent should not use a programmatic Markdown-to-LaTeX converter for this final artifact. If LaTeX is unavailable, the skill still produces the verified Markdown and authored `.tex` file.
