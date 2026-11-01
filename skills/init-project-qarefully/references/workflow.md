# Workflow

## Outcome and modes

- result: concise selected instruction files; reusable evidence + final decision report inside retained run folder. Explicit invocation only.
- Light: root selected file only; 2-3 scouts total across investigation rounds; no flows section. Broad main domains; supporting areas merge into nearest domain.
- Full: root + useful nested selected files; only meaningful independent boundaries; <=20 scouts total across rounds. Split large domains before context becomes unwieldy. Fewer than 20 expected.
- scout total counts initial/follow-up scout agents, including retry agents. Total differs from concurrency; lower host/user limits always win.
- models: scouts -> selected scout binding (`inherit` -> orchestrator's model/effort). Scan + every other role -> inherit orchestrator's model/effort; never scout override, no per-role overrides or cheaper substitutes.
- roles never merge across phases, Full or Light: scan, scout, checker, placement, writer, reviewer, fixer, Verify each separate fresh agents per contracts.
- completion: current proposal + accepted-scope coverage PASS, consequential question dispositions, accepted routing, writer preflight clean, fresh review + report-only probe, routed repairs, final index PASS, passing current Verify report, all required children terminal. Unresolved evidence gaps may remain reported; missing required output/check is never completion.

## Bundled resources

No sibling-skill dependency. Resolve resources from package root in recipient's workspace; pass absolute recipient-visible paths or exact selected text when inaccessible. Missing role, policy, style, helper, or accepted artifact blocks affected dispatch; do not replace missing resource with guessed procedure.

- [repository policy](repository-analysis.md): scan, content selection, placement, commands, architecture, flows, shape; roles read selected sections.
- [generated-content rules](generated-content.md): every writing/review/repair/Verify phase.
- [bundled style](../assets/llm-oriented-markdowns/llm-oriented-markdowns.md): writers/reviewer/fixers/Verify; scan for shared digest.
- [contracts](contracts.md): binding, dispatch, records, routing/provenance, helpers/runner roles, helper failure routes, acceptance, recovery; supply relevant sections to each child.
- `scripts/ledger.py`, `scripts/check-paths.py`, `scripts/check-shape.py`: deterministic helpers per contracts runner roles.

## Task boundary and run folder

- `AGENTS.md` selected -> no create/update/delete of `CLAUDE.md` or `.claude/` files. `CLAUDE.md` selected -> no create/update/delete of `AGENTS.md` or `.agents/` files.
- Only task writes: selected mode-approved instruction files + actual run folder. Light never modifies nested instruction files. No repository `.gitignore` changes.
- Default run folder: `<repository-root>/.init-project/runs/<YYYY-MM-DDTHHMM>/`; unique suffix on collision. User/host location restrictions override default; never hardcode host paths. Alternate approved root -> stable repository-specific directory (avoid basename collisions) -> timestamped run directory (`--external-run` for baseline).
- Scan creates run folder, inner `.gitignore` containing `*`, manifest, then immutable baseline via `ledger.py baseline` before any task write to instruction files. All scratch/evidence stays in run folder; keep it uncommitted, including without Git.
- Discover prior runs in allowed repository-specific + default locations only. Prior notes/records are leads; matching clean HEAD raises priority, never establishes truth.
- Manifest: actual root/run path, timestamp, Git availability, HEAD + dirty flag when available, file/mode/scout binding.
- `state.md` (orchestrator-owned after scan): capability binding, choices, proposal path/hash, accepted-scope path/hash, current proposal/accepted coverage report paths/hashes + PASS identities, approved external prefixes, assigned ID prefixes, attempts/status, accepted artifact pointers, QID -> follow-up assignment or reported-gap reason, batch -> targets, target owners/revisions, cap counters, decisions, scout count, usage. Consumer = scheduling/resume; no evidence payload copies.
- Layout: `accepted-scopes.md`; `attempts/<stage>-<attempt>/` per attempt (scope proposals + coverage reports, notes, `facts.md` + `gaps.md`, question index, `routing.json` + `doubts.md`, projections, manifests, index output, findings, reports); `provenance/provenance-<batch>.json` mutable sidecars; `quarantine/` stale/cancelled/unaccepted artifacts; `baseline/` never overwritten.

## Flow

intake -> binding -> scan + proposal coverage -> accepted scopes + coverage -> scouts (barrier) -> question index -> checkers -> question dispositions/follow-up -> placement -> projections -> fresh writers + preflight -> index -> fresh reviewer/probe -> fixers as needed -> Verify -> final acceptance.

Ready independent scouts/checkers/writers run in parallel with disjoint outputs + available slots. Stage starts only after its required inputs are terminal; overlap only with explicit immutable dependencies. Contracts own failures, helper FAIL routes, invalidation, retries, caps, cancellation, resume.

## Dispatch matrix

Use this scheduling summary + exact role/resource paths; keep long role procedures in dispatched resources. Each role receives selected contract sections, boundary rules, bindings, immutable input paths, and exact owned writes per contracts Dispatch. Parent evidence visibility stays unchanged.

| Role | Inputs | Owned outputs | Done / route check |
| --- | --- | --- | --- |
| scan | root/context; rewrite: proposal + coverage report | bootstrap artifacts; proposal + coverage report; or assigned rewrite | proposal PASS + IDs/counts; scope failure -> fresh scope rewrite |
| scout | accepted scopes, context, assigned paths/QIDs | bounded note | IDs + question counts; round barrier -> question index |
| checker | assigned notes/scan IDs, question index; candidates if assigned | facts + gaps | verdict/gap counts + unresolved QIDs/codes -> dispositions |
| placement | accepted records, existing-file baseline, doubts/decisions | routing + doubts | batch identity/targets; revisions -> retire sidecars + project |
| writer | batch projection, directives, expected revisions | owned targets + sidecar | changed paths/revisions + preflight; blocked IDs/conflict -> contracts |
| reviewer | sanitized manifest + bound harness/version | path-local probe + findings | initial probe before global read; route counts -> repair/placement |
| fixer | current batch projection + findings/FAILs + revisions | owned targets + sidecar + candidates | changes/revisions, meaning-risk, route counts -> index/review |
| Verify | current artifacts/gates, index/projection, dispositions | report + own index output | helper/semantic results + route counts; failures -> contracts |

## 1. Intake and binding

Reuse known choices. Ask only missing file (`AGENTS.md` or `CLAUDE.md`), mode (Light/Full with scout counts), scout model. Recommend cheap model for scouts; name actual cheap model only when availability/cost known. Invite optional history/constraints/traps alongside missing questions. Missing optional context never blocks.

No repository inspection or child dispatch until three required choices resolved. Preserve choices entire run. Unavailable requested model/profile -> explain and ask; never substitute. Bind capabilities per contracts before first child.

## 2. Scan and scope decision

- role: [scan](../agents/scan.md).
- inputs: per role + task boundary/run-folder rules, bindings, user context.
- writes: run folder, manifest, baseline, `context.md`, `scan-note.md`, proposal + coverage report in assigned attempt folder.
- done: root/baseline resolved; proposal coverage PASS + report identity/input hashes/counts; artifacts + scan-ID mappings present; ambiguity -> `needs_user` before deeper work.
- orchestrator reads proposal/reply only; chooses mode-sized scopes from IDs/paths/reasons. Coverage measures investigation assignment, never instruction-file count. Light merges explicit paths into its 2-3 total scout scopes; Full retains <=20 total scouts including retries/follow-ups.
- orchestrator writes `<run>/accepted-scopes.md` using contracts Scope grammar (identity/reasons only, no evidence): accepted scope ownership + per-directory reasons; each scan claim and question ID -> accepted scope checker; merged/rejected proposed scope ID -> accepted scope (orphan owner reassignment). Every proposed investigation path remains assigned, including rejected/merged scope paths. Pass to every scout + checker.
- orchestrator runs `ledger.py coverage <run> <proposal> --accepted <accepted-scopes> --out <fresh attempt report>`; require current PASS before scout dispatch. Record proposal/accepted hashes + coverage identities in state. Accepted identity-format errors may be corrected administratively; a changed path/container/skip boundary requires a fresh scan scope rewrite + both coverage checks. Diagnostic reports stay opaque to parent.
- coverage FAIL -> fresh scan `scope-rewrite` with proposal + diagnostic report paths, baseline/context reused; no bootstrap/deep investigation. Exit 2 -> contracts blocked/correction route. Observe attempt caps; exhausted mandatory coverage gate -> incomplete, never WARN or invented skip.
- root scout: Light may assign root guidance investigation; Full only when proposal flags genuinely complex runtime/E2E behavior; otherwise scan covers root orientation. Declaring/scoping `.` never excuses child coverage.

## 3. Investigate

- role: [scout](../agents/scout.md); inputs per role; `ids:` = scope ID (follow-up -> assigned `<scopeID>-R<k>`); writes assigned note. Initial scopes narrow/non-overlapping; order by dependencies.
- barrier: all scouts of round terminal -> orchestrator runs `ledger.py questions` per contracts -> fresh question index path per round.

## 4. Check

- role: [checker](../agents/checker.md); fresh agent per area assignment.
- inputs: per role; writes `facts.md` + `gaps.md` in own attempt folder.
- question owner: explicit question ID mapping in `accepted-scopes.md` -> mapped scope's checker; otherwise accepted or merged/rejected scope from `owner` -> its checker; `unassigned` -> asking scope resolved from the question ID prefix through the same mapping.
- Full: area checker gets a few related notes, routed scan claims, and explicitly assigned scan questions; no separate scan checker or scan pseudo-scope. Split before notes exceed context. Light: one checker gets scan + all 2-3 notes.
- every consequential unresolved QID must occur in checker `gaps.md`, including `unassigned`, outside accepted paths, or assigned-but-unanswered questions. Missing gap entry -> fresh checker rewrite. Administrative ownership never proves investigation.
- disposition: record each consequential unresolved QID -> targeted follow-up assignment while budget remains, or explicit reported-gap reason. Outside-scope/unassigned questions cannot disappear for lacking an accepted path. Reported gap may cite unavailable evidence, unresolved intent, declined expansion, exhausted budget, or a bounded prior unsuccessful follow-up; remaining budget alone does not require unlimited expansion.
- follow-up: fresh targeted scout with new `<scopeID>-R<k>` prefix, gap/QID + artifact paths + needed evidence; may cross initial domains. Count every scout retry/follow-up against mode cap. New note -> rebuild question index with accepted answer files -> fresh checker (own `-R<k>` prefix) -> update dispositions. Already answered QIDs need no follow-up. A targeted question investigation does not change standing scopes; adding/changing those scopes requires both coverage gates again.
- unknown intent/dependency -> bounded uncertainty reported; no repeated expansion solely to eliminate unknowns. Unresolved -> gap, never generated fact. Final Verify reconciles current question index, gap artifacts, and state dispositions.

## 5. Placement

- role: [placement](../agents/placement.md).
- inputs: per role; writes `routing.json` + `doubts.md`.
- done: routing covers each existing selected file disposition, targets, fact IDs, directives, disjoint writer batches; unplaced/alternatives explicit.
- orchestrator accepts from reply/doubts only. Evidence doubt -> fresh checker -> fresh placement revision. Home alternative -> orchestrator decides from doubts reasons -> fresh placement revision applies decision (prior routing + decisions; unaffected batches may proceed).
- every placement revision -> sidecar retirement per contracts.
- per batch: orchestrator runs `ledger.py project` over all targets in placement reply's batch -> targets list, verbatim keys; no disposition knowledge needed. FAIL -> contracts helper routes; never hand-edit routing.

## 6. Write

- role: [writer](../agents/writer.md); fresh agent per disjoint batch, batch chosen in routing before dispatch.
- inputs: per role; expected revisions per contracts (first writer -> `ledger.py hash --baseline`).
- done: dispositions applied, helpers clean per contracts Helper results, sidecar written, revisions returned.
- blocked IDs / target conflict -> contracts recovery routes.
- all writers terminal + blocked-ID rounds resolved (contracts) -> orchestrator runs `ledger.py index` over current-batch sidecars; FAIL -> contracts helper routes.

## 7. Fresh review and report-only probe

- role: [reviewer](../agents/reviewer.md).
- inputs: `ledger.py manifest` output + bound harness/version + observable loading capability + per role; no run evidence. writes: findings file only.
- done: representative unnoted sibling, route, test mirror path-local results written before global generated-file reading, then semantic findings + probe gaps tagged by route; distinguish ancestor-chain simulation from observed loading. If separation unavailable, fresh bounded read-only probe assignment writes its result first; record capability/cost limit. Reply counts per target per route; `probe` still routes through fixer/candidate, `location` through placement.
- routes per contracts Helper results and routing; `fixer` -> stage 8.

## 8. Repair

- role: [fixer](../agents/fixer.md); partitioned by writer batch (reply per-target counts -> placement batch list).
- inputs: per role; dispatch passes reviewer findings and/or Verify report path(s) (`fixer`-route items only) or helper FAIL lines; batch projection re-run at current routing.
- checker-/placement-route candidate files -> contracts routes.
- after fixer: `ledger.py index`; changed targets with `meaning-risk: yes` -> fresh targeted reviewer scoped to those files only; `no` -> no review. No findings -> no fixer.

## 9. Verify and accept

- role: [verify](../agents/verify.md).
- inputs: per role Inputs; all-target projection per contracts `project`.
- done: helpers rerun + semantic checks + report; each failure tagged `format`, `semantic`, or `boundary` with route.
- orchestrator routes from Verify reply alone (contracts route vocabulary): `fixer` -> stage 8; `checker`/`placement` -> those routes; then fresh Verify on current revisions; cycle counted per contracts caps (`format`/`semantic` split). `boundary` -> contracts compare route.
- optional rationale question at end: finish supported guidance first; route answer through checker -> placement -> fixer, then revalidate. Never infer rationale.
- final acceptance: Outcome completion + current proposal/accepted coverage PASS identities/hashes, reconciled question dispositions, scout binding/count/host limits, non-scout inheritance, fresh roles per contracts, compare PASS, routed findings/gaps. Relay passing Verify report (contracts route vocabulary), actual retained run path, unresolved limits. Never claim success from tool termination alone.
