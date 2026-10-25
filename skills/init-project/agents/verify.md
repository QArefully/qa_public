# Verify

Report-only acceptance checks; no instruction-file repair or new factual verdicts. Full: dedicated verify worker. Light: reviewer enters explicit Verify phase after repairs/mapping reconciliation; prior edit authority ends. Follow supplied [contracts](../references/contracts.md); read [policy](../references/repository-analysis.md), [generated content](../references/generated-content.md), bundled style. No entrypoint/conversation inheritance.

## Inputs and authority

- shared: repository root, mode/file choice, current generated files/revisions, actual run folder + exact manifest/baseline paths, review/fixer decision replies, resolved path-helper, assigned report path.
- Full: accepted current placement + verified-facts paths, producer conflicts/skipped sections (scan/checkers/placement).
- Light: producer-supplied final mapping/verdict refs + evidence-verdict audit result + conflicts/skipped extracts + flow summary only; never notes/verdict/placement access. Evidence-verdict audit belongs to checker/placement, not reviewer.
- Read source/generated files + listed verification inputs; read-only Git/baseline comparisons; path helper. Write assigned report only. Missing input/audit/check capability -> blocked, never assumed pass.

## Boundary checks

- Compare actual task writes against immutable baseline, accounting for pre-existing dirty/untracked changes + approved external run folder. No task writes outside mode-approved primary instruction files + actual run folder; repository `.gitignore` unchanged. Unexpected write -> file/line (or path) + impact; outside-write failure never authorizes more writes.
- `AGENTS.md` chosen -> no `CLAUDE.md` or `.claude/` changes. `CLAUDE.md` chosen -> no `AGENTS.md` or `.agents/` changes. Light -> no nested instruction changes.
- Actual run folder allowed; inner `.gitignore` contains `*`; manifest/baseline present. Bundled style resource never copied outside skill directory.
- Reviewer permissions from baseline + producer replies: Full no run-folder writes; Light only assigned Verify/report artifacts, no notes/verdict/placement edits. Do not demand proof of runtime reads.
- Review final-pass diff for lost scope/meaning or unsupported formatting change; protect pre-existing/user/task-generated changes. Application tests only if changes beyond instruction files separately authorized; this workflow does not authorize those changes/tests.

## Evidence and usefulness checks

- Full: every generated factual line maps through placement to exact confirmed/corrected verdict covering wording/conditions/scope, including orientation/runtime/commands/late edits. Refuted absent; unresolved omitted or reported. Mandatory/generated + preserved user/process directives exempt, embedded factual assertions still checked.
- Light: compare final files/current revisions with supplied final mapping + successful producer audit; no independent underlying verdict audit. Missing mapping/audit -> failure.
- Questionable factual support -> failure to checker route, never new Verify verdict. Pitfalls evidence-backed; empty/low-value sections -> fixer finding.
- Material gaps resolved or reported; nonstandard architecture documented, rationale supported or explicitly unknown; complex domains have actionable entry/authority pointers.
- Explicit source pointers exist; cited file itself contains claimed thing, not sibling/caller. Run `python -B <resolved-skill-directory>/scripts/check-paths.py <repository-root>` with Python 3 stdlib only. Helper reads instruction files, writes stdout only; exit 0 clean, 1 reports, 2 usage error. Judge heuristic missing/format reports in context; failure -> fixer. Missing Python/helper -> blocked check.
- Flow entry (including sole headingless section) maps through flow-ID group to checked facts, meets doc-worthy threshold, lives once in owning-domain nested file. Light uses supplied mapping; distilled flows never create root Flows section.

## Shape checks

- Root starts `# Agent instructions` + one-line project description; no root `## Flows`. Mandatory Maintenance + AI Documentation rules in root only; legend includes only used labels/intent marker.
- One-fact bullets; multi-fact entries + multi-file change triggers use sub-bullets. Labels match checked placement wording. Nested opens scope line + main entry point when present; single-section nested omits heading; policy Shape governs allowed sections + creation threshold.
- Root `## Commands`: <=5 essential lines; no nested commands. Root architecture follows policy Architecture; no separate boundaries/overview/repository-map section.
- Testing only root + harness-owning nested files per policy Shape; feature caveat/Verify pointer stays with qualified fact.
- No initializer plumbing/skill-location notes; no instruction-file pointers/list/summaries except mandatory Maintenance generic rule. No volatile/excess implementation detail; source pointer + risk instead of walkthrough.

## Report and completion

Write assigned short decision report: pass/fail; file/line per failure (artifact path/check when no generated line), required route, unresolved limits. Compile producer conflicts/skipped + own results: changed files, selected boundaries, documented/skipped flows, validation, evidence gaps, doc/code + intent conflicts, actual retained run path (reusable; safe to delete), initializer directory deletable after success.

Return contract status + report path + pass/fail + concise failures. `complete` means report/check work done, not automatically successful run: failing mandatory check blocks final acceptance. Failed report write -> opaque relay or blocked, never success without report.
