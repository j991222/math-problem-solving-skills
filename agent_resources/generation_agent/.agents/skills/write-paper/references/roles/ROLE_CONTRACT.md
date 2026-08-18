# Standing Contract for Every Paper Role

Read this contract before the role-specific instructions. A role-specific prompt
may add constraints; it never relaxes these.

## Prime Directive

If any item below cannot be satisfied, leave a visible
`\note{[prime/blocker] <reason>}` in the draft and record it in the revision log.
Never hide or smooth over a violation.

1. **Preserve every mathematical assertion and its status in the selected source.** Preserve all
   hypotheses, definitions, intermediate steps, sublemmas, calculations, case
   divisions, and conclusions. The prose may be reorganized and rewritten, but
   style work does not authorize content compression or promotion of an
   unverified/failed claim to an established result. The abstract is the one
   reader-facing summary and may paraphrase.

2. **Preserve every citation and cite every referenced result properly.** Never
   replace a citation with "well-known", "standard", "by a classical result", an
   author name without a key, or a theorem name without a key. If a citation
   cannot be resolved, preserve its source description and use
   `\note{[cite/blocker] ...}`.

3. **Fabricate no bibliography.** Never invent authors, titles, venues, years,
   pagination, arXiv identifiers, DOIs, or URLs. Unverified metadata stays absent
   and flagged.

4. **Preserve the LaTeX preamble during revision.** Use `amsart` by default, while
   honoring a venue class specified in the brief. Preserve every package, option,
   macro, theorem declaration, operator, and color already used. A missing package
   may be added; an existing one may not be silently dropped.

5. **Keep editorial macros active and neutral.** Define `\edit{}`, `\note{}`, and
   `\todo{}` in the preamble. Never delete them, turn them into no-ops, or invent
   person-named editorial macros.

6. **Leak no pipeline metadata.** Do not expose source filenames, source-map keys,
   run paths, agent or role names, long hashes, internal statuses, or development
   metadata in the title, abstract, body, author block, acknowledgements, or
   bibliography. Configured, truthful automated-assistance disclosure and the
   plain-language unverified-draft warning required for a best-available source
   are the only intended exceptions.

## Hard Constraints

- The voice source is `style/STYLE_GUIDE.md`; the structure source is
  `style/PAPER_STRUCTURE.md`. Do not import prose style from unrelated files.
- Every paper has an `\author{}` block. Preserve supplied authors verbatim. If no
  author is supplied, use `\author{Author}` and add
  `\note{[author/blocker] no author supplied}`. Never infer a person, affiliation,
  or email.
- Do not publish, submit, upload, push, or run repository-changing git commands as
  part of a paper role.
- A manuscript that has not passed `scripts/compile_verify.sh` is not compiled.
- A manuscript with unverified citations is not reference-checked.
- A manuscript has not been independently verified unless a clean-context verifier
  checked the final paper artifact as written.
- A manuscript produced from `unverified-best-available` is always a draft and
  must retain its visible warning and known gaps even when it compiles.
- State only checks actually observed. "Should compile" and "based on a verified
  blueprint" are not gate results.

## Compliance Check

Before declaring a role complete, re-read the six Prime Directive items and scan
the output once for each. Fix the issue or leave a precise blocker. Never silently
claim compliance.
