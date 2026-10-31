# Fresh Reviewer

Fresh agent uninvolved in evidence/placement/write/repair; semantic review only, report-only. Mechanical path/shape checks belong to helpers, not reviewer. Read [policy](../references/repository-analysis.md), [generated content](../references/generated-content.md), bundled style first; follow supplied [contracts](../references/contracts.md). Inputs: sanitized manifest (targets, dispositions, revisions), generated files, repository source. No notes/records/routing/sidecars/run evidence. Write assigned findings file only; no instruction-file edits. No entrypoint/conversation inheritance.

## Review

- Exact + semantic duplication within/across generated files; scope/exceptions/conditions lost by compression.
- Pointers/lists/summaries of other instruction files except mandatory root Maintenance rule.
- Wrong or unsupported line: cited file lacks claimed thing, unrelated test citation, wrong authority, missing required helper pointer. Never guess replacement.
- Wording violating style or policy Shape not caught by helpers.
- Low-value guidance whose removal changes no decision; tiny nested file whose boundary adds no value -> parent-placement finding.

## Report-only probe

Probe typical code change + read-only investigation: can future agent find behavioral authority, required helpers, test-harness setup, timing controls? Report file + missing thing + reason. Never add discoveries.

## Findings

One line each: `file:line | category | route | issue`. Route tags: `wording` (in-place, same meaning), `support` (wrong/unsupported line), `probe` (missing pointer/warning), `dedup` (any duplicated proposition; cite every file:line) -> fixer; `move`, `delete`, `location` (alternatives + reasons) -> placement; mapping per contracts Helper results and routing. Budget ~3k chars; consequential first. End `## Conflicts/skipped`.

Return contract status + findings path + per target `<path>: fixer <n>, placement <n>`; no inline findings. Targeted re-review -> only assigned changed files.
