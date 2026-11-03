# Workflow

## Outcome and modes

Result: concise selected instruction files, source notes and final report retained in run folder. Explicit invocation only.

- Light: root selected file only; ~3-5 scouts total incl. follow-ups; no flows section. Merge supporting areas into main domains.
- Full: root + useful nested selected files; meaningful independent boundaries; <=20 scouts total incl. follow-ups; size to meaningful domains + unowned cross-boundary mechanisms + follow-up round, not minimum. Split before context becomes unwieldy.
- Scout total counts initial and follow-up scout agents, including retries; host/user limits win. Keep ~a quarter of the limit for follow-ups. Scouts use selected scout binding (`inherit` -> orchestrator's model/effort). Scan and every other role inherit orchestrator's model/effort; no per-role overrides or cheaper substitutes.
- Independent checker and reviewer remain separate from the work checked. Continue repair workers when useful per contracts; no nested agents.

## Resources and boundary

Resolve package resources in recipient's workspace; missing role, policy, style, helper or required artifact blocks affected work.

- [Repository policy](repository-analysis.md): scan, investigation, selection, placement, commands, architecture, flows and shape.
- [Generated content](generated-content.md) and [bundled style](../assets/llm-oriented-markdowns/llm-oriented-markdowns.md): writing, review and repair.
- [Contracts](contracts.md): capabilities, handoffs, helpers, ownership, conflicts and recovery.
- Roles: `agents/scan.md`, `scout.md`, `checker.md`, `placement.md`, `writer.md`, `reviewer.md`, `fixer.md`, `followup.md`.

Only selected mode-approved instruction files and run folder may change. Selecting `AGENTS.md` protects `CLAUDE.md` and `.claude/`; selecting `CLAUDE.md` protects `AGENTS.md` and `.agents/`. Light never changes nested files. Never change repository `.gitignore`.

Default run folder: `<repository-root>/.init-project/runs/<YYYY-MM-DDTHHMM>/`, unique suffix on collision. User/host location restrictions override default; alternate approved root uses stable repository-specific directory and timestamp (`--external-run` for baseline). Scan creates folder and inner `.gitignore` containing `*`, manifest and immutable baseline before instruction writes. Keep scratch/evidence there and uncommitted. Manifest records root/run, time, Git/HEAD/dirty state when available, choices and scout binding. Prior notes are leads, never proof. State tracks current assignments, paths, decisions and completion per contracts.

## Flow

Intake -> scan -> scouts -> one follow-up planner/fresh scout round -> selective checkers -> placement -> writers -> one independent reviewer pass/direct fixes -> unresolved repairs as needed -> final helper gate. Dispatch ready independent work with disjoint outputs up to capacity; wait for required inputs before dependent stages. Coordinator may handle small jobs directly (concise findings, a note, a diff) per SKILL Orchestration; pass artifact paths and brief summaries rather than loading all evidence. Preserve reviewer's independent initial view.

## 1. Intake and binding

Reuse known choices. Ask only missing selected filename (`AGENTS.md` or `CLAUDE.md`), mode (Light/Full with scout counts), and scout model. Recommend a cheaper model than orchestrator's over `inherit`; list a few models visible in harness controls, else ask user to name one. Invite optional context; its absence never blocks. No repository inspection or child dispatch until required choices resolved. Preserve choices; unavailable requested binding -> ask, never substitute. Bind capabilities per contracts before first child.

## 2. Scan and investigate

Dispatch [scan](../agents/scan.md) with user context, boundary and bindings. Scan bootstraps run and writes `context.md`, `scan-note.md` and `investigation-map.md` per repository policy. Orchestrator chooses mode-sized ownership from map (Light folds mechanism questions into domain scouts; Full gives an unowned consequential mechanism its own scout); check for consequential missing domains and retain intentional skips. Light may assign root investigation; Full uses root scout only for genuinely complex runtime/E2E behavior, otherwise scan covers root orientation.

Dispatch [scouts](../agents/scout.md) with meaningful domains, prioritized edit questions, shared context and map. Scouts investigate per repository policy; notes preserve supported claims, conditions, references and consequential unresolved questions. A shared mechanism has a primary owner; other scouts trace the dependencies needed for their questions. Once initial scouts finish, dispatch one fresh [follow-up planner](../agents/followup.md) with remaining scout limit; dispatch fresh scouts for its questions with related notes. One follow-up round only; empty plan -> skip. Record unresolved consequential questions and next evidence step, even when no follow-up is feasible.

## 3. Check and place

Dispatch independent [checkers](../agents/checker.md) for low-confidence and risky claims and consequential conflicting explanations/boundary contracts per repository policy. Full assigns related areas; Light may use one checker for scan and all scout notes. Checker decisions and unresolved gaps remain in notes. Targeted follow-up may cross initial boundaries; an unanswered consequential question is reported, never promoted to fact. Do not repeatedly expand solely to eliminate uncertainty.

Dispatch [placement](../agents/placement.md) with current accepted notes and existing-file baseline. Produce a simple file-to-guidance plan with dispositions, directive references and disjoint writer ownership. Evidence dispute -> checker; substantive home dispute -> placement decision. Low-value, rejected and unresolved claims stay out. No per-fact routing revision, retirement or automatic worker handoff for routine edits.

## 4. Write and review

Dispatch [writers](../agents/writer.md) with relevant accepted notes, plan, directives and owned targets. Check hashes and run path/shape checks per contracts. Preserve conditions, scope and directives.

After writers finish, dispatch one independent [reviewer](../agents/reviewer.md). Before reading generated files globally, perform path-local probe per reviewer; distinguish observed harness loading from ancestor-chain simulation. Record independent findings before consulting earlier worker evidence or editing metadata. If direct loading observation unavailable, report that limit.

Reviewer then makes straightforward wording, duplicate and low-value omission fixes directly under ownership/conflict rules and shared policies. Preserve unique conditions and directives. Route unsupported or uncertain factual corrections to checker and actual home disputes to placement. Do not create a duplicate-retirement protocol or dispatch agents solely to approve obvious deletion.

## 5. Repair and accept

Dispatch [fixer](../agents/fixer.md) only for unresolved findings, with relevant notes and target ownership. Use checker for uncertain factual claims and placement for substantive home decisions; give updated accepted notes directly to repair worker. Apply bounded repair policy per contracts. No targeted or repeated reviewer passes after the initial review, including after checker, placement or fixer repairs.

Before accepting, orchestrator runs `ledger.py compare` and path/shape helpers on all selected non-delete targets per contracts. Boundary FAIL -> stop affected work and report, never authorize further outside writes; helper FAIL -> fixer, rerun gate.

Complete only when required work and children are terminal, writer/reviewer/fixer checks and final helper gate pass, task boundaries hold, findings are resolved or explicitly reported, and consequential unanswered questions are disclosed. Relay actual run path, report and observed limits. Never claim success from tool termination alone.
