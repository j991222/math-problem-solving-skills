# Paper Section Writer

Use this role only with an approved `CHUNK_PLAN.json`. Read the standing contract,
complete style guide, structure guide, brief, ledger, fixed preamble and label
registry, and every source unit assigned to the section in full.

## Goal

Write one section body, from `\section{...}\label{...}` through the section's final
proof or prose. Do not emit a preamble, `\begin{document}`, front matter,
bibliography, or `\end{document}`.

## Context

Receive:

- this section's assigned source units with complete statements and proofs;
- statements and paper labels for results established in earlier sections;
- verified external inputs and citation keys from the ledger;
- the exact fixed macros and theorem environments;
- the section purpose and interface from the chunk plan.

Do not re-prove another section's result. Reference its paper label. Do not rely on
a later section. If a forward dependency exists, stop and repair the plan rather
than writing a logically cyclic paper.

## Writing Rules

- Preserve every assigned source assertion, integrating local units into cohesive
  proofs when appropriate.
- Use only fixed macros. If a necessary macro is missing, record a blocker and
  amend the central preamble before stitching.
- Use only ledger-backed citation keys.
- Derive novel pivots; use mechanism plus outcome for routine local steps.
- Never expose source headings or filenames in the section body.
- Update `SOURCE_MAP.json` for each labeled result.

## Stitch Check

After all sections are written, stitch them in plan order and check:

- one preamble, author block, disclosure, acknowledgement, and bibliography;
- no duplicate labels or definitions;
- every reference points to an existing earlier result or section;
- macro definitions agree semantically, not merely by name;
- every source unit remains represented;
- no section carries standalone-paper residue such as its own title or abstract.
