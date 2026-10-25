# Scan

Own preflight + shallow root scan; deep investigation belongs to scouts. Follow supplied [contracts](../references/contracts.md), workflow task boundary/run-folder rules, [policy](../references/repository-analysis.md) Scan, and bundled style. No entrypoint/conversation inheritance.

## Procedure

1. Resolve invocation root/location hint. Ambiguous repository or allowed run location -> `needs_user` decision reply before deeper scan. Respect user/host location restrictions.
2. Capture immutable before-state sufficient for later write-boundary comparison: Git availability/status/diff/HEAD/dirty state when available, existing dirty/untracked content + relevant inventory/hashes/copies. No Git -> before-state inventory/hashes/copies. Cover repository + approved external run boundary. Never reset user changes.
3. Create unique allowed run folder + inner `.gitignore` containing `*`; write manifest. Discover allowed prior runs; matching clean HEAD only prioritizes leads. All scratch stays in current run. Baseline must distinguish initial run-shell creation from pre-existing content.
4. Perform bounded root scan per policy Scan. Read existing selected instructions fully; separate user/process directives (source/location/scope) from factual leads. Executable code/config wins; doc/code + intent conflicts retained for report, never smuggled into guidance.
5. Write context, scan note, scope proposal using policy schemas; scan note uses [scout](scout.md) Output claim/flow/question schema. Existing-instruction facts include orientation/runtime/commands. Scope proposal includes existing selected instruction paths, candidate meaningful boundaries, prior-note paths, reasons, conflicts/skipped.
6. Return root/run/baseline/artifact paths + concise scope alternatives. After orchestrator selects, explicit continuation records accepted scopes in manifest; do not choose accepted boundaries yourself.

## Completion

Baseline/manifest + all assigned artifacts present; scope proposal sufficient for mode-sized selection; ambiguities surfaced. Write only assigned run artifacts. Read-only search/list/Git; no tests/application/install/state effects. Return contract status; raw context/notes never echoed.
