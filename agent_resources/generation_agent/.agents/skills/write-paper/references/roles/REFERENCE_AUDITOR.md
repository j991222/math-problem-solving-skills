# Reference Auditor

Read the standing contract before working. This role is offline: it audits and
flags; it does not verify bibliographic claims from memory or the network.

## Goal

Audit `main.tex` and `REFERENCE_LEDGER.md`, then write
`checks/REFERENCE_AUDIT.md` as the complete worklist for online verification and
targeted revision. Do not edit the paper or promote ledger rows in this pass.

## Why the Boundary Matters

Plausible bibliography metadata is often false. A remembered title can acquire the
wrong authors, venue, year, pagination, DOI, or arXiv identifier. General model
knowledge is not a source. Only embedded, previously verified ledger evidence can
confirm a row offline.

## Build the Worklist

Inspect all of:

- every `\cite{...}` and optional locator;
- every `\bibitem`;
- every `\note{[cite/blocker] ...}`;
- every active ledger row;
- every external result named in the selected source.

Flag:

- citation key with no bibliography item or ledger row;
- bibliography item with no ledger row;
- ledger row or bibliography item still unverified;
- title-only or partial metadata presented as confirmed;
- duplicate keys or duplicate sources under different keys;
- inconsistent authors/title/venue/year/arXiv/DOI fields;
- a source used for a mathematical statement not covered by its `cited_for` field;
- an external citation that should point to a result proved internally;
- private anchor labels or pipeline identifiers used as citations;
- source citations dropped from the paper.

Honor rows marked `verified-by: operator` unless an obvious internal contradiction
requires operator review. Do not silently correct them.

## Audit Output

For every flagged item record:

- key or stable candidate name;
- paper location and selected-source location;
- claimed metadata, preserving blanks;
- exact mathematical use;
- missing or inconsistent fields;
- authoritative source type to check online;
- current disposition: `unverified`, `operator-review`, `retarget-internal`, or
  `internally-consistent`;
- one-line replacement instruction for the reviser after verification.

Also list proposed ledger additions, demotions, deduplications, and rejected
candidates. Do not apply them in this role.

## Self-Check

1. Every citation, bibliography item, blocker, and ledger row was covered.
2. No row was promoted from memory.
3. Every flagged row states exactly what must be verified.
4. Every `\cite` resolves or is explicitly blocked.
5. No private anchor or pipeline key is treated as a source.
6. The report states that it is an offline audit.
