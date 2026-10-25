#!/usr/bin/env python3
"""Report missing or misformatted path tokens in AGENTS.md/CLAUDE.md files.

Usage: check-paths.py <repository-root>
Bare filename -> instruction file's directory, else repository root. Path with "/" -> repository root.
Checked: tokens whose last segment has known extension (backticked or not); extensionless "/" tokens whose
first segment is existing directory. Skipped: fenced blocks, spans with spaces (commands), globs/placeholders,
URLs, routes, options, package names, AGENTS/CLAUDE.md alternations, unquoted Node.js-style names.
Format reports: Markdown links, "./"/"../", absolute paths, "\" separators, full path to same-directory file.
Heuristic -> judge reports in context. Exit 0 = clean, 1 = reports, 2 = usage error.
"""
import os
import re
import sys

NAMES = {"AGENTS.md", "CLAUDE.md"}
SKIP_DIRS = {".git", "node_modules", ".init-project"}
EXTENSIONS = set(
    "c cc cfg cjs conf cpp cs css cts csv env go gradle h hpp html ini java js json jsonc jsx kt lock md mdx "
    "mjs mts php prisma proto py rb rs scss sh sql svelte swift toml ts tsx txt vue xml yaml yml".split()
)
CODE_SPAN = re.compile(r"`([^`]+)`")
BARE_TOKEN = re.compile(r"[\w.\-/:\[\]\\]+")
MD_LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")
LINE_SUFFIX = re.compile(r":\d+(-\d+)?$")
INSTRUCTION_ALTERNATION = re.compile(r"(AGENTS|CLAUDE)(\.md)?/(AGENTS|CLAUDE)\.md")
TOOL_NAME = re.compile(r"[A-Z]\w*\.js")  # Node.js, Next.js


def has_extension(name):
    stem, dot, ext = name.rpartition(".")
    return bool(stem) and dot == "." and ext.lower() in EXTENSIONS


def same(a, b):
    return os.path.normcase(os.path.normpath(a)) == os.path.normcase(os.path.normpath(b))


def resolve(token, base, root):
    if "/" not in token:
        found = os.path.exists(os.path.join(base, token)) or os.path.exists(os.path.join(root, token))
        return None if found else "missing"
    path = os.path.join(root, token)
    if os.path.exists(path):
        return "use bare filename" if os.path.isfile(path) and same(os.path.dirname(path), base) else None
    if os.path.exists(os.path.join(base, token)):
        return "nested-relative; use repo-relative"
    return "missing"


def problem(token, quoted, base, root):
    token = LINE_SUFFIX.sub("", token.strip().rstrip(".,;:)").lstrip("("))
    if not token or "://" in token or token[0] in "-@$#" or any(c in token for c in " *?<>{}$|="):
        return None, token
    pathlike = has_extension(re.split(r"[\\/]", token.rstrip("/\\"))[-1])
    if re.match(r"[A-Za-z]:[\\/]", token) or (token[0] in "/~" and pathlike):
        return "absolute path; use repo-relative", token
    if "\\" in token:
        return ("use /" if pathlike else None), token
    if token.startswith(("./", "../")):
        return "relative prefix; use bare or repo-relative", token
    if INSTRUCTION_ALTERNATION.fullmatch(token) or token[0] in "/~":
        return None, token
    if not quoted and "/" not in token and TOOL_NAME.fullmatch(token):
        return None, token
    if not pathlike:
        first = token.split("/", 1)[0]
        if "/" not in token or not any(os.path.isdir(os.path.join(d, first)) for d in (root, base)):
            return None, token  # prose slash list, e.g. read/write
    return resolve(token, base, root), token


def tokens(line):
    for span in CODE_SPAN.findall(line):
        yield span, True
    for bare in BARE_TOKEN.findall(CODE_SPAN.sub(" ", line)):
        yield bare, False


def check_file(path, root):
    reports = []
    base = os.path.dirname(path)
    fenced = False
    with open(path, encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if line.lstrip().startswith(("```", "~~~")):
                fenced = not fenced
                continue
            if fenced:
                continue
            for target in MD_LINK.findall(CODE_SPAN.sub(" ", line)):
                if "://" not in target:
                    reports.append((number, "Markdown link; use plain path", target))
            seen = set()
            for raw, quoted in tokens(line):
                message, token = problem(raw, quoted, base, root)
                if message and (message, token) not in seen:
                    seen.add((message, token))
                    reports.append((number, message, token))
    return reports


def main(argv):
    if len(argv) != 2 or not os.path.isdir(argv[1]):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    root = os.path.abspath(argv[1])
    missing = formatting = files = 0
    for directory, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(NAMES.intersection(names)):
            path = os.path.join(directory, name)
            files += 1
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            for number, message, token in check_file(path, root):
                if message == "missing":
                    missing += 1
                else:
                    formatting += 1
                print(f"{rel}:{number}: {message}: {token}")
    print(f"{files} instruction files, {missing} missing, {formatting} format")
    return 1 if missing or formatting else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
