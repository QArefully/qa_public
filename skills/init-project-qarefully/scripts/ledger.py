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
  project <run-dir> <routing.json> --out <file> <target>...
      Writer input: per target disposition/batch/directives + exact fact record text (checker record preferred
      over scout claim). Records: routing "inputs" (run-relative *.md) + vetoes from every facts.md under run dir
      except <run-dir>/quarantine/ and <run-dir>/baseline/ (refuted|conflict verdict or "supersedes" counts even
      when unlisted). FAIL rules: unparsed-record (scanned fact-ID record, ID ending -C<n>|-F<n>, lacking verdict
      and confidence field; verdict/confidence field in record without fact ID or outside any record),
      unrouted-target, superseded (any ID inside any scanned "supersedes" value), refuted (first word of any
      verdict line refuted|conflict), duplicate-checker, invalid-verdict (verdict first word not
      confirmed|corrected|refuted|conflict; >1 distinct verdict), duplicate-claim, missing, low-confidence
      (confidence first word != high). Any FAIL -> exit 1, nothing written.
  questions <run-dir> <note>... [--answers <gaps.md>...] --out <file>
      Question index lines "<ID> | flow | contract | owner | status | answer" (notes/gaps run-relative or
      absolute). Gaps lines "answered: <QID> -> <ID>" set status answered + answer (later line wins); unknown QID
      -> WARN unknown-question. Duplicate question IDs -> FAIL duplicate-id, exit 1, nothing written.
  manifest <repo-root> <routing.json> --out <file>
      Reviewer manifest lines "<target> <disposition> <sha256|absent>"; no fact IDs or evidence.
  index <repo-root> <routing.json> <provenance-*.json>... --out <file>
      Final index JSON (target -> disposition, batch, revision, facts -> lines, directives -> lines). FAIL rules:
      missing-provenance (create/update target without sidecar entry; routed fact or routed directive ref absent
      from sidecar), unrouted-fact, unrouted-target, multiple-owners, batch-mismatch, fact-multiple-targets,
      delete-has-facts, stale-revision (sidecar revision != current sha256; delete target != absent),
      line-out-of-range, target-missing, delete-present. Any FAIL -> exit 1, nothing written.
Target args (project <target>, routing keys, sidecar keys) = routing "targets" keys exactly (repo-relative, "/").
Path args: repo content (hash paths, --allow) -> repo-relative or absolute; run-dir, routing, provenance, notes,
--out -> cwd-relative or absolute. Paths resolved through symlinks/junctions. Outputs use "/", UTF-8.
--out guard (project, questions, manifest, index): exit 2, nothing written/deleted, when basename AGENTS.md,
CLAUDE.md or facts.md, a path component .agents/.claude (below run dir when inside it), inside
<run-dir>/baseline/, inside repo but outside run dir, or same file as any input (routing, routing inputs,
provenance, notes, answers; case-insensitive on Windows; existing --out hardlinked to input). Repo root + run
dir: project/questions -> <run-dir>/baseline/inventory.json; manifest/index -> nearest ancestor of routing.json
holding baseline/inventory.json for <repo-root> (routing must live inside run dir). Guard passed + exit 1|2 ->
stale --out deleted.
Records (*.md): heading level 3-6 -> record until next heading (# / ## end records); ID = first
"<prefix>-C|F|Q<n>" anywhere in heading text ("### Refuted: s1-C1", "#### 1. `s1-C4`"). Field lines
"[-*+|1.] [**]key[**]: value" (any indent); verdict/confidence = first word of value, markup/punctuation ignored.
Scout claim has confidence; checker record has verdict; question has contract or ID ending -Q<n>. Text files:
BOM -> utf-8/utf-16 decoded; NUL bytes without BOM -> exit 2; lines split on "\\n" only.
Signatures: sha256 hex | absent | stat:<size>:<mtime_ns> | unreadable:<size>:<mtime_ns> (locked file).
Baseline unreadable:<..> -> compared
by current stat (inventory too), never by sha256.
Exit 0 pass, 1 failures, 2 usage/input error (malformed JSON shapes, unexpected error -> one stderr line).
Python 3 stdlib only.
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
DISPOSITIONS = ("create", "update", "keep", "delete")
CAP = 1024 * 1024
HASH_BUDGET = 256 * CAP
TEMP_PREFIX = ".baseline-tmp-"
HEADING = re.compile(r"(#{1,6})\s+(.*?)\s*$")
FIELD = re.compile(r"\s*(?:[-*+]|\d+[.)])\s+[*_]{0,2}([A-Za-z][\w-]*?)[*_]{0,2}\s*:[*_]{0,2}\s*(.*?)\s*$")
FENCE = re.compile(r"\s*(`{3,}|~{3,})")
QUESTION_ID = re.compile(r".+-Q\d+$")
FACT_ID = re.compile(r".+-[CF]\d+$")
RECORD_ID = re.compile(r"[\w.-]+-[CFQ]\d+(?!\w)")  # searched anywhere in heading / supersedes value
SHA = re.compile(r"[0-9a-f]{64}")
VETO = {"refuted", "conflict"}
VERDICTS = {"confirmed", "corrected"} | VETO
ANSWERED = re.compile(r"\s*(?:[-*+]\s+)?answered:\s*`?([^\s`]+)`?\s*(?:->|→)\s*`?([^\s`]+)`?")


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

def read_text(path):
    return common.read_text(path, slash(path))


def norm(value):
    """-> first word (first run of letters) of lower-cased field value; markup/punctuation ignored, "" when none.
    "**Refuted** (stale)" -> refuted; "confirmed (not refuted)" -> confirmed."""
    word = re.search(r"[a-z]+", value.lower())
    return word.group() if word else ""


def new_record(ident, line, number, path, orphan=False):
    return {"id": ident, "orphan": orphan, "line": number, "fields": {}, "verdicts": [], "lines": [line],
            "file": path}


def parse_records(path):
    """-> [{"id", "orphan", "line", "fields", "verdicts", "text", "file"}] outside fenced blocks. Heading level 3-6
    -> record (ID = first RECORD_ID match anywhere in heading text, else first word, e.g. "Summary"); level 1-2
    heading ends record. Field lines before any record or after level 1-2 heading -> orphan record (id None),
    returned only when it holds fields."""
    records, fence = [], None
    current = new_record(None, "", 0, path, orphan=True)
    orphans = [current]
    for number, line in enumerate(common.split_lines(read_text(path)), 1):
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
        heading = None if fence or match else HEADING.match(line)
        if heading:
            text = heading.group(2)
            if len(heading.group(1)) <= 2 or not text:
                current = new_record(None, line, number, path, orphan=True)
                orphans.append(current)
                continue
            found = RECORD_ID.search(text)
            ident = found.group() if found else text.split()[0].strip("`*_").rstrip(":").strip("`*_")
            current = new_record(ident, line, number, path)
            records.append(current)
            continue
        current["lines"].append(line)
        field = None if fence or match else FIELD.match(line)
        if field:
            name = field.group(1).strip("_").lower()
            if current["orphan"] and not current["fields"]:
                current["line"] = number  # orphan reported at its first field line
            current["fields"].setdefault(name, field.group(2))
            if name == "verdict":
                current["verdicts"].append(norm(field.group(2)))
    records += [o for o in orphans if o["fields"]]
    for record in records:
        lines = record.pop("lines")
        while lines and not lines[-1].strip():
            lines.pop()
        record["text"] = "\n".join(lines)
    return records


def vetoed_record(record):
    """Any verdict line whose first word is refuted|conflict -> veto."""
    return any(v in VETO for v in record["verdicts"])


def invalid_verdict(record):
    """Any verdict line whose first word is outside confirmed|corrected|refuted|conflict."""
    return any(v not in VERDICTS for v in record["verdicts"])


def supersedes(record):
    """-> every record ID (RECORD_ID) inside record's "supersedes" field value, own ID excluded."""
    value = record["fields"].get("supersedes", "")
    return [i for i in RECORD_ID.findall(value) if i != record["id"]]


def is_fact(record):
    return not record["orphan"] and bool(FACT_ID.match(record["id"]))


def load_json(path):
    try:
        return json.loads(common.read_text(path, slash(path)))
    except (InputError, ValueError) as error:
        raise InputError(f"unreadable JSON: {slash(path)}: {error.__class__.__name__}")


def str_list(value):
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def target_key(target):
    return slash(os.path.normpath(target))


def load_routing(path):
    routing = load_json(path)
    if not isinstance(routing, dict) or not isinstance(routing.get("targets"), dict):
        raise InputError(f"routing lacks targets object: {slash(path)}")
    if not str_list(routing.get("inputs", [])):
        raise InputError(f"routing inputs not a list of strings: {slash(path)}")
    targets = {}
    for target, entry in routing["targets"].items():
        if (not isinstance(entry, dict) or not str_list(entry.get("facts", []))
                or not str_list(entry.get("directives", [])) or entry.get("disposition") not in DISPOSITIONS
                or not isinstance(entry.get("batch", ""), str)):
            raise InputError(f"bad routing entry: {target}")
        if target_key(target) in targets:
            raise InputError(f"duplicate routing target after normalization: {target}")
        targets[target_key(target)] = entry
    routing["targets"] = targets
    return routing


def load_sidecar(path):
    data = load_json(path)
    if not isinstance(data, dict) or not isinstance(data.get("targets"), dict):
        raise InputError(f"provenance lacks targets object: {slash(path)}")
    if not isinstance(data.get("batch"), str):
        raise InputError(f"provenance lacks batch string: {slash(path)}")
    for target, entry in data["targets"].items():
        if (not isinstance(entry, dict) or not isinstance(entry.get("revision", ""), str)
                or not isinstance(entry.get("facts") or {}, dict) or not isinstance(entry.get("directives") or {}, dict)):
            raise InputError(f"bad provenance entry: {slash(path)}: {target}")
    return data


def run_file(run_dir, name):
    return name if os.path.isabs(name) else os.path.join(run_dir, name)


def write_out(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(fs(path), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def unlisted_facts(run_dir, listed):
    """-> sorted facts.md paths under run dir not in listed, skipping quarantine/, baseline/, baseline temp dirs.
    Unreadable directory -> InputError (never silent skip)."""
    skip = {key(os.path.join(run_dir, d)) for d in ("quarantine", "baseline")}
    found = []

    def failed(error):
        raise InputError(f"unreadable directory: {slash(getattr(error, 'filename', '') or run_dir)}")

    for directory, dirs, names in os.walk(run_dir, onerror=failed):
        dirs[:] = sorted(d for d in dirs if key(os.path.join(directory, d)) not in skip
                         and not d.startswith(TEMP_PREFIX))
        found += [os.path.join(directory, n) for n in names if n == "facts.md"]
    return sorted(p for p in found if key(real(p)) not in listed)


def placeable(ident, scouts, checkers):
    """-> (record, None) or (None, failure rule)."""
    checks, claims = checkers.get(ident, []), scouts.get(ident, [])
    if any(vetoed_record(r) for r in checks):
        return None, "refuted"
    if len(checks) > 1:
        return None, "duplicate-checker"
    if checks:
        verdicts = set(checks[0]["verdicts"])
        ok = len(verdicts) == 1 and verdicts <= {"confirmed", "corrected"}
        return (checks[0], None) if ok else (None, "invalid-verdict")
    if len(claims) > 1:
        return None, "duplicate-claim"
    if not claims:
        return None, "missing"
    high = norm(claims[0]["fields"].get("confidence", "")) == "high"
    return (claims[0], None) if high else (None, "low-confidence")


def unparsed(record, run_dir):
    """-> failure detail when record is unparsed, else None: fact-ID record (ID ending -C<n>|-F<n>) lacking both
    verdict and confidence field, or verdict/confidence field in record without fact ID (non-ID heading, -Q<n>
    question, orphan field outside any record)."""
    fields = record["fields"]
    graded = "verdict" in fields or "confidence" in fields
    if is_fact(record) != graded:
        path = real(record["file"])
        shown = rel(path, run_dir) if inside(path, run_dir) else slash(path)
        return f"{shown} {record['id'] if is_fact(record) else 'line ' + str(record['line'])}"
    return None


def label(record):
    return record["id"] or f"{slash(os.path.basename(record['file']))}:{record['line']}"


def cmd_project(args):
    run_dir = args.run_dir
    routing = load_routing(args.routing)
    scouts, checkers, superseded, vetoed, invalid, listed, failures = {}, {}, {}, set(), set(), set(), []

    def scan(record):
        detail = unparsed(record, run_dir)
        if detail:
            failures.append(("unparsed-record", detail))
        for old in supersedes(record):
            superseded.setdefault(old, label(record))

    for name in routing.get("inputs", []):
        path = run_file(run_dir, name)
        if not os.path.isfile(path):
            raise InputError(f"routing input missing: {slash(name)}")
        if key(real(path)) in listed:
            continue
        listed.add(key(real(path)))
        for record in parse_records(path):
            scan(record)
            if not is_fact(record):
                continue
            if "verdict" in record["fields"]:
                checkers.setdefault(record["id"], []).append(record)
            elif "confidence" in record["fields"]:
                scouts.setdefault(record["id"], []).append(record)
    for path in unlisted_facts(run_dir, listed):
        for record in parse_records(path):
            scan(record)
            if is_fact(record) and vetoed_record(record):
                vetoed.add(record["id"])
            elif is_fact(record) and invalid_verdict(record):
                invalid.add(record["id"])
    sections, facts = [], 0
    for target in args.targets:
        target = target_key(target)
        entry = routing["targets"].get(target)
        if entry is None:
            failures.append(("unrouted-target", target))
            continue
        directives = entry.get("directives", [])
        section = [f"## {target}", f"- disposition: {entry['disposition']}",
                   f"- batch: {entry.get('batch', 'unknown')}", f"- directives: {'; '.join(directives) or 'none'}"]
        for ident in entry.get("facts", []):
            if ident in superseded:
                failures.append(("superseded", f"{target} {ident} by {superseded[ident]}"))
                continue
            if ident in vetoed or ident in invalid:
                record, rule = None, "refuted" if ident in vetoed else "invalid-verdict"
            else:
                record, rule = placeable(ident, scouts, checkers)
            if rule:
                failures.append((rule, f"{target} {ident}"))
            else:
                section += ["", record["text"]]
                facts += 1
        sections.append("\n".join(section))
    for rule, detail in failures:
        print(f"FAIL: {rule}: {detail}")
    if failures:
        print(f"FAIL: project: {len(failures)} fail, nothing written")
        return 1
    write_out(args.out, "# Writer input\n\n" + "\n\n".join(sections) + "\n")
    print(f"PASS: project {slash(args.out)}: {len(sections)} targets, {facts} facts")
    return 0


def cmd_questions(args):
    run_dir = args.run_dir
    rows, order, duplicates = {}, [], []
    for name in args.notes:
        for record in parse_records(run_file(run_dir, name)):
            fields = record["fields"]
            if record["orphan"] or not (QUESTION_ID.match(record["id"]) or "contract" in fields):
                continue
            if record["id"] in rows:
                duplicates.append(record["id"])
                continue
            rows[record["id"]] = [fields.get(k, "") or "-" for k in ("flow", "contract", "owner", "status", "answer")]
            order.append(record["id"])
    warnings = []
    for name in args.answers:
        for line in common.split_lines(read_text(run_file(run_dir, name))):
            match = ANSWERED.match(line)
            if not match:
                continue
            question, answer = match.groups()
            if question not in rows:
                warnings.append(question)
                continue
            rows[question][3], rows[question][4] = "answered", answer
    for ident in sorted(set(duplicates)):
        print(f"FAIL: duplicate-id: {ident}")
    for ident in sorted(set(warnings)):
        print(f"WARN: unknown-question: {ident}")
    statuses = {}
    for ident in order:
        statuses[rows[ident][3]] = statuses.get(rows[ident][3], 0) + 1
    counts = ", ".join(f"{status} {n}" for status, n in sorted(statuses.items()))
    summary = f"{len(order)} questions{', ' + counts if counts else ''}, {len(set(duplicates))} duplicate"
    if duplicates:
        print(f"FAIL: questions: {summary}, nothing written")
        return 1
    write_out(args.out, "".join(" | ".join([i] + [v.replace("|", "/") for v in rows[i]]) + "\n" for i in order))
    print(f"PASS: questions {slash(args.out)}: {summary}")
    return 0


def cmd_manifest(args):
    routing = load_routing(args.routing)
    lines = []
    for target, entry in sorted(routing["targets"].items()):
        path, relative = repo_path(args.root, target)
        lines.append(f"{relative} {entry['disposition']} {sha256(path)}")
    write_out(args.out, "".join(line + "\n" for line in lines))
    print(f"PASS: manifest {slash(args.out)}: {len(lines)} targets")
    return 0


def line_count(path):
    return len(common.split_lines(read_text(path)))


def check_lines(refs, length, where, failures):
    for ref, numbers in refs.items():
        if not isinstance(numbers, list) or not numbers:
            failures.append(("missing-provenance", f"{where} {ref}"))
            continue
        for number in numbers:
            if not isinstance(number, int) or isinstance(number, bool) or number < 1 or (length is not None and number > length):
                failures.append(("line-out-of-range", f"{where} {ref}:{number}"))


def routed_refs(target, entry, side, failures):
    """Routed directive refs absent from sidecar -> missing-provenance; sidecar facts not routed -> unrouted-fact."""
    directives, facts = side.get("directives") or {}, side.get("facts") or {}
    for ref in entry.get("directives", []):
        if ref not in directives:
            failures.append(("missing-provenance", f"{target} {ref}"))
    for ident in facts:
        if ident not in entry.get("facts", []):
            failures.append(("unrouted-fact", f"{target} {ident}"))


def cmd_index(args):
    root = args.root
    routing = load_routing(args.routing)
    sidecars = {}
    failures = []
    for name in args.provenance:
        data = load_sidecar(name)
        for target, entry in data["targets"].items():
            target = target_key(target)
            if target in sidecars:
                failures.append(("multiple-owners", target))
                continue
            sidecars[target] = dict(entry, batch=data["batch"])
    homes = {}
    for target, entry in routing["targets"].items():
        for ident in entry.get("facts", []):
            homes.setdefault(ident, set()).add(target)
    for target, entry in sidecars.items():
        for ident in (entry.get("facts") or {}):
            homes.setdefault(ident, set()).add(target)
    for ident, targets in sorted(homes.items()):
        if len(targets) > 1:
            failures.append(("fact-multiple-targets", f"{ident}: {', '.join(sorted(targets))}"))
    index, fact_count = {}, 0
    for target in sorted(set(routing["targets"]) | set(sidecars)):
        path, relative = repo_path(root, target)
        entry, side = routing["targets"].get(target), sidecars.get(target)
        if entry is None:
            failures.append(("unrouted-target", target))
            continue
        disposition = entry["disposition"]
        exists = os.path.isfile(path)
        if disposition == "delete":
            if entry.get("facts"):
                failures.append(("delete-has-facts", f"{target} {', '.join(entry['facts'])}"))
            if exists:
                failures.append(("delete-present", target))
            if side and side.get("revision") != "absent":
                failures.append(("stale-revision", f"{target} {side.get('revision')} != absent"))
            routed_refs(target, entry, side or {}, failures)
            index[relative] = {"disposition": "delete", "batch": entry.get("batch"), "revision": "absent"}
            continue
        if not exists:
            failures.append(("target-missing", target))
        if side is None and disposition in ("create", "update"):
            failures.append(("missing-provenance", target))
        side = side or {}
        if side and side.get("batch") != entry.get("batch"):
            failures.append(("batch-mismatch", f"{target} {side.get('batch')} != {entry.get('batch')}"))
        facts, directives = side.get("facts") or {}, side.get("directives") or {}
        revision = sha256(path)
        if side and side.get("revision") != revision:
            failures.append(("stale-revision", f"{target} {side.get('revision')} != {revision}"))
        for ident in entry.get("facts", []):
            if ident not in facts:
                failures.append(("missing-provenance", f"{target} {ident}"))
        routed_refs(target, entry, side, failures)
        length = line_count(path) if exists else None
        check_lines(facts, length, target, failures)
        check_lines(directives, length, target, failures)
        fact_count += len(facts)
        index[relative] = {"disposition": disposition, "batch": entry.get("batch"), "revision": revision,
                           "facts": facts, "directives": directives}
    for rule, detail in failures:
        print(f"FAIL: {rule}: {detail}")
    if failures:
        print(f"FAIL: index: {len(failures)} fail, nothing written")
        return 1
    write_out(args.out, json.dumps({"routing_revision": routing.get("revision"), "targets": index},
                                   indent=1, sort_keys=True) + "\n")
    print(f"PASS: index {slash(args.out)}: {len(index)} targets, {fact_count} facts")
    return 0


# --out guard

def find_run_dir(start, root):
    """-> nearest ancestor of start holding baseline/inventory.json whose root is root."""
    directory = os.path.dirname(real(start))
    while True:
        if os.path.isfile(os.path.join(baseline_path(directory), "inventory.json")):
            if key(real(load_baseline(directory)["root"])) == key(root):
                return directory
        parent = os.path.dirname(directory)
        if parent == directory:
            raise InputError(f"no run dir baseline above {slash(start)} for repository root; routing must live in run dir")
        directory = parent


def same_file(a, b):
    try:
        return os.path.samefile(fs(a), fs(b))
    except (OSError, ValueError):  # input missing -> cannot alias
        return False


def guard_out(out, root, run_dir, inputs=()):
    """-> real --out path; InputError when it could clobber instruction surfaces, repository content, baseline,
    a checker facts.md, or any input file of this command (real paths, case-insensitive on Windows)."""
    path = real(out)
    if {os.path.basename(out).lower(), os.path.basename(path).lower()} & {n.lower() for n in NAMES}:
        raise InputError(f"--out must not be an instruction file: {slash(out)}")
    if "facts.md" in {os.path.basename(out).lower(), os.path.basename(path).lower()}:
        raise InputError(f"--out must not be a facts.md record file: {slash(out)}")
    if key(path) in {key(real(p)) for p in inputs} or (os.path.isfile(fs(path)) and any(
            same_file(path, p) for p in inputs)):  # second test: hardlink alias (different name, same file)
        raise InputError(f"--out is an input of this command: {slash(out)}")
    if os.path.isdir(path):
        raise InputError(f"--out is a directory: {slash(out)}")
    if inside(path, run_dir):
        if inside(path, baseline_path(run_dir)):
            raise InputError(f"--out inside immutable baseline: {slash(out)}")
        parts = rel(path, run_dir).split("/")
    elif inside(path, root):
        raise InputError(f"--out inside repository but outside run dir: {slash(out)}")
    else:
        parts = slash(path).split("/")
    if any(part.lower() in PROTECTED_DIRS for part in parts):
        raise InputError(f"--out under .agents/ or .claude/: {slash(out)}")
    return path


def prepare_out(args):
    """Resolve repo root + run dir for --out guard; sets args.out to guarded real path."""
    if args.command in ("project", "questions"):
        args.run_dir = real(args.run_dir)
        root = real(load_baseline(args.run_dir)["root"])
        run_dir = args.run_dir
    else:
        root, run_dir = args.root, find_run_dir(args.routing, args.root)
    inputs = [args.routing] if hasattr(args, "routing") else []
    inputs += getattr(args, "provenance", [])
    if args.command == "project":  # routing must load before guard passes; inputs it lists count too
        inputs += [run_file(run_dir, name) for name in load_routing(args.routing).get("inputs", [])]
    if args.command == "questions":
        inputs += [run_file(run_dir, name) for name in args.notes + args.answers]
    args.out = guard_out(args.out, root, run_dir, inputs)


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

    out = {"out": {"required": True}}
    add("baseline", "root", "run_dir", external_run={"action": "store_true"})
    add("hash", "root", "paths+", baseline={"metavar": "RUN-DIR"})
    add("compare", "root", "run_dir", file={"required": True, "choices": NAMES},
        mode={"required": True, "choices": ("light", "full")}, allow={"action": "append", "default": []})
    add("project", "run_dir", "routing", "targets+", **out)
    add("questions", "run_dir", "notes+", answers={"nargs": "+", "action": "extend", "default": []}, **out)
    add("manifest", "root", "routing", **out)
    add("index", "root", "routing", "provenance+", **out)
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
    guarded = None
    try:
        if hasattr(args, "out"):
            prepare_out(args)
            guarded = args.out
        code = globals()["cmd_" + args.command](args)
    except InputError as error:
        print(f"error: {' '.join(str(error).split())}", file=sys.stderr)
        code = 2
    except Exception as error:  # never traceback; partial --out removed below
        print(f"error: unexpected {common.one_line(error)}", file=sys.stderr)
        code = 2
    if code and guarded and os.path.isfile(fs(guarded)):
        try:
            os.remove(fs(guarded))
        except OSError:
            pass
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
