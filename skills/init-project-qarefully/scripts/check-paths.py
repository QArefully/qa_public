#!/usr/bin/env python3
"""Report missing or misformatted path tokens in AGENTS.md/CLAUDE.md files. Report only; never edits files.

Usage: check-paths.py <repo-root> [--allow-external <abs-prefix>]... [<instruction-file>...]
Files: none -> walk every AGENTS.md/CLAUDE.md under root (skips .git, node_modules, .init-project); given ->
check only those (absolute or repo-relative). --allow-external -> absolute paths under prefix accepted
(user/host-approved location); repeatable.
Resolution: bare filename -> instruction file's directory, else repository root. Path with "/" -> repository root.
`path#symbol`, `path:line[-end]`, `path:ident`, pytest `path::node` -> path part checked; suffix never checked.
Checked: tokens whose last segment has known extension or is env-like (.env, .env.local; backticked or not);
backticked extensionless "/" tokens whose first segment is existing directory; unbackticked extensionless tokens
only when ending "/". Skipped as ambiguous: fenced blocks, spans with spaces (commands), globs/placeholders, URLs,
host:port, domains, web routes, options, package names, AGENTS/CLAUDE.md alternations, tool names not found
(Node.js, `Next.js`), code objects (process.env), calls (res.json()), unbackticked bare filenames not found,
unbackticked extensionless slash prose (client/server), missing env files other than templates (.env.example),
markdown links to #anchor or mailto:.
Output: <rel>:<line>: missing: not-found: <token> | <rel>:<line>: format: <detail>: <token>
  details: markdown-link, relative-prefix (./ ../), absolute, backslash (use /), same-dir-full-path (use bare
  filename), nested-relative (relative to instruction directory; use repo-relative).
Text: BOM -> utf-8/utf-16 LE|BE decoded; NUL bytes without BOM -> exit 2 naming file; split on "\\n" only.
Root + file args resolved through symlinks/junctions before outside-root check. Output UTF-8.
Last line: <n> files, <m> missing, <f> format. Exit 0 clean, 1 reports, 2 usage/input error (unreadable dir/file,
unexpected error -> one stderr line).
"""
import argparse
import importlib.util
import os
import re
import sys

sys.dont_write_bytecode = True  # before any by-path load: no __pycache__ beside installed skill (-I ignores env)


def _load_common():
    """Shared helpers module, loaded by file path once (sys.modules "iq_common")."""
    if "iq_common" not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            "iq_common", os.path.join(os.path.dirname(os.path.abspath(__file__)), "common.py"))
        module = importlib.util.module_from_spec(spec)
        sys.modules["iq_common"] = module
        spec.loader.exec_module(module)
    return sys.modules["iq_common"]


common = _load_common()
InputError = common.InputError

NAMES = {"AGENTS.md", "CLAUDE.md"}
SKIP_DIRS = {".git", "node_modules", ".init-project"}
EXTENSIONS = set(
    "adoc astro bash bat bazel bzl c cc cfg cjs clj cljs cmake cmd conf cpp cs csproj css cts csv cue dart "
    "dockerfile ejs env erl ex exs fish fs fsproj fsx gemspec go gql gradle graphql groovy h hbs hcl hpp hs html "
    "ini ipynb j2 java jinja jl js json json5 jsonc jsx kt kts less lock lockb lua md mdx mjs mk ml mod mts nix "
    "php pl pm prisma proto props ps1 psm1 pug py pyi pyx r rake rb rego rs rst sass sbt scala scss sh sln sol "
    "sql sum svelte svg swift tex tf tfvars tmpl toml tpl ts tsv tsx txt vb vim vue xaml xml xsd yaml yml zig "
    "zsh".split()
)
ENV_LIKE = re.compile(r"\.env(\.[\w-]+)?", re.I)  # .env, .env.local, .env.example
ENV_TEMPLATES = {"example", "sample", "template", "dist", "defaults"}  # committed -> missing reported
CODE_SPAN = re.compile(r"`([^`]+)`")
BARE_TOKEN = re.compile(r"[\w.\-/:\[\]\\#~]+")
MD_LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")
LINE_SUFFIX = re.compile(r":\d+(-\d+)?$")
SYMBOL_SUFFIX = re.compile(r":[A-Za-z_][\w$]*$")  # path:ident
HOST_PORT = re.compile(r"[\w.-]+:\d+(/|$)")  # localhost:3000/api
INSTRUCTION_ALTERNATION = re.compile(r"(AGENTS|CLAUDE)(\.md)?/(AGENTS|CLAUDE)\.md")
TOOL_NAME = re.compile(r"[A-Z]\w*\.js")  # Node.js, Next.js
CODE_OBJECT = re.compile(r"(process|import\.meta)\.env")
DOMAIN = re.compile(r"[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
DRIVE = re.compile(r"[A-Za-z]:[\\/]")
HOST_ROOTS = {"Users", "Volumes", "etc", "home", "mnt", "opt", "private", "root", "srv", "tmp", "usr", "var"}
FENCE = re.compile(r"\s*(`{3,}|~{3,})")


def fexists(path):
    return os.path.exists(common.fs(path))  # extended-length: paths >260 chars on Windows


def fisfile(path):
    return os.path.isfile(common.fs(path))


def fisdir(path):
    return os.path.isdir(common.fs(path))


def realpath(path):
    """-> real absolute path, extended-length safe, returned without extended-length prefix (relpath against plain root)."""
    return common.unfs(os.path.realpath(common.fs(os.path.abspath(path))))


def has_extension(name):
    stem, dot, ext = name.rpartition(".")
    return bool(ENV_LIKE.fullmatch(name)) or (bool(stem) and dot == "." and ext.lower() in EXTENSIONS)


def untemplated_env(token):
    """Env-like file other than committed template (.env, .env.local): often Git-ignored -> missing ambiguous."""
    name = re.split(r"[\\/]", token)[-1]
    return bool(ENV_LIKE.fullmatch(name)) and name.rpartition(".")[2].lower() not in ENV_TEMPLATES


def same(a, b):
    return os.path.normcase(os.path.normpath(a)) == os.path.normcase(os.path.normpath(b))


def norm_abs(path):
    return os.path.normcase(os.path.normpath(os.path.expanduser(path))).replace("\\", "/").rstrip("/")


def looks_absolute(path):
    return bool(DRIVE.match(path)) or path.startswith(("/", "\\", "~"))


def allowed_external(token, allow):
    token = norm_abs(token)
    return any(token == prefix or token.startswith(prefix + "/") for prefix in allow)


def is_absolute(token, pathlike, root):
    if DRIVE.match(token) or token.startswith("\\\\"):
        return True
    if not pathlike or token[0] not in "/~":
        return False
    if token[0] == "~":
        return True
    first = token.lstrip("/").split("/", 1)[0]  # leading "/" -> absolute only when not plausibly web route
    return first in HOST_ROOTS or fexists(token) or fexists(os.path.join(root, token.lstrip("/")))


def locate(path, base, root):
    """Filesystem path a reference points at (existing candidate preferred)."""
    if looks_absolute(path):
        return os.path.expanduser(path)
    if "/" not in path:
        local = os.path.join(base, path)
        return local if fexists(local) else os.path.join(root, path)
    full, local = os.path.join(root, path), os.path.join(base, path)
    return local if not fexists(full) and fexists(local) else full


def resolve(token, base, root):
    if "/" not in token:
        found = fexists(os.path.join(base, token)) or fexists(os.path.join(root, token))
        return None if found else ("missing", "not-found")
    path = os.path.join(root, token)
    if fexists(path):
        return ("format", "same-dir-full-path") if fisfile(path) and same(os.path.dirname(path), base) else None
    if fexists(os.path.join(base, token)):
        return "format", "nested-relative"
    return "missing", "not-found"


def clean(raw):
    token = raw.strip().rstrip(".,;:)").lstrip("(")
    if token and token[0] != "#":
        token = token.split("#", 1)[0]  # path#symbol -> path
    token = token.split("::", 1)[0]  # pytest node tests/x.py::TestA::test_b -> path
    token = LINE_SUFFIX.sub("", token.rstrip(".,;:"))
    match = SYMBOL_SUFFIX.search(token)
    return token[:match.start()] if match and match.start() > 1 else token  # path:ident; C:x drive kept


def examine(raw, quoted, base, root, allow=()):
    """-> (path, report). path None = not a path reference; report None = valid; report = (category, detail)."""
    token = clean(raw)
    if (not token or "://" in token or token[0] in "-@$#" or token[-1] == "(" or HOST_PORT.match(token)
            or any(c in token for c in " *?<>{}$|=")):
        return None, None
    pathlike = has_extension(re.split(r"[\\/]", token.rstrip("/\\"))[-1])
    if looks_absolute(token) and allow and allowed_external(token, allow):
        return token, None
    if is_absolute(token, pathlike, root):
        return token, ("format", "absolute")
    if "\\" in token:
        return (token, ("format", "backslash")) if pathlike else (None, None)
    if token.startswith(("./", "../")):
        return token, ("format", "relative-prefix")
    if INSTRUCTION_ALTERNATION.fullmatch(token) or token[0] in "/~":
        return None, None
    if "/" not in token and (CODE_OBJECT.fullmatch(token) or (TOOL_NAME.fullmatch(token)
                                                              and not fexists(locate(token, base, root)))):
        return None, None  # tool name (Node.js, Next.js) unless such file exists
    if not pathlike and not quoted and not token.endswith("/"):
        exists = "/" in token and fexists(locate(token, base, root))
        return (token, None) if exists else (None, None)  # prose slash list, e.g. client/server, read/write
    first = token.split("/", 1)[0]
    first_is_dir = "/" in token and any(fisdir(os.path.join(d, first)) for d in (root, base))
    if not pathlike and not first_is_dir:
        return None, None  # prose slash list, e.g. read/write
    if "/" in token and not first_is_dir and DOMAIN.fullmatch(first) and not first.startswith("."):
        return None, None  # example.com/x.json
    report = resolve(token, base, root)
    if report and report[0] == "missing" and ((not quoted and "/" not in token) or untemplated_env(token)):
        return None, None  # unbackticked identifier such as res.json; local env file
    return token, report


def tokens(line):
    """-> (raw token, quoted) pairs; bare token followed by "(" is call, skipped."""
    for span in CODE_SPAN.findall(line):
        yield span, True
    rest = CODE_SPAN.sub(" ", line)
    for match in BARE_TOKEN.finditer(rest):
        if not rest.startswith("(", match.end()):
            yield match.group(), False


def read_lines(path, name=None):
    """-> [(number, line)] outside fenced blocks; BOM-aware (utf-8/utf-16), CRLF-safe, split on "\\n" only.
    NUL bytes without BOM -> InputError."""
    text = common.read_text(path, name or path)
    result, fence = [], None
    for number, line in enumerate(common.split_lines(text), 1):
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            result.append((number, line))
    return result


def check_file(path, root, allow=(), name=None):
    reports = []
    base = os.path.dirname(path)
    for number, line in read_lines(path, name):
        seen = set()
        for target in MD_LINK.findall(CODE_SPAN.sub(" ", line)):
            if "://" not in target and not target.startswith(("#", "mailto:")):
                seen.add(("format", "markdown-link", target))
                reports.append((number, "format", "markdown-link", target))
        for raw, quoted in tokens(MD_LINK.sub(lambda m: m.group(0).split("](", 1)[0] + "]", line)):
            token, report = examine(raw, quoted, base, root, allow)  # link target reported once, above
            if report and (report + (token,)) not in seen:
                seen.add(report + (token,))
                reports.append((number,) + report + (token,))
    return reports


def rel(path, root):
    return os.path.relpath(path, root).replace(os.sep, "/")


def inside(path, root):
    try:
        return os.path.commonpath([os.path.normcase(path), os.path.normcase(root)]) == os.path.normcase(root)
    except ValueError:  # different drives
        return False


def walk_error(error):
    name = common.unfs(str(getattr(error, "filename", "") or "")) or error
    raise InputError(f"unreadable directory: {name}: {error.__class__.__name__}")


def instruction_files(root, files):
    """-> sorted absolute instruction paths (root real path); raises ValueError for bad file args, InputError
    for unreadable directories (never silently skipped)."""
    if not files:
        found = []
        for directory, dirs, names in os.walk(common.fs(root), onerror=walk_error):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            found += [os.path.join(common.unfs(directory), name) for name in sorted(NAMES.intersection(names))]
        return found
    result = []
    for name in files:
        path = realpath(name if os.path.isabs(name) else os.path.join(root, name))
        if not fisfile(path):
            raise ValueError(f"not a file: {name}")
        if not inside(path, root):  # real paths: symlink/junction alias cannot escape root
            raise ValueError(f"outside repository root: {name}")
        result.append(path)
    return result


def parse(argv, doc=__doc__, extra=False):
    parser = argparse.ArgumentParser(description=doc, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("root")
    if extra:
        parser.add_argument("--allow-external", action="append", default=[], metavar="ABS-PREFIX")
    parser.add_argument("files", nargs="*")
    args = parser.parse_intermixed_args(argv)
    if not fisdir(args.root):
        parser.error(f"not a directory: {args.root}")
    args.root = realpath(args.root)
    for prefix in getattr(args, "allow_external", []):
        if not looks_absolute(prefix):
            parser.error(f"--allow-external needs absolute prefix: {prefix}")
    try:
        args.paths = instruction_files(args.root, args.files)
    except ValueError as error:
        parser.error(str(error))
    return args


def run(argv):
    args = parse(argv, extra=True)
    allow = [norm_abs(prefix) for prefix in args.allow_external]
    counts = {"missing": 0, "format": 0}
    for path in args.paths:
        for number, category, detail, token in check_file(path, args.root, allow, rel(path, args.root)):
            counts[category] += 1
            print(f"{rel(path, args.root)}:{number}: {category}: {detail}: {token}")
    print(f"{len(args.paths)} files, {counts['missing']} missing, {counts['format']} format")
    return 1 if counts["missing"] or counts["format"] else 0


def main(argv):
    return common.guarded_main(run, argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
