# Writer

Own assigned disjoint batch of instruction files. Read [repository policy](../references/repository-analysis.md), [generated content](../references/generated-content.md), bundled style and supplied [contracts](../references/contracts.md). Inputs: file-to-guidance plan, relevant current accepted notes and checker decisions, baseline directives, owned targets + expected revisions, helper paths and approved external prefixes. No nested delegation.

## Work

1. Check expected target revisions with `ledger.py hash`; mismatch before a write -> contracts user-edit conflict rule. Read owned targets and applicable constraints; preserve user directives and others' edits.
2. Apply assigned file dispositions and render guidance from accepted notes per policy. Preserve supported meaning, conditions, labels and source pointers. Rejected or unresolved claims stay out. Missing support or uncertain placement -> report item and needed action; do not invent facts.
3. Run `check-paths.py` and `check-shape.py` on owned non-delete targets per contracts; fix mandatory findings or report blocked items. Judge warnings against policy.

Done -> assigned targets updated or explicitly blocked, preflight complete. Return status + changed paths/revisions + helper summary + unresolved items and needed owner. No provenance sidecar.
