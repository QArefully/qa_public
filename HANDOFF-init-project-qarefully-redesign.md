# Handoff: simplify init-project-qarefully

## Status and authorization

- Current request: capture execution audit + redesign plan. No skill implementation authorized by this handoff alone.
- Skill/package unchanged during audit. This handoff is the only requested new deliverable.
- User requirement: agents have one responsibility; avoid repeatedly waking an agent for new responsibilities as its context accumulates.
- Recommendations below -> proposed implementation direction; preserve existing protections unless explicitly replaced with equivalent checks.
- Future skill edits -> use `skills/writing-skills-qarefully`, not built-in system skill-creator. Read applicable repository/user instructions first.

## Target and evidence

- Package: `C:/Users/iwano/Desktop/repos/qa_public/skills/init-project-qarefully/`.
- Evaluated repository: `C:/wt/qarefully-init-project`.
- Evaluated choices: Full, CLAUDE.md, luna_max scan/scouts.
- Baseline HEAD: `ffbedd36d4247deaecd68e1ccd1b1dc0fb07a89f`.
- Retained run: `C:/wt/qarefully-init-project/.init-project/runs/2026-10-27T1954/`.
- Scheduling history: retained run `state.md`.
- Reports: retained run `attempts/verify-1/report.md` and `attempts/verify-2/report.md`.
- Usage evidence: `C:/Users/iwano/.codex/sessions/2026/10/27/`; filter root session `01a17eea-7436-7650-ae9c-b78763a4ef44` and its children, original root turn `01a17eea-82a2-7e70-96b4-979e4aa3e813`. Exclude subsequent audit/handoff turns.
- Placement session: `01a17efc-68c6-70f0-b17e-b4856f5b7f0b`.
- Run finished PASS: 33 instruction files, 92 mappings, 23 flows with one owning home; all 1,025 baseline files unchanged. Application tests not run; instruction acceptance used static inspection/checks.

## Observed problems

### Placement became writer and mapping maintainer

- Same agent received five assignments: placement -> writing -> reconciliation -> final mapping -> post-Verify formatting reconciliation.
- `references/workflow.md` explicitly defaults placement producer to writer, then returns mapping reconciliation to that producer. Change those contracts together.
- Initial placement contains finished supported wording; writer reproduces that wording in generated files.
- Initial placement: 57,010 bytes. All 33 final instruction files combined: 29,813 bytes. Four placement/mapping revisions combined: 103,968 bytes.
- Placement agent generated 68,547 output tokens across five assignments; initial placement 37,247, writing 14,141, later mapping work 17,159. Counts include reasoning.
- No recorded context exhaustion: peak placement call input 182,507 tokens; recorded context window 475,000; no compaction recorded. Concern is excessive retained context, responsibility switching and serial work; do not claim overflow occurred.

### Coordination and checks multiplied

- Original execution: approximately 56 minutes; 20 subagents; 33 total agent turns including root.
- Root: 196 model calls; 110 wait calls; 24 messages to agents; 12 follow-up dispatches.
- Checking started while scouts were active. Scan checker needed a later question-only follow-up that added no verdicts.
- Scan/root-runtime investigation and verification overlapped.
- First independent review found useful issues: unrelated test citation, missing authority/helper pointers, missing checkout timing-test pointers.
- Later Verify failed only seven formatting/shape rules: four same-directory filename forms and three packed multi-file change triggers. Repair required another fixer, review, mapping revision and Verify cycle.
- Full hash lists repeatedly copied into agent replies/prompts; mapping revisions repeatedly restated machine-verifiable metadata.
- 33 small output files increased placement, ownership and review overhead. Count alone does not prove files unnecessary; require individual usefulness decisions earlier.

### Token accounting

- Aggregate total: 58,617,261 tokens; input 58,160,478; cached input 55,736,960; uncached input 2,423,518; output 456,783, including 213,510 reasoning tokens.
- Approximately 95.8% of input cached. Aggregate counts include repeated context across model calls; do not present as unique content or monetary cost. Models/rates/cache categories differ.
- Nine scouts combined: 21,743,994 total; 238,445 output, including 149,949 reasoning.
- Root orchestrator: 12,882,067 total; 33,050 output.
- Checkers combined: 12,406,278 total; 62,323 output.
- Placement/writing/mapping agent: 5,805,917 total; 68,547 output.
- Review/fixers/Verify combined: 4,817,053 total; 29,854 output.
- Initial scan: 961,952 total; 24,564 output.
- Largest individual total: orchestrator. Largest individual output: placement agent. Largest combined phase: scouts.
- Recorded models: scan/scouts gpt-6-luna, max; other roles gpt-6.1-sol, high. Existing instruction forces non-scout roles to inherit main binding.

## Proposed workflow

`scan -> bounded scouts -> focused verification -> compact placement -> fresh writers -> independent review/probe -> scripted acceptance`

### 1. Separate responsibilities and bound context

- Agent -> one role + bounded assignment. Never transition placement agent into writer.
- New independent assignment -> fresh agent with relevant artifacts; no accumulated conversation handoff.
- Continuation permitted only to complete/correct the same bounded assignment; context pressure -> save artifact + hand off to fresh worker.
- Avoid replacing each cosmetic administrative operation with a new agent. Remove operation or implement deterministic helper where possible.
- Writers -> disjoint owned file batches; explicit target revisions; preserve other workers/user edits. Choose batch size before dispatch.
- Keep orchestrator responsible for routing, scheduling and acceptance. Keep fresh reviewer independent of evidence production.

### 2. Store facts once; write prose once

- Checker owns canonical verified fact records: stable ID, precise statement/conditions, authority, verdict, optional flow ID and qualification.
- Placement owns only fact IDs -> target homes, file dispositions, dedup decisions and unresolved location alternatives. No second full manuscript.
- Writers consume assigned canonical fact records + placement routing; render final prose once. Update writer input contract: relevant verified facts must be readable, replacing current placement-as-sole-factual-payload rule.
- Preserve exact supported meaning, conditions, labels and provenance through rendering; source browsing cannot introduce unverified claims.
- Keep fact-to-file references in compact machine-readable sidecar. Scripts maintain hashes/inventory; agents decide semantic homes and wording.
- Final mapping -> one authoritative index, with bounded change records where useful. Avoid chains of large base/delta/final manuscripts and repeated 33-hash prompt blocks.
- Reviewer may read sanitized target/revision/ownership manifest without access to underlying investigation evidence.

### 3. Remove overlapping investigation and artificial follow-ups

- Merge root/scan factual verification where scopes overlap; no mandatory separate scan checker solely because mode is Full.
- Scan collects orientation/intake/scopes. Extra root scout justified only by genuinely complex runtime/E2E behavior.
- Checkers start after their required inputs are terminal. Prefer one clear barrier initially; optimize overlap only with explicit immutable dependencies.
- Pending producer -> scheduling state, not evidence gap requiring another verification assignment.
- Structured cross-scope question index -> question ID, original flow, contract, target owner, status. Each question routed once; avoid every checker repeatedly searching every note.
- Select/deduplicate guidance-worthy candidates before expensive verification; preserve independent checking of selected consequential claims.
- Unknown intent/dependency behavior -> report bounded uncertainty; no repeated expansion solely to eliminate all unknowns.

### 4. Separate mechanical acceptance from semantic review

- Before independent review: deterministic path/style/shape preflight on draft files.
- Extend path helper to distinguish file#symbol references, approved external process paths, missing targets and cosmetic filename forms.
- Resolve same-directory filename rules consistently in writer instructions and validator.
- Parent + per-file sub-bullets for multi-file triggers -> writer preflight; automate detection/normalization where reliable.
- Keep fresh semantic review/probe: authority discoverability, wrong test claims, lost scope, duplication, practical harness/timing pointers.
- New/corrected behavioral claim -> focused checker then supported fix. Existing-authority formatting repair -> no new factual verdict cycle.
- Formatting-only repair -> changed-file checks + targeted review when meaning could be lost. Preserve unaffected semantic acceptance using confirmed unchanged revisions.
- Final acceptance mostly scripted: allowed writes, baseline comparison, counterparts, target inventory, path checks, required structure and complete provenance references.
- Cosmetic failure must not restart unrelated evidence investigation. Decide explicitly which style rules are mandatory versus autoformatted/warnings.

### 5. Budget work and configure role costs

- Add explicit per-assignment scope, artifact and completion budgets. Ceiling is not a target to fill.
- Placement output bounded by routing metadata; checker/scout output prioritizes decisions affecting future edits.
- Model/effort binding configurable by role; avoid forcing rendering, formatting and metadata work onto main model/high effort.
- Respect explicitly requested profiles exactly. Escalate difficult factual disputes selectively; do not silently change user-selected models.
- Nested file -> concrete edit trigger/hidden risk + useful loading boundary. Review tiny one-fact files for parent placement when boundary adds no value; no arbitrary universal file cap.
- Use completion notifications/bounded waits; reduce short polling, repeated nudges and empty status updates. Respect host-required communication intervals.
- Record per-role and per-phase usage, cached/uncached input, output/reasoning, calls, duration and artifact sizes for future comparisons.

## Protections to retain

- Immutable baseline and final allowed-write comparison, including pre-existing dirty/untracked edits.
- Selected AGENTS.md/CLAUDE.md mode and counterpart protections; no repository ignore-file changes.
- One owner per mutable target; no conflicting writers; terminal handoff and current revision checks.
- One home per fact/flow; supported labels/qualifications; no instruction-to-instruction inventory.
- Independent review/probe; actionable exact failures; bounded retries and honest incomplete status.
- Useful ignored run artifacts for resume/audit; no application/test/install/network effects merely to initialize instructions.
- Full/Light scope differences and explicit invocation policy; preserve unless user requests change.

## Other execution issues

- Oversized Windows command failed before process launch. Use bounded patch writes; avoid shell arguments carrying entire artifacts.
- PowerShell rg wildcard arguments required concrete roots plus -g filters.
- Helper returned false positives for four file#symbol pointers and authorized C:/wt directive; final PASS required contextual classification despite exit 1.
- API test helpers use os.tmpdir(); future authorized tests must route C: scratch beneath C:/wt.
- Known repository uncertainties: dependency nested rollback/savepoints, intended standing-order production scheduler/cadence, lasting membership-export omission policy. Preserve reported uncertainty; do not turn into guarantees during skill refactor.

## Suggested implementation order and acceptance

1. Read package entrypoint, workflow, contracts, policy, role scripts, style and helpers. Map role/schema dependencies before editing; replace contradictory contracts together.
2. Define canonical fact records, compact placement routing, writer provenance output and sanitized reviewer manifest.
3. Remove role switching and LLM-only hash/mapping administration; implement bounded fresh writer dispatch and deterministic metadata handling.
4. Move mechanical preflight before semantic review; correct path-helper classifications; define narrow repair invalidation rules.
5. Add focused helper tests/scenarios: valid symbol/external references, genuine missing path, same-directory normalization, packed triggers, missing provenance, outside write, dirty baseline preservation and stale target conflict.
6. Walk through Light and Full; late factual correction, formatting-only repair, changed user file and unavailable model/tool. No silent substitutions or permission broadening.
7. Benchmark comparable untouched fixture/checkout under C:/wt. Preserve current repository and generated output; never delete/reset user files to recreate original baseline.
8. Report measured differences in duration, per-role usage, generated output usefulness and validation failures. No unsupported promised savings percentage.

Completion criteria:
- Placement agent never becomes writer; independent assignments start with bounded fresh context.
- No placement manuscript duplicating generated files; provenance remains exact and auditable.
- Mechanical errors detected before independent review; cosmetic repair does not rerun unrelated semantic work.
- Useful factual checking, fresh review and write-boundary protections preserved.
- No artificial pending-input evidence gaps or duplicate scan/root verification requirement.
- Fewer coordination calls, repeated artifact reads and mapping rewrites demonstrated against baseline; no regression hidden by reduced checks.
