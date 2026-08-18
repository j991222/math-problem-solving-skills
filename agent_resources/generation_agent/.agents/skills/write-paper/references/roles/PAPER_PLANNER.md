# Paper Planner for Large Sources

Use this role only when a coherent single-pass write cannot fit. Read the standing
contract, style guide, structure guide, brief, ledger, and the statements and
dependency data of every selected-source unit.

## Goal

Produce the fixed paper skeleton without writing proofs:

- complete preamble;
- front matter;
- ordered section plan;
- one assignment of every source unit to a section;
- label registry;
- bibliography from the ledger.

## Planning Contract

Every source unit appears in exactly one section assignment. This assignment is a
coverage map, not a command to promote every unit to a named result. A section
writer may integrate local source units into a larger proof.

Order sections so every internal dependency points backward or stays within the
same section. Never partition by byte count, consecutive pages, or arbitrary equal
chunks. Partition by mathematical result, shared setup, and proof dependency.

## Output Artifact

Write `checks/CHUNK_PLAN.json`:

```json
{
  "tier": "note|mid|long",
  "sections": [
    {
      "title": "Introduction",
      "label": "sec:introduction",
      "source_units": [],
      "purpose": "context and headline statements"
    },
    {
      "title": "Main argument",
      "label": "sec:main",
      "source_units": ["exact source heading"],
      "purpose": "prove the headline theorem"
    }
  ],
  "labels": {"paper-label": "exact source heading"}
}
```

Labels must be unique. Every source unit must be assigned exactly once. Record
cross-section inputs explicitly. Do not put internal source headings in any LaTeX
block that will be shipped.

## Front Matter and Bibliography

Use only brief metadata. If author data is absent, use the required placeholder.
The abstract opens with the result, contains no citations, and avoids heavy
notation. Build bibliography items only from verified or operator-trusted ledger
rows; unresolved candidates remain blockers for section writers.

## Self-Check

- All source units assigned exactly once.
- Section labels unique.
- Dependencies point backward.
- The preamble declares every planned macro and theorem environment.
- The bibliography contains nothing invented.
- Operational source identifiers appear only in `CHUNK_PLAN.json` and
  `SOURCE_MAP.json`, never in visible paper text.
