# Workflow

## Outcome and modes

- result: concise selected instruction files; reusable evidence + final decision report inside retained run folder. Explicit invocation only.
- Light: root selected file only; 2-3 scouts total across investigation rounds; no flows section. Broad main domains; supporting areas merge into nearest domain.
- Full: root + useful nested selected files; only meaningful independent boundaries; <=20 scouts total across rounds. Split large domains before context becomes unwieldy. Fewer than 20 expected.
- scout total counts initial/follow-up scout agents, including retry agents. Total differs from concurrency; lower host/user limits always win.
- models: scouts -> selected scout binding (`inherit` -> orchestrator's model/effort). Scan + every other role -> inherit orchestrator's model/effort; never scout override, no per-role overrides or cheaper substitutes.
- roles never merge across phases, Full or Light: scan, scout, checker, placement, writer, reviewer, fixer, Verify each separate fresh agents per contracts.
- completion: accepted routing, writer preflight clean, fresh review + report-only probe, routed repairs, final index PASS, passing current Verify report, all required children terminal. Unresolved evidence gaps may remain reported; missing required output/check is never completion.

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
- `state.md` (orchestrator-owned after scan): capability binding, choices, `accepted-scopes.md` pointer, approved external prefixes, assigned ID prefixes, attempts/status, accepted artifact pointers, batch -> targets, target owners/revisions, cap counters, decisions, scout count, usage. Consumer = scheduling/resume; no payload copies.
- Layout: `accepted-scopes.md`; `attempts/<stage>-<attempt>/` per attempt (notes, `facts.md` + `gaps.md`, question index, `routing.json` + `doubts.md`, projections, manifests, index output, findings, reports); `provenance/provenance-<batch>.json` mutable sidecars; `quarantine/` stale/cancelled/unaccepted artifacts; `baseline/` never overwritten.

## Flow

intake -> binding -> scan -> accepted scopes -> scouts (barrier) -> question index -> checkers -> optional follow-up -> placement -> projections -> fresh writers + preflight -> index -> fresh reviewer/probe -> fixers as needed -> Verify -> final acceptance.

Ready independent scouts/checkers/writers run in parallel with disjoint outputs + available slots. Stage starts only after its required inputs are terminal; overlap only with explicit immutable dependencies. Contracts own failures, helper FAIL routes, invalidation, retries, caps, cancellation, resume.

## 1. Intake and binding

Reuse known choices. Ask only missing file (`AGENTS.md` or `CLAUDE.md`), mode (Light/Full with scout counts), scout model. Recommend cheap model for scouts; name actual cheap model only when availability/cost known. Invite optional history/constraints/traps alongside missing questions. Missing optional context never blocks.

No repository inspection or child dispatch until three required choices resolved. Preserve choices entire run. Unavailable requested model/profile -> explain and ask; never substitute. Bind capabilities per contracts before first child.

## 2. Scan and scope decision

- role: [scan](../agents/scan.md).
- inputs: per role + task boundary/run-folder rules, bindings, user context.
- writes: run folder, manifest, baseline, `context.md`, `scan-note.md`, `scope-proposal.md`.
- done: root/baseline resolved; proposal + artifacts present; ambiguity -> `needs_user` before deeper work.
- orchestrator reads proposal/reply only; chooses mode-sized scopes from IDs/paths/reasons. No scan continuation for recording.
- orchestrator writes `<run>/accepted-scopes.md` (identity only, no evidence): accepted scope ID + paths per line; each scan claim and question ID -> accepted scope checker; merged/rejected proposed scope ID -> accepted scope (orphan owner reassignment). Scan proposes checker scopes before accepted scopes exist; orchestrator chooses the final mappings. Pass to every scout + checker.
- root scout only when proposal flags genuinely complex runtime/E2E behavior; otherwise scan covers root orientation.

## 3. Investigate

- role: [scout](../agents/scout.md); inputs per role; `ids:` = scope ID (follow-up -> assigned `<scopeID>-R<k>`); writes assigned note. Initial scopes narrow/non-overlapping; order by dependencies.
- barrier: all scouts of round terminal -> orchestrator runs `ledger.py questions` per contracts -> fresh question index path per round.

## 4. Check

- role: [checker](../agents/checker.md); fresh agent per area assignment.
- inputs: per role; writes `facts.md` + `gaps.md` in own attempt folder.
- question owner: explicit question ID mapping in `accepted-scopes.md` -> mapped scope's checker; otherwise accepted or merged/rejected scope from `owner` -> its checker; `unassigned` -> asking scope resolved from the question ID prefix through the same mapping.
- Full: area checker gets a few related notes, routed scan claims, and explicitly assigned scan questions; no separate scan checker or scan pseudo-scope. Split before notes exceed context. Light: one checker gets scan + all 2-3 notes.
- follow-up: orchestrator picks consequential items from gap lists only: conflicting evidence, cross-domain question, unclear behavior, weak support. Fresh targeted scout with new `<scopeID>-R<k>` prefix, gap/question ID, artifact paths, needed evidence; may cross initial domains. New note -> rebuilt question index -> fresh checker (own `-R<k>` prefix). Complexity alone needs no extra round. Exhausted scout budget -> checker investigates within assignment or reports gap; never exceed cap.
- unknown intent/dependency -> bounded uncertainty reported; no repeated expansion solely to eliminate unknowns. Unresolved -> gap, never generated fact.

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
- inputs: `ledger.py manifest` output + per role; no run evidence. writes: findings file only.
- done: semantic findings + probe gaps tagged by route; reply counts per target per route.
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
- final acceptance: Outcome completion + scout binding/count/host limits, non-scout inheritance, fresh roles per contracts, compare PASS, routed findings/gaps. Relay passing Verify report (contracts route vocabulary), actual retained run path, unresolved limits. Never claim success from tool termination alone.
