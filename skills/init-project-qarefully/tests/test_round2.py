"""Fix round 2 regressions: encoding, record parsing, ignored/nested/long/locked files, --out aliasing, lines."""
import contextlib
import hashlib
import io
import json
import os
import subprocess
import sys
import unittest

from support import HAS_GIT, RepoCase, legacy_env, load_script, run


def digest(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def in_process(module, *argv):
    """-> (exit code, stdout, stderr) running module.main in-process."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = module.main(list(argv))
    return code, out.getvalue().splitlines(), err.getvalue()


class Base(RepoCase):
    def setUp(self):
        super().setUp()
        self.write("CLAUDE.md", "# Agent instructions\n")
        self.write("src/app.ts", "app\n")
        self.run_dir = os.path.join(self.root, ".init-project", "runs", "r1")
        self.write(".gitignore", "*\n", base=self.run_dir)

    def need_git(self):
        if not HAS_GIT:
            self.skipTest("git unavailable")

    def baseline(self, *extra):
        return run("ledger.py", "baseline", self.root, self.run_dir, *extra)

    def compare(self, *extra):
        return run("ledger.py", "compare", self.root, self.run_dir, "--file", "CLAUDE.md", "--mode", "full", *extra)

    def inventory(self):
        with open(os.path.join(self.run_dir, "baseline", "inventory.json"), encoding="utf-8") as handle:
            return json.load(handle)

    def touch_later(self, rel, text):
        """Rewrite file, forcing mtime forward (same-size edits still detectable by stat signature)."""
        path = self.write(rel, text)
        info = os.stat(path)
        os.utime(path, ns=(info.st_atime_ns, info.st_mtime_ns + 5_000_000_000))


class HashBaseline(Base):
    def test_hash_baseline_reads_inventory_not_tree(self):
        self.need_git()
        self.write("notes.txt", "untracked\n")
        self.commit_all()
        self.write("notes.txt", "dirty\n")
        original = digest(os.path.join(self.root, "CLAUDE.md"))
        self.assertEqual(self.baseline()[0], 0)
        self.write("CLAUDE.md", "# changed by writer\n")
        self.write("apps/web/CLAUDE.md", "new\n")
        code, out, _ = run("ledger.py", "hash", self.root, "--baseline", self.run_dir, "CLAUDE.md",
                           "apps/web/CLAUDE.md", "notes.txt")
        self.assertEqual(code, 0, out)
        dirty = hashlib.sha256(b"dirty\n").hexdigest()
        self.assertEqual(out, [f"CLAUDE.md {original}", "apps/web/CLAUDE.md absent", f"notes.txt {dirty}"])
        self.assertEqual(run("ledger.py", "hash", self.root, "--baseline", self.run_dir, "src/app.ts")[0], 2)
        current = run("ledger.py", "hash", self.root, "CLAUDE.md")[1]
        self.assertEqual(current, [f"CLAUDE.md {digest(os.path.join(self.root, 'CLAUDE.md'))}"])


class Encoding(Base):
    def test_non_cp1252_paths_with_legacy_stdout(self):
        self.write("Łódź/数据.ts", "x\n")
        code, out, err = run("ledger.py", "baseline", self.root, self.run_dir, env=legacy_env())
        self.assertEqual(code, 0, err)
        self.write("Łódź/数据.ts", "changed\n")
        code, out, err = run("ledger.py", "compare", self.root, self.run_dir, "--file", "CLAUDE.md", "--mode",
                             "full", env=legacy_env())
        self.assertEqual(code, 1, err)
        self.assertIn("FAIL: outside-write: Łódź/数据.ts", out)
        self.assertNotIn("Traceback", err)
        code, out, err = run("ledger.py", "hash", self.root, "Łódź/数据.ts", env=legacy_env())
        self.assertEqual(code, 0, err)
        self.write("Łódź/CLAUDE.md", "- `src/gone数据.ts`\n")
        code, out, err = run("check-paths.py", self.root, "Łódź/CLAUDE.md", env=legacy_env())
        self.assertEqual(code, 1, err)
        self.assertIn("Łódź/CLAUDE.md:1: missing: not-found: src/gone数据.ts", out)
        code, out, err = run("check-shape.py", self.root, "Łódź/CLAUDE.md", env=legacy_env())
        self.assertEqual(code, 0, err)

    def test_baseline_failure_leaves_no_baseline(self):
        ledger = load_script("ledger")
        original = ledger.json.dump

        def boom(*args, **kwargs):
            raise RuntimeError("disk\nfull")

        ledger.json.dump = boom
        try:
            code, out, err = in_process(ledger, "baseline", self.root, self.run_dir)
        finally:
            ledger.json.dump = original
        self.assertEqual(code, 2)
        self.assertEqual(err.strip().count("\n"), 0, err)
        self.assertIn("unexpected RuntimeError", err)
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "baseline")))
        self.assertEqual([n for n in os.listdir(self.run_dir) if n.startswith(".baseline-tmp-")], [])
        self.assertEqual(self.baseline()[0], 0)  # rerun works, no baseline-exists loop

    def test_unexpected_error_deletes_partial_out(self):
        self.assertEqual(self.baseline()[0], 0)
        routing = self.write("routing.json", json.dumps({"targets": {"CLAUDE.md": {"disposition": "keep"}}}),
                             base=self.run_dir)
        out = os.path.join(self.run_dir, "manifest.txt")
        ledger = load_script("ledger")
        original = ledger.write_out

        def partial(path, text):
            original(path, text[:3])
            raise OSError("device gone")

        ledger.write_out = partial
        code, _, err = in_process(ledger, "manifest", self.root, routing, "--out", out)
        self.assertEqual(code, 2)
        self.assertIn("unexpected OSError", err)
        self.assertFalse(os.path.exists(out))


SCOUT = "### api-C1\nOrders persist.\n- confidence: high\n- authority: src/o.ts#x\n"


class RecordParsing(Base):
    def setUp(self):
        super().setUp()
        self.write("notes/scout.md", SCOUT, base=self.run_dir)
        self.assertEqual(self.baseline()[0], 0)
        self.routing = self.write("routing.json", json.dumps({"inputs": ["notes/scout.md"], "targets": {
            "CLAUDE.md": {"disposition": "update", "facts": ["api-C1"], "batch": "b1"}}}), base=self.run_dir)
        self.out = os.path.join(self.run_dir, "writer-input.md")

    def project(self):
        return run("ledger.py", "project", self.run_dir, self.routing, "--out", self.out, "CLAUDE.md")

    def test_loose_field_formats_still_veto(self):
        self.assertEqual(self.project()[0], 0)
        for line in ("-  verdict: refuted", "  - verdict: refuted", "- **verdict**: refuted",
                     "- **verdict:** refuted", "* verdict: **Refuted**", "+ Verdict: `conflict`",
                     "1. verdict: refuted (stale evidence)"):
            self.write("attempts/check-9/facts.md", f"### api-C1\n{line}\n- authority: src/o.ts#x\n",
                       base=self.run_dir)
            code, lines, _ = self.project()
            self.assertEqual(code, 1, (line, lines))
            self.assertIn("FAIL: refuted: CLAUDE.md api-C1", lines, line)
            self.assertFalse(os.path.exists(self.out))

    def test_loose_confidence_in_input(self):
        self.write("notes/scout.md", "### api-C1\nOrders persist.\n  - **confidence**: **High**\n", base=self.run_dir)
        code, lines, _ = self.project()
        self.assertEqual(code, 0, lines)

    def test_unparsed_record_fails(self):
        self.write("attempts/check-9/facts.md", "# Checker\n\n### Summary\nprose heading ok\n\n"
                   "### api-C1\nverdict: refuted\n", base=self.run_dir)
        code, lines, _ = self.project()
        self.assertEqual(code, 1, lines)
        self.assertIn("FAIL: unparsed-record: attempts/check-9/facts.md api-C1", lines)
        self.assertEqual(sum(1 for line in lines if "unparsed-record" in line), 1)  # "### Summary" not flagged
        self.write("attempts/check-9/facts.md", "### api-C1\n- verdict: confirmed\n", base=self.run_dir)
        self.write("notes/scout.md", SCOUT + "\n### api-C2\nno fields\n\n### api-Q1\n- status: open\n",
                   base=self.run_dir)
        code, lines, _ = self.project()
        self.assertEqual(lines[0], "FAIL: unparsed-record: notes/scout.md api-C2")
        self.assertEqual(code, 1)

    def test_utf16_record_files(self):
        with open(self.write("attempts/c/facts.md", "", base=self.run_dir), "wb") as handle:
            handle.write("### api-C1\n- verdict: refuted\n".encode("utf-16"))
        code, lines, _ = self.project()
        self.assertIn("FAIL: refuted: CLAUDE.md api-C1", lines)
        with open(os.path.join(self.run_dir, "attempts", "c", "facts.md"), "wb") as handle:
            handle.write("### api-C1\n- verdict: refuted\n".encode("utf-16-le"))  # no BOM
        code, _, err = self.project()
        self.assertEqual(code, 2)
        self.assertIn("attempts/c/facts.md", err.replace("\\", "/"))
        self.assertIn("NUL", err)

    def test_out_aliasing_inputs_refused(self):
        notes = os.path.join(self.run_dir, "notes", "scout.md")
        before = digest(notes)
        aliases = [self.routing, notes, os.path.join(self.run_dir, "s1", "facts.md")]
        if os.name == "nt":
            aliases.append(notes.upper())
        for out in aliases:
            code, lines, err = run("ledger.py", "project", self.run_dir, self.routing, "--out", out, "CLAUDE.md")
            self.assertEqual(code, 2, (out, lines))
            self.assertIn("--out", err)
        self.assertTrue(os.path.isfile(self.routing))
        self.assertEqual(digest(notes), before)
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "s1", "facts.md")))
        code, _, err = run("ledger.py", "questions", self.run_dir, "notes/scout.md", "--out", notes)
        self.assertEqual(code, 2, err)
        self.assertEqual(digest(notes), before)
        sidecar = self.write("provenance/p.json", json.dumps({"batch": "b1", "targets": {}}), base=self.run_dir)
        code, _, err = run("ledger.py", "index", self.root, self.routing, sidecar, "--out", sidecar)
        self.assertEqual(code, 2, err)
        self.assertTrue(os.path.isfile(sidecar))
        code, _, err = run("ledger.py", "manifest", self.root, self.routing, "--out", self.routing)
        self.assertEqual(code, 2, err)
        self.assertTrue(os.path.isfile(self.routing))


class Trees(Base):
    def test_node_modules_writes_are_observed_without_blocking(self):
        self.need_git()
        self.write(".gitignore", "node_modules\n")
        self.write("node_modules/pkg/index.js", "module.exports = 1;\n")
        self.commit_all()
        code, out, _ = self.baseline()
        self.assertEqual(code, 0, out)
        self.assertIn("ignored 1", out[1])
        self.assertEqual(self.compare()[0], 0)
        self.touch_later("node_modules/pkg/index.js", "module.exports = 2;\n")  # same size
        self.write("node_modules/pkg/new.js", "x\n")
        code, out, _ = self.compare()
        self.assertEqual(code, 0, out)
        self.assertIn("WARN: observed-other: node_modules/pkg/index.js", out)
        self.assertIn("WARN: observed-other: node_modules/pkg/new.js", out)
        self.assertEqual(out[-1], "PASS: compare CLAUDE.md full: 2 changed, 0 fail, 2 warn")

    def test_ignored_signature_is_stat_only(self):
        self.need_git()
        self.write(".gitignore", "dist\n")
        self.write("dist/a.js", "a\n")
        self.commit_all()
        self.assertEqual(self.baseline()[0], 0)
        self.assertTrue(self.inventory()["other"]["dist/a.js"].startswith("stat:"))

    def test_ignored_changes_keep_per_file_identity_and_exact_allows(self):
        self.need_git()
        self.write(".gitignore", "dist/\n")
        for n in range(6):
            self.write(f"dist/f{n}.js", f"{n}\n")
        self.commit_all()
        self.assertEqual(self.baseline()[0], 0)
        args = ("--allow", "dist/f0.js", "--allow", "dist/f1.js", "--allow", "dist/new.js")
        self.assertEqual(self.compare(*args)[0], 0)
        self.write("dist/f0.js", "allowed edit\n")
        os.remove(os.path.join(self.root, "dist", "f1.js"))
        self.write("dist/new.js", "allowed addition\n")
        self.write("dist/f2.js", "unallowed sibling edit\n")
        code, out, _ = self.compare(*args)
        self.assertEqual(code, 0, out)
        self.assertIn("WARN: observed-other: dist/f2.js", out)
        self.assertNotIn("WARN: observed-other: dist/f0.js", out)
        self.assertNotIn("WARN: observed-other: dist/f1.js", out)
        self.assertNotIn("WARN: observed-other: dist/new.js", out)
        self.assertEqual(out[-1], "PASS: compare CLAUDE.md full: 4 changed, 0 fail, 1 warn")

    def test_nested_repo_contents_tracked(self):
        self.need_git()
        self.commit_all()
        nested = os.path.join(self.root, "nested")
        self.write("nested/a.txt", "user\n")
        subprocess.run(["git", "init", "-q", nested], check=True, capture_output=True)
        code, out, _ = self.baseline()
        self.assertEqual(code, 0, out)
        self.assertIn("nested/a.txt", self.inventory()["dirty"])
        self.assertEqual(self.compare()[0], 0)
        self.write("nested/a.txt", "clobbered\n")
        self.write("nested/b.txt", "new\n")
        code, out, _ = self.compare()
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL: dirty-changed: nested/a.txt", out)
        self.assertIn("FAIL: outside-write: nested/b.txt", out)

    def test_worktree_rename_status_parsed(self):
        self.need_git()
        self.write("a.txt", "hello world content here\nline2\nline3\n")
        self.commit_all()
        os.replace(os.path.join(self.root, "a.txt"), os.path.join(self.root, "b.txt"))
        self.git("add", "-N", "b.txt")
        self.assertEqual(self.baseline()[0], 0)
        data = self.inventory()
        status = data["git"]["status"]
        if " R b.txt" not in status:
            self.skipTest(f"git did not report worktree rename: {status}")
        self.assertIn(" R a.txt", status)
        self.assertEqual(sorted(data["dirty"]), ["a.txt", "b.txt"])

    @unittest.skipUnless(os.name == "nt", "MAX_PATH limit is Windows-only")
    def test_long_paths_visible(self):
        deep = "/".join(["d" * 50] * 6)
        long_rel = f"{deep}/file.txt"
        full = "\\\\?\\" + os.path.join(self.root, *long_rel.split("/"))
        os.makedirs(os.path.dirname(full))
        with open(full, "w", encoding="utf-8") as handle:
            handle.write("x\n")
        self.assertGreater(len(full), 260)
        self.assertEqual(self.baseline()[0], 0)  # no Git -> tree hashed
        self.assertIn(long_rel, self.inventory()["other"])
        with open(full, "w", encoding="utf-8") as handle:
            handle.write("changed\n")
        code, out, _ = self.compare()
        self.assertEqual(code, 1, out)
        self.assertIn(f"FAIL: outside-write: {long_rel}", out)

    def test_unreadable_directory_is_input_error(self):
        self.write("secret/x.txt", "x\n")
        ledger = load_script("ledger")
        scandir = ledger.os.scandir

        def failing(path):
            if os.path.basename(str(path)) == "secret":
                raise PermissionError(13, "denied", path)
            return scandir(path)

        ledger.os.scandir = failing
        try:
            code, _, err = in_process(ledger, "baseline", self.root, self.run_dir)
        finally:
            ledger.os.scandir = scandir
        self.assertEqual(code, 2)
        self.assertIn("unreadable directory: secret", err)
        self.assertFalse(os.path.exists(os.path.join(self.run_dir, "baseline")))

    def lock(self, path):
        """-> unlock callable; skip when file cannot be made unreadable."""
        if os.name == "nt":
            import msvcrt
            handle = open(path, "r+b")
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, os.path.getsize(path))

            def unlock():
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, os.path.getsize(path))
                handle.close()
            return unlock
        os.chmod(path, 0)
        try:
            open(path, "rb").close()
            self.skipTest("running as root; chmod does not block reads")
        except PermissionError:
            pass
        return lambda: os.chmod(path, 0o644)

    def test_locked_file_signature(self):
        self.need_git()
        self.commit_all()
        path = self.write("locked.db", "data\n")
        unlock = self.lock(path)
        try:
            code, out, err = self.baseline()
            self.assertEqual(code, 0, err)
            self.assertTrue(self.inventory()["dirty"]["locked.db"].startswith("unreadable:"))
            code, out, err = self.compare()
            self.assertEqual(code, 0, (out, err))
        finally:
            unlock()
        self.assertEqual(self.compare()[0], 0)  # readable again, same stat -> unchanged
        self.touch_later("locked.db", "more data\n")
        code, out, _ = self.compare()
        self.assertIn("FAIL: dirty-changed: locked.db", out)


class TextFiles(RepoCase):
    def setUp(self):
        super().setUp()
        self.write("src/a.ts")
        self.write("src/b.ts")

    def write_bytes(self, rel, data):
        path = self.write(rel, "")
        with open(path, "wb") as handle:
            handle.write(data)
        return path

    def test_utf16_instruction_files_checked(self):
        self.write_bytes("CLAUDE.md", "# T\n- `src/gone.ts`\n- Change `src/a.ts` or `src/b.ts` -> x\n".encode("utf-16"))
        code, out, _ = run("check-paths.py", self.root, "CLAUDE.md")
        self.assertEqual(code, 1, out)
        self.assertIn("CLAUDE.md:2: missing: not-found: src/gone.ts", out)
        code, out, _ = run("check-shape.py", self.root, "CLAUDE.md")
        self.assertEqual(code, 1, out)
        self.write_bytes("CLAUDE.md", "﻿- `src/gone.ts`\n".encode("utf-16-be"))
        self.assertEqual(run("check-paths.py", self.root, "CLAUDE.md")[0], 1)

    def test_nul_without_bom_is_input_error(self):
        self.write_bytes("apps/CLAUDE.md", "- `src/gone.ts`\n".encode("utf-16-le"))
        for script in ("check-paths.py", "check-shape.py"):
            code, _, err = run(script, self.root)
            self.assertEqual(code, 2, script)
            self.assertIn("apps/CLAUDE.md", err)
            self.assertNotIn("Traceback", err)

    def test_line_numbers_ignore_exotic_separators(self):
        self.write("CLAUDE.md", "a\x0cb\u2028c\x85d\n- `src/gone.ts`\n")
        code, out, _ = run("check-paths.py", self.root, "CLAUDE.md")
        self.assertEqual(out[0], "CLAUDE.md:2: missing: not-found: src/gone.ts")

    def test_orientation_not_taken_from_bullet(self):
        self.write("apps/api/services.ts", "".join(f"l{n}\n" for n in range(10)))
        self.write("apps/api/CLAUDE.md", "# API\n\n- `services.ts#wire` wires\n- `services.ts#run` runs\n")
        code, out, _ = run("check-shape.py", self.root, "apps/api/CLAUDE.md")
        self.assertEqual((code, out), (0, ["1 files, 0 fail, 0 warn"]))

    def test_file_arg_alias_outside_root_refused(self):
        outside = os.path.join(self.tmp, "outside")
        os.makedirs(outside)
        with open(os.path.join(outside, "CLAUDE.md"), "w", encoding="utf-8") as handle:
            handle.write("x\n")
        link = os.path.join(self.root, "link")
        try:
            os.symlink(outside, link, target_is_directory=True)
        except (OSError, NotImplementedError):
            if os.name != "nt" or subprocess.run(["cmd", "/c", "mklink", "/J", link, outside],
                                                 capture_output=True).returncode:
                self.skipTest("symlink/junction not creatable")
        for script in ("check-paths.py", "check-shape.py"):
            code, _, err = run(script, self.root, "link/CLAUDE.md")
            self.assertEqual(code, 2, script)
            self.assertIn("outside repository root", err)


class IndexRound2(RepoCase):
    def setUp(self):
        super().setUp()
        self.run_dir = os.path.join(self.root, ".init-project", "runs", "r1")
        self.target = self.write("CLAUDE.md", "a\u2028b\nc\n")
        self.assertEqual(run("ledger.py", "baseline", self.root, self.run_dir)[0], 0)

    def index(self, targets, sidecar_targets):
        routing = self.write("routing.json", json.dumps({"targets": targets}), base=self.run_dir)
        sidecar = self.write("provenance/p.json", json.dumps({"batch": "b1", "targets": sidecar_targets}),
                             base=self.run_dir)
        return run("ledger.py", "index", self.root, routing, sidecar, "--out", os.path.join(self.run_dir, "i.json"))

    def test_line_count_split_on_newline_only(self):
        targets = {"CLAUDE.md": {"disposition": "update", "facts": ["a-C1"], "batch": "b1"}}
        code, lines, _ = self.index(targets, {"CLAUDE.md": {"revision": digest(self.target), "facts": {"a-C1": [3]}}})
        self.assertIn("FAIL: line-out-of-range: CLAUDE.md a-C1:3", lines)
        code, lines, _ = self.index(targets, {"CLAUDE.md": {"revision": digest(self.target), "facts": {"a-C1": [2]}}})
        self.assertEqual(code, 0, lines)

    def test_delete_target_unrouted_fact_and_directive(self):
        targets = {"CLAUDE.md": {"disposition": "keep", "batch": "b1"},
                   "old/CLAUDE.md": {"disposition": "delete", "directives": ["existing old/CLAUDE.md:1"],
                                     "batch": "b1"}}
        code, lines, _ = self.index(targets, {"old/CLAUDE.md": {"revision": "absent", "facts": {"a-C7": [1]}}})
        self.assertEqual(code, 1)
        self.assertIn("FAIL: unrouted-fact: old/CLAUDE.md a-C7", lines)
        self.assertIn("FAIL: missing-provenance: old/CLAUDE.md existing old/CLAUDE.md:1", lines)


if __name__ == "__main__":
    unittest.main()
