"""Handoff integration regressions; role-policy walkthroughs are retained separately.

These exercise real helpers, not a simulated skill or harness run.
"""
import json
import os

from support import RepoCase, run
from test_round2 import digest


class DirectionalPlacement(RepoCase):
    def setUp(self):
        super().setUp()
        self.run_dir = os.path.join(self.root, ".init-project", "runs", "acceptance")
        self.targets = {
            "apps/api/src/features/checkout/CLAUDE.md": "checkout-C1",
            "apps/api/src/features/payments/CLAUDE.md": "payments-C1",
            "apps/api/src/features/promos/CLAUDE.md": "promos-C1",
            "apps/api/src/features/bundles/CLAUDE.md": "bundles-C1",
            "apps/api/CLAUDE.md": "api-C1",
        }
        for path in self.targets:
            self.write(path, "# Instructions\n- Verified source navigation.\n")
        self.write("apps/api/src/features/checkout/guard.ts", "export const guard = true;\n")
        self.write("apps/api/src/features/payments/provider.ts", "export const provider = true;\n")
        self.write("apps/api/src/features/promos/eligibility.ts", "export const eligible = true;\n")
        self.write("apps/api/src/features/bundles/price.ts", "export const price = 1;\n")
        self.write("apps/api/src/routes/invoices.ts", "export const route = true;\n")
        self.write("apps/api/test/invoices/route.test.ts", "test();\n")
        self.write(".gitignore", "*\n", base=self.run_dir)
        self.assertEqual(run("ledger.py", "baseline", self.root, self.run_dir)[0], 0)
        self.records = self.write("attempts/check-1/facts.md", (
            "### checkout-C1\nCheckout guard owns payment authorization.\n- verdict: confirmed\n"
            "- authority: apps/api/src/features/checkout/guard.ts\n- flow: checkout-FL1\n\n"
            "### payments-C1\nChange the provider response -> review the checkout guard contract.\n"
            "- verdict: confirmed\n- authority: apps/api/src/features/payments/provider.ts\n"
            "- evidence: apps/api/src/features/checkout/guard.ts\n\n"
            "### promos-C1\nChange promo eligibility -> review the checkout guard contract.\n"
            "- verdict: confirmed\n- authority: apps/api/src/features/promos/eligibility.ts\n"
            "- evidence: apps/api/src/features/checkout/guard.ts\n\n"
            "### bundles-C1\nChange bundle pricing -> review the checkout guard contract.\n"
            "- verdict: confirmed\n- authority: apps/api/src/features/bundles/price.ts\n"
            "- evidence: apps/api/src/features/checkout/guard.ts\n\n"
            "### api-C1\nChange invoice routes or mirrors -> review feature authority first.\n"
            "- verdict: confirmed\n- authority: apps/api/src/routes/invoices.ts\n"
            "- evidence: apps/api/test/invoices/route.test.ts\n"), base=self.run_dir)

    def routing(self, duplicate=False):
        targets = {path: {"disposition": "update", "facts": [fact], "batch": "b1"}
                   for path, fact in self.targets.items()}
        if duplicate:
            targets["apps/api/src/features/payments/CLAUDE.md"]["facts"] = ["checkout-C1"]
        return self.write("attempts/place-1/routing.json", json.dumps({
            "revision": "p1", "inputs": ["attempts/check-1/facts.md"], "targets": targets}), base=self.run_dir)

    def sidecar(self, duplicate=False):
        targets = {}
        for path, fact in self.targets.items():
            if duplicate and "/payments/" in path:
                fact = "checkout-C1"
            targets[path] = {"revision": digest(os.path.join(self.root, *path.split("/"))),
                             "facts": {fact: [2]}, "directives": {}}
        return self.write("provenance/b1.json", json.dumps({"batch": "b1", "targets": targets}), base=self.run_dir)

    def test_distinct_trigger_ids_and_homes_pass_project_and_index(self):
        routing = self.routing()
        projection = os.path.join(self.run_dir, "attempts", "project-1", "input.md")
        code, lines, err = run("ledger.py", "project", self.run_dir, routing, "--out", projection,
                               *self.targets)
        self.assertEqual(code, 0, (lines, err))
        self.assertNotIn("provider response", "\n".join(lines))
        index = os.path.join(self.run_dir, "attempts", "verify-1", "index.json")
        code, lines, err = run("ledger.py", "index", self.root, routing, self.sidecar(), "--out", index)
        self.assertEqual(code, 0, (lines, err))
        with open(index, encoding="utf-8") as handle:
            data = json.load(handle)
        self.assertEqual({fact for entry in data["targets"].values() for fact in entry["facts"]},
                         set(self.targets.values()))

    def test_same_id_two_homes_still_fails_both_helpers(self):
        routing = self.routing(duplicate=True)
        projection = os.path.join(self.run_dir, "attempts", "project-1", "input.md")
        code, lines, err = run("ledger.py", "project", self.run_dir, routing, "--out", projection,
                               *self.targets)
        self.assertEqual(code, 1, (lines, err))
        self.assertTrue(any("multiple-targets" in line for line in lines), lines)
        self.assertFalse(os.path.exists(projection))
        # Ownership is run-wide even when a writer receives just one batch target.
        code, lines, err = run("ledger.py", "project", self.run_dir, routing, "--out", projection,
                               "apps/api/src/features/checkout/CLAUDE.md")
        self.assertEqual(code, 1, (lines, err))
        self.assertTrue(any("multiple-targets" in line for line in lines), lines)
        self.assertFalse(os.path.exists(projection))
        index = os.path.join(self.run_dir, "attempts", "verify-1", "index.json")
        code, lines, err = run("ledger.py", "index", self.root, routing, self.sidecar(duplicate=True),
                               "--out", index)
        self.assertEqual(code, 1, (lines, err))
        self.assertTrue(any("fact-multiple-targets" in line for line in lines), lines)
        self.assertFalse(os.path.exists(index))

    def test_user_edit_invalidates_current_sidecar(self):
        sidecar = self.sidecar()
        target = "apps/api/src/features/payments/CLAUDE.md"
        self.write(target, "# Instructions\n- Verified source navigation.\n- User addition.\n")
        code, lines, err = run("ledger.py", "index", self.root, self.routing(), sidecar, "--out",
                               os.path.join(self.run_dir, "attempts", "verify-1", "index.json"))
        self.assertEqual(code, 1, (lines, err))
        self.assertTrue(any("stale-revision: " + target in line for line in lines), lines)
        with open(os.path.join(self.root, *target.split("/")), encoding="utf-8") as handle:
            self.assertIn("User addition.", handle.read())


class ConsequentialQuestions(RepoCase):
    def test_unassigned_and_outside_scope_remain_open_until_explicit_answer(self):
        run_dir = os.path.join(self.root, ".init-project", "runs", "acceptance")
        self.write(".gitignore", "*\n", base=run_dir)
        self.assertEqual(run("ledger.py", "baseline", self.root, run_dir)[0], 0)
        self.write("attempts/scout-1/note.md", (
            "### commerce-Q1\n- flow: commerce-FL1\n- contract: invoice guard outside accepted paths\n"
            "- owner: unassigned\n- status: open\n\n"
            "### commerce-Q2\n- contract: payment error owner\n- owner: payments\n- status: open\n"), base=run_dir)
        out = os.path.join(run_dir, "attempts", "questions-1", "index.md")
        code, lines, err = run("ledger.py", "questions", run_dir, "attempts/scout-1/note.md", "--out", out)
        self.assertEqual(code, 0, (lines, err))
        with open(out, encoding="utf-8") as handle:
            self.assertIn("commerce-Q1 | commerce-FL1 | invoice guard outside accepted paths | unassigned | open | -",
                          handle.read())
        self.write("attempts/check-1/gaps.md", "# Gaps\n- answered: commerce-Q2 -> payments-F1\n", base=run_dir)
        code, lines, err = run("ledger.py", "questions", run_dir, "attempts/scout-1/note.md", "--answers",
                               "attempts/check-1/gaps.md", "--out", out)
        self.assertEqual(code, 0, (lines, err))
        with open(out, encoding="utf-8") as handle:
            result = handle.read()
        self.assertIn("unassigned | open | -", result)
        self.assertIn("payments | answered | payments-F1", result)
        self.assertNotIn("invoice guard", "\n".join(lines))


class GeneratedReferences(RepoCase):
    def test_absent_install_outputs_are_missing_and_real_producer_passes(self):
        self.write("build/npm/postinstall.js", "// writes watcher configuration\n")
        self.write("src/bootstrap-node.js", "// injects remote dependencies\n")
        for missing in ("build/lib/watch/.yarnrc", "remote/node_modules", "src/broken.ts"):
            with self.subTest(path=missing):
                self.write("CLAUDE.md", "# Instructions\n- Read `" + missing + "`.\n")
                code, lines, err = run("check-paths.py", self.root, "CLAUDE.md")
                self.assertEqual(code, 1, (lines, err))
                self.assertIn("CLAUDE.md:2: missing: not-found: " + missing, lines)
        self.write("CLAUDE.md", "# Instructions\n"
                   "- Watcher install configuration is generated; review `build/npm/postinstall.js`.\n"
                   "- Remote dependency lookup is generated at install time; review `src/bootstrap-node.js`.\n")
        code, lines, err = run("check-paths.py", self.root, "CLAUDE.md")
        self.assertEqual(code, 0, (lines, err))
        self.assertEqual(lines[-1], "1 files, 0 missing, 0 format")
