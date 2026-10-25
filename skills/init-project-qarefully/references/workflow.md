# Workflow

## Outcome and modes

- result: concise selected instruction files; reusable evidence + final decision report inside retained run folder. Explicit invocation only.
- Light: root selected file only; 2-3 scouts total across investigation rounds. Broad main domains; supporting areas merge into nearest domain.
- Full: root + useful nested selected files; only meaningful independent boundaries; <=20 scouts total across rounds. Split large domains before context becomes unwieldy. Fewer than 20 expected.
- scout total counts initial/follow-up scout agents, including new retry agents; reuse completed scout for compatible bounded follow-up when possible. Total differs from concurrency; lower host/user limits always win.
- scouts: selected scan binding (`inherit` -> no override). Every other role: immediate parent's model/effort binding; never replace with scout model. All roles dispatched directly by orchestrator; nested delegation disabled.
- Light temporal merges: one checker -> placement -> root writer; fresh reviewer -> Verify/report. Each transition needs explicit dispatch granting next phase's inputs/writes; earlier completion does not grant later permissions. Optional disjoint writers remain available.
- completion: accepted placement, fresh review + report-only probe, routed repairs, reconciled mapping, passing current Verify report, all required children terminal. Unresolved evidence gaps may remain reported; missing required output/check is never completion.

## Bundled resources

No sibling-skill dependency. Copy entire package when relocating. Resolve resources from package root in recipient's workspace; pass absolute recipient-visible paths or exact selected text when inaccessible. Missing role, policy, style, helper, or accepted artifact blocks affected dispatch; do not replace missing resource with guessed procedure.

- [repository policy](repository-analysis.md): content selection, placement, commands, architecture, flows, shape; roles read selected sections.
- [generated-content rules](generated-content.md): every writing/review/repair/Verify phase.
- [bundled style](../assets/llm-oriented-markdowns/llm-oriented-markdowns.md): instruction-file writers/reviewer/fixers/Verify; scan also receives it for shared digest.
- [contracts](contracts.md): orchestrator binds dispatch, status, acceptance, recovery; supply relevant contract text to each child.

## Task boundary and run folder

- `AGENTS.md` selected -> no create/update/delete of `CLAUDE.md` or `.claude/` files. `CLAUDE.md` selected -> no create/update/delete of `AGENTS.md` or `.agents/` files.
- Only task writes: selected mode-approved instruction files + actual run folder. Light never modifies nested instruction files. No repository `.gitignore` changes.
- Default run folder: `<repository-root>/.init-project/runs/<YYYY-MM-DDTHHMM>/`; unique suffix on collision. User/host location restrictions override default. Alternate approved root -> stable repository-specific directory (avoid basename collisions) -> timestamped run directory.
- Scan creates run folder, inner `.gitignore` containing `*`, manifest, immutable baseline. All scratch/evidence stays there. Keep run folder uncommitted, including without Git.
- Discover prior runs in allowed repository-specific + default locations only. Prior notes/verdicts are leads; matching clean HEAD raises priority, never establishes truth.
- Manifest: actual root/run path, timestamp, Git availability, HEAD + dirty flag when available, file/mode/scan binding, accepted scopes. Scan checks Git once during preflight; later Verify may compare baseline read-only.
- Baseline: status/diff plus before-state copies/hashes + inventory sufficient to compare task writes, including dirty/untracked files and approved external run folder. Capture before first task write to each boundary; scan may create run-folder shell first, but record shell creation explicitly. Baseline measures deliverable write scope, not runtime reads.
- After scan, orchestrator may maintain `state.md` in run folder: capability binding, selected choices, current attempt/status, accepted artifact pointers/revisions, target owners/revisions, decisions, scout count. Consumer = scheduling/resume; no payload copies or access ledger. Later artifacts use unique `attempts/<stage>-<attempt>/` paths; baseline never overwritten.

## Flow

intake -> capability binding -> scan -> accepted scopes -> scouts -> checkers -> optional follow-up -> placement -> writers -> fresh reviewer/probe -> fixers as needed -> mapping reconciliation -> Verify -> final acceptance.

Ready independent scouts/checkers/writers may run in parallel with disjoint outputs + available slots. Serialize source-dependent work and mutable ownership transfers. Contracts own failures, invalidation, retries, cancellation, and resume.

## 1. Intake and binding

Orchestrator reuses known choices. Ask only missing file (`AGENTS.md` or `CLAUDE.md`), mode (Light/Full with scout counts), scan model. Recommend cheap model; name actual cheap model only when availability/cost known. Invite optional history/constraints/traps alongside missing questions. Missing optional context never blocks.

No repository inspection or child dispatch until three required choices resolved. Preserve choices entire run. Unavailable requested model/profile -> explain and ask; never substitute. Before first child, bind capabilities per contracts; no isolation/dispatch -> capability issue, never orchestrator evidence-role takeover.

## 2. Scan and scope decision

- role: [scan](../agents/scan.md).
- inputs: root/location hint, optional user context, task boundary/run-folder rules, mode, bindings, repository policy + style.
- writes: run initialization/baseline/manifest, `context.md`, `scan-note.md`, `scope-proposal.md`.
- done: root/baseline resolved; scope proposal + artifacts present; ambiguity -> `needs_user` before deeper work.
- orchestrator reads proposal/reply only; chooses mode-sized scopes using IDs/paths/reasons. Scan records accepted scopes in manifest through explicit continuation.

## 3. Investigate and check

- role: [scout](../agents/scout.md); inputs = accepted scope IDs/paths, proposal/context, in-scope prior-note/existing-instruction paths, user context; writes assigned note. Initial scopes narrow/non-overlapping; order by dependencies.
- role: [checker](../agents/checker.md); inputs = assigned notes/scope IDs, all-notes directory for tagged questions, scope proposal, policy Select content/Shape; writes verified facts + short gap list.
- Full: separate checker for scan note; area checker gets few related notes. Split before many notes exceed context. Light: one checker gets scan + all 2-3 scout notes.
- orchestrator chooses consequential follow-up from gap lists only: conflicting evidence, cross-domain question, unclear behavior, weak support. Dispatch targeted scout with gap ID/question, artifact paths, needed evidence; may cross initial domains. Route new note to one checker; complexity alone needs no extra round. Exhausted scout budget -> checker investigates within assignment or reports gap; never exceed cap.
- unresolved after useful bounded follow-up -> report gap; never generated fact. Stable claim/flow/verdict IDs survive handoffs; original asking flow ID survives cross-scope answer.

## 4. Placement decision

- role: [placement](../agents/placement.md); Light reuses checker with explicit new phase.
- inputs: accepted verified facts, existing selected instruction paths/directives, policy Placement/Flows/Shape, style; writes placement + short doubts decision artifact.
- done: each existing selected file disposition, planned targets, exact fact-to-verdict mapping, one-home ownership map, directives, doubts/conflicts. Planned deletion in Light cannot include nested file.
- orchestrator accepts from short reply/doubts only. Evidence doubt -> one checker -> placement; uncertain home -> decide from placement's location alternatives. No orchestrator evidence resolution.

## 5. Write

- role: [writer](../agents/writer.md); default placement producer changes to write-only phase. Optional writers when disjoint file sets make parallel work useful. Light checker explicitly gains root write ownership.
- inputs: current accepted placement, assigned target files, policy/style/generated-content rules. Placement is sole factual input; no notes/verdict/source reads in writing phase.
- done: only planned facts/directives written, target dispositions applied, changed paths/current target revisions returned. Placement producer's retained evidence does not authorize new factual synthesis during writing.

## 6. Fresh review and report-only probe

- role: [reviewer](../agents/reviewer.md); fresh agent uninvolved in scan/check/placement/write, including root-only runs.
- inputs: current generated file list, compact ownership map + conflict-free target revisions, policy/style/generated-content rules. No notes/verdicts/placement.
- writes: assigned generated/updated instruction files only. Full reviewer gets no run-folder access; returns short findings in reply. Light review phase also has no run-folder access; later explicit Verify phase grants exact verification inputs + report path only.
- done: dedup/wording corrections + report-only typical-change/investigation probe; reply includes moved/deleted guidance, file/line support findings, probe gaps, conflicts/skipped. Reviewer never adds probe discoveries or deletes on support grounds.

## 7. Repair and reconcile

- role: [fixer](../agents/fixer.md); fresh worker per repair assignment, never reviewer repairing own support findings or Verify failures. Disjoint ownership when parallel.
- inputs: findings, current accepted placement, assigned current targets, policy/style/generated-content rules; source reads allowed for verification.
- exact verdict-supported correction or unsupported-line deletion -> fixer edits. New/corrected fact/scope -> candidate artifact -> one checker -> placement -> fixer using revised accepted placement; no factual write before verdict.
- consequential probe gap -> same checker -> placement -> fixer route for smallest pointer/warning. Location doubt -> placement alternatives -> orchestrator decision -> updated placement.
- placement producer reconciles reviewer/fixer move/delete replies and updates mapping at new revision; contradictions -> checker. Light producer also emits compact final mapping/verdict refs + audit result and producer conflicts/skipped extracts for Verify-only payload. Reviewer receives payload only after review phase ends; no underlying evidence access.
- no findings -> no fixer. Later input/target changes invalidate affected review/Verify acceptance; contracts define bounded reruns.

## 8. Verify and accept

- role: [verify](../agents/verify.md); Full dedicated worker; Light reviewer transitions explicitly to report-only Verify after repairs/reconciliation. No instruction-file writes during Verify.
- shared inputs: root/mode/file choice, current generated paths/revisions, actual run + exact manifest/baseline paths, policy/style/generated-content/helper paths, review/fixer decision replies, assigned report path. Full adds current placement, verified-facts paths, producer conflicts/skipped sections. Light receives final mapping/audit/extract payload only; no notes/verdict/placement access.
- done: checks + short report present, pass/fail and failures routed. Missing inputs/report or failed mandatory check -> dependent completion blocked; repair through stage 7, rerun affected checks on current revisions.
- optional rationale question at end: finish supported guidance first; route user answer through checker/placement/fixer, then revalidate. Never infer rationale.
- orchestrator checks replies: scout binding/count/host limits, non-scout inheritance, fresh reviewer/probe, accepted placement + reconciled mapping, routed findings/gaps, passing current report, terminal children. Relay report, actual retained run path, unresolved limits. Run folder reusable/safe to delete; initializer package deletable after success. Do not claim success from tool termination alone.
