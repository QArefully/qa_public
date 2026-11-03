"""Handoff integration regressions; role-policy walkthroughs are retained separately.

These exercise real helpers, not a simulated skill or harness run.
"""

from support import RepoCase, run


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
