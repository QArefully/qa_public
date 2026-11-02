# Verify

Final independent verification against source notes and output; report only, no repairs or new factual verdicts. Read [repository policy](../references/repository-analysis.md), [generated content](../references/generated-content.md), bundled style and supplied [contracts](../references/contracts.md). Inputs: repository root, mode/file choice, run folder/manifest/baseline, investigation map, placement plan, current accepted notes and checker decisions, generated files, reviewer findings/probe, unresolved gaps, helper paths and approved external prefixes/allow paths. No nested delegation.

## Checks

- Run `ledger.py compare <repo-root> <run-dir> --file <choice> --mode <mode>` with only supplied `--allow` paths; apply contracts boundary and user-edit rules. Run `check-paths.py` and `check-shape.py` on all selected non-delete targets; judge warnings per policy. Missing required input/helper -> blocked, never assumed pass.
- Check generated guidance against accepted source notes and relevant source: support, conditions, qualifications, labels, test pointers, useful placement and preserved directives. Rejected/unresolved claims must not appear as facts. Questionable support -> checker; actual home dispute -> placement; straightforward wording/format -> fixer. Verify cites existing authority, including producer/configuration for generated output.
- Confirm user content and task boundaries per contracts, including selected counterpart protection and Light scope. Check relevant shape/content rules helpers miss. Keep material open questions, conflicts and skipped work explicit; unresolved evidence stays a reported gap.
- Check reviewer recorded its independent path-local probe and findings before consulting earlier evidence or editing metadata. Distinguish observed harness loading from simulation; report unavailable controls. Do not audit duplicate-retirement history or trigger another reviewer.

## Handoff

Write concise report: pass/fail; each failure `file:line + issue`, needed action and owner; helper results, changed files, consequential gaps/conflicts, loading limits and retained run path. Return status + report path + pass/fail + unresolved items and owners. Mandatory failures block acceptance; after repairs Verify may confirm them without another review.
