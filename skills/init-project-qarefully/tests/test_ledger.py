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


SCOUT = """# Scout note api

### api-C1
Orders persist before notify.
- confidence: high
- authority: src/orders.ts#create

### api-C2
Retries never exceed 3.
- confidence: low
- authority: src/retry.ts#run

### api-C3
Cache is shared.
- confidence: high
- authority: src/cache.ts:4

### api-C4
Webhooks idempotent.
- confidence: low
- authority: src/hooks.ts#handle

### api-Q1
- flow: api-FL1
- contract: who validates payload
- owner: web
- status: open

- api-FL1 checkout flow (bullet, not record)
"""

CHECKER = """# Checker api

### api-C2
Retries capped at 3 by MAX_RETRY.
- verdict: corrected
- authority: src/retry.ts#MAX_RETRY

Evidence: src/retry.ts lines 3-9.

### api-C3
- verdict: refuted
- authority: src/cache.ts:4

### api-F1
Late addition.
- verdict: confirmed
- authority: src/late.ts#x
"""


class Records(RepoCase):
    def setUp(self):
        super().setUp()
        self.run_dir = os.path.join(self.root, ".init-project", "runs", "r1")
        self.write("notes/scout-api.md", SCOUT, base=self.run_dir)
        self.write("verified/checker-api.md", CHECKER, base=self.run_dir)
        self.assertEqual(run("ledger.py", "baseline", self.root, self.run_dir)[0], 0)

    def routing(self, targets, name="routing.json", inputs=("notes/scout-api.md", "verified/checker-api.md")):
        data = {"revision": "p1", "inputs": list(inputs), "targets": targets}
        return self.write(name, json.dumps(data), base=self.run_dir)

    def project(self, routing, *targets, out=None):
        out = out or os.path.join(self.run_dir, "writer-input.md")
        code, lines, _ = run("ledger.py", "project", self.run_dir, routing, "--out", out, *targets)
        return code, lines, out

    def test_project_projects_placeable_records(self):
        routing = self.routing({"CLAUDE.md": {"disposition": "update", "facts": ["api-C1", "api-C2", "api-F1"],
                                              "directives": ["existing CLAUDE.md:3"], "batch": "b1"},
                                "apps/web/CLAUDE.md": {"disposition": "create", "facts": ["api-C3"], "batch": "b2"}})
        code, lines, out = self.project(routing, "CLAUDE.md")
        self.assertEqual(code, 0, lines)
        self.assertEqual(lines, [f"PASS: project {out.replace(os.sep, '/')}: 1 targets, 3 facts"])
        with open(out, encoding="utf-8") as handle:
            text = handle.read()
        self.assertIn("### api-C1\nOrders persist before notify.", text)
        self.assertIn("Retries capped at 3 by MAX_RETRY.", text)  # checker preferred
        self.assertIn("Evidence: src/retry.ts lines 3-9.", text)  # full record text
        self.assertNotIn("never exceed", text)
        self.assertNotIn("api-C3", text)  # unassigned / refuted
        self.assertNotIn("api-Q1", text)
        self.assertNotIn("api-FL1", text)
        self.assertIn("- directives: existing CLAUDE.md:3", text)

    def test_project_refuses_refuted(self):
        routing = self.routing({"CLAUDE.md": {"disposition": "update", "facts": ["api-C1", "api-C3"], "batch": "b1"}})
        code, lines, out = self.project(routing, "CLAUDE.md")
        self.assertEqual(code, 1)
        self.assertIn("FAIL: refuted: CLAUDE.md api-C3", lines)
        self.assertFalse(os.path.exists(out))

    def test_project_refuses_low_confidence_and_missing(self):
        routing = self.routing({"CLAUDE.md": {"disposition": "update", "facts": ["api-C4", "api-C9"], "batch": "b1"}})
        code, lines, out = self.project(routing, "CLAUDE.md")
        self.assertEqual(code, 1)
        self.assertIn("FAIL: low-confidence: CLAUDE.md api-C4", lines)
        self.assertIn("FAIL: missing: CLAUDE.md api-C9", lines)
        self.assertFalse(os.path.exists(out))

    def test_project_unrouted_target_and_bad_input(self):
        routing = self.routing({})
        self.assertEqual(self.project(routing, "CLAUDE.md")[0], 1)
        bad = self.write("bad.json", "{not json", base=self.run_dir)
        self.assertEqual(self.project(bad, "CLAUDE.md")[0], 2)

    def test_project_conflict_verdict_refused(self):
        self.write("verified/checker-api.md", CHECKER + "\n### api-C1\n- verdict: conflict\n- authority: src/o.ts:1\n",
                   base=self.run_dir)
        routing = self.routing({"CLAUDE.md": {"disposition": "update", "facts": ["api-C1"], "batch": "b1"}})
        code, lines, _ = self.project(routing, "CLAUDE.md")
        self.assertEqual(code, 1)
        self.assertIn("FAIL: refuted: CLAUDE.md api-C1", lines)

    def test_project_superseded(self):
        self.write("attempts/check-2/facts.md", "### api-R1-C1\nOrders persist then notify async.\n"
                   "- verdict: confirmed\n- authority: src/orders.ts#create\n- supersedes: api-C1\n", base=self.run_dir)
        inputs = ("notes/scout-api.md", "verified/checker-api.md", "attempts/check-2/facts.md")
        routing = self.routing({"CLAUDE.md": {"disposition": "update", "facts": ["api-C1"], "batch": "b1"}},
                               inputs=inputs)
        code, lines, _ = self.project(routing, "CLAUDE.md")
        self.assertEqual(code, 1)
        self.assertIn("FAIL: superseded: CLAUDE.md api-C1 by api-R1-C1", lines)
        routing = self.routing({"CLAUDE.md": {"disposition": "update", "facts": ["api-R1-C1"], "batch": "b1"}},
                               inputs=inputs)
        code, lines, out = self.project(routing, "CLAUDE.md")
        self.assertEqual(code, 0, lines)
        with open(out, encoding="utf-8") as handle:
            self.assertIn("### api-R1-C1\nOrders persist then notify async.", handle.read())

    def test_project_unlisted_facts_veto(self):
        routing = self.routing({"CLAUDE.md": {"disposition": "update", "facts": ["api-C1", "api-F1"], "batch": "b1"}})
        self.write("quarantine/check-old/facts.md", "### api-C1\n- verdict: refuted\n- authority: x.ts:1\n",
                   base=self.run_dir)
        self.write("baseline/before/docs/facts.md", "### api-F1\n- verdict: refuted\n", base=self.run_dir)
        self.assertEqual(self.project(routing, "CLAUDE.md")[0], 0)  # quarantine + baseline ignored
        self.write("attempts/check-3/facts.md", "### api-C1\n- verdict: refuted\n- authority: x.ts:1\n\n"
                   "### api-F2\n- verdict: confirmed\n- authority: y.ts:1\n- supersedes: api-F1\n", base=self.run_dir)
        code, lines, out = self.project(routing, "CLAUDE.md")
        self.assertEqual(code, 1)
        self.assertIn("FAIL: refuted: CLAUDE.md api-C1", lines)
        self.assertIn("FAIL: superseded: CLAUDE.md api-F1 by api-F2", lines)
        self.assertFalse(os.path.exists(out))  # stale --out from first run deleted

    def test_project_delete_target(self):
        routing = self.routing({"old/CLAUDE.md": {"disposition": "delete", "facts": [], "batch": "b1"}})
        code, lines, out = self.project(routing, "old/CLAUDE.md")
        self.assertEqual(code, 0, lines)
        self.assertEqual(lines[0], f"PASS: project {out.replace(os.sep, '/')}: 1 targets, 0 facts")

    def test_out_guard(self):
        routing = self.routing({"CLAUDE.md": {"disposition": "update", "facts": ["api-C1"], "batch": "b1"}})
        victim = self.write("docs/notes.md", "user file\n")
        for out in (os.path.join(self.run_dir, "AGENTS.md"), os.path.join(self.run_dir, "x", "claude.md"),
                    os.path.join(self.root, ".claude", "out.md"), os.path.join(self.run_dir, ".agents", "out.md"),
                    victim, os.path.join(self.run_dir, "baseline", "out.md")):
            code, lines, err = run("ledger.py", "project", self.run_dir, routing, "--out", out, "CLAUDE.md")
            self.assertEqual(code, 2, (out, lines))
            self.assertIn("--out", err)
        with open(victim, encoding="utf-8") as handle:
            self.assertEqual(handle.read(), "user file\n")  # refused out never deleted
        outside = os.path.join(self.tmp, "elsewhere", "writer-input.md")
        self.assertEqual(self.project(routing, "CLAUDE.md", out=outside)[0], 0)

    def test_out_guard_external_run_dir(self):
        external = os.path.join(self.tmp, "external", "r1")
        self.write("facts.md", "### api-C1\nOrders persist.\n- verdict: confirmed\n- authority: src/o.ts:1\n",
                   base=external)
        self.assertEqual(run("ledger.py", "baseline", self.root, external, "--external-run")[0], 0)
        routing = self.write("attempts/place-1/routing.json", json.dumps({"revision": "p1", "inputs": ["facts.md"],
                             "targets": {"CLAUDE.md": {"disposition": "update", "facts": ["api-C1"], "batch": "b1"}}}),
                             base=external)
        out = os.path.join(external, "attempts", "write-1", "writer-input.md")
        code, lines, _ = run("ledger.py", "project", external, routing, "--out", out, "CLAUDE.md")
        self.assertEqual(code, 0, lines)
        manifest = os.path.join(external, "manifest.txt")
        code, lines, _ = run("ledger.py", "manifest", self.root, routing, "--out", manifest)
        self.assertEqual(code, 0, lines)
        code, _, err = run("ledger.py", "manifest", self.root, routing, "--out", os.path.join(self.root, "m.txt"))
        self.assertEqual(code, 2, err)

    def test_malformed_routing_shapes(self):
        for data in ([], {"targets": []}, {"targets": {"CLAUDE.md": []}}, {"targets": {"CLAUDE.md": {"facts": "x"}}},
                     {"targets": {"CLAUDE.md": {"disposition": "rewrite"}}}, {"inputs": "x", "targets": {}}):
            routing = self.write("bad-routing.json", json.dumps(data), base=self.run_dir)
            code, _, err = self.project(routing, "CLAUDE.md")
            self.assertEqual(code, 2, data)
            self.assertNotIn("Traceback", err)

    def test_questions(self):
        self.write("notes/scout-web.md", "### web-Q1\n- flow: web-FL2\n- contract: a | b\n- owner: unassigned\n"
                   "- status: open\n\n### api-Q1\n- status: gap\n", base=self.run_dir)
        out = os.path.join(self.run_dir, "questions.md")
        code, lines, _ = run("ledger.py", "questions", self.run_dir, "notes/scout-api.md", "notes/scout-web.md",
                             "--out", out)
        self.assertEqual(code, 1)
        self.assertIn("FAIL: duplicate-id: api-Q1", lines)
        self.assertFalse(os.path.exists(out))  # FAIL -> nothing written
        self.write("notes/scout-web.md", "### web-Q1\n- flow: web-FL2\n- contract: a | b\n- owner: unassigned\n"
                   "- status: open\n", base=self.run_dir)
        code, lines, _ = run("ledger.py", "questions", self.run_dir, "notes/scout-api.md", "notes/scout-web.md",
                             "--out", out)
        self.assertEqual(code, 0, lines)
        with open(out, encoding="utf-8") as handle:
            index = handle.read().splitlines()
        self.assertEqual(index[0], "api-Q1 | api-FL1 | who validates payload | web | open | -")
        self.assertEqual(index[1], "web-Q1 | web-FL2 | a / b | unassigned | open | -")
        code, lines, _ = run("ledger.py", "questions", self.run_dir, "notes/scout-api.md", "notes/scout-api.md",
                             "--out", out)
        self.assertEqual(code, 1)
        self.assertFalse(os.path.exists(out))  # stale --out deleted on FAIL

    def test_questions_answers(self):
        self.write("attempts/check-1/gaps.md", "# Gaps\n- answered: api-Q1 -> api-C1\nanswered: `nope-Q9` -> x-C1\n",
                   base=self.run_dir)
        self.write("notes/scout-api-R1.md", "### api-R1-Q1\n- flow: api-FL1\n- contract: retry owner\n"
                   "- owner: api\n- status: open\n", base=self.run_dir)
        out = os.path.join(self.run_dir, "questions.md")
        code, lines, _ = run("ledger.py", "questions", self.run_dir, "notes/scout-api.md", "notes/scout-api-R1.md",
                             "--answers", "attempts/check-1/gaps.md", "--out", out)
        self.assertEqual(code, 0, lines)
        self.assertIn("WARN: unknown-question: nope-Q9", lines)
        with open(out, encoding="utf-8") as handle:
            index = handle.read().splitlines()
        self.assertEqual(index, ["api-Q1 | api-FL1 | who validates payload | web | answered | api-C1",
                                 "api-R1-Q1 | api-FL1 | retry owner | api | open | -"])


class Index(RepoCase):
    def setUp(self):
        super().setUp()
        self.run_dir = os.path.join(self.root, ".init-project", "runs", "r1")
        self.target = self.write("CLAUDE.md", "# Agent instructions\n- fact one\n- fact two\n")
        self.write("old/CLAUDE.md", "stale\n")
        self.routing = self.write("routing.json", json.dumps({"revision": "p1", "inputs": [], "targets": {
            "CLAUDE.md": {"disposition": "update", "facts": ["a-C1", "a-C2"], "directives": [], "batch": "b1"},
            "old/CLAUDE.md": {"disposition": "delete", "facts": [], "batch": "b1"}}}), base=self.run_dir)
        self.assertEqual(run("ledger.py", "baseline", self.root, self.run_dir)[0], 0)

    def sidecar(self, facts, revision=None, extra=None):
        targets = {"CLAUDE.md": {"revision": revision or digest(self.target), "facts": facts, "directives": {}},
                   "old/CLAUDE.md": {"revision": "absent", "facts": {}}}
        targets.update(extra or {})
        return self.write("provenance/provenance-b1.json", json.dumps({"batch": "b1", "targets": targets}),
                          base=self.run_dir)

    def index(self, *sidecars):
        out = os.path.join(self.run_dir, "index.json")
        code, lines, _ = run("ledger.py", "index", self.root, self.routing, *sidecars, "--out", out)
        return code, lines, out

    def test_index_pass(self):
        os.remove(os.path.join(self.root, "old", "CLAUDE.md"))
        code, lines, out = self.index(self.sidecar({"a-C1": [2], "a-C2": [3]}))
        self.assertEqual(code, 0, lines)
        with open(out, encoding="utf-8") as handle:
            data = json.load(handle)
        self.assertEqual(data["targets"]["CLAUDE.md"]["facts"], {"a-C1": [2], "a-C2": [3]})
        self.assertEqual(data["targets"]["old/CLAUDE.md"]["revision"], "absent")

    def test_delete_target_present(self):
        code, lines, out = self.index(self.sidecar({"a-C1": [2], "a-C2": [3]}))
        self.assertEqual(code, 1)
        self.assertIn("FAIL: delete-present: old/CLAUDE.md", lines)
        self.assertFalse(os.path.exists(out))

    def test_missing_provenance_routed_but_unwritten(self):
        os.remove(os.path.join(self.root, "old", "CLAUDE.md"))
        code, lines, _ = self.index(self.sidecar({"a-C1": [2]}))
        self.assertEqual(code, 1)
        self.assertIn("FAIL: missing-provenance: CLAUDE.md a-C2", lines)

    def test_missing_sidecar_entirely(self):
        os.remove(os.path.join(self.root, "old", "CLAUDE.md"))
        empty = self.write("provenance/provenance-b2.json", json.dumps({"batch": "b2", "targets": {}}), base=self.run_dir)
        code, lines, _ = self.index(empty)
        self.assertIn("FAIL: missing-provenance: CLAUDE.md a-C1", lines)

    def test_stale_sidecar_revision(self):
        os.remove(os.path.join(self.root, "old", "CLAUDE.md"))
        sidecar = self.sidecar({"a-C1": [2], "a-C2": [3]})
        self.write("CLAUDE.md", "# Agent instructions\n- fact one\n- fact two\n- user edit\n")
        code, lines, _ = self.index(sidecar)
        self.assertEqual(code, 1)
        self.assertTrue(any(line.startswith("FAIL: stale-revision: CLAUDE.md") for line in lines), lines)

    def test_unrouted_multi_target_and_range(self):
        self.write("apps/CLAUDE.md", "one\n")
        os.remove(os.path.join(self.root, "old", "CLAUDE.md"))
        sidecar = self.sidecar({"a-C1": [2], "a-C2": [9], "a-C3": [1]})
        other = self.write("provenance/provenance-b2.json", json.dumps({"batch": "b2", "targets": {
            "apps/CLAUDE.md": {"revision": digest(os.path.join(self.root, "apps", "CLAUDE.md")), "facts": {"a-C1": [1]}}}}),
            base=self.run_dir)
        code, lines, _ = self.index(sidecar, other)
        self.assertEqual(code, 1)
        self.assertIn("FAIL: line-out-of-range: CLAUDE.md a-C2:9", lines)
        self.assertIn("FAIL: unrouted-fact: CLAUDE.md a-C3", lines)
        self.assertIn("FAIL: unrouted-target: apps/CLAUDE.md", lines)
        self.assertIn("FAIL: fact-multiple-targets: a-C1: CLAUDE.md, apps/CLAUDE.md", lines)

    def test_non_delete_target_missing(self):
        os.remove(self.target)
        code, lines, _ = self.index(self.sidecar({"a-C1": [2], "a-C2": [3]}, revision="abc"))
        self.assertIn("FAIL: target-missing: CLAUDE.md", lines)

    def set_routing(self, targets):
        self.routing = self.write("routing.json", json.dumps({"revision": "p2", "inputs": [], "targets": targets}),
                                  base=self.run_dir)

    def test_directive_missing_provenance(self):
        os.remove(os.path.join(self.root, "old", "CLAUDE.md"))
        self.set_routing({"CLAUDE.md": {"disposition": "update", "facts": ["a-C1"], "batch": "b1",
                                        "directives": ["existing CLAUDE.md:2-3", "existing CLAUDE.md:1"]}})
        sidecar = self.write("provenance/provenance-b1.json", json.dumps({"batch": "b1", "targets": {"CLAUDE.md": {
            "revision": digest(self.target), "facts": {"a-C1": [2]}, "directives": {"existing CLAUDE.md:2-3": [3]}}}}),
            base=self.run_dir)
        code, lines, _ = self.index(sidecar)
        self.assertEqual(code, 1)
        self.assertEqual(lines[0], "FAIL: missing-provenance: CLAUDE.md existing CLAUDE.md:1")

    def test_create_target_needs_sidecar_entry(self):
        self.write("apps/CLAUDE.md", "API\n")
        os.remove(os.path.join(self.root, "old", "CLAUDE.md"))
        self.set_routing({"apps/CLAUDE.md": {"disposition": "create", "facts": [], "batch": "b1"},
                          "CLAUDE.md": {"disposition": "keep", "facts": [], "batch": "b1"}})
        empty = self.write("provenance/provenance-b1.json", json.dumps({"batch": "b1", "targets": {}}), base=self.run_dir)
        code, lines, _ = self.index(empty)
        self.assertEqual(code, 1)
        self.assertEqual(lines[0], "FAIL: missing-provenance: apps/CLAUDE.md")
        self.assertEqual(len(lines), 2, lines)  # keep target needs no entry

    def test_delete_has_facts_and_sidecar_revision(self):
        os.remove(os.path.join(self.root, "old", "CLAUDE.md"))
        self.set_routing({"old/CLAUDE.md": {"disposition": "delete", "facts": ["a-C9"], "batch": "b1"}})
        sidecar = self.write("provenance/provenance-b1.json", json.dumps({"batch": "b1", "targets": {
            "old/CLAUDE.md": {"revision": "abc123", "facts": {}}}}), base=self.run_dir)
        code, lines, _ = self.index(sidecar)
        self.assertEqual(code, 1)
        self.assertIn("FAIL: delete-has-facts: old/CLAUDE.md a-C9", lines)
        self.assertIn("FAIL: stale-revision: old/CLAUDE.md abc123 != absent", lines)

    def test_malformed_sidecar_shapes(self):
        os.remove(os.path.join(self.root, "old", "CLAUDE.md"))
        for data in ([], {"batch": "b1", "targets": []}, {"targets": {}}, {"batch": "b1", "targets": {"CLAUDE.md": 1}},
                     {"batch": "b1", "targets": {"CLAUDE.md": {"facts": ["a-C1"]}}},
                     {"batch": "b1", "targets": {"CLAUDE.md": {"revision": 5}}}):
            sidecar = self.write("provenance/bad.json", json.dumps(data), base=self.run_dir)
            code, _, err = self.index(sidecar)
            self.assertEqual(code, 2, data)
            self.assertNotIn("Traceback", err)

    def test_index_out_to_instruction_file_refused(self):
        os.remove(os.path.join(self.root, "old", "CLAUDE.md"))
        sidecar = self.sidecar({"a-C1": [2], "a-C2": [3]})
        before = digest(self.target)
        for out in (self.target, os.path.join(self.run_dir, "AGENTS.md"), os.path.join(self.root, "index.json")):
            code, _, err = run("ledger.py", "index", self.root, self.routing, sidecar, "--out", out)
            self.assertEqual(code, 2, out)
            self.assertIn("--out", err)
        self.assertEqual(digest(self.target), before)

    def test_routing_outside_run_dir_refused(self):
        routing = self.write("routing.json", json.dumps({"targets": {}}), base=os.path.join(self.tmp, "loose"))
        code, _, err = run("ledger.py", "manifest", self.root, routing, "--out", os.path.join(self.run_dir, "m.txt"))
        self.assertEqual(code, 2)
        self.assertIn("run dir", err)

    def test_manifest_sanitized(self):
        out = os.path.join(self.run_dir, "manifest.txt")
        code, lines, _ = run("ledger.py", "manifest", self.root, self.routing, "--out", out)
        self.assertEqual(code, 0, lines)
        with open(out, encoding="utf-8") as handle:
            text = handle.read()
        self.assertEqual(text.splitlines(), [f"CLAUDE.md update {digest(self.target)}",
                                             f"old/CLAUDE.md delete {digest(os.path.join(self.root, 'old', 'CLAUDE.md'))}"])
        self.assertNotIn("a-C1", text)


if __name__ == "__main__":
    unittest.main()
