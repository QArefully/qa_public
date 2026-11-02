# Workflow

## Outcome and modes

Result: concise selected instruction files, source notes and final report retained in run folder. Explicit invocation only.

- Light: root selected file only; 2-3 scouts total across investigation rounds; no flows section. Merge supporting areas into main domains.
- Full: root + useful nested selected files; meaningful independent boundaries; <=20 scouts total across rounds. Split before context becomes unwieldy; fewer expected.
- Scout total counts initial and follow-up scout agents, including retries; host/user limits win. Scouts use selected scout binding (`inherit` -> orchestrator's model/effort). Scan and every other role inherit orchestrator's model/effort; no per-role overrides or cheaper substitutes.
- Independent checker and reviewer remain separate from the work checked. Continue scouts or repair workers when useful per contracts; no nested agents.

## Resources and boundary

Resolve package resources in recipient's workspace; missing role, policy, style, helper or required artifact blocks affected work.

- [Repository policy](repository-analysis.md): scan, investigation, selection, placement, commands, architecture, flows and shape.
- [Generated content](generated-content.md) and [bundled style](../assets/llm-oriented-markdowns/llm-oriented-markdowns.md): writing, review, repair and Verify.
- [Contracts](contracts.md): capabilities, handoffs, helpers, ownership, conflicts and recovery.
- Roles: `agents/scan.md`, `scout.md`, `checker.md`, `placement.md`, `writer.md`, `reviewer.md`, `fixer.md`, `verify.md`.

Only selected mode-approved instruction files and run folder may change. Selecting `AGENTS.md` protects `CLAUDE.md` and `.claude/`; selecting `CLAUDE.md` protects `AGENTS.md` and `.agents/`. Light never changes nested files. Never change repository `.gitignore`.

Default run folder: `<repository-root>/.init-project/runs/<YYYY-MM-DDTHHMM>/`, unique suffix on collision. User/host location restrictions override default; alternate approved root uses stable repository-specific directory and timestamp (`--external-run` for baseline). Scan creates folder and inner `.gitignore` containing `*`, manifest and immutable baseline before instruction writes. Keep scratch/evidence there and uncommitted. Manifest records root/run, time, Git/HEAD/dirty state when available, choices and scout binding. Prior notes are leads, never proof. State tracks current assignments, paths, decisions and completion per contracts.

## Flow

Intake -> scan -> scouts -> selective checkers -> placement -> writers -> one independent reviewer pass/direct fixes -> unresolved repairs as needed -> final Verify. Dispatch ready independent work with disjoint outputs up to capacity; wait for required inputs before dependent stages. Coordinator may inspect concise findings, relevant notes, output or diff to resolve a concrete question; pass artifact paths and brief summaries rather than loading all evidence. Preserve reviewer's independent initial view.

## 1. Intake and binding

Reuse known choices. Ask only missing selected filename (`AGENTS.md` or `CLAUDE.md`), mode (Light/Full with scout counts), and scout model. Recommend a cheap scout model only when availability/cost known. Invite optional context; its absence never blocks. No repository inspection or child dispatch until required choices resolved. Preserve choices; unavailable requested binding -> ask, never substitute. Bind capabilities per contracts before first child.

## 2. Scan and investigate

Dispatch [scan](../agents/scan.md) with user context, boundary and bindings. Scan bootstraps run and writes `context.md`, `scan-note.md` and `investigation-map.md` per repository policy. Orchestrator chooses mode-sized ownership from map; check for consequential missing domains and retain intentional skips. Light may assign root investigation; Full uses root scout only for genuinely complex runtime/E2E behavior, otherwise scan covers root orientation.

Dispatch [scouts](../agents/scout.md) with meaningful domains, prioritized edit questions, shared context and map. Scouts investigate per repository policy; notes preserve supported claims, conditions, references and consequential unresolved questions. A shared mechanism has a primary owner; other scouts trace the dependencies needed for their questions. Once initial scouts finish, use focused follow-ups when needed and within scout limits. Continue a scout when its context is useful and limits permit; use a fresh scout for different context or a finished scout. Record unresolved consequential questions and next evidence step, even when no follow-up is feasible.

## 3. Check and place

Dispatch independent [checkers](../agents/checker.md) for mandatory categories and consequential conflicting explanations/boundary contracts per repository policy. Full assigns related areas; Light may use one checker for scan and all scout notes. Checker decisions and unresolved gaps remain in notes. Targeted follow-up may cross initial boundaries; an unanswered consequential question is reported, never promoted to fact. Do not repeatedly expand solely to eliminate uncertainty.

Dispatch [placement](../agents/placement.md) with current accepted notes and existing-file baseline. Produce a simple file-to-guidance plan with dispositions, directive references and disjoint writer ownership. Evidence dispute -> checker; substantive home dispute -> placement decision. Low-value, rejected and unresolved claims stay out. No per-fact routing revision, retirement or automatic worker handoff for routine edits.

## 4. Write and review

Dispatch [writers](../agents/writer.md) with relevant accepted notes, plan, directives and owned targets. Check hashes and run path/shape checks per contracts. Preserve conditions, scope and directives.

After writers finish, dispatch one independent [reviewer](../agents/reviewer.md). Before reading generated files globally, perform path-local probe in representative unnoted sibling, route and test mirror contexts; distinguish observed harness loading from ancestor-chain simulation. Record independent findings before consulting earlier worker evidence or editing metadata. If direct loading observation unavailable, report that limit.

Reviewer then makes straightforward wording and duplicate fixes directly under ownership/conflict rules and shared policies. Preserve unique conditions and directives. Route unsupported or uncertain factual corrections to checker and actual home disputes to placement. Do not create a duplicate-retirement protocol or dispatch agents solely to approve obvious deletion.

## 5. Repair, Verify and accept

Dispatch [fixer](../agents/fixer.md) only for unresolved findings, with relevant notes and target ownership. Use checker for uncertain factual claims and placement for substantive home decisions; give updated accepted notes directly to repair worker. Apply bounded repair policy per contracts. No targeted or repeated reviewer passes after the initial review, including after checker, placement or Verify repairs.

Dispatch [Verify](../agents/verify.md) with source notes, plan, outputs, baseline and unresolved decisions. Check source support, useful placement, preserved directives and task boundaries; run helpers per contracts. Repair specific failures as needed and rerun Verify when required to establish completion, without another reviewer. Boundary failure -> stop affected work and report, never authorize further outside writes.

Complete only when required work and children are terminal, writers/reviewer checks and final Verify pass, task boundaries hold, findings are resolved or explicitly reported, and consequential unanswered questions are disclosed. Relay actual run path, report and observed limits. Never claim success from tool termination alone.
