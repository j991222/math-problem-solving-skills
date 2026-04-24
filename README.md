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
│   └── verification-agent-workflow.md
├── agent_resources/
│   ├── generation_agent/
│   │   └── .agents/skills/
│   └── verify_agent/
│       └── .agents/skills/
└── scripts/
    ├── blueprint_to_latex.py
    ├── search_arxiv_theorems.py
    └── compile_latex.sh
```

The generation and verification subskills are bundled under `agent_resources/*/.agents/skills/`. The generation-side `verify-proof` subskill is intentionally excluded because verification is handled by a separate clean-context subagent. Datasets, old setup scripts, API wrappers, MCP servers, verification services, and computation experiments are intentionally excluded.

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
| `low` | 1 | One generation attempt, with verification if a candidate appears |
| `medium` | 5 | Up to five generation and verification iterations |
| `high` | 10 | Up to ten generation and verification iterations |

Generation iteration `0` allows retrieval. After that, odd iterations forbid web search and theorem search, while even iterations allow retrieval again.

## Workflow

1. The master agent creates a local run directory such as `math_problem_runs/{run_id}/`.
2. The generation agent uses the bundled generation skills to write `blueprint.md`.
3. When a candidate blueprint exists, the master agent starts a clean-context verification agent.
4. The verification agent uses the bundled verification skills and writes `verification_iter_{n}.json`.
5. If verification fails, the report is sent back to the generation agent for another iteration.
6. If verification passes, `blueprint.md` is renamed to `blueprint_verified.md`.
7. The verified blueprint is converted to LaTeX and compiled to `blueprint_verified.pdf`.

The skill never treats an attempt as solved unless the clean-context verifier returns `correct` with no critical errors and no gaps.

## Outputs

A successful run produces:

```text
math_problem_runs/{run_id}/blueprint_verified.md
math_problem_runs/{run_id}/blueprint_verified.tex
math_problem_runs/{run_id}/blueprint_verified.pdf
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

For PDF generation, install either `latexmk` or `pdflatex`. If LaTeX is unavailable, the skill still produces the verified Markdown and `.tex` file.
