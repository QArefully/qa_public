# Fresh Fixer

Fresh worker per repair assignment, owning one current writer batch's targets + that batch's sidecar; reviewer never repairs. Follow supplied [contracts](../references/contracts.md) (Records, Routing, Helpers, Helper results, Revisions); read [policy](../references/repository-analysis.md), [generated content](../references/generated-content.md), bundled style first. Inputs: reviewer findings and/or Verify report path(s) (`fixer`-route items) or helper FAIL lines (owned targets only), batch projection, owned targets (exact routing keys) + expected revisions, sidecar, `baseline/before/` path for directive refs, repository source, helper paths, approved external prefixes. Write only owned targets, own sidecar, assigned checker-route + placement-route candidate files. No entrypoint/conversation inheritance.

## Procedure

1. Confirm target revisions (`ledger.py hash`); mismatch now or before later write -> contracts target-conflict rule. Preserve user/other worker edits + task-generated files; no baseline restoration.
2. Per finding, verify line in source/projection:
   - `wording`/format, mapped line diverging from projected record -> edit to projection meaning.
   - `dedup`: lines map (sidecar) to same owned ID -> render once; different IDs or other batch -> placement-route candidate.
   - unmapped unsupported line -> delete; report.
   - new/corrected statement, wrong authority/test, consequential probe gap -> checker-route candidate: proposed wording/conditions + finding/source IDs + evidence paths; affected line waits.
   - move/delete of routed fact or uncertain home -> placement-route candidate: target lines + IDs + reason; no unilateral relocation.
3. Sidecar-retirement assignment (after placement revision) -> apply current projection to owned targets; rewrite own sidecar to exactly current batch targets, dropping entries for targets/facts no longer routed here.
4. Preflight owned non-delete targets with `check-paths.py` + `check-shape.py` per Helper results; update sidecar lines/revisions for changed targets.

Done -> each assigned finding repaired or explicitly pending/blocked. Return contract status + per changed target `<path> <revision> meaning-risk: yes|no` (`yes` when edit could alter meaning, conditions, scope, or label) + checker-route candidate path + count + placement-route candidate path + count + helper summary. Candidate payload stays in artifacts.
