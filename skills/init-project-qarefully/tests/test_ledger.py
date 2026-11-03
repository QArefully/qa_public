import hashlib
import json
import os
import unittest

from support import HAS_GIT, RepoCase, load_script, run


def digest(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


class Baseline(RepoCase):
    def setUp(self):
        super().setUp()
        self.write("CLAUDE.md", "# Agent instructions\n")
        self.write("src/app.ts", "app\n")
        self.write(".gitignore", "dist\n")
        self.write(".claude/settings.json", "{}\n")
        self.run_dir = os.path.join(self.root, ".init-project", "runs", "r1")
        self.write(".gitignore", "*\n", base=self.run_dir)

    def baseline(self, *extra, run_dir=None):
        return run("ledger.py", "baseline", self.root, run_dir or self.run_dir, *extra)

    def compare(self, *extra, run_dir=None):
        return run("ledger.py", "compare", self.root, run_dir or self.run_dir, *extra)

    def git_setup(self, dirty=True):
        if not HAS_GIT:
            self.skipTest("git unavailable")
        self.commit_all()
        if dirty:
            self.write("src/app.ts", "user edit\n")
            self.write("notes.txt", "untracked\n")

    def test_baseline_immutable(self):
        self.git_setup()
        code, out, _ = self.baseline()
        self.assertEqual(code, 0, out)
        self.assertTrue(out[0].startswith("baseline "))
        inventory = os.path.join(self.run_dir, "baseline", "inventory.json")
        with open(inventory, encoding="utf-8") as handle:
            data = json.load(handle)
        self.assertEqual(sorted(data["dirty"]), ["notes.txt", "src/app.ts"])
        self.assertIn(".claude/settings.json", data["inventory"])
        self.assertTrue(os.path.isfile(os.path.join(self.run_dir, "baseline", "before", "src", "app.ts")))
        self.assertTrue(os.path.isfile(os.path.join(self.run_dir, "baseline", "before", "CLAUDE.md")))
        before = digest(inventory)
        code, out, _ = self.baseline()
        self.assertEqual(code, 1)
        self.assertTrue(out[0].startswith("FAIL: baseline-exists"))
        self.assertEqual(digest(inventory), before)

    def test_output_never_contains_content(self):
        self.write("CLAUDE.md", "SECRET-CONTENT\n")
        self.git_setup()
        outputs = self.baseline()[1] + self.compare("--file", "CLAUDE.md", "--mode", "full")[1]
        self.assertNotIn("SECRET-CONTENT", "\n".join(outputs))

    def test_compare_pass_with_allowed_and_run_dir_writes(self):
        self.git_setup()
        self.baseline()
        self.write("CLAUDE.md", "# Agent instructions\n- new\n")
        self.write("apps/api/CLAUDE.md", "API\n")
        self.write("scratch.md", "run artifact\n", base=self.run_dir)
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full")
        self.assertEqual(code, 0, out)
        self.assertEqual(out[-1], "PASS: compare CLAUDE.md full: 2 changed, 0 fail, 0 warn")

    def test_light_allows_root_only(self):
        self.git_setup()
        self.baseline()
        self.write("apps/api/CLAUDE.md", "API\n")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "light")
        self.assertEqual(code, 1)
        self.assertIn("FAIL: outside-write: apps/api/CLAUDE.md", out)
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "light", "--allow", "apps/api/CLAUDE.md")
        self.assertEqual(code, 0, out)

    def test_outside_write(self):
        self.git_setup()
        self.baseline()
        self.write("src/other.ts", "new\n")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full")
        self.assertEqual(code, 1)
        self.assertIn("FAIL: outside-write: src/other.ts", out)

    def test_counterpart_touch(self):
        self.git_setup()
        self.baseline()
        self.write("AGENTS.md", "x\n")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full")
        self.assertIn("FAIL: counterpart: AGENTS.md", out)
        os.remove(os.path.join(self.root, "AGENTS.md"))
        self.write(".claude/settings.json", '{"a": 1}\n')
        code, out, _ = self.compare("--file", "AGENTS.md", "--mode", "full")
        self.assertEqual(code, 1)
        self.assertIn("FAIL: counterpart: .claude/settings.json", out)

    def test_gitignore_change(self):
        self.git_setup()
        self.baseline()
        self.write(".gitignore", "dist\n.init-project\n")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full", "--allow", ".gitignore")
        self.assertIn("FAIL: gitignore: .gitignore", out)

    def test_dirty_baseline_file_changed(self):
        self.git_setup()
        self.baseline()
        self.assertEqual(self.compare("--file", "CLAUDE.md", "--mode", "full")[0], 0)
        self.write("src/app.ts", "user edit lost\n")
        os.remove(os.path.join(self.root, "notes.txt"))
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full")
        self.assertEqual(code, 1)
        self.assertIn("FAIL: dirty-changed: src/app.ts", out)
        self.assertIn("FAIL: dirty-changed: notes.txt", out)

    def test_head_change_fails(self):
        self.git_setup(dirty=False)
        self.baseline()
        self.write("CLAUDE.md", "changed\n")
        self.git("commit", "-q", "-am", "sneak")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full")
        self.assertEqual(code, 1)
        self.assertTrue(any(line.startswith("FAIL: head-changed") for line in out), out)

    def test_no_git_full_walk(self):
        self.baseline()
        self.write("CLAUDE.md", "ok\n")
        self.assertEqual(self.compare("--file", "CLAUDE.md", "--mode", "light")[0], 0)
        self.write("src/app.ts", "changed\n")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "light")
        self.assertEqual(code, 1)
        self.assertIn("FAIL: outside-write: src/app.ts", out)

    def test_external_run_dir(self):
        external = os.path.join(self.tmp, "external", "r1")
        self.assertEqual(self.baseline(run_dir=external)[0], 2)  # needs --external-run
        self.assertEqual(self.baseline("--external-run")[0], 2)  # inside repo with flag
        code, out, _ = self.baseline("--external-run", run_dir=external)
        self.assertEqual(code, 0, out)
        self.write("notes.md", "run\n", base=external)
        self.write("CLAUDE.md", "ok\n")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full", run_dir=external)
        self.assertEqual(code, 0, out)

    def test_agents_counterpart_when_claude_selected(self):
        self.git_setup(dirty=False)
        self.baseline()
        self.write(".agents/skills/x.md", "new\n")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full")
        self.assertEqual(code, 1)
        self.assertIn("FAIL: counterpart: .agents/skills/x.md", out)

    def test_dirty_allowed_warn_only(self):
        self.git_setup(dirty=False)
        self.write("CLAUDE.md", "# Agent instructions\n- user edit\n")
        self.baseline()
        self.write("CLAUDE.md", "# Agent instructions\n- user edit\n- run edit\n")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full")
        self.assertEqual(code, 0, out)
        self.assertIn("WARN: dirty-allowed: CLAUDE.md", out)
        self.assertEqual(out[-1], "PASS: compare CLAUDE.md full: 1 changed, 0 fail, 1 warn")

    def test_ignored_file_changes_are_observed_without_blocking(self):
        self.write(".gitignore", "dist/\n.next/\nnode_modules/\n")
        self.write("dist/old.js", "build\n")
        self.write("dist/deleted.js", "remove me\n")
        self.write(".next/cache/result", "old cache\n")
        self.write("node_modules/pkg/index.js", "old module\n")
        self.git_setup(dirty=False)
        code, out, _ = self.baseline()
        self.assertEqual(code, 0, out)
        self.assertIn("ignored 4", out[1])
        self.assertEqual(self.compare("--file", "CLAUDE.md", "--mode", "full")[0], 0)
        self.write("dist/old.js", "rebuilt\n")
        self.write("dist/new.js", "new\n")
        os.remove(os.path.join(self.root, "dist", "deleted.js"))
        self.write(".next/cache/result", "new cache\n")
        self.write("node_modules/pkg/new.js", "new module\n")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full")
        self.assertEqual(code, 0, out)
        for path in ("dist/old.js", "dist/deleted.js", "dist/new.js", ".next/cache/result",
                     "node_modules/pkg/new.js"):
            self.assertIn(f"WARN: observed-other: {path}", out)
        self.assertEqual(out[-1], "PASS: compare CLAUDE.md full: 5 changed, 0 fail, 5 warn")

    def test_ignored_counterpart_remains_strict(self):
        self.write("dist/AGENTS.md", "original instructions\n")
        self.git_setup(dirty=False)
        self.assertEqual(self.baseline()[0], 0)
        self.write("dist/AGENTS.md", "changed instructions\n")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full")
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL: counterpart: dist/AGENTS.md", out)

    def test_exact_allow_does_not_cover_same_directory_sibling(self):
        self.write("src/edit.ts", "before edit\n")
        self.write("src/delete.ts", "remove me\n")
        self.write("src/sibling.ts", "before sibling edit\n")
        self.git_setup(dirty=False)
        self.assertEqual(self.baseline()[0], 0)
        self.write("src/edit.ts", "after edit\n")
        os.remove(os.path.join(self.root, "src", "delete.ts"))
        self.write("src/add.ts", "new file\n")
        self.write("src/sibling.ts", "after sibling edit\n")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full",
                                    "--allow", "src/edit.ts", "--allow", "src/delete.ts",
                                    "--allow", "src/add.ts")
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL: outside-write: src/sibling.ts", out)
        for path in ("src/edit.ts", "src/delete.ts", "src/add.ts"):
            self.assertNotIn(f"FAIL: outside-write: {path}", out)

    def test_tracked_file_matching_gitignore_remains_strict(self):
        self.write(".gitignore", "dist/\nsrc/app.ts\n")
        self.git("init", "-q")
        self.git("config", "core.autocrlf", "false")
        self.git("add", "-A")
        self.git("add", "-f", "src/app.ts")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init")
        self.assertEqual(self.baseline()[0], 0)
        self.write("src/app.ts", "tracked edit\n")
        code, out, _ = self.compare("--file", "CLAUDE.md", "--mode", "full")
        self.assertEqual(code, 1, out)
        self.assertIn("FAIL: outside-write: src/app.ts", out)
        self.assertNotIn("WARN: observed-other: src/app.ts", out)

    def test_ignored_snapshot_stat_only(self):
        ledger = load_script("ledger")
        self.write("a.log", "a\n")
        scan = ledger.scan_tree(self.root, self.run_dir)
        sigs, budget = ledger.signatures(self.root, ["a.log", "gone.log"], scan, 0)
        self.assertTrue(sigs["a.log"].startswith("stat:"))
        self.assertEqual(sigs["gone.log"], "absent")
        sigs, _ = ledger.signatures(self.root, ["a.log"], scan, ledger.HASH_BUDGET)
        self.assertEqual(sigs["a.log"], digest(os.path.join(self.root, "a.log")))

    def link_root(self):
        """-> alias path of repo (symlink, else Windows junction); skip when neither creatable."""
        link = os.path.join(self.tmp, "alias")
        try:
            os.symlink(self.root, link, target_is_directory=True)
            return link
        except (OSError, NotImplementedError, AttributeError):
            pass
        if os.name == "nt":
            import subprocess
            done = subprocess.run(["cmd", "/c", "mklink", "/J", link, self.root], capture_output=True)
            if done.returncode == 0:
                return link
        self.skipTest("symlink/junction not creatable")

    def test_aliased_root_keeps_dirty_paths(self):
        self.git_setup()
        alias = self.link_root()
        alias_run = os.path.join(alias, ".init-project", "runs", "r1")
        code, out, _ = run("ledger.py", "baseline", alias, alias_run)
        self.assertEqual(code, 0, out)
        self.assertIn("dirty 2", out[1])
        self.write("src/app.ts", "user edit lost\n")
        self.write("src/new.ts", "new\n")
        for root, run_dir in ((alias, alias_run), (self.root, self.run_dir)):
            code, out, _ = run("ledger.py", "compare", root, run_dir, "--file", "CLAUDE.md", "--mode", "full")
            self.assertEqual(code, 1, out)
            self.assertIn("FAIL: dirty-changed: src/app.ts", out)
            self.assertIn("FAIL: outside-write: src/new.ts", out)

    def test_hash(self):
        code, out, _ = run("ledger.py", "hash", self.root, "CLAUDE.md", "gone.md")
        self.assertEqual(out, [f"CLAUDE.md {digest(os.path.join(self.root, 'CLAUDE.md'))}", "gone.md absent"])
        self.assertEqual(run("ledger.py", "hash", self.root, "../outside.md")[0], 2)
