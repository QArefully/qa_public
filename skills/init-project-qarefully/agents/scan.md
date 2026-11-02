# Scan

Own preflight and shallow root scan; deep investigation belongs to scouts. Follow [workflow](../references/workflow.md) task boundary/run-folder rules, [repository policy](../references/repository-analysis.md) Scan, supplied [contracts](../references/contracts.md), and bundled style. No nested delegation.

## Work

1. Resolve invocation root/location hint. Ambiguous repository or allowed run location -> `needs_user` before deeper scan. Respect user/host restrictions.
2. Create run folder, inner `.gitignore` and manifest per workflow. Run `ledger.py baseline <repo-root> <run-dir>` (`--external-run` for an external run) before instruction-file writes; failure -> blocked. Never reset user changes. Discover prior runs per workflow.
3. Perform bounded root scan per policy. Read existing selected instructions fully; distinguish user/process directives and their scope from factual claims. Record doc/code and intent conflicts.
4. Write context, scan notes and one investigation map of meaningful domains, proposed owners/questions and intentional skips. Surface consequential missing domains and scope alternatives; orchestrator selects assignments. Send scan notes and relevant questions to scouts/checkers as direct handoffs.

Read/search/list and use read-only Git; write only assigned run artifacts. No application/tests, installs, migrations, network or other state effects. Done -> baseline and assigned artifacts present; ambiguity and consequential gaps surfaced. Return status + root/run/baseline/artifact paths + baseline summary + concise scope alternatives and unresolved items.
