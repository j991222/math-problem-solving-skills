#!/usr/bin/env python3
"""Reject TeX changes outside explicitly approved before-file line ranges."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, order=True)
class LineRange:
    start: int
    end: int

    def contains_line(self, line: int) -> bool:
        return self.start <= line <= self.end

    def contains_insertion(self, anchor: int) -> bool:
        # anchor 0 is before line 1; anchor N is after before-file line N.
        return self.start - 1 <= anchor <= self.end


def parse_range(value: str) -> LineRange:
    try:
        if ":" in value:
            start_text, end_text = value.split(":", 1)
            start, end = int(start_text), int(end_text)
        else:
            start = end = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid range {value!r}; use N or START:END"
        ) from exc
    if start < 1 or end < start:
        raise argparse.ArgumentTypeError(
            f"invalid range {value!r}; require 1 <= START <= END"
        )
    return LineRange(start, end)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def changed_opcodes(before: list[str], after: list[str]) -> list[tuple[str, int, int, int, int]]:
    matcher = difflib.SequenceMatcher(a=before, b=after, autojunk=False)
    return [opcode for opcode in matcher.get_opcodes() if opcode[0] != "equal"]


def opcode_allowed(
    opcode: tuple[str, int, int, int, int], allowed: list[LineRange]
) -> bool:
    _, before_start, before_end, _, _ = opcode
    if before_start == before_end:
        return any(item.contains_insertion(before_start) for item in allowed)
    affected_lines = range(before_start + 1, before_end + 1)
    return all(any(item.contains_line(line) for item in allowed) for line in affected_lines)


def describe(opcode: tuple[str, int, int, int, int]) -> str:
    tag, before_start, before_end, after_start, after_end = opcode
    if before_start == before_end:
        before_location = f"insertion after before line {before_start}"
    else:
        before_location = f"before lines {before_start + 1}:{before_end}"
    return f"{tag}: {before_location} -> after lines {after_start + 1}:{after_end}"


def check_scope(
    before: list[str], after: list[str], allowed: list[LineRange]
) -> tuple[list[str], list[str]]:
    changes = changed_opcodes(before, after)
    violations = [describe(opcode) for opcode in changes if not opcode_allowed(opcode, allowed)]
    return [describe(opcode) for opcode in changes], violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check that a revised file changed only approved before-file lines."
    )
    parser.add_argument("before", help="immediate pre-edit TeX snapshot")
    parser.add_argument("after", help="revised TeX file")
    parser.add_argument(
        "--allow",
        action="append",
        required=True,
        type=parse_range,
        metavar="START:END",
        help="approved inclusive line range in the before file; repeat as needed",
    )
    parser.add_argument(
        "--allow-no-change",
        action="store_true",
        help="return success when the files are identical",
    )
    args = parser.parse_args(argv)

    before_path = Path(args.before)
    after_path = Path(args.after)
    for label, path in (("before", before_path), ("after", after_path)):
        if not path.is_file():
            parser.error(f"{label} file not found: {path}")

    before_bytes = before_path.read_bytes()
    after_bytes = after_path.read_bytes()
    before = before_bytes.decode("utf-8").splitlines(keepends=True)
    after = after_bytes.decode("utf-8").splitlines(keepends=True)

    for item in args.allow:
        if item.end > len(before):
            parser.error(
                f"allowed range {item.start}:{item.end} exceeds before file "
                f"length {len(before)}"
            )

    changes, violations = check_scope(before, after, args.allow)
    if not changes and not args.allow_no_change:
        print("SCOPE FAILED: no TeX change detected", file=sys.stderr)
        return 1

    print(f"before_sha256={digest(before_bytes)}")
    print(f"after_sha256={digest(after_bytes)}")
    for change in changes:
        print(f"CHANGE {change}")

    if violations:
        for violation in violations:
            print(f"UNAPPROVED {violation}", file=sys.stderr)
        print(
            f"SCOPE FAILED: {len(violations)} change hunk(s) exceed approved ranges",
            file=sys.stderr,
        )
        return 1

    print(f"SCOPE OK: {len(changes)} change hunk(s) within approved ranges")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
