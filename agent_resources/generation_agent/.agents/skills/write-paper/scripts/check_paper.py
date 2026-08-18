#!/usr/bin/env python3
"""Run deterministic static checks on a generated mathematics paper."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE = re.compile(r"\\(?:ref|eqref)\{([^}]+)\}")
CITE_RE = re.compile(r"\\cite(?:\s*\[[^\]]*\])?\s*\{([^}]+)\}")
BIB_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}")
BLOCKER_RE = re.compile(r"\\note\s*\{\s*\[[^\]]*blocker[^\]]*\]", re.IGNORECASE)


def keys(matches: list[str]) -> list[str]:
    out: list[str] = []
    for match in matches:
        out.extend(key.strip() for key in match.split(",") if key.strip())
    return out


def abstract_body(tex: str) -> str:
    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.DOTALL)
    return match.group(1) if match else ""


def without_latex_comments(tex: str) -> str:
    visible_lines: list[str] = []
    for line in tex.splitlines():
        for index, character in enumerate(line):
            if character != "%":
                continue
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                line = line[:index]
                break
        visible_lines.append(line)
    return "\n".join(visible_lines)


def check(tex: str, source: Path | None, strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    visible_tex = without_latex_comments(tex)

    stripped = tex.lstrip()
    if not stripped.startswith("\\documentclass"):
        errors.append("manuscript does not begin with \\documentclass")
    for required in (
        "\\begin{document}",
        "\\end{document}",
        "\\title{",
        "\\author{",
        "\\begin{abstract}",
        "\\end{abstract}",
        "\\maketitle",
        "\\subjclass[2020]{",
        "\\keywords{",
        "\\date{",
    ):
        if required not in tex:
            errors.append(f"missing required LaTeX element: {required}")

    for macro in ("edit", "note", "todo"):
        pattern = re.compile(rf"\\(?:re)?newcommand\s*\{{\\{macro}\}}")
        if not pattern.search(tex):
            errors.append(f"editorial macro \\{macro} is not actively defined")

    labels = LABEL_RE.findall(tex)
    label_counts = Counter(labels)
    for label, count in sorted(label_counts.items()):
        if count > 1:
            errors.append(f"duplicate label {label!r} appears {count} times")

    known_labels = set(labels)
    for label in sorted(set(REF_RE.findall(tex)) - known_labels):
        errors.append(f"reference points to missing label {label!r}")

    cite_keys = keys(CITE_RE.findall(tex))
    bib_keys = BIB_RE.findall(tex)
    bib_counts = Counter(bib_keys)
    for key, count in sorted(bib_counts.items()):
        if count > 1:
            errors.append(f"duplicate bibliography key {key!r} appears {count} times")
    for key in sorted(set(cite_keys) - set(bib_keys)):
        errors.append(f"citation key {key!r} has no matching \\bibitem")
    for key in sorted(set(bib_keys) - set(cite_keys)):
        warnings.append(f"bibliography item {key!r} is never cited")

    abstract = abstract_body(tex)
    if abstract and CITE_RE.search(abstract):
        errors.append("abstract contains a citation")

    blockers = BLOCKER_RE.findall(tex)
    if blockers:
        message = f"manuscript contains {len(blockers)} visible blocker note(s)"
        (errors if strict else warnings).append(message)

    if re.search(r"^\s*```", tex, re.MULTILINE):
        errors.append("manuscript contains a Markdown code fence")
    if re.search(r"^\s*#{1,6}\s+", tex, re.MULTILINE):
        errors.append("manuscript contains a raw Markdown heading")

    leak_patterns = {
        "blueprint filename": r"\bblueprint(?:_verified)?\.md\b",
        "source-map marker": r"\bSOURCE_MAP(?:\.json)?\b",
        "run status": (
            r"\b(?:verified-blueprint|unverified-blueprint|"
            r"unverified-best-available|candidate_ready)\b"
        ),
        "absolute workspace path": r"/(?:AI4M|home|root|Users)/[^\s{}]+",
        "long hexadecimal identifier": r"\b[0-9a-fA-F]{24,}\b",
    }
    if source is not None:
        leak_patterns["selected source filename"] = re.escape(source.name)
    for name, pattern in leak_patterns.items():
        if re.search(pattern, visible_tex):
            errors.append(f"visible pipeline metadata detected: {name}")

    if source is not None and source.name == "best_available_artifacts.md":
        after_title = visible_tex.split("\\maketitle", 1)[-1]
        normalized = re.sub(r"\s+", " ", after_title).lower()
        for phrase in (
            "unverified draft",
            "may contain gaps or errors",
            "does not establish the original problem",
        ):
            if phrase not in normalized:
                errors.append(
                    "best-available manuscript is missing required visible warning: "
                    f"{phrase!r}"
                )

    if "—" in tex:
        warnings.append("house style forbids em dashes")
    for command in ("\\cref", "\\Cref", "\\autoref"):
        if command in tex:
            warnings.append(f"house style prefers typed manual references over {command}")
    if "\\bibliography{" in tex or "\\bibliographystyle{" in tex:
        warnings.append("house style uses a manual thebibliography by default")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Static consistency checks for main.tex")
    parser.add_argument("tex", help="path to main.tex")
    parser.add_argument("--source", help="selected Markdown source path, used for leak checks")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat visible blocker notes as errors for the publishable gate",
    )
    args = parser.parse_args(argv)

    tex_path = Path(args.tex)
    if not tex_path.is_file():
        sys.stderr.write(f"check_paper: manuscript not found: {tex_path}\n")
        return 2
    source = Path(args.source) if args.source else None
    if source is not None and not source.is_file():
        sys.stderr.write(f"check_paper: source Markdown file not found: {source}\n")
        return 2

    errors, warnings = check(tex_path.read_text(encoding="utf-8"), source, args.strict)
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")
    print(f"SUMMARY: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
