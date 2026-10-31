# Scan

Own preflight + shallow root scan; deep investigation belongs to scouts. Follow supplied [contracts](../references/contracts.md) (Records, Helpers), workflow task boundary/run-folder rules, [policy](../references/repository-analysis.md) Scan, [scout](scout.md) Output (scan-note schema), bundled style. No entrypoint/conversation inheritance.

## Procedure

1. Resolve invocation root/location hint. Ambiguous repository or allowed run location -> `needs_user` before deeper scan. Respect user/host location restrictions.
2. Create run folder + inner `.gitignore` + manifest per workflow run-folder rules. Run `ledger.py baseline <repo-root> <run-dir>` (`--external-run` when run folder outside repository) before any other task write; exit != 0 -> blocked. Never reset user changes. Discover prior runs per workflow.
3. Perform bounded root scan per policy Scan. Read existing selected instructions fully; separate user/process directives (file:line, scope) from factual claims. Executable code/config wins; doc/code + intent conflicts retained for report, never smuggled into guidance.
4. Write context, scan note, scope proposal per policy schemas. Scan note claims = `scan-C<n>` records, all `confidence: low`; questions = `scan-Q<n>` records. Proposal routes each scan claim and question ID to a proposed scope's checker; the orchestrator maps each ID to an accepted scope after choosing scopes.
5. Return root/run/baseline/artifact paths + baseline summary line + concise scope alternatives. Orchestrator selects and records accepted scopes; do not choose accepted boundaries.

Rewrite-only assignment (contracts author rewrite) -> skip steps 1-2 + 5, never rerun baseline; steps 3-4 for assigned `scan-note.md` path only.

## Completion

Baseline/manifest + all assigned artifacts present; proposal sufficient for mode-sized selection + scan claim/question routing; ambiguities surfaced. Write only assigned run artifacts. Read-only search/list/Git + baseline helper; no tests/application/install/state effects. Budget: shallow; search/outline first, ranges over full dumps. Return contract status; raw context/notes never echoed.
