#!/usr/bin/env python3
"""Convert a markdown proof blueprint into a standalone LaTeX document."""

from __future__ import annotations

import argparse
import datetime as _dt
import re
from pathlib import Path


HEADING_COMMANDS = {
    1: "section",
    2: "subsection",
    3: "subsubsection",
    4: "paragraph",
    5: "subparagraph",
    6: "subparagraph",
}

LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape_latex_text(value: str) -> str:
    return "".join(LATEX_SPECIALS.get(char, char) for char in value)


def convert_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    in_verbatim = False
    in_itemize = False
    in_enumerate = False

    def close_lists() -> None:
        nonlocal in_itemize, in_enumerate
        if in_itemize:
            output.append(r"\end{itemize}")
            in_itemize = False
        if in_enumerate:
            output.append(r"\end{enumerate}")
            in_enumerate = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            close_lists()
            if in_verbatim:
                output.append(r"\end{verbatim}")
                in_verbatim = False
            else:
                output.append(r"\begin{verbatim}")
                in_verbatim = True
            continue

        if in_verbatim:
            output.append(line)
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            close_lists()
            level = len(heading.group(1))
            command = HEADING_COMMANDS[level]
            text = escape_latex_text(heading.group(2).strip())
            output.append(rf"\{command}*{{{text}}}")
            continue

        bullet = re.match(r"^\s*[-*]\s+(.*)$", line)
        if bullet:
            if in_enumerate:
                output.append(r"\end{enumerate}")
                in_enumerate = False
            if not in_itemize:
                output.append(r"\begin{itemize}")
                in_itemize = True
            output.append(rf"\item {bullet.group(1)}")
            continue

        numbered = re.match(r"^\s*\d+[.)]\s+(.*)$", line)
        if numbered:
            if in_itemize:
                output.append(r"\end{itemize}")
                in_itemize = False
            if not in_enumerate:
                output.append(r"\begin{enumerate}")
                in_enumerate = True
            output.append(rf"\item {numbered.group(1)}")
            continue

        close_lists()

        if re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
            output.append(r"\medskip\hrule\medskip")
            continue

        output.append(line)

    if in_verbatim:
        output.append(r"\end{verbatim}")
    close_lists()
    return "\n".join(output).strip() + "\n"


def build_document(body: str, title: str) -> str:
    date = _dt.date.today().isoformat()
    escaped_title = escape_latex_text(title)
    return rf"""\documentclass[11pt]{{article}}
\usepackage[margin=1in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{amsmath,amssymb,amsthm}}
\usepackage{{hyperref}}
\title{{{escaped_title}}}
\date{{{date}}}

\begin{{document}}
\maketitle

{body}
\end{{document}}
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a markdown proof blueprint to standalone LaTeX.",
    )
    parser.add_argument("input", help="Path to blueprint markdown")
    parser.add_argument(
        "--output",
        "-o",
        help="Output .tex path. Defaults to input path with .tex suffix.",
    )
    parser.add_argument(
        "--title",
        help="Document title. Defaults to the input filename stem.",
    )
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve() if args.output else input_path.with_suffix(".tex")
    title = args.title or input_path.stem.replace("_", " ").replace("-", " ").title()

    markdown = input_path.read_text(encoding="utf-8")
    body = convert_markdown(markdown)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_document(body, title), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
