import unittest

from support import RepoCase, run


class CheckShape(RepoCase):
    def setUp(self):
        super().setUp()
        self.write("src/a.ts")
        self.write("src/b.ts")
        self.write("src/c.ts")
        self.write("apps/api/main.ts", "import { runServer } from './runServer';\nrunServer();\n")
        self.write("apps/api/runServer.ts", "".join(f"line {n}\n" for n in range(10)))
        self.write("apps/api/services.ts", "".join(f"line {n}\n" for n in range(10)))

    def check(self, rel, text):
        self.write(rel, text)
        return run("check-shape.py", self.root, rel)

    def test_packed_trigger_fail(self):
        code, out, _ = self.check("CLAUDE.md", "- Change `src/a.ts` or `src/b.ts` -> review `src/c.ts`\n")
        self.assertEqual(code, 1)
        self.assertTrue(out[0].startswith("CLAUDE.md:1: FAIL: packed-trigger: 2 paths before ->"), out)
        self.assertEqual(out[-1], "1 files, 1 fail, 0 warn")

    def test_packed_trigger_maybe_warn(self):
        code, out, _ = self.check("CLAUDE.md", "- Change `src/a.ts` -> review `src/b.ts`, `src/c.ts#run`\n")
        self.assertEqual(code, 0)
        self.assertTrue(out[0].startswith("CLAUDE.md:1: WARN: packed-trigger-maybe: 3 paths"), out)

    def test_split_trigger_clean(self):
        text = "- Change `src/a.ts` -> review:\n  - `src/b.ts`: update types\n  - `src/c.ts`: update calls\n"
        code, out, _ = self.check("CLAUDE.md", text)
        self.assertEqual((code, out), (0, ["1 files, 0 fail, 0 warn"]))

    def test_same_path_twice_not_packed(self):
        code, out, _ = self.check("CLAUDE.md", "- `src/a.ts#x` and `src/a.ts#y` -> review tests\n")
        self.assertEqual(out, ["1 files, 0 fail, 0 warn"])

    def test_arrow_inside_code_span_ignored(self):
        code, out, _ = self.check("CLAUDE.md", "- `src/a.ts` maps `a->b` in `src/b.ts`\n")
        self.assertEqual(out, ["1 files, 0 fail, 0 warn"])

    def test_numbered_packed_trigger(self):
        code, out, _ = self.check("CLAUDE.md", "1. Change `src/a.ts` or `src/b.ts` -> review `src/c.ts`\n"
                                               "2) Edit `src/a.ts`, `src/c.ts` -> rerun\n")
        self.assertEqual(code, 1)
        self.assertTrue(out[0].startswith("CLAUDE.md:1: FAIL: packed-trigger"), out)
        self.assertTrue(out[1].startswith("CLAUDE.md:2: FAIL: packed-trigger"), out)

    def test_other_arrows(self):
        code, out, _ = self.check("CLAUDE.md", "- Change `src/a.ts` or `src/b.ts` → review\n"
                                               "- Change `src/a.ts` and `src/c.ts` => rerun\n")
        self.assertEqual(out[-1], "1 files, 2 fail, 0 warn")

    def test_prose_slash_not_packed(self):
        self.write("client/x.ts")
        self.write("server/x.ts")
        code, out, _ = self.check("CLAUDE.md", "- Change client/server split in `src/a.ts` -> review tests\n")
        self.assertEqual((code, out), (0, ["1 files, 0 fail, 0 warn"]))

    def test_orientation_skips_leading_heading(self):
        text = "# API\n\nAPI server; composition `services.ts`.\n\n## Architecture\n- `services.ts#wire` wires\n"
        code, out, _ = self.check("apps/api/CLAUDE.md", text)
        self.assertEqual(code, 1)
        self.assertIn("apps/api/CLAUDE.md:3: FAIL: orientation-repeat: services.ts also cited at line 6", out)

    def test_orientation_repeat(self):
        text = "API server; composition `services.ts`.\n\n## Architecture\n- `services.ts#createAppServices` wires repos\n"
        code, out, _ = self.check("apps/api/CLAUDE.md", text)
        self.assertEqual(code, 1)
        self.assertIn("apps/api/CLAUDE.md:1: FAIL: orientation-repeat: services.ts also cited at line 4", out)

    def test_orientation_conventional_and_shim(self):
        code, out, _ = self.check("apps/api/CLAUDE.md", "API server; entry `main.ts`.\n\n- Startup in `runServer.ts`.\n")
        self.assertEqual(code, 0)
        joined = "\n".join(out)
        self.assertIn("WARN: orientation-conventional: main.ts", joined)
        self.assertIn("WARN: orientation-shim: main.ts", joined)
        self.assertEqual(out[-1], "1 files, 0 fail, 2 warn")

    def test_orientation_without_pointer_not_reported(self):
        code, out, _ = self.check("apps/api/CLAUDE.md", "API server subtree.\n\n- Startup in `runServer.ts`.\n")
        self.assertEqual((code, out), (0, ["1 files, 0 fail, 0 warn"]))

    def test_root_file_has_no_orientation_rules(self):
        code, out, _ = self.check("CLAUDE.md", "# Agent instructions `src/a.ts`\n\n- `src/a.ts` again\n")
        self.assertEqual(out, ["1 files, 0 fail, 0 warn"])

    def test_walk_all_files(self):
        self.write("CLAUDE.md", "# Agent instructions\n")
        self.write("apps/api/AGENTS.md", "API; `index.ts`\n")
        code, out, _ = run("check-shape.py", self.root)
        self.assertEqual(out[-1], "2 files, 0 fail, 1 warn")


if __name__ == "__main__":
    unittest.main()
