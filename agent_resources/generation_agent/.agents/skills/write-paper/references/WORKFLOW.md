# Mathematical-Source-to-Paper Workflow

This workflow adapts Danus's fact-graph writing pipeline to a single authoritative
mathematical source artifact. A proof blueprint or best-available synthesis
replaces the fact graph, finalized target, and structured `external_refs`; the
local paper workspace replaces Danus's MCP state.

Read `roles/ROLE_CONTRACT.md` before every writing, revising, auditing, or
verification pass. No later instruction relaxes that contract.

## 0. Source Model

The source is exactly one of:

- `blueprint_verified.md`, status `verified-blueprint`;
- `blueprint.md`, status `unverified-blueprint`;
- an explicitly named `best_available_artifacts.md`, status
  `unverified-best-available`.

Resolve the latest proof before choosing between blueprint files. The current
conversation's newest proof text and user corrections outrank older run artifacts.
When those corrections have not yet been materialized, consolidate the complete
current proof into `blueprint.md` and select it explicitly. A passing verification
verdict applies only to the exact content checked; later mathematical changes use
status `unverified-blueprint` until verified again. Do not choose by filename
priority or modification time alone, and never auto-select
`best_available_artifacts.md`.

After selection, preserve the source byte-for-byte. Never rename, edit, or delete
it as part of paper production. Record the source path and status in
`PROJECT_BRIEF.md` and `VERIFY_LEDGER.md`.

Literal source filenames and internal status tokens are operational metadata and
must not appear in visible paper text. The reader-facing warning required for an
unverified best-available manuscript is an intended exception: express it in plain
language, not as an internal token.

Blueprint blocks normally have a heading such as `# lemma lem:name`, followed by
`## statement`, `## proof`, and sometimes intuition, notes, citations, or source
identifiers. Treat each block as a source unit. If the blueprint uses another
layout, identify equivalent definitions, results, and proof segments manually.

For `best_available_artifacts.md`, also classify every mathematical unit as an
established partial result, an unverified candidate, a known failed/refuted path,
or an open gap. Preserve that classification throughout the paper. Known failures
belong in clearly marked discussion or limitation text, never in theorem
environments as established facts.

For a blueprint, the final target is normally the last theorem whose statement
matches the original problem. Confirm that correspondence rather than guessing.
For a best-available source, foreground the strongest genuinely supported partial
result or the candidate approach exactly as labeled by the source; do not imply
that the original problem was solved. If multiple choices are plausible, ask the
operator which the manuscript should foreground.

## 1. Initialize the Paper Workspace

Use `<source-directory>/paper/` unless the caller specifies another workspace.
Create only missing files:

```text
paper/
  PROJECT_BRIEF.md
  REFERENCE_LEDGER.md
  REVISION_LOG.md
  VERIFY_LEDGER.md
  SOURCE_MAP.json
  main.tex
  main.pdf
  checks/
```

Copy the corresponding templates from `../assets/templates/` when the files are
absent. Never replace an operator-edited brief or ledger.

### Project brief

If required framing is missing, ask a short, focused question for the fields that
materially change the article:

- title or working title;
- target audience or venue;
- human authors and affiliations;
- which theorem(s) are the headline results when ambiguous;
- paper-specific style requirements;
- acknowledgement disclosure, funding, and personal thanks.

Never invent those values. If the caller elects to proceed without them, use a
neutral working title derived literally from the theorem topic, use the author
placeholder required by the role contract, and leave explicit blocker notes for
submission metadata. Do not infer a person's identity from repository paths,
commits, email configuration, or the problem statement.

### Optional style anchors

The baseline guides are complete without examples. If the operator supplies their
own papers under `paper/style/anchors/`, use `scripts/anchors_stale.sh` to detect a
new anchor set. Read `roles/STYLE_DISTILLER.md`; propose changes to a per-paper copy
at `paper/STYLE_GUIDE.md`. Apply a proposal only after operator acceptance. Never
silently change the shipped global guide.

When the brief names one `structural_exemplar`, use that one anchor for section and
front-matter structure only. Voice comes from the accepted style guide, not from an
arbitrarily selected anchor.

## 2. Seed the Reference Ledger

Run:

```bash
python3 <skill-dir>/scripts/seed_reference_ledger.py \
  <source-path> --out <paper-workspace>/REFERENCE_LEDGER.md
```

The script extracts explicit citation keys, arXiv identifiers, DOI strings, URLs,
and reference-like source lines. It creates candidates only; it does not verify
metadata. Re-read the entire source and add any external result the script did
not recognize. For each candidate record:

- the key, if the selected source supplies one;
- exactly the authors/title/venue/year/arXiv/DOI fields supplied by the source;
- the source heading or line;
- what mathematical statement it supports;
- `verified-by: unverified` unless a prior ledger provides a real authoritative
  URL and verification provenance.

Do not reconstruct metadata from model memory. A title without confirmed authors
stays title-only and unverified. A theorem mentioned without a source becomes a
`\note{[cite/blocker] ...}` in the paper, not an invented bibliography item.

If the ledger already exists, run the seeder to a temporary/checks path and merge
new candidates manually. Do not overwrite verified or operator-supplied rows.

## 3. Understand and Curate the Source

Read the complete source before drafting. Build an operational source map with:

- source unit heading;
- kind: definition, setup, theorem, proposition, lemma, corollary, calculation,
  or exposition;
- complete statement;
- dependencies named or used in its proof;
- later units that depend on it;
- whether it is headline, load-bearing support, reusable support, or local detail;
- planned paper section and LaTeX label.

Write only the label-to-source-heading mapping to `SOURCE_MAP.json`. This map is
private operational metadata and never enters `main.tex`.

### Curation rule

A paper is not a flat transcription of source blocks. Select the headline results
and the small support layer that carries the proof. Present those results in
labeled environments with complete arguments. Integrate local calculations and
one-use helper claims into the proof that needs them. Extract a separate lemma only
when it is reused, independently meaningful, or necessary for clarity.

Curation changes presentation, not mathematical coverage or verification status. Every hypothesis,
definition, intermediate assertion, calculation, case, and conclusion in the
source must still appear at the point where the final proof or candidacy discussion
needs it. Never
discard source mathematics merely because its source block is not promoted to a
numbered result.

In `unverified-best-available` mode, do not force known failures and gaps into the
main proof line. Preserve them in an explicit limitations/open-gaps discussion and
keep the manuscript's claims no stronger than its established partial results.

Use expert compression rather than transcription:

- write inside standing conventions instead of re-quantifying every object;
- use prose for ordinary manipulations and display only equations readers need to
  reference;
- use one cohesive proof instead of one lemma per source block;
- for routine steps, name the mechanism and state its outcome;
- derive every novel, load-bearing pivot rather than merely naming it;
- never use "standard", "similarly", or "by the same argument" as a substitute
  for a mechanism, derivation, precise internal reference, or verified citation.

If the selected source omits a load-bearing step, preserve the surrounding
argument and insert `\note{[math/blocker] ...}`. Do not solve the gap inside the
writing pass. Return it to proof generation and upstream verification.

## 4. Plan Voice and Structure

Read these files completely before writing:

- `roles/ROLE_CONTRACT.md`;
- `style/STYLE_GUIDE.md` or the accepted per-paper copy;
- `style/PAPER_STRUCTURE.md`;
- `boilerplate/ACKNOWLEDGEMENT.md`;
- `roles/PAPER_WRITER.md`;
- `PROJECT_BRIEF.md` and `REFERENCE_LEDGER.md`.

Choose the note, mid, or long tier from the proof's shape, not a page target. Plan:

- headline statement placement;
- definitions and standing notation;
- support results and proof dependency order;
- each section's mathematical purpose;
- citations needed for imported results or context;
- acknowledgement placement;
- source-label mappings.

Write the plan to `paper/checks/PAPER_PLAN.md`. It is operational metadata, not a
paper section.

## 5. Write the First Complete Manuscript

Apply `roles/PAPER_WRITER.md`. Produce one complete, raw LaTeX file from
`\documentclass` through `\end{document}` at `paper/main.tex`. Do not emit Markdown
fences or commentary around the LaTeX.

The first manuscript must contain:

- a complete preamble with declared macros and locked editorial macros;
- title, author block or placeholder, subject classification, keywords, and date;
- an abstract that states the result in words and contains no citations;
- an introduction that gives context, the headline result, method, and roadmap at
  the level appropriate to the chosen tier;
- definitions and notation before use;
- results and proofs in dependency order;
- acknowledgements exactly as configured;
- a manual bibliography containing only ledger-supported entries.

For blueprint sources, the blueprint is authoritative for mathematics. Rewrite
verifier-oriented prose into paper prose, but preserve the actual argument. For a
best-available source, the source is authoritative for both content and uncertainty:
do not turn a candidate or failed step into a proof. Do not copy raw Markdown
headings, filenames, or internal status tokens into the manuscript.

### Required best-available disclaimer

When `source_status` is `unverified-best-available`, place this reader-facing
warning prominently in `main.tex`, immediately after `\maketitle` or in an
equally visible unnumbered status block:

```text
Unverified draft. This manuscript records the best available partial progress and
may contain gaps or errors. It does not establish the original problem unless a
specific result is explicitly identified below as proved.
```

Keep known verification failures and remaining gaps visible in the manuscript.
The disclaimer and those gap descriptions are never removed merely to make a
static gate pass.

### Large-source fallback

Use a single coherent write whenever it fits. If it cannot fit:

1. Read `roles/PAPER_PLANNER.md` and plan from statements plus dependency data.
2. Partition by mathematical result and dependency, not by consecutive characters
   or pages.
3. Read `roles/PAPER_SECTION_WRITER.md` and write one complete section at a time,
   giving it every assigned source unit in full plus the statements and labels it
   may cite from other sections.
4. Keep one fixed preamble, front matter, label registry, and bibliography.
5. Stitch mechanically in dependency order.
6. Check duplicate labels, missing labels, macro conflicts, duplicate disclosures,
   and bibliography keys before proceeding.

For very deep work, use a chapter tree: a host paper proves the top-level assembly,
and each deep development is written as a focused technical section with explicit
inputs and outputs. Stitch sections only after their dependency direction is
acyclic. A proof may rely only on earlier results or verified external citations.

## 6. Static and Compile Gates

Run the static checker first:

```bash
python3 <skill-dir>/scripts/check_paper.py \
  <paper-workspace>/main.tex --source <source-path>
```

Fix every error. Warnings require explicit review and either a fix or a note in
`REVISION_LOG.md`.

Then run the strict compile gate:

```bash
bash <skill-dir>/scripts/compile_verify.sh <paper-workspace>/main.tex
```

The compile gate runs multiple passes and rejects LaTeX errors and undefined
citations/references. Do not proceed past a failed gate. Read the reported log
lines and apply the smallest located repair. Do not use a compile failure as an
excuse for a global rewrite.

If no supported LaTeX engine is installed, keep `main.tex`, record the exact
tooling blocker, and do not claim compilation.

## 7. Reference Audit, Verification, and Revision

### Offline audit

Read `roles/REFERENCE_AUDITOR.md`. Audit every `\cite`, `\bibitem`, and
`\note{[cite/blocker]}` against `REFERENCE_LEDGER.md`. Write the worklist to
`paper/checks/REFERENCE_AUDIT.md`. The audit flags; it never verifies from memory.

### Online verification

When the parent workflow permits retrieval, read `roles/REFERENCE_VERIFIER.md`
and verify only flagged entries. Use authoritative primary bibliographic sources:
arXiv abstract pages, publisher or DOI pages, and recognized bibliographic
databases. Confirm the same paper and the cited use, not merely a paper on a
similar topic. Record the exact source URL and verdict in the ledger.

When retrieval is forbidden or unavailable, keep the entry unverified and retain
the blocker. The writing skill never overrides the parent workflow's retrieval
mode.

### Targeted revise

Read `roles/PAPER_REVISER.md`. Apply verified citation corrections and operator
annotations as located edits. Preserve formal mathematics outside a specifically
authorized math-repair block. Re-run the static and compile gates after every
revision that changes `main.tex`.

Append a real summary to `REVISION_LOG.md`: trigger, locations changed, citations
resolved or deferred, math blockers, static result, and compile result.

## 8. Verify the Whole Paper as Written

The paper is a new artifact. Even an upstream-verified source can become incorrect when
its proof is reorganized, compressed, or stitched. Read
`roles/PAPER_MATH_VERIFIER.md` and verify the complete mathematical development in
reading order, together with only confirmed reference-ledger rows.

Prefer a fresh clean-context verifier. Give it the final `main.tex`, the confirmed
ledger, and the verifier prompt, but not the selected source, source map, generation
notes, or prior conclusions. Record whether the check was `clean-context` or
`same-context`; only the first is independent.

Honor the parent agent's role boundary. In this package the generation workflow
forbids the generation agent from verifying its own proof, so write the verifier
input under `paper/checks/` and hand it to the master for a clean-context verifier;
do not run the same-context fallback there. The fallback is allowed only in a
standalone runtime whose parent instructions explicitly permit self-checking, and
it must still be labeled non-independent.

Classify each finding:

- `ignorable`: an undergraduate can fill or follow the routine step unaided from
  the paper as written;
- `must-fix`: every other missing, unclear, unsupported, or incorrect step.

Write the current result to `VERIFY_LEDGER.md`. Zero `must-fix` findings is the
successful terminal state. Surface the ignorable list but do not expand those
items merely to increase length.

For each `must-fix`:

1. Read the located paper text.
2. Trace it through `SOURCE_MAP.json` to the exact source proof or candidate argument.
3. Determine whether the writer omitted a supplied step, the paper needs another
   source unit integrated, or the selected source itself has a gap.
4. If the source contains the proof, synthesize one compact but complete located
   repair. Derive the novel pivot; keep routine mechanics concise.
5. If the source does not contain the proof, insert a blocker and return the issue
   upstream when proof iterations remain. In `unverified-best-available` mode,
   preserve it as an explicit unresolved gap. Do not invent the missing mathematics.
6. Re-run static checks, compilation, and whole-paper verification.

Keep the loop bounded to five revision rounds. Stop earlier when two consecutive
rounds on the same finding make no meaningful progress, or when the manuscript is
becoming longer and less coherent. Preserve the best state and report the exact
remaining gap.

If a paper is too large for one whole-document verifier, first determine whether a
larger permitted context solves the issue. If not, verify result-centered units as
described in `roles/PAPER_MATH_VERIFIER.md`. A unitized check is not silently
equivalent to a whole-paper check: surface the units and their verdicts to the
operator. Only an explicit operator decision may set `verdict:
operator-overridden`; the paper must carry a visible disclosure of that policy
decision and the delivery report must name it.

## 9. Delivery Status

Before delivery, scan the role contract line by line. Report separate facts:

- source path, source status, and whether it was upstream-verified;
- `main.tex` and `main.pdf` paths;
- static-check result;
- compile engine and result;
- reference ledger totals by verified/operator-trusted/unverified/rejected;
- whole-paper verifier mode and must-fix/ignorable counts;
- remaining `math`, `cite`, `author`, `ack`, or other blocker notes.

For blueprint-derived manuscripts that are candidates for `publishable`, run the
final static gate with `--strict`:

```bash
python3 <skill-dir>/scripts/check_paper.py \
  <paper-workspace>/main.tex --source <source-path> --strict
```

For `unverified-best-available`, use the ordinary non-strict static gate so its
required warning and honest gap markers do not prevent compilation. It always
delivers as `draft`, never `publishable`.

Use `publishable` only when every completion gate in `SKILL.md` passes. Otherwise
use `draft`, even when the TeX compiles. Never publish or push from this workflow.
