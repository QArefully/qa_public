# Scan

Own preflight + shallow root scan; deep investigation belongs to scouts. Follow supplied [contracts](../references/contracts.md) (Records, Scope grammar, Helpers, recovery), workflow task boundary/run-folder rules, [policy](../references/repository-analysis.md) Scan, [scout](scout.md) Output (scan-note schema), bundled style. No entrypoint/conversation inheritance.

## Procedure

1. Resolve invocation root/location hint. Ambiguous repository or allowed run location -> `needs_user` before deeper scan. Respect user/host location restrictions.
2. Create run folder + inner `.gitignore` + manifest per workflow run-folder rules. Run `ledger.py baseline <repo-root> <run-dir>` (`--external-run` when run folder outside repository) before any other task write; exit != 0 -> blocked. Never reset user changes. Discover prior runs per workflow.
3. Perform bounded root scan per policy Scan. Read existing selected instructions fully; separate user/process directives (file:line, scope) from factual claims. Executable code/config wins; doc/code + intent conflicts retained for report, never smuggled into guidance.
4. Write context, scan note, scope proposal per policy Scan + contracts Records/Scope grammar.
5. Run `ledger.py coverage <run> <proposal> --out <assigned attempt report>`. Exit 0 + current PASS required for completion; return proposal path/hash, report path/hash + counts. Exit 1 -> retain diagnostic report; incomplete proposal requires fresh scope-rewrite under contracts caps. Exit 2 -> blocked + exact error; never assume pass.
6. Return root/run/baseline/artifact paths + baseline summary line + concise scope alternatives + coverage identities/results. Orchestrator selects/records accepted scopes and runs accepted coverage; do not choose accepted boundaries.

## Rewrite assignments

- `note-rewrite` (former scan-note rewrite-only): accepted baseline/context + assigned note/failure; skip bootstrap, repair only assigned `scan-note.md` at new attempt path. Preserve IDs unless contracts require correction. Never rerun baseline or modify proposal/context.
- `scope-rewrite`: accepted baseline/context, current proposal + coverage diagnostic report paths, mode/cap limits, assigned new proposal/report paths. Read report; use bounded shallow listings/config checks to repair declarations/ownership/reasons/mappings. Reuse immutable baseline + context; never bootstrap, deep-investigate source, or change accepted scopes. Run proposal coverage again; return only current proposal/report identities/hashes/counts + alternatives/exceptions. Parent reruns accepted coverage after selection. Consume one bounded assignment attempt per contracts; no hidden self-retry loop.

## Completion

Baseline/manifest + all assigned artifacts present; proposal sufficient for mode-sized selection + scan claim/question routing; current proposal coverage PASS except note-only rewrite; ambiguities surfaced. Write only assigned run artifacts. Read-only search/list/Git + baseline/coverage helpers (baseline only bootstrap); no tests/application/install/state effects. Budget: shallow; search/outline first, ranges over full dumps. Return contract status + required identities/counts/failures; raw context/notes/report diagnostics never echoed. Exhausted required coverage gate -> incomplete, never fabricated skip or WARN.
