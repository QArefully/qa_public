# Handoff Contracts

## Capability binding

Before first child, inspect exposed controls and record binding in `state.md`:

- Dispatch isolated bounded children able to read assigned role/resources; only orchestrator starts children.
- Model: requested and observable effective model/effort/profile; `inherit` retains immediate parent's binding. Exact named profile only when requested. Unavailable or unverifiable required binding -> report and ask; never silently substitute.
- Map recipient-visible input/output paths; assign writable disjoint targets. Missing dispatch, isolation, resource, Python 3, or write capability -> block affected work, never assume success or take over an evidence role.
- Respect host/user concurrency limit; queue when full. Wait for terminal notification, avoid short polling. A writer that cannot be stopped retains ownership until terminal.

## Dispatch and continuity

One agent -> one role and bounded objective. Supply exact role and relevant policy/style paths, selected filename/mode, model binding, task boundaries, input paths, owned outputs, expected target hashes when writing, and done checks. No child invokes another agent. Give concise summaries and artifact paths, not whole transcripts. Parallel writers own disjoint files and preserve others' changes.

Continue a scout or repair worker when context remains useful; use a fresh scout for different context or when the previous one has finished. Independent checking and review require agents independent of the work checked. Administrative corrections do not require fresh agents or attempts. No application, test, install, migration, network, or state effects unless user separately authorizes them.

## Notes and handoffs

- Investigation map: meaningful domains, primary owners, questions and intentional skips with reasons. Ownership coordinates reads, not exclusion.
- Notes: consequential claims with conditions and source references, direct implementation support or uncertainty, and unresolved questions with next evidence step. Checker notes retain decisions and corrected claims, conditions and references. Rejected and unresolved claims never become guidance. Use a note path + heading or other lightweight reference where another agent needs to identify an item; no mandatory ID allocation or supersession protocol.
- Placement plan: file -> disposition, guidance and relevant accepted note/directive references, writer owner. Record meaningful home alternatives and unresolved questions. One target has one writer at a time. Writers receive relevant current accepted notes directly, including applicable existing directives; no generated-line sidecars or projection.
- Review findings: `file:line + issue`; record independent findings before consulting earlier evidence or editing metadata. Replies name unresolved items, needed action and owner. Final Verify receives relevant notes, plan, output and unresolved decisions.
- Existing user/process directives include source and applicable scope; preserve their intent. Questions that remain consequential become explicit reported gaps with next evidence step; never treat missing evidence as proof.

## Helpers

Bundled `scripts/` helpers use Python 3.8+ stdlib; run `python -B <package>/scripts/<helper>`. Exit 0 = pass, 1 = findings, 2 = input/usage error. Helpers do not edit instruction files.

- `ledger.py baseline <repo-root> <run-dir> [--external-run]` -> scan once before instruction-file edits; immutable baseline includes existing content and dirty state.
- `ledger.py hash <repo-root> <path>...` -> current target hashes; `ledger.py hash <repo-root> --baseline <run-dir> <path>...` -> baseline hashes. Compare before writes per ownership below.
- `ledger.py compare <repo-root> <run-dir> --file AGENTS.md|CLAUDE.md --mode light|full [--allow <rel>]...` -> Verify task boundaries. `--allow` only exact user-approved paths. Boundary FAIL -> stop and report; never restore or repair outside writes without user decision. Dirty-allowed WARN -> inspect for unaccounted user-content loss; observed-other WARN is informational.
- `check-paths.py <repo-root> [--allow-external <abs-prefix>]... <file>...` and `check-shape.py <repo-root> <file>...` -> writer/reviewer/fixer on owned non-delete targets and Verify on all such targets. Skip when none; no-file invocation walks all. Path/shape FAIL -> repair or report blocked; shape WARN -> judge against policy, explain kept warnings. Backtick intended path tokens; extensionless unbackticked tokens are checked only with trailing `/`.

## Ownership, conflicts, recovery

Baseline captures original selected files and dirty state. Before first target write compare current hash with baseline (or last handoff hash after ownership transfer); before subsequent writes compare with own last write. Mismatch -> stop writing that target, return `needs_user` with path; orchestrator asks whether to incorporate the edit or stop. Never overwrite or restore user edits. Transfer ownership only after prior writer is terminal and communicate current hash.

Keep current assignments, artifact paths, open decisions and completion in `state.md`; include binding and available usage (model calls, tokens, duration, artifact bytes; unavailable when unexposed). No quarantine or revision chain. On interruption, preserve user edits and task boundaries; rerun if current work cannot be safely resumed. Missing required artifact or check blocks dependent completion.

Use bounded repairs: correct a specific failure while useful progress is possible; repeated unchanged failure -> blocked with cause and next step. Context exhaustion -> retain concise partial work and remaining question; continue or split without silently claiming completion. Do not expand write scope to work around failure.

## Return

Reply with `status: complete|blocked|needs_user`, owned artifact paths, and concise unresolved items, needed action and owner. Report helper failures and kept warnings. Complete requires actual outputs and required checks, not merely a successful tool call; only orchestrator asks user.
