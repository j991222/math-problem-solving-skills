# Acknowledgement Boilerplate

Acknowledgement content is operator-configurable. Automated-assistance disclosure
is on by default; funding and personal thanks are opt-in. Every name, affiliation,
grant number, and factual claim must come from the operator or a verified run
record.

## Automated-Assistance Disclosure

Unless the operator disables it, include a plain disclosure such as:

```text
This paper was prepared with the assistance of an automated mathematical
proof-generation and writing system.
```

Use a more specific system name only when the operator supplies the public name.
Do not claim that the final manuscript was independently verified unless a
clean-context verifier actually checked `main.tex` as written. When that happened,
the operator may supply a truthful verification sentence. Do not infer one from the
selected source's filename or upstream status.

The neutral default is one visible sentence in `\section*{Acknowledgements}`.
The operator may instead request a final abstract sentence or a nearby Remark. Use
one consistent placement unless the brief explicitly requests multiple visible
placements.

Do not create a bibliography entry for the system unless a real, independently
verified publication is supplied.

## Funding

Include funding only when the operator gives the exact text. Never invent a grant
number or agency. Otherwise omit the funding sentence; do not leave an empty
placeholder in a final manuscript.

## Personal Thanks

Include personal thanks only when the operator gives the exact text. Never infer
names from repository history, correspondence, citations, or source paths.

## Unresolved Configuration

If acknowledgement content is required but unresolved, use
`\note{[ack/blocker] <missing decision>}` and report the draft as blocked. Never
fill a placeholder by guessing.
