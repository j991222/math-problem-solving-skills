---
name: revise-paper
description: Review an existing LaTeX paper without editing it, propose selectable revisions, and then apply only the changes the user explicitly approves. Use for post-draft or post-delivery manuscript revision where unrequested text, mathematics, formatting, and user edits must remain untouched and every completed revision must return both TeX and a freshly compiled PDF.
---

# Revise Paper

Revise an existing paper incrementally. Treat the supplied TeX as an established
manuscript, not raw material for a replacement paper. The user may already have
edited and finalized any unmentioned passage.

## Resources

Resolve paths relative to this `SKILL.md`.

- Detailed workflow: `references/WORKFLOW.md`
- Edit-scope gate: `scripts/check_revision_scope.py`
- Strict compiler for a self-contained TeX file:
  `../write-paper/scripts/compile_verify.sh`

Read the full workflow before reviewing or editing a manuscript.

## Input Contract

Require one explicit root `.tex` path or an unambiguous TeX attachment. If several
candidate root files exist, ask which one to revise. Read the current file from
disk on every turn so manual edits made between turns are preserved.

Also accept user notes, compiler logs, referee comments, or a list of requested
changes. These are instructions about the existing manuscript; they do not
authorize a general rewrite.

## Two-Phase Authorization

### Phase 1: review only

The first turn for a manuscript is advisory. Read the whole current TeX and return
a concise set of independently selectable suggestions with stable IDs such as
`R1`, `R2`, and `R3`. For each suggestion, name the exact location, the issue, the
proposed change, and every coupled location that would need editing.

Do not edit the TeX, create a replacement TeX, run a formatter, or overwrite its
PDF in this phase. End by stating explicitly that no files were changed and ask
the user to select suggestion IDs or specify another exact edit.

### Phase 2: approved edits only

Edit only after a later user message explicitly selects suggestion IDs or gives a
concrete replacement instruction. Approval of one suggestion does not approve the
others. A vague request such as "polish it" starts another review-only proposal
round; it is not blanket authorization.

Before editing, re-read the current TeX and resolve every approved change to exact
locations. If the user modified a proposed location since the review, preserve the
new text and re-propose that item instead of overwriting it. If an approved change
now requires an additional location that was not disclosed, ask for approval
before touching it.

## Preservation Contract

- Every byte outside approved edit locations is protected, including whitespace,
  comments, line wrapping, macros, labels, citations, bibliography entries,
  author metadata, acknowledgements, and ordering.
- Do not run global formatters, cleanup passes, search-and-replace operations, or
  full-paper rewrites unless the user explicitly approves that exact global scope.
- Do not silently apply unselected review suggestions, even when they seem
  obviously beneficial.
- Preserve mathematical content unless the user explicitly approves a located
  mathematical change. Do not invent a proof repair.
- Preserve explicit exclusions such as "change R2 but leave the theorem statement
  alone" as hard boundaries.
- Compilation does not authorize unrelated fixes. If compilation needs a change
  outside approved scope, stop and request expanded approval.

## Mandatory Scope Gate

Immediately before editing, copy the current TeX to a temporary snapshot and note
the minimal one-based line ranges covering each approved location. After editing,
run:

```bash
python3 <skill-dir>/scripts/check_revision_scope.py \
  <temporary-before.tex> <current-paper.tex> \
  --allow <start:end> [--allow <start:end> ...]
```

The gate must pass before compilation. Inspect its reported diff hunks as well as
the edited passages. For a multi-file paper, snapshot and gate every edited TeX
file separately; never edit an included file merely because the root file includes
it.

If the scope gate fails, restore only this turn's attempted edits from the
temporary snapshot and make a narrower edit. Never weaken the allowed ranges to
excuse an accidental change.

## Compile and Deliver

After the scope gate passes, compile the exact revised source. For a self-contained
file, use the sibling strict compiler. For a multi-file project, use its existing
build command from the project directory and require a newly successful build of
the root PDF. Never return a pre-existing or stale PDF as the result of a failed
build.

A revision is complete only when both conditions hold:

- the scope gate proves that every TeX change was approved;
- the revised TeX compiles successfully to a fresh PDF.

Then return the actual revised `.tex` and `.pdf` files to the user, not only their
paths. Include a short list of the approved items applied and state that all other
regions were preserved.

If compilation cannot succeed without an unapproved edit or unavailable tooling,
restore this turn's attempted TeX changes, report the blocker, and request the
smallest additional authorization needed. Do not claim the revision is complete.
