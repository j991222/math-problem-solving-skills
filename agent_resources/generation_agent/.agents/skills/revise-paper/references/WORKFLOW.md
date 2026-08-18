# Selective TeX Revision Workflow

Use this workflow for an already-written paper. The source is user-owned state.
Preservation is the default; editing requires specific approval.

## 1. Resolve the Current Manuscript

Identify one explicit root TeX file. Do not search unrelated directories for a
more convenient draft. Read the complete current file, including the preamble,
comments, appendices, and bibliography. Note any `\input`, `\include`, local style,
figure, or bibliography dependencies, but do not edit those files without explicit
authorization.

Always re-read files at the start of a new user turn. The on-disk version outranks
the version seen during an earlier review because the user may have edited it in
the meantime.

## 2. First Response: Suggestions Only

Do not modify any file. Review the manuscript for issues that materially affect:

- mathematical clarity or an apparent unsupported step;
- statement/hypothesis consistency;
- organization and local redundancy;
- notation and cross-reference consistency;
- citations and bibliography consistency;
- prose, grammar, and readability;
- LaTeX correctness or likely compilation failure.

Do not manufacture suggestions to fill a quota. Separate changes that the user can
approve independently. Use this format:

```text
R1 - <short title>
Priority: blocking | important | optional
Location: <section/environment plus current line numbers>
Observation: <specific issue>
Suggested change: <concrete action, not replacement prose unless useful>
Authorized footprint if selected: <every TeX location that would change>
Coupled with: <other proposal ID or none>
```

An authorized footprint must disclose preamble, bibliography, label, citation, or
other secondary edits needed by the suggestion. If a suggestion cannot be safely
separated from another, mark them as coupled rather than hiding the dependency.

End the review response with both facts:

- no file was changed;
- the user may select any subset by ID or state another exact edit.

Do not produce a revised TeX or PDF during review-only mode.

## 3. Interpret the User's Selection

A later message such as `apply R1 and R4`, `only fix the abstract as proposed`, or
an exact custom edit authorizes only the named work. Explicit exclusions override
proposal text. `Apply all` authorizes all currently listed proposals only when the
user says it explicitly.

If the request is vague, respond with a smaller set of located proposals and do
not edit. If an edit could reasonably mean two materially different changes, ask
one focused question.

Before applying a selected proposal:

1. Re-read the complete current TeX.
2. Confirm that the quoted issue and location still exist.
3. If the user changed that region, do not overwrite it; explain that the proposal
   is stale and offer a revised suggestion.
4. Enumerate the exact current line ranges and intended operation for every file
   to be touched.
5. Include only coupled locations disclosed in the selected proposal. A newly
   discovered dependency requires new approval.

## 4. Snapshot and Edit Locally

Create a temporary directory with `mktemp -d` and copy each file to be edited into
it immediately before the edit. The snapshot is rollback state for this turn, not
a new manuscript version.

Apply small, uniquely located edits. Do not rewrite a section when one sentence is
approved. Do not normalize nearby whitespace, rewrap paragraphs, reorder macros,
sort bibliography entries, rename labels, or clean comments unless that operation
was selected.

Never run a formatter or broad replacement command. For a repeated change approved
globally, enumerate and gate every actual occurrence; do not assume all textual
matches are semantically equivalent.

## 5. Enforce the Approved Footprint

For each edited file, run `scripts/check_revision_scope.py` against its immediate
pre-edit snapshot. Supply minimal inclusive one-based ranges from the snapshot:

```bash
python3 <skill-dir>/scripts/check_revision_scope.py \
  <before.tex> <after.tex> \
  --allow 42:45 --allow 118:118
```

Read every reported hunk. Passing the script is necessary but not sufficient:
manually confirm that each changed hunk implements a selected request and no other
suggestion.

If the gate fails, restore this turn's snapshot and retry with a more precise edit.
Do not broaden `--allow` ranges after seeing the diff unless the user independently
approved the broader location.

## 6. Compile the Exact Revision

For a single self-contained TeX file, run:

```bash
bash <skill-dir>/../write-paper/scripts/compile_verify.sh <paper.tex>
```

For a multi-file or venue-specific project, use the existing project build command
from its project directory. The successful command must compile the current root
TeX and produce a fresh corresponding PDF with no fatal errors or unresolved
references/citations introduced by the selected edit.

Compilation repairs remain inside the approved footprint. If a missing package,
macro, label, bibliography entry, or included-file change outside that footprint
is required, roll back this turn and ask the user to approve that additional
location. Do not return an old PDF after a failed command.

After compilation, rerun the scope gate to ensure no tool or repair changed the
TeX outside approval.

## 7. Complete or Roll Back

Complete the turn only when the final scope gate passes and a fresh PDF exists.
Return the actual revised TeX and PDF files. Report:

- selected IDs or exact custom request applied;
- edited locations;
- scope-gate result;
- compile command/engine result;
- confirmation that unselected regions were unchanged.

Do not repeat the full suggestion list unless useful. Unselected suggestions stay
pending, not implicitly rejected or applied.

If the edit or compilation cannot finish within approved scope, restore the
immediate pre-edit snapshot, state that no revision was completed, and ask for the
smallest additional choice needed.

For another user-requested revision, restart at section 3 using the newly current
TeX. Each turn has a new snapshot, a new approved footprint, and a new TeX/PDF
delivery.
