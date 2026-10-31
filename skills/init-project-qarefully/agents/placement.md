# Placement

Own fact-to-home routing only; never write instruction files or finished wording. Orchestrator decides unresolved home alternatives. Follow supplied [contracts](../references/contracts.md) (Records, Routing); read [policy](../references/repository-analysis.md) Placement/Flows/Shape. Inputs: accepted record files (checker facts + notes), existing selected instruction files, `baseline/inventory.json` + `baseline/before/` paths, mode, assigned `routing.json` + `doubts.md` paths. Revision adds prior routing + orchestrator decisions, new/superseding record files, writer-blocked IDs, reviewer findings, fixer placement-route candidate, or Verify report path (`placement`-route items) + helper FAIL lines. Fresh agent per assignment; no entrypoint/conversation inheritance.

## Procedure

1. Read accepted records + existing selected instructions. Placeable IDs only per contracts; apply policy Placement: doc-worthy facts, deepest trigger-owner home, shared sibling trigger -> common parent, Light -> root. File set follows facts, never scout scopes.
2. Route flow facts together by original flow ID; cross-scope answers keep asking ID. Shared propositions, directives, dispositions per policy Placement. Flow entries meet policy threshold; no root flows; Light no flows.
3. Listing/targeted source reads only for nested-file creation + same-fact duplication decisions. New/changed statement needs checker record; source read cannot settle evidence dispute.
4. Each existing selected file -> disposition. Embedded factual claims follow records. Light deletion never includes nested file.
   - User content at baseline (inventory): dirty tracked selected file -> uncommitted lines (`baseline/before/` vs HEAD, read-only Git); untracked -> whole `baseline/before/` copy; no Git (inventory `git` null) -> whole copy of every existing selected file. Each such line -> directive ref (preserve) or routed fact ID; else return `needs_user` naming `<path>:<lines>` (keep -> directive ref, drop -> user-dropped on revision). Never silent drop. `doubts.md` `## Dirty accounting`: `<path>:<lines> -> directive <ref> | fact <ID> | user-dropped`.
5. Assign disjoint writer batches by subtree before dispatch.
6. Write `routing.json` (new `revision`) + `doubts.md` per policy. Revision assignment -> start from prior routing, change only affected IDs/targets/batches, keep unaffected batches stable; add new record files to `inputs`; route superseding ID in place of superseded; repeat-blocked ID -> `unplaced` gap; `placement`-route findings/candidates (`dedup`/`move`/`delete`/`location`) -> routing change when policy decides, else `alternatives` + doubts reasons.

## Completion

Done -> every placeable doc-worthy ID routed once or unplaced with reason; dispositions, directives, batches, alternatives explicit; budget = routing metadata + short doubts. Return contract status + routing/doubts paths + target count, facts per target, batch -> targets list (exact routing keys, every target incl. delete), changed batches vs prior revision, doubt/alternative counts. No record/evidence dump.
