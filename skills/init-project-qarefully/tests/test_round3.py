"""Fix round 3 regressions: record heading IDs, orphan fields, first-word verdicts, supersedes values, bytecode,
other run dirs, long-path walks, locked inventory files, hardlinked --out."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from support import SCRIPTS, RepoCase, run
from test_round2 import SCOUT, Base, digest


def lock(case, path):
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
        case.skipTest("running as root; chmod does not block reads")
    except PermissionError:
        pass
    return lambda: os.chmod(path, 0o644)


def long_name(path):
    """Extended-length form on Windows (create/write paths >260 chars)."""
    return "\\\\?\\" + os.path.abspath(path) if os.name == "nt" else path


def tree_size(path):
    return sum(os.path.getsize(os.path.join(d, n)) for d, _, names in os.walk(path) for n in names)


class Records(Base):
    def setUp(self):
        super().setUp()
        self.write("notes/scout.md", SCOUT, base=self.run_dir)
        self.assertEqual(self.baseline()[0], 0)
        self.routing = self.write("routing.json", json.dumps({"inputs": ["notes/scout.md"], "targets": {
            "CLAUDE.md": {"disposition": "update", "facts": ["api-C1"], "batch": "b1"}}}), base=self.run_dir)
        self.out = os.path.join(self.run_dir, "writer-input.md")

    def project(self):
        return run("ledger.py", "project", self.run_dir, self.routing, "--out", self.out, "CLAUDE.md")

    def facts(self, text):
        self.write("attempts/check-9/facts.md", text, base=self.run_dir)

    def test_heading_id_anywhere_and_levels_3_to_6(self):
        self.assertEqual(self.project()[0], 0)
        for heading in ("### Refuted: api-C1", "### 1. api-C1", "#### api-C1", "###### api-C1",
                        "### **`api-C1`** (recheck)", "### Claim api-C1: orders"):
            self.facts(f"# Checker\n\n{heading}\n- verdict: refuted\n")
            code, lines, _ = self.project()
            self.assertEqual(code, 1, (heading, lines))
            self.assertIn("FAIL: refuted: CLAUDE.md api-C1", lines, heading)
            self.assertFalse(os.path.exists(self.out))

    def test_graded_field_without_fact_id_fails(self):
        for text, line in (("### Summary\n- verdict: refuted\n", 1),
                           ("- verdict: refuted\n", 1),
                           ("### api-C1\n- verdict: confirmed\n\n## Other\n- confidence: high\n", 5),
                           ("### api-Q1\n- verdict: refuted\n", 1)):
            self.facts(text)
            code, lines, _ = self.project()
            self.assertEqual(code, 1, (text, lines))
            self.assertIn(f"FAIL: unparsed-record: attempts/check-9/facts.md line {line}", lines, text)
        self.facts("### api-C1\n- verdict: confirmed\n\n#### Evidence\nprose only\n\n## Appendix\ntext\n")
        code, lines, _ = self.project()
        self.assertEqual(code, 0, lines)

    def test_input_record_heading_variants_placed(self):
        self.write("notes/scout.md", "## Claims\n\n### 1. `api-C1` orders\nOrders persist.\n- confidence: High\n",
                   base=self.run_dir)
        code, lines, _ = self.project()
        self.assertEqual(code, 0, lines)
        with open(self.out, encoding="utf-8") as handle:
            self.assertIn("### 1. `api-C1` orders", handle.read())

    def test_supersedes_value_markup(self):
        for value in ("**api-C1**", '"api-C1";', "`api-C2`, api-C1", "api-C1 (stale evidence)"):
            self.facts(f"### api-C9\n- verdict: confirmed\n- supersedes: {value}\n")
            code, lines, _ = self.project()
            self.assertEqual(code, 1, (value, lines))
            self.assertIn("FAIL: superseded: CLAUDE.md api-C1 by api-C9", lines, value)

    def test_verdict_first_word(self):
        for verdict, expected in (("confirmed (not refuted)", None), ("**Corrected** — narrower", None),
                                  ("**Refuted** (stale)", "refuted"), ("`conflict`: two owners", "refuted"),
                                  ("not refuted", "invalid-verdict"), ("rejected", "invalid-verdict")):
            self.write("notes/check.md", f"### api-C1\n- verdict: {verdict}\n", base=self.run_dir)
            with open(self.routing, "w", encoding="utf-8") as handle:
                json.dump({"inputs": ["notes/scout.md", "notes/check.md"], "targets": {
                    "CLAUDE.md": {"disposition": "update", "facts": ["api-C1"], "batch": "b1"}}}, handle)
            code, lines, _ = self.project()
            if expected is None:
                self.assertEqual(code, 0, (verdict, lines))
            else:
                self.assertIn(f"FAIL: {expected}: CLAUDE.md api-C1", lines, verdict)

    def test_unlisted_invalid_verdict_fails(self):
        self.facts("### api-C1\n- verdict: rejected\n")
        code, lines, _ = self.project()
        self.assertEqual(code, 1, lines)
        self.assertIn("FAIL: invalid-verdict: CLAUDE.md api-C1", lines)
        self.facts("### api-C1\n- verdict: confirmed (not refuted)\n")
        self.assertEqual(self.project()[0], 0)

    def test_hardlinked_out_refused(self):
        notes = os.path.join(self.run_dir, "notes", "scout.md")
        alias = os.path.join(self.run_dir, "writer-alias.md")
        try:
            os.link(notes, alias)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"hardlinks unsupported: {error}")
        before = digest(notes)
        code, lines, err = run("ledger.py", "project", self.run_dir, self.routing, "--out", alias, "CLAUDE.md")
        self.assertEqual(code, 2, lines)
        self.assertIn("--out is an input", err)
        code, _, err = run("ledger.py", "questions", self.run_dir, "notes/scout.md", "--out", alias)
        self.assertEqual(code, 2, err)
        self.assertEqual(digest(notes), before)
        self.assertTrue(os.path.isfile(alias))


class Bytecode(unittest.TestCase):
    def test_scripts_write_no_pycache(self):
        tmp = tempfile.mkdtemp()
        try:
            scripts = os.path.join(tmp, "skill", "scripts")
            os.makedirs(scripts)
            for name in os.listdir(SCRIPTS):
                if name.endswith(".py"):
                    shutil.copyfile(os.path.join(SCRIPTS, name), os.path.join(scripts, name))
            repo = os.path.join(tmp, "repo")
            os.makedirs(repo)
            for script, args in (("ledger.py", []), ("check-paths.py", [repo]), ("check-shape.py", [repo])):
                done = subprocess.run([sys.executable, "-I", os.path.join(scripts, script), *args],
                                      capture_output=True, text=True)
                self.assertIn(done.returncode, (0, 2), (script, done.stderr))
                self.assertNotIn("Traceback", done.stderr, script)
                self.assertFalse(os.path.exists(os.path.join(scripts, "__pycache__")), script)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class OtherRuns(RepoCase):
    def setUp(self):
        super().setUp()
        self.write("CLAUDE.md", "# Agent instructions\n")
        self.write("src/app.ts", "app\n")
        self.runs = os.path.join(self.root, ".init-project", "runs")

    def inventory(self, run_dir):
        with open(os.path.join(run_dir, "baseline", "inventory.json"), encoding="utf-8") as handle:
            return json.load(handle)

    def test_sequential_baselines_constant_size(self):
        if not shutil.which("git"):
            self.skipTest("git unavailable")
        self.commit_all()
        self.write("notes.txt", "user dirty edit\n")
        sizes = []
        for number in (1, 2, 3):
            run_dir = os.path.join(self.runs, f"r{number}")
            self.write("notes/scout.md", SCOUT, base=run_dir)  # untracked, not ignored
            code, _, err = run("ledger.py", "baseline", self.root, run_dir)
            self.assertEqual(code, 0, err)
            sizes.append(tree_size(os.path.join(run_dir, "baseline", "before")))
            data = self.inventory(run_dir)
            self.assertEqual(sorted(data["dirty"]), ["notes.txt"])
            self.assertEqual(sorted(data["inventory"]), ["CLAUDE.md"])
            self.assertEqual(data["runs"], [f".init-project/runs/r{n}" for n in range(1, number)])
            foreign = [p for p in data["other"] if p.startswith(".init-project/")]
            self.assertEqual(len(foreign) > 0, number > 1)
            self.assertTrue(all(data["other"][p].startswith("stat:") for p in foreign))
        self.assertEqual(len(set(sizes)), 1, sizes)
        self.write("notes/scout.md", "rewritten by stray writer, longer\n", base=os.path.join(self.runs, "r1"))
        code, out, _ = run("ledger.py", "compare", self.root, os.path.join(self.runs, "r3"), "--file", "CLAUDE.md",
                           "--mode", "full")
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL: outside-write: .init-project/runs/r1/notes/scout.md", out)
        self.assertFalse(any("r2/" in line for line in out), out)

    def test_temp_dir_marks_run_without_git(self):
        stale = os.path.join(self.runs, "r0")
        self.write("notes/scout.md", SCOUT, base=stale)
        self.write("CLAUDE.md", "copy\n", base=os.path.join(stale, ".baseline-tmp-abc", "before"))
        run_dir = os.path.join(self.runs, "r1")
        code, _, err = run("ledger.py", "baseline", self.root, run_dir)  # no Git -> other hashed within budget
        self.assertEqual(code, 0, err)
        data = self.inventory(run_dir)
        self.assertEqual(data["runs"], [".init-project/runs/r0"])
        self.assertEqual(sorted(data["inventory"]), ["CLAUDE.md"])
        self.assertTrue(data["other"][".init-project/runs/r0/notes/scout.md"].startswith("stat:"))
        self.assertEqual(len(data["other"]["src/app.ts"]), 64)  # non-run file still hashed
        self.assertEqual(data["copied"], ["CLAUDE.md"])
        code, out, _ = run("ledger.py", "compare", self.root, run_dir, "--file", "CLAUDE.md", "--mode", "full")
        self.assertEqual(code, 0, out)


class LongPaths(RepoCase):
    def test_walk_and_file_args_beyond_max_path(self):
        self.write("CLAUDE.md", "# Root\n- `src/app.ts` -> app\n")
        self.write("src/app.ts", "app\n")
        deep = "/".join(["d" * 50] * 6)
        directory = long_name(os.path.join(self.root, *deep.split("/")))
        os.makedirs(directory)
        for name, text in (("CLAUDE.md", "Uses `helper.py` for x.\n\n- `src/app.ts` -> app\n"),
                           ("helper.py", "x = 1\n")):
            with open(os.path.join(directory, name), "w", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
        self.assertGreater(len(os.path.join(self.root, *deep.split("/"), "CLAUDE.md")), 260)
        for script in ("check-paths.py", "check-shape.py"):
            code, out, err = run(script, self.root)
            self.assertEqual(code, 0, (script, out, err))
            self.assertEqual(out[-1].split(",")[0], "2 files", (script, out))
            code, out, err = run(script, self.root, f"{deep}/CLAUDE.md")
            self.assertEqual(code, 0, (script, out, err))
        with open(os.path.join(directory, "CLAUDE.md"), "w", encoding="utf-8", newline="\n") as handle:
            handle.write("Uses `missing.py` here.\n")
        code, out, _ = run("check-paths.py", self.root)
        self.assertEqual(code, 1, out)
        self.assertIn(f"{deep}/CLAUDE.md:1: missing: not-found: missing.py", out)


class LockedInventory(Base):
    def test_locked_inventory_file_unlocked_later(self):
        path = self.write(".agents/notes.md", "agent notes\n")
        unlock = lock(self, path)
        try:
            code, _, err = self.baseline()
            self.assertEqual(code, 0, err)
            self.assertTrue(self.inventory()["inventory"][".agents/notes.md"].startswith("unreadable:"))
        finally:
            unlock()
        code, out, err = self.compare()
        self.assertEqual(code, 0, (out, err))
        self.touch_later(".agents/notes.md", "agent notes edited\n")
        code, out, _ = self.compare()
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL: counterpart: .agents/notes.md", out)


if __name__ == "__main__":
    unittest.main()
