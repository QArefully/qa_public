#!/usr/bin/env python3
"""Report instruction-file shape problems in AGENTS.md/CLAUDE.md files. Report only; never edits files.

Usage: check-shape.py <repo-root> [<instruction-file>...]
Files + path tokens: same discovery/recognition as check-paths.py (sibling script; `path#symbol` -> path part).
Rules (bullet = "-", "*", "+", "1." or "1)" line; arrow = "->", "=>" or U+2192 outside code spans; fenced
blocks skipped):
  FAIL packed-trigger: bullet text before first arrow cites >=2 distinct paths -> parent bullet + one sub-bullet
  per file.
  WARN packed-trigger-maybe: bullet with arrow cites >=2 distinct paths in total, FAIL rule not matched.
  Nested file only (not repository root), first non-empty non-heading line = orientation line unless it is a
  bullet (first content bullet -> no orientation line, no orientation rules):
  FAIL orientation-repeat: orientation path also cited on another line of same file.
  WARN orientation-conventional: orientation path stem is main, index, config or App (case-insensitive).
  WARN orientation-shim: orientation path is file with <=5 non-blank lines -> point at delegate or omit.
  Missing entry pointer never reported.
Output: <rel>:<line>: FAIL|WARN: <rule>: <detail>. Last line: <n> files, <x> fail, <y> warn.
Exit 0 no FAIL (WARN alone passes), 1 FAIL present, 2 usage/input error (encoding/NUL rules as check-paths.py).
"""
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True  # before any by-path load: no __pycache__ beside installed skill (-I ignores env)

_spec = importlib.util.spec_from_file_location("check_paths", os.path.join(os.path.dirname(__file__), "check-paths.py"))
paths = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(paths)

BULLET = re.compile(r"\s*(?:[-*+]|\d+[.)])\s+")
HEADING = re.compile(r"\s{0,3}#{1,6}(\s|$)")
ARROWS = ("->", "=>", "→")
CONVENTIONAL = {"main", "index", "config", "app"}
SHIM_LINES = 5


def refs(text, base, root):
    """-> {resolved key: path as written} for path references in text."""
    found = {}
    for raw, quoted in paths.tokens(text):
        token, _ = paths.examine(raw, quoted, base, root)
        if token:
            found.setdefault(os.path.normcase(os.path.normpath(paths.locate(token, base, root))), token)
    return found


def arrow(line):
    """-> index of first arrow ("->", "=>", U+2192) outside code spans, or -1."""
    masked = paths.CODE_SPAN.sub(lambda m: "`" + "x" * len(m.group(1)) + "`", line)
    found = [i for i in (masked.find(a) for a in ARROWS) if i >= 0]
    return min(found) if found else -1


def nonblank_lines(path):
    """-> non-blank line count of cited file; binary/unreadable -> None (shim rule skipped)."""
    try:
        text = paths.common.read_text(path)
    except paths.InputError:
        return None
    return sum(1 for line in paths.common.split_lines(text) if line.strip())


def check_file(path, root):
    reports = []
    base = os.path.dirname(path)
    lines = paths.read_lines(path, paths.rel(path, root))
    for number, line in lines:
        cut = arrow(line)
        if not BULLET.match(line) or cut < 0:
            continue
        before, total = refs(line[:cut], base, root), refs(line, base, root)
        if len(before) >= 2:
            reports.append((number, "FAIL", "packed-trigger", f"{len(before)} paths before ->: {', '.join(before.values())}"))
        elif len(total) >= 2:
            reports.append((number, "WARN", "packed-trigger-maybe", f"{len(total)} paths: {', '.join(total.values())}"))
    nested = not paths.same(base, root)
    first = next(((n, l) for n, l in lines if l.strip() and not HEADING.match(l)), None)
    if first and BULLET.match(first[1]):
        first = None  # content starts with bullet -> no orientation line
    if nested and first:
        number, line = first
        elsewhere = {}
        for other, text in lines:
            if other != number:
                for key in refs(text, base, root):
                    elsewhere.setdefault(key, other)
        for key, token in refs(line, base, root).items():
            if key in elsewhere:
                reports.append((number, "FAIL", "orientation-repeat", f"{token} also cited at line {elsewhere[key]}"))
            name = re.split(r"[\\/]", token.rstrip("/\\"))[-1]
            if name.split(".", 1)[0].lower() in CONVENTIONAL:
                reports.append((number, "WARN", "orientation-conventional", f"{token} is conventional entry name; omit"))
            count = nonblank_lines(key) if paths.fisfile(key) else None
            if count is not None and count <= SHIM_LINES:
                reports.append((number, "WARN", "orientation-shim", f"{token} has <={SHIM_LINES} non-blank lines; point at delegate or omit"))
    return sorted(reports, key=lambda r: r[0])


def run(argv):
    args = paths.parse(argv, __doc__)
    counts = {"FAIL": 0, "WARN": 0}
    for path in args.paths:
        for number, level, rule, detail in check_file(path, args.root):
            counts[level] += 1
            print(f"{paths.rel(path, args.root)}:{number}: {level}: {rule}: {detail}")
    print(f"{len(args.paths)} files, {counts['FAIL']} fail, {counts['WARN']} warn")
    return 1 if counts["FAIL"] else 0


def main(argv):
    return paths.common.guarded_main(run, argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
