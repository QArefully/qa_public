# Fixer

Repair only unresolved assigned findings; reviewer-completed edits need no fixer. Read [repository policy](../references/repository-analysis.md), [generated content](../references/generated-content.md), bundled style and supplied [contracts](../references/contracts.md). Inputs: relevant findings/Verify report, current accepted notes and decisions, owned targets + expected revisions, baseline directives and helpers. No nested delegation.

## Work

1. Check target revisions with `ledger.py hash`; mismatch before a write -> contracts user-edit conflict rule. Preserve user/other worker edits; never restore baseline over them.
2. Resolve assigned wording/format or supported duplicate edits directly per shared rules. Preserve distinct conditions and directives. Unsupported or uncertain factual correction -> checker; substantive home dispute -> placement. Do not invent facts or discard unique guidance to resolve uncertainty.
3. Run `check-paths.py` and `check-shape.py` on changed non-delete targets per contracts; fix mandatory findings or report blocked items.

Done -> assigned findings repaired or explicitly unresolved. Return status + changed paths/revisions + helper summary + unresolved items, needed action and owner.
