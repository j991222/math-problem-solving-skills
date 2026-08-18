---
name: write-paper
description: Turn blueprint_verified.md, blueprint.md, or an explicitly supplied best_available_artifacts.md into a polished LaTeX mathematics manuscript, with citation auditing, targeted revision, strict compilation, and whole-paper mathematical checking. Use after proof work exists and the user wants a paper-quality manuscript rather than another proof-search iteration.
---

# Write Paper

Transform one mathematical source artifact into a professional mathematics paper
without changing its mathematical content or verification status. This is the
blueprint-adapted form of Danus's writing
system: it retains separate planning, writing, reference, revision, compilation,
and whole-paper verification stages, but does not depend on Danus's fact graph or
MCP services.

## Resolve Paths

Resolve every resource path relative to this `SKILL.md`.

- Full workflow: `references/WORKFLOW.md`
- Standing integrity contract: `references/roles/ROLE_CONTRACT.md`
- Writer and revision roles: `references/roles/PAPER_WRITER.md` and
  `references/roles/PAPER_REVISER.md`
- Reference roles: `references/roles/REFERENCE_AUDITOR.md` and
  `references/roles/REFERENCE_VERIFIER.md`
- Whole-paper verifier: `references/roles/PAPER_MATH_VERIFIER.md`
- Large-source roles: `references/roles/PAPER_PLANNER.md` and
  `references/roles/PAPER_SECTION_WRITER.md`
- Voice and structure: `references/style/STYLE_GUIDE.md` and
  `references/style/PAPER_STRUCTURE.md`
- Acknowledgement policy: `references/boilerplate/ACKNOWLEDGEMENT.md`
- Workspace templates: `assets/templates/`
- Citation candidate seeder: `scripts/seed_reference_ledger.py`
- Static manuscript checker: `scripts/check_paper.py`
- Strict compile gate: `scripts/compile_verify.sh`

## Input Contract

Accept an explicit source path when supplied. Supported sources are:

1. `blueprint_verified.md` -> `source_status: verified-blueprint`.
2. `blueprint.md` -> `source_status: unverified-blueprint`.
3. `best_available_artifacts.md` -> `source_status:
   unverified-best-available`; accept this only when the caller explicitly names
   the file.

When the caller asks to use the latest or current proof, or the request follows
conversational proof corrections, resolve the proof version before applying any
filename fallback. The newest user correction overrides older agent proofs and run
artifacts. Consolidate the latest complete proof into `blueprint.md`, then select
that path explicitly. Do not ask the paper writer to infer a proof from scattered
chat fragments.

Verification status belongs to exact content. Select `blueprint_verified.md` only
when it contains the current proof verbatim in mathematical content and that exact
version received a passing clean-context verdict. If any later correction changes
a statement, hypothesis, proof step, calculation, or conclusion, select the
updated `blueprint.md` as `unverified-blueprint` until it is verified again. Never
let an older verified filename take priority over a newer proof.

Without an explicit path or conversational revision context, search the active run
directory only. If both blueprint files exist, use the conversation, iteration
log, and verification report to identify the latest complete proof; do not decide
from filename priority or modification time alone. Never auto-select
`best_available_artifacts.md`. If neither blueprint exists, stop and report the
missing input. Do not search unrelated run directories or reconstruct the source
from memory files.

If the available conversation and run artifacts do not determine one coherent
latest proof, ask one focused question about the conflicting version or correction.
Do not merge incompatible arguments and do not fall back to a stale verified
source merely to avoid the question.

Record which file and source status were selected. A `blueprint_verified.md` source means the
blueprint passed the upstream clean-context check; it does not mean the rewritten
paper has passed whole-paper verification. A `blueprint.md` source is unverified,
and every deliverable must remain visibly described as a draft until independently
verified. A `best_available_artifacts.md` source is an unverified best-effort
record: the TeX/PDF must visibly state that it may contain gaps or errors, and it
can never be labeled publishable by this run.

Treat the selected source as the sole source of mathematical content. Supporting
memory files may clarify provenance or citation metadata, but they may not supply
new claims unless the selected source is first amended and, when applicable,
re-verified. For `unverified-best-available`, preserve the status of every item:
established partial results may be stated as such, candidate arguments remain
candidate arguments, and known failed/refuted steps remain identified as failures.

## Workspace

Keep the selected source unchanged. Unless the caller specifies another location, use:

```text
<source-directory>/paper/
  PROJECT_BRIEF.md
  REFERENCE_LEDGER.md
  REVISION_LOG.md
  VERIFY_LEDGER.md
  SOURCE_MAP.json
  main.tex
  main.pdf
  checks/
```

Initialize missing control files from `assets/templates/`; never overwrite
operator-filled files. `SOURCE_MAP.json` maps paper labels to source headings and
stays out of the visible paper.

## Required Workflow

Read `references/WORKFLOW.md` before writing. Its stages are binding:

1. Resolve and assess the selected source and its verification status.
2. Initialize and fill the project brief without inventing title, authorship,
   affiliation, venue, funding, or thanks.
3. Build the reference ledger from citations actually present in the source.
4. Read both style references in full and plan the paper's narrative and source
   mapping.
5. Write `main.tex` from the source, preserving all hypotheses, definitions,
   intermediate claims, proof steps, calculations, conclusions, and citations.
6. Run the static checker and strict compile gate; repair failures with small,
   located edits.
7. Audit every citation, verify flagged entries online only when retrieval is
   allowed, and revise the paper from sourced verdicts.
8. Verify the complete paper as written. Revise only `must-fix` findings and keep
   the loop bounded.
9. Deliver only with an honest status that distinguishes compiled, reference-
   checked, whole-paper-checked, independently verified, and unverified states.

## Non-Negotiable Rules

- Preserve all mathematical assertions and their status from the selected source. Exposition may be
  reorganized and rewritten; mathematics may not be strengthened, weakened,
  silently compressed away, or invented. A known failed argument may not be
  promoted to an established result.
- Preserve every citation. Never replace a citation with "standard" or
  "well-known". Never invent bibliographic metadata.
- Do not introduce new load-bearing mathematics while repairing prose. A missing
  argument becomes `\note{[math/blocker] ...}`, not a plausible bridge.
- Do not expose source filenames, run paths, source-map identifiers, hashes,
  agent names, or pipeline internals in the title, abstract, body, author block,
  or bibliography.
- Never claim independent verification unless a clean-context verifier actually
  checked the final paper artifact. Same-context checking must be labeled as such.
- Do not publish, push, submit, or upload the paper as part of this skill.

## Large Sources

Do not render a long source as one lemma per source block. First identify the
headline result and the small support layer that carries its proof. Routine local
steps should be integrated into the proof that uses them; genuinely reusable or
independent results receive labeled environments.

If a single pass would exceed context or output limits, follow the large-input
procedure in `references/WORKFLOW.md`: plan from statements first, write sections
from complete assigned source blocks, then stitch mechanically. Partition by
mathematical result and dependency, never by raw character count.

## Completion Gate

A publishable result requires all of the following:

- `scripts/check_paper.py` reports no errors;
- `scripts/compile_verify.sh` succeeds with no undefined citations or references;
- every bibliography entry is verified or explicitly operator-trusted;
- whole-paper verification has zero `must-fix` findings;
- no visible blocker notes remain, unless the operator explicitly accepts a
  clearly labeled draft.

When any gate is unavailable or fails, preserve the best manuscript and report it
as a draft with the exact blockers. Do not use optimistic language such as
"should compile" or "effectively verified".

`source_status: unverified-best-available` always produces a draft, even when the
static and compile gates pass. Its required visible disclaimer and known-gap
markers are intentional draft content, not items to erase merely to satisfy the
publishable gate.

## Post-Delivery Revisions

After `main.tex` has been delivered, route user-requested selective revisions to
the sibling `../revise-paper/SKILL.md`. Do not rerun this full writing workflow for
an existing manuscript: doing so can replace user edits and alter passages the user
already accepted. The revision skill must propose changes before editing, apply
only the user's selected subset, enforce its scope gate, compile, and return the
revised TeX and PDF after every completed revision turn.
