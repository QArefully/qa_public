#!/usr/bin/env python3
"""Deterministic init-project run metadata. Prints identity only (paths, hashes, counts, PASS/WARN/FAIL); never
file content or diffs. Never edits instruction files.

Usage: ledger.py <command> ...
  baseline <repo-root> <run-dir> [--external-run]
      Write <run-dir>/baseline/ once (exists -> refuse, exit 1): inventory.json + before/ byte copies; built in temp
      dir, renamed atomically (failure -> no baseline/). Walk = every file except entries named .git and run dir
      (node_modules included; directory symlinks/junctions not followed; unreadable dir -> exit 2).
      Inventory: every AGENTS.md, CLAUDE.md, .gitignore, file under .agents/ or .claude/ -> sha256. Git -> HEAD,
      dirty flag, porcelain status; dirty = status files, directory entries (nested repo, submodule) expanded to
      files -> sha256 (<=1 MiB while 256 MiB hash budget lasts) else stat signature; other = every remaining
      untracked file (Git-ignored, node_modules, submodule content) -> stat signature, never hashed. No Git ->
      other = all non-inventory files, hashed within budget. All signatures are per-file, regardless of count.
      Baseline v4 records tracked Git paths; older baselines require a new run.
      before/: instruction files + dirty text files <=1 MiB. Other run dirs (any dir holding
      baseline/inventory.json or a .baseline-tmp-* dir) -> never inventory/dirty/hashed/copied; files listed in
      other with stat signature (writes there still FAIL outside-write). Run dir inside repo; --external-run ->
      must be outside.
  hash <repo-root> [--baseline <run-dir>] <path>...
      Print "<rel> <sha256|absent>" per path (absolute or repo-relative). --baseline -> value from baseline
      inventory.json, not current tree: inventory path (AGENTS.md, CLAUDE.md, .gitignore, .agents/, .claude/)
      absent from inventory -> absent; other path -> recorded sha256|absent, else exit 2.
  compare <repo-root> <run-dir> --file AGENTS.md|CLAUDE.md --mode light|full [--allow <rel>]...
      Current tree (tracked, untracked, Git-ignored) vs baseline. Allowed: selected-name files (light -> root file
      only), --allow paths, run dir. Boundary FAIL rules: gitignore (any .gitignore change), counterpart (other
      name; .claude/ when AGENTS.md selected, .agents/ when CLAUDE.md selected), dirty-changed (pre-existing
      dirty/untracked file not allowed, bytes changed), outside-write, head-changed, git-unavailable.
      WARN rules: dirty-allowed (allowed path already dirty at baseline, now changed -> check user edits kept),
      observed-other (Git other-file changes; excludes inventory, tracked, baseline dirty/untracked, current
      status paths and other run dirs). Observation gives no attribution or write authorization. WARN alone
      -> exit 0.
      Last line "PASS|FAIL: compare <file> <mode>: <n> changed, <f> fail, <w> warn".
Path args: repository paths are repo-relative or absolute. Paths resolve through links; output uses UTF-8.
Signatures: sha256 hex | absent | stat:<size>:<mtime_ns> | unreadable:<size>:<mtime_ns>.
Exit 0 pass, 1 failures, 2 usage/input error. Python 3 stdlib only.
"""
import argparse
import bisect
import datetime
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

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
fs = common.fs

NAMES = ("AGENTS.md", "CLAUDE.md")
PROTECTED_DIRS = (".agents", ".claude")
CAP = 1024 * 1024
HASH_BUDGET = 256 * CAP
TEMP_PREFIX = ".baseline-tmp-"
SHA = re.compile(r"[0-9a-f]{64}")


# paths

def slash(path):
    return path.replace("\\", "/")


def key(path):
    return os.path.normcase(os.path.normpath(path))


def real(path):
    return os.path.realpath(os.path.abspath(path))


def inside(path, root):
    try:
        return os.path.commonpath([key(path), key(root)]) == key(root)
    except ValueError:  # different drives
        return False


def rel(path, root):
    return slash(os.path.relpath(path, root))


def repo_path(root, name):
    """-> (abs, rel) for absolute or repo-relative name inside (real) root; absolute alias paths resolved."""
    path = os.path.abspath(name if os.path.isabs(name) else os.path.join(root, name))
    if not inside(path, root):
        aliased = os.path.join(real(os.path.dirname(path)), os.path.basename(path))
        path = aliased if inside(aliased, root) else path
    if not inside(path, root) or key(path) == key(root):
        raise InputError(f"path outside repository root: {name}")
    return path, rel(path, root)


def file_info(path):
    """-> (size, mtime_ns) of regular file, or None."""
    try:
        info = os.stat(fs(path))
    except OSError:
        return None
    return None if os.path.isdir(fs(path)) else (info.st_size, info.st_mtime_ns)


def unreadable(info):
    return f"unreadable:{info[0]}:{info[1]}" if info else "unreadable:?:?"


def sha256(path):
    """-> sha256 hex | absent | unreadable:<size>:<mtime_ns> (locked/permission-denied; never raises)."""
    full = fs(path)
    if not os.path.isfile(full):
        return "absent"
    digest = hashlib.sha256()
    try:
        with open(full, "rb") as handle:
            for chunk in iter(lambda: handle.read(65536), b""):
                digest.update(chunk)
    except OSError:
        return unreadable(file_info(path))
    return digest.hexdigest()


def is_linked_dir(entry):
    """Directory symlink or junction -> not followed (target inside repo is walked directly)."""
    junction = getattr(entry, "is_junction", None)
    linked = entry.is_symlink() or (junction() if junction else False)
    if not linked and os.name == "nt" and not junction:
        try:
            linked = entry.stat(follow_symlinks=False).st_reparse_tag == 0xA0000003  # mount point (junction)
        except (OSError, AttributeError):
            linked = False
    return linked and entry.is_dir()


def scan_tree(root, run_dir, temps=None):
    """-> {repo-rel file: (size, mtime_ns) | None (stat failed)} for every file under root. Skips entries named
    .git, run dir, linked directories. Extended-length paths on Windows; unreadable directory -> InputError.
    temps set -> filled with repo-rel parents of .baseline-tmp-* directories (other run dirs)."""
    found, skip = {}, os.path.normcase(fs(run_dir))
    stack = [(fs(root), "")]
    while stack:
        directory, prefix = stack.pop()
        try:
            with os.scandir(directory) as listing:
                entries = list(listing)
        except OSError as error:
            raise InputError(f"unreadable directory: {prefix.rstrip('/') or '.'}: {error.__class__.__name__}")
        for entry in entries:
            if entry.name == ".git":
                continue
            path = prefix + entry.name
            try:
                if is_linked_dir(entry):
                    continue
                if entry.is_dir(follow_symlinks=False):
                    if temps is not None and entry.name.startswith(TEMP_PREFIX) and prefix:
                        temps.add(prefix.rstrip("/"))
                    if os.path.normcase(entry.path) != skip:
                        stack.append((entry.path, path + "/"))
                    continue
                info = entry.stat()
            except OSError:
                try:
                    info = entry.stat(follow_symlinks=False)
                except OSError:
                    found[path] = None
                    continue
            found[path] = (info.st_size, info.st_mtime_ns)
    return found


RUN_MARK = "/baseline/inventory.json"


def tree(root, run_dir, known=()):
    """-> (scan, runs, foreign): runs = repo-rel other run dirs (dir holding baseline/inventory.json or
    .baseline-tmp-* dir, plus known from baseline); foreign = scanned files inside them."""
    temps = set()
    scan = scan_tree(root, run_dir, temps)
    runs = temps | set(known) | {p[:-len(RUN_MARK)] for p in scan if p.endswith(RUN_MARK)}
    return scan, runs, ({p for p in scan if in_runs(p, runs)} if runs else set())


def in_runs(path, runs):
    """path equals or lies below any repo-rel dir in runs."""
    parts = path.rstrip("/").split("/")
    return any("/".join(parts[:i]) in runs for i in range(1, len(parts) + 1))


def drop_runs(state, runs, foreign):
    """Other run dirs never dirty/tracked: their files fall to "other" (stat signature, never hashed/copied)."""
    if state and runs:
        state["paths"] = [p for p in state["paths"] if p not in foreign]
        state["tracked"] = state["tracked"] - foreign
        state["status"] = [s for s in state["status"] if not in_runs(s[3:], runs)]
        state["dirty"] = bool(state["paths"])
    return state


def is_inventory(path):
    parts = path.split("/")
    return parts[-1] in NAMES or parts[-1] == ".gitignore" or any(p in PROTECTED_DIRS for p in parts[:-1])


def under(path, root, run_dir):
    return inside(os.path.join(root, path), run_dir)


# signatures

def signatures(root, paths, scan, budget):
    """-> ({path: sha256|stat:..|unreadable:..|absent}, budget left). sha256 when <=CAP and budget lasts."""
    result = {}
    for path in sorted(paths):
        info = scan.get(path)
        if path not in scan:
            result[path] = "absent"
        elif info is None:
            result[path] = unreadable(None)
        elif info[0] <= CAP and info[0] <= budget:
            budget -= info[0]
            result[path] = sha256(os.path.join(root, path))
        else:
            result[path] = f"stat:{info[0]}:{info[1]}"
    return result, budget


def current_signature(root, path, signature, scan):
    """-> current signature of same kind as baseline signature (scan info for stat kinds)."""
    if path not in scan:
        return "absent"
    if signature.startswith(("stat:", "unreadable:")):
        info = scan[path]
        kind = signature.split(":", 1)[0]
        return f"{kind}:{info[0]}:{info[1]}" if info else unreadable(None)
    return sha256(os.path.join(root, path))


# git

def git(root, *args):
    try:
        done = subprocess.run(["git", "-C", root, *args], capture_output=True, check=False)
    except OSError:
        return None
    return done.stdout if done.returncode == 0 else None


def repo_names(top, root, run_dir, names):
    """Git top-relative names -> repo-relative paths inside root, outside run dir (real paths compared)."""
    result = []
    for name in names:
        path = os.path.join(top, name)
        if inside(path, root) and not inside(path, run_dir) and key(path) != key(root):
            result.append(rel(path, root))
    return result


def expand(paths, root, scan):
    """Status paths -> files; directory entry (nested repo "?? dir/", submodule) -> every scanned file inside."""
    keys, result = sorted(scan), set()
    for path in paths:
        if path in scan or not os.path.isdir(fs(os.path.join(root, path))):
            result.add(path)
            continue
        prefix = path.rstrip("/") + "/"
        start = bisect.bisect_left(keys, prefix)
        while start < len(keys) and keys[start].startswith(prefix):
            result.add(keys[start])
            start += 1
    return result


def git_state(root, run_dir, scan):
    """-> {"head", "dirty" flag, "status", "paths" (dirty files, expanded), "tracked"} or None when root not in Git
    work tree. root/run_dir must be real paths; Git top resolved too, so aliases never hide paths."""
    top = git(root, "rev-parse", "--show-toplevel")
    if top is None:
        return None
    top = real(top.decode("utf-8", "replace").strip())
    head = git(root, "rev-parse", "--verify", "-q", "HEAD")
    raw = git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all") or b""
    entries, status, listed = raw.split(b"\0"), [], set()
    index = 0
    while index < len(entries):
        entry = entries[index].decode("utf-8", "replace")
        index += 1
        if len(entry) < 4:
            continue
        names = [entry[3:]]
        if ("R" in entry[:2] or "C" in entry[:2]) and index < len(entries):  # rename/copy: old path follows
            names.append(entries[index].decode("utf-8", "replace"))
            index += 1
        for path in repo_names(top, root, run_dir, names):
            listed.add(path)
            status.append(f"{entry[:2]} {path}")
    raw = git(root, "ls-files", "-z", "--cached", "--full-name") or b""
    tracked = set(repo_names(top, root, run_dir, [n.decode("utf-8", "replace") for n in raw.split(b"\0") if n]))
    paths = expand(listed, root, scan)
    return {"head": head.decode().strip() if head else None, "dirty": bool(paths), "status": status,
            "paths": sorted(paths), "tracked": tracked}


def other_files(scan, state, inventory):
    """-> files outside inventory, tracked set and dirty set (Git-ignored, node_modules, submodule content)."""
    skip = set(inventory) | (state["tracked"] | set(state["paths"]) if state else set())
    return {p for p in scan if p not in skip}


# baseline / compare

def baseline_path(run_dir):
    return os.path.join(run_dir, "baseline")


def check_run_dir(root, run_dir, external):
    if key(run_dir) == key(root) or inside(root, run_dir):
        raise InputError("run dir must not contain repository root")
    if external and inside(run_dir, root):
        raise InputError("--external-run given but run dir is inside repository root")
    if not external and not inside(run_dir, root):
        raise InputError("run dir outside repository root; pass --external-run")


def is_text(path):
    try:
        with open(fs(path), "rb") as handle:
            return b"\0" not in handle.read(CAP + 1)
    except OSError:
        return False


def cmd_baseline(args):
    root, run_dir = args.root, real(args.run_dir)
    check_run_dir(root, run_dir, args.external_run)
    target = baseline_path(run_dir)
    if os.path.lexists(fs(target)):
        print(f"FAIL: baseline-exists: {slash(target)}")
        return 1
    scan, runs, foreign = tree(root, run_dir)
    state = drop_runs(git_state(root, run_dir, scan), runs, foreign)
    inventory = {p: sha256(os.path.join(root, p))
                 for p in sorted(p for p in scan if is_inventory(p) and p not in foreign)}
    data = {"version": 4, "runs": sorted(runs),
            "created": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "root": slash(root), "run_dir": slash(run_dir), "external_run": args.external_run, "cap": CAP,
            "git": None, "inventory": inventory, "dirty": {}, "other": {}, "other_dirs": None,
            "copied": [], "not_copied": []}
    budget = HASH_BUDGET
    if state:
        data["git"] = {k: state[k] for k in ("head", "dirty", "status")}
        data["git"]["tracked"] = sorted(state["tracked"])
        data["dirty"], budget = signatures(root, state["paths"], scan, budget)
        budget = 0  # Git-ignored / untracked-other files: stat signature only
    others = other_files(scan, state, inventory)
    data["other"] = signatures(root, others - foreign, scan, budget)[0]
    data["other"].update(signatures(root, others & foreign, scan, 0)[0])  # other run dirs: stat only
    candidates = sorted({p for p in inventory if p.split("/")[-1] in NAMES}
                        | {p for p, sig in data["dirty"].items() if SHA.fullmatch(sig)})
    os.makedirs(fs(run_dir), exist_ok=True)
    temp = tempfile.mkdtemp(prefix=TEMP_PREFIX, dir=fs(run_dir))
    try:
        for path in candidates:
            source, copy = fs(os.path.join(root, path)), os.path.join(temp, "before", *path.split("/"))
            try:
                if os.path.isfile(source) and os.path.getsize(source) <= CAP and is_text(source):
                    os.makedirs(os.path.dirname(copy), exist_ok=True)
                    shutil.copyfile(source, copy)
                    data["copied"].append(path)
                elif os.path.isfile(source):
                    data["not_copied"].append(path)
            except OSError:
                data["not_copied"].append(path)
        os.makedirs(os.path.join(temp, "before"), exist_ok=True)
        with open(os.path.join(temp, "inventory.json"), "w", encoding="utf-8", newline="\n") as handle:
            json.dump(data, handle, indent=1, sort_keys=True)
        head = state["head"] if state and state["head"] else "none"
        listed = f"ignored {len(others)}" if state else f"tree {len(others)}"
        lines = [f"baseline {slash(target)}",
                 f"git {'yes' if state else 'no'}, head {head}, dirty {len(data['dirty'])}, inventory {len(inventory)},"
                 f" {listed}, copied {len(data['copied'])}, not-copied {len(data['not_copied'])}"]
        os.replace(temp, fs(target))
    except BaseException:
        shutil.rmtree(temp, ignore_errors=True)
        raise
    print("\n".join(lines))
    return 0


def str_list(value):
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def load_baseline(run_dir):
    path = os.path.join(baseline_path(run_dir), "inventory.json")
    try:
        data = json.loads(common.read_text(path, slash(path)))
    except (InputError, ValueError) as error:
        raise InputError(f"baseline unreadable: {slash(path)}: {error.__class__.__name__}")
    if isinstance(data, dict) and data.get("version") != 4:
        raise InputError(f"baseline version {data.get('version')} unsupported; start new run: "
                         f"{slash(path)}")
    if not (isinstance(data, dict) and isinstance(data.get("root"), str) and isinstance(data.get("inventory"), dict)
            and isinstance(data.get("dirty"), dict) and isinstance(data.get("other"), dict)
            and data.get("other_dirs") is None
            and (data.get("git") is None or (isinstance(data["git"], dict)
                                            and str_list(data["git"].get("tracked"))))):
        raise InputError(f"baseline malformed: {slash(path)}")
    return data


def classify(path, args, dirty):
    """-> (level, rule) or None when allowed and clean."""
    parts, name = path.split("/"), path.split("/")[-1]
    other = NAMES[1] if args.file == NAMES[0] else NAMES[0]
    protected = ".claude" if args.file == "AGENTS.md" else ".agents"
    if name == ".gitignore":
        return "FAIL", "gitignore"
    if name == other or protected in parts[:-1]:
        return "FAIL", "counterpart"
    allow = {key(p) for p in args.allow}
    if key(path) in allow or (path == args.file if args.mode == "light" else name == args.file):
        return ("WARN", "dirty-allowed") if path in dirty else None
    return "FAIL", "dirty-changed" if path in dirty else "outside-write"


def cmd_compare(args):
    root, run_dir = args.root, real(args.run_dir)
    base = load_baseline(run_dir)
    if key(real(base["root"])) != key(root):
        raise InputError("repository root differs from baseline root")
    args.allow = [repo_path(root, p)[1] for p in args.allow]
    known = base.get("runs") if isinstance(base.get("runs"), list) else []
    scan, runs, foreign = tree(root, run_dir, [r for r in known if isinstance(r, str)])
    reports, changed, observed = [], set(), set()
    current = {p: sha256(os.path.join(root, p)) for p in scan if is_inventory(p) and p not in foreign}
    for path in set(current) | set(base["inventory"]):
        then = base["inventory"].get(path)
        now = (current_signature(root, path, then, scan) if path in current and str(then).startswith("unreadable:")
               else current.get(path))
        if now != then:
            changed.add(path)
    others = None
    if base["git"] is not None:
        state = drop_runs(git_state(root, run_dir, scan), runs, foreign)
        if state is None:
            reports.append(("FAIL", "git-unavailable", slash(root)))
        else:
            if state["head"] != base["git"].get("head"):
                reports.append(("FAIL", "head-changed", f"{base['git'].get('head')} -> {state['head']}"))
            changed |= {p for p in state["paths"] if p not in base["dirty"]}
            others = other_files(scan, state, current)
            strict = (set(base["dirty"]) | set(base["git"]["tracked"]) | state["tracked"]
                      | set(state["paths"]))
            observed = {p for p in set(base["other"]) | others
                        if p not in strict and not is_inventory(p) and not in_runs(p, runs)}
        changed |= {p for p, sig in base["dirty"].items() if current_signature(root, p, sig, scan) != sig}
    else:
        others = other_files(scan, None, current)
    if others is not None:
        changed |= {p for p in others if p not in base["other"] and p not in base["dirty"]}
        changed |= {p for p, sig in base["other"].items() if current_signature(root, p, sig, scan) != sig}
    changed = {p for p in changed if not under(p, root, run_dir)}
    for path in sorted(changed):
        verdict = classify(path, args, base["dirty"])
        if verdict == ("FAIL", "outside-write") and path in observed:
            verdict = "WARN", "observed-other"
        if verdict:
            reports.append(verdict + (path,))
    for level, rule, detail in reports:
        print(f"{level}: {rule}: {detail}")
    fails = sum(1 for r in reports if r[0] == "FAIL")
    warns = len(reports) - fails
    print(f"{'FAIL' if fails else 'PASS'}: compare {args.file} {args.mode}: {len(changed)} changed, {fails} fail, "
          f"{warns} warn")
    return 1 if fails else 0


def baseline_hash(base, relative):
    """-> baseline sha256|absent for repo-relative path; InputError when baseline recorded no hash."""
    if is_inventory(relative):
        return {key(p): v for p, v in base["inventory"].items()}.get(key(relative), "absent")
    for table in (base["dirty"], base["other"]):
        sig = {key(p): v for p, v in table.items()}.get(key(relative))
        if sig is not None and (sig == "absent" or SHA.fullmatch(sig)):
            return sig
    raise InputError(f"baseline holds no sha256 for non-inventory path: {relative}")


def cmd_hash(args):
    base = None
    if args.baseline:
        base = load_baseline(real(args.baseline))
        if key(real(base["root"])) != key(args.root):
            raise InputError("repository root differs from baseline root")
    lines = []
    for name in args.paths:
        path, relative = repo_path(args.root, name)
        if base is not None:
            lines.append(f"{relative} {baseline_hash(base, relative)}")
            continue
        if os.path.isdir(fs(path)):
            raise InputError(f"directory, not file: {name}")
        lines.append(f"{relative} {sha256(path)}")
    print("\n".join(lines))
    return 0


# records

def parsers():
    """-> {command: parser}; one parser per command so options and positionals may intermix."""
    table = {}

    def add(name, *positionals, **options):
        sub = argparse.ArgumentParser(prog=f"ledger.py {name}", description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
        for positional in positionals:  # trailing "+" -> one or more
            sub.add_argument(positional.rstrip("+"), nargs="+" if positional.endswith("+") else None)
        for option, spec in options.items():
            sub.add_argument("--" + option.replace("_", "-"), **spec)
        table[name] = sub

    add("baseline", "root", "run_dir", external_run={"action": "store_true"})
    add("hash", "root", "paths+", baseline={"metavar": "RUN-DIR"})
    add("compare", "root", "run_dir", file={"required": True, "choices": NAMES},
        mode={"required": True, "choices": ("light", "full")}, allow={"action": "append", "default": []})
    return table


def main(argv):
    common.setup_stdio()
    table = parsers()
    if not argv or argv[0] not in table:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    args = table[argv[0]].parse_intermixed_args(argv[1:])
    args.command = argv[0]
    if hasattr(args, "root"):
        if not os.path.isdir(args.root):
            print(f"error: not a directory: {args.root}", file=sys.stderr)
            return 2
        args.root = real(args.root)
    try:
        code = globals()["cmd_" + args.command](args)
    except InputError as error:
        print(f"error: {' '.join(str(error).split())}", file=sys.stderr)
        code = 2
    except Exception as error:
        print(f"error: unexpected {common.one_line(error)}", file=sys.stderr)
        code = 2
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
