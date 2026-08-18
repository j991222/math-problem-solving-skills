#!/usr/bin/env python3
"""Seed an unverified reference ledger from a mathematical Markdown source.

The source format does not have Danus's structured ``external_refs`` field, so
this helper deliberately extracts candidates rather than pretending to verify
metadata. It recognizes explicit LaTeX citation keys, arXiv identifiers, DOI
strings, URLs, and source-like lines. A human/agent must read the complete
source, add missed dependencies, and verify every candidate independently.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import OrderedDict
from pathlib import Path


CITE_RE = re.compile(r"\\cite(?:\s*\[[^\]]*\])?\s*\{([^}]+)\}")
ARXIV_RE = re.compile(
    r"(?:arXiv\s*:\s*|arxiv\.org/(?:abs|pdf)/)"
    r"([a-z-]+(?:\.[A-Z]{2})?/\d{7}|\d{4}\.\d{4,5})(?:v\d+)?",
    re.IGNORECASE,
)
DOI_RE = re.compile(r"(?:doi\s*:\s*|doi\.org/)(10\.\d{4,9}/[^\s<>\]\[{}]+)", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s<>\]\[{}()]+")
SOURCE_LINE_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:source|sources|reference|references|citation|citations|"
    r"published\s+as|see\s+also|external\s+result)\s*[:\-]",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")


def clean_token(value: str) -> str:
    return value.rstrip(".,;:)").strip()


def stable_candidate(text: str) -> str:
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
    return f"candidate-{digest}"


def add_candidate(
    rows: OrderedDict[str, dict],
    key: str,
    kind: str,
    value: str,
    heading: str,
    line_number: int,
    excerpt: str,
) -> None:
    row = rows.setdefault(
        key,
        {
            "key": key,
            "kind": kind,
            "value": value,
            "locations": [],
            "excerpts": [],
        },
    )
    location = f"line {line_number}"
    if heading:
        location += f" under {heading!r}"
    if location not in row["locations"]:
        row["locations"].append(location)
    excerpt = " ".join(excerpt.strip().split())
    if excerpt and excerpt not in row["excerpts"]:
        row["excerpts"].append(excerpt[:500])


def collect(text: str) -> OrderedDict[str, dict]:
    rows: OrderedDict[str, dict] = OrderedDict()
    heading = ""

    for line_number, line in enumerate(text.splitlines(), 1):
        heading_match = HEADING_RE.match(line)
        if heading_match:
            heading = heading_match.group(1).strip()

        for match in CITE_RE.finditer(line):
            for raw_key in match.group(1).split(","):
                key = clean_token(raw_key)
                if key:
                    add_candidate(rows, key, "latex-citation-key", key, heading, line_number, line)

        for match in ARXIV_RE.finditer(line):
            arxiv_id = clean_token(match.group(1))
            add_candidate(
                rows,
                f"arxiv:{arxiv_id.lower()}",
                "arxiv",
                arxiv_id,
                heading,
                line_number,
                line,
            )

        for match in DOI_RE.finditer(line):
            doi = clean_token(match.group(1))
            add_candidate(rows, f"doi:{doi.lower()}", "doi", doi, heading, line_number, line)

        for match in URL_RE.finditer(line):
            url = clean_token(match.group(0))
            if "arxiv.org/" in url.lower() or "doi.org/" in url.lower():
                continue
            add_candidate(rows, f"url:{url}", "url", url, heading, line_number, line)

        if SOURCE_LINE_RE.search(line):
            normalized = " ".join(line.strip().split())
            key = stable_candidate(normalized)
            add_candidate(rows, key, "source-line", normalized, heading, line_number, line)

    return rows


def render(rows: OrderedDict[str, dict]) -> str:
    lines = [
        "# REFERENCE_LEDGER",
        "",
        "Seeded from explicit reference signals in the selected mathematical source. These",
        "rows are candidates, not verified bibliography. Read the complete source",
        "for missed dependencies and verify every active row independently.",
        "",
    ]
    if not rows:
        lines.extend(["_(no explicit reference candidates detected)_", ""])
        return "\n".join(lines)

    for key, row in rows.items():
        lines.append(f"## {key}")
        lines.append("- authors:")
        lines.append("- title:")
        lines.append("- venue:")
        lines.append("- year:")
        lines.append(f"- arxiv: {row['value'] if row['kind'] == 'arxiv' else ''}")
        lines.append(f"- doi: {row['value'] if row['kind'] == 'doi' else ''}")
        lines.append(f"- source_url: {row['value'] if row['kind'] == 'url' else ''}")
        lines.append("- cited_for:")
        lines.append(f"- source_location: {'; '.join(row['locations'])}")
        lines.append(f"- extracted_as: {row['kind']}")
        lines.append("- verified-by: unverified")
        lines.append("- status: active")
        if row["excerpts"]:
            lines.append(f"- notes: {' | '.join(row['excerpts'])}")
        else:
            lines.append("- notes:")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Seed unverified reference candidates from a mathematical Markdown source."
    )
    parser.add_argument(
        "source",
        help="path to blueprint.md, blueprint_verified.md, or best_available_artifacts.md",
    )
    parser.add_argument("--out", required=True, help="ledger output path")
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing output (normally seed to a temporary path and merge)",
    )
    args = parser.parse_args(argv)

    source = Path(args.source)
    output = Path(args.out)
    if not source.is_file():
        sys.stderr.write(f"seed_reference_ledger: source not found: {source}\n")
        return 2
    if output.exists() and not args.force:
        sys.stderr.write(
            f"seed_reference_ledger: output exists: {output}; use a temporary path "
            "and merge, or pass --force explicitly\n"
        )
        return 3

    text = source.read_text(encoding="utf-8")
    rows = collect(text)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(rows), encoding="utf-8")
    print(f"wrote {output} ({len(rows)} candidate(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
