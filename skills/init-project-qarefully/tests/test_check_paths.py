import os
import unittest

from support import RepoCase, run


class CheckPaths(RepoCase):
    def setUp(self):
        super().setUp()
        self.write("src/app.ts")
        self.write("src/main.ts")
        self.write("package.json", "{}\n")
        self.write("apps/api/server.ts")
        self.write("apps/api/lib/db.ts")

    def check(self, text, rel="CLAUDE.md", *extra):
        self.write(rel, text)
        return run("check-paths.py", self.root, *extra)

    def test_clean_file_exit_zero(self):
        code, out, _ = self.check("# Agent instructions\n\n- Entry `src/app.ts`; config package.json.\n")
        self.assertEqual(code, 0)
        self.assertEqual(out[-1], "1 files, 0 missing, 0 format")

    def test_file_symbol_valid(self):
        code, out, _ = self.check("- `src/app.ts#createApp` and src/main.ts#run and `src/app.ts:12-20`\n")
        self.assertEqual(code, 0, out)

    def test_file_symbol_missing_path_reports_path_only(self):
        code, out, _ = self.check("- `src/gone.ts#createApp`\n")
        self.assertEqual(code, 1)
        self.assertEqual(out[0], "CLAUDE.md:1: missing: not-found: src/gone.ts")

    def test_genuine_missing_path(self):
        code, out, _ = self.check("intro\n- See `src/missing.ts`.\n")
        self.assertEqual(code, 1)
        self.assertIn("CLAUDE.md:2: missing: not-found: src/missing.ts", out)
        self.assertEqual(out[-1], "1 files, 1 missing, 0 format")

    def test_approved_external_path(self):
        ext = os.path.join(self.tmp, "external", "runs").replace("\\", "/")
        text = f"- Run folder `{ext}/2026/notes.md`\n"
        code, out, _ = self.check(text, "CLAUDE.md", "--allow-external", os.path.join(self.tmp, "external"))
        self.assertEqual(code, 0, out)
        code, out, _ = self.check(text)
        self.assertEqual(code, 1)
        self.assertIn("format: absolute", out[0])

    def test_allow_external_requires_absolute_prefix(self):
        code, _, err = self.check("x\n", "CLAUDE.md", "--allow-external", "relative/dir")
        self.assertEqual(code, 2)
        self.assertIn("absolute", err)

    def test_same_directory_full_path(self):
        code, out, _ = self.check("Scope.\n- `apps/api/server.ts` and `server.ts`\n", "apps/api/CLAUDE.md")
        self.assertEqual(code, 1)
        self.assertEqual(out[0], "apps/api/CLAUDE.md:2: format: same-dir-full-path: apps/api/server.ts")
        self.assertEqual(out[-1], "1 files, 0 missing, 1 format")

    def test_nested_relative(self):
        code, out, _ = self.check("Scope.\n- `lib/db.ts`\n", "apps/api/CLAUDE.md")
        self.assertEqual(out[0], "apps/api/CLAUDE.md:2: format: nested-relative: lib/db.ts")

    def test_format_categories(self):
        text = ("- [app](src/app.ts)\n- `./src/app.ts`\n- `src\\app.ts`\n- `C:/work/x.ts`\n"
                "- `/home/me/x.ts`\n")
        code, out, _ = self.check(text)
        self.assertEqual(code, 1)
        joined = "\n".join(out)
        for detail in ("markdown-link", "relative-prefix", "backslash", "absolute"):
            self.assertIn(f"format: {detail}", joined)
        self.assertIn("CLAUDE.md:5: format: absolute: /home/me/x.ts", out)

    def test_markdown_link_reported_once(self):
        code, out, _ = self.check("- [guide](../docs/x.md) and [app](https://x.io/a.md)\n")
        self.assertEqual(out, ["CLAUDE.md:1: format: markdown-link: ../docs/x.md", "1 files, 0 missing, 1 format"])

    def test_ambiguous_tokens_skipped(self):
        text = ("Uses Node.js and res.json() plus `process.env` and `import.meta.env`.\n"
                "Prose read/write, example.com/api.json, route `/api/users.json`, `@scope/pkg`, `apps/*/CLAUDE.md`.\n"
                "Unquoted helper.json mention, `AGENTS.md/CLAUDE.md`, `npm run build.ts`, https://x.io/a.md\n"
                "```\nsrc/nothing.ts\n```\n")
        code, out, _ = self.check(text)
        self.assertEqual(code, 0, out)

    def test_prose_slash_with_existing_dirs_skipped(self):
        self.write("client/x.ts")
        self.write("server/x.ts")
        self.write("types/x.ts")
        code, out, _ = self.check("- Split client/server and types/interfaces; see src/ and apps/api\n")
        self.assertEqual(code, 0, out)
        code, out, _ = self.check("- See client/gone/\n")
        self.assertEqual(out[0], "CLAUDE.md:1: missing: not-found: client/gone/")

    def test_pytest_node_and_symbol_suffix(self):
        self.write("tests/test_api.py")
        text = ("- `tests/test_api.py::TestOrders::test_create[slow]` and tests/test_api.py::test_x\n"
                "- `src/app.ts:createApp` and src/main.ts:run\n")
        code, out, _ = self.check(text)
        self.assertEqual(code, 0, out)
        code, out, _ = self.check("- `tests/gone.py::test_x` `src/gone.ts:createApp`\n")
        self.assertEqual(out[:2], ["CLAUDE.md:1: missing: not-found: tests/gone.py",
                                   "CLAUDE.md:1: missing: not-found: src/gone.ts"])

    def test_low_ambiguities_skipped(self):
        text = ("- Built with `Node.js`, `Next.js`; see [setup](#setup), [mail](mailto:a@b.io)\n"
                "- Dev server `localhost:3000/api/users.json` and 127.0.0.1:8080/x.json\n"
                "- Copy `.env.example` to `.env`; local `.env.local`\n")
        self.write(".env.example", "A=1\n")
        code, out, _ = self.check(text)
        self.assertEqual(code, 0, out)
        code, out, _ = self.check("- `apps/.env.sample`\n")
        self.assertEqual(out[0], "CLAUDE.md:1: missing: not-found: apps/.env.sample")

    def test_extended_extensions(self):
        code, out, _ = self.check("- `schema.graphql` `go.mod` `deploy.ps1` `main.tf` `build.gradle.kts` `x.dart`"
                                  " `init.lua` `A.scala` `page.astro` `q.gql` `go.sum`\n")
        self.assertEqual(out[-1], "1 files, 11 missing, 0 format")

    def test_backslash_windows_path_under_allow_external(self):
        ext = os.path.join(self.tmp, "external")
        windows = ext.replace("/", "\\") + "\\runs\\notes.md"
        code, out, _ = self.check(f"- Run notes `{windows}`\n", "CLAUDE.md", "--allow-external", ext)
        self.assertEqual(code, 0, out)

    def test_backticked_bare_missing_reported(self):
        code, out, _ = self.check("- `helper.json`\n")
        self.assertEqual(out[0], "CLAUDE.md:1: missing: not-found: helper.json")

    def test_extensionless_directory_token(self):
        code, out, _ = self.check("- `src/` and `src/nope`\n")
        self.assertEqual(out[0], "CLAUDE.md:1: missing: not-found: src/nope")

    def test_file_args_limit_scope(self):
        self.write("CLAUDE.md", "- `src/missing.ts`\n")
        self.write("apps/api/CLAUDE.md", "Scope.\n- `server.ts`\n")
        code, out, _ = run("check-paths.py", self.root, "apps/api/CLAUDE.md")
        self.assertEqual(code, 0)
        self.assertEqual(out, ["1 files, 0 missing, 0 format"])
        code, out, _ = run("check-paths.py", self.root)
        self.assertEqual(out[-1], "2 files, 1 missing, 0 format")

    def test_bad_file_arg_usage_error(self):
        code, _, _ = run("check-paths.py", self.root, "nope/CLAUDE.md")
        self.assertEqual(code, 2)
        self.assertEqual(run("check-paths.py", os.path.join(self.root, "absent"))[0], 2)

    def test_skip_dirs_and_crlf(self):
        self.write("node_modules/x/CLAUDE.md", "`gone.ts`\n")
        self.write(".init-project/runs/1/CLAUDE.md", "`gone.ts`\n")
        code, out, _ = self.check("# T\r\n- `src/app.ts`\r\n- `src/gone.ts`\r\n")
        self.assertEqual(out, ["CLAUDE.md:3: missing: not-found: src/gone.ts", "1 files, 1 missing, 0 format"])


if __name__ == "__main__":
    unittest.main()
