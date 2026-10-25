---
name: init-project
description: Initialize or refresh concise AGENTS.md or CLAUDE.md from repository scans that trace application flow in depth
disable-model-invocation: true
---

# Initialize Project Agent Context

Create minimal harness-agnostic navigation and warnings; leave detailed explanations in source.

## Scope

- Copying this skill to another repository -> copy entire `skills/init-project/` directory, including all `assets/`, `references/`, and `scripts/` files. Exclude nothing.
- Running this skill -> use bundled `assets/llm-oriented-markdowns/llm-oriented-markdowns.md` only within this workflow; do not copy it outside skill directory.

## Start

Reuse file, mode, scan model, and context supplied in invocation or established conversation. Before repository scan, ask only missing required choices; wait for answers:

`Before I scan repository:`

`1. Which file do you want: AGENTS.md or CLAUDE.md?`

`2. Which run do you want: Light (2-3 scan subagents, root instruction file only) or Full (up to 20 scan subagents, root plus useful nested instruction files)? Both trace application flow in depth; fact-check and review agents run in addition.`

`3. Which model should scan subagents use? A cheap model is recommended.`

Context optional -> invite project history, constraints, or known traps alongside missing choices; missing context alone never blocks scan.

Question 3 -> harness knows available cheap model -> replace `A cheap model` with `A cheap model (<model name>)`, using actual model name. Availability or cost unknown -> keep generic wording; never guess.

Do not inspect repository or spawn subagents until file, mode, and scan model resolved. All supplied -> proceed without repeating questions. Preserve choices for entire run. Named model unavailable in harness -> tell user, ask again; never silently substitute.

## Files

- AGENTS.md -> generate root and mode-selected nested `AGENTS.md` files. Do not create, update, or delete `CLAUDE.md` or `.claude/` files.
- CLAUDE.md -> generate root and mode-selected nested `CLAUDE.md` files. Do not create, update, or delete `AGENTS.md` or `.agents/` files.
- Selected file name = primary instruction file for rest of workflow.
- Light and Full -> only allowed write outside selected primary instruction files = run folder.

## Run folder

- Default path -> `<repository-root>/.init-project/runs/<YYYY-MM-DDTHHMM>/` (no colons; unique suffix on collision). User/host location restrictions override default. Alternate approved run root -> stable repository-specific directory beneath it, then timestamped run directory; avoid collisions between repositories sharing basename.
- Discover prior runs in selected repository-specific location and default location when allowed; never read forbidden locations. Record actual run path in manifest and final report. All scratch and evidence writes stay inside current run folder.
- Inner `.gitignore` containing `*` -> never committed; never edit repository `.gitignore`; works without git.
- `manifest.md` -> actual run path, timestamp, Git availability, commit hash + dirty-tree flag when available, file choice, mode, scan model, scopes once chosen.
- Holds scan context/proposal, baseline, notes, verified facts, gap lists, placement, verification/report. Scan agent creates run folder; later dispatches assign exact output paths. Scan, scouts, checkers, placement, fixers, and verify agents write only assigned artifacts; placement/writers/fixers also own assigned primary instruction files. Reviewer permissions per workflow.
- Harness lacks write-capable subagents -> producer returns content for assigned path; orchestrator saves content verbatim without reading, interpreting, or acting on raw evidence. Decision replies remain separate. No subagents available -> explain missing isolation and ask for viable harness; never silently execute evidence work as orchestrator.
- Kept after run for cheap re-analysis. Prior notes/verdicts = leads, never fact; manifest commit = HEAD and clean tree -> higher priority, still verify.

## Modes

- Light -> 2-3 scouts total across investigation rounds. Split repository into broad main domains; merge small or supporting areas into nearest main domain; no separate scans for minor boundaries. Create or update selected root instruction file only; do not modify nested instruction files.
- Full -> only scouts needed for meaningful independent boundaries, max 20 total across rounds. Prefer one narrow, non-overlapping domain per initial scout; large domain -> split across scouts rather than stretch one scout's context (cost and accuracy degrade as context grows). Fewer than 20 expected when evidence does not justify more.
- Roles: orchestrator = this agent; scouts (initial + follow-up) = only role counted toward mode total, use selected scan model. Scan, checkers, placement, writers, reviewer, fixers, verify -> inherit orchestrator model, not counted. Respect lower user or host agent limits.
- Light merges: scan; 2-3 scouts; one checker also places/writes root; fresh reviewer also runs agent-checkable Verify and writes report; fixers only for findings. Merged roles retain separate phase permissions and evidence gates.
- Payloads -> paths for references/artifacts when readable; paste content when not, and always for sections from this file. Subagents never read `SKILL.md` or inherit conversation. Every dispatch includes repository/run paths, mode, file choice, user/host restrictions, bounded ownership, permitted tools, expected output/reply; use only role tools, no skill invocations/task tracking, report contradictions/questions to orchestrator; only orchestrator asks user. Parallel writers -> disjoint ownership; preserve others' edits.
- Orchestrator dispatches every phase; owns scope, follow-up, placement acceptance, routing, and final acceptance decisions only. Read this file, short subagent replies, and short decision artifacts (scope proposal, gap lists, placement doubts, final verify report). References below -> delegation paths, read by assigned roles. Never read repository source, notes, verified facts/verdicts, placement evidence, generated files, or diffs. Never reconstruct evidence in dispatch; pass paths/scope IDs. Producer replies -> paths + few decision lines, never raw evidence.

## Workflow

1. Dispatch scan agent. Payload: invocation root/location hint, user context, pasted `## Files`, `## Run folder`, `## Modes`, paths to [repository analysis](references/repository-analysis.md) and bundled [LLM-oriented Markdown rules](assets/llm-oriented-markdowns/llm-oriented-markdowns.md). Agent resolves root; creates allowed run folder; discovers prior runs; checks Git once; captures status/diff baseline or before-state copies/hashes + inventory sufficient for write-boundary checks; writes manifest. Preflight ambiguity -> short question reply, orchestrator resolves before scan continues.
2. Scan agent performs bounded root scan per repository analysis `## Scan`; writes `context.md` shared digest, `scan-note.md` root-level factual claims (runtime, commands, architecture, orientation, existing-instruction facts; stable claim ID + statement + evidence path each), and `scope-proposal.md`. Kept user/process directives -> separate source/location + scope list, not factual claims. Scope proposal: scope ID, paths, one-line reason, prior-note paths, existing-instruction paths; end with conflicts/skipped section. Reply: root/run/baseline/artifact paths + proposed scope list. Orchestrator chooses scopes from proposal; scan agent records choice in manifest. Executable config/code win; doc/code and intent conflicts stay for final report, never generated files.
3. Dispatch scouts with [flow investigation brief](references/flow-investigation.md), accepted scope proposal, selected mode/model ("inherit" -> no model override), narrow non-overlapping scopes. Payload per brief: scope IDs/paths, proposal/context paths, prior-note/existing-instruction paths, assigned note path. Choose order from dependencies. Scout notes use stable claim IDs and flow IDs `<scope id>.F<n>`; cross-scope questions retain flow ID + contract path. Orchestrator reads note replies only; flow joining belongs to placement.
4. Dispatch checkers per [fact-check brief](references/fact-check.md). Full -> scan note gets own checker; area checkers get few relevant notes, split before one checker would read many. Light -> single checker gets scan + all scout notes. Payload: mode, scope IDs, note paths, all-notes directory, scope proposal, repository analysis `## Select content`/`## Shape` paths, assigned verified-facts + short gap-list paths. Checkers select doc-worthy claims, verify every candidate fact, group shared propositions within batch, resolve questions tagged for their scopes, assign labels, and promote only consequential leads. Verified facts use stable `#V<n>` verdict refs, exact supported statement/conditions, authority, source IDs, flow ID when any; refuted/unresolved never placed. Reply: paths + counts + top corrections; each producer ends output with conflicts/skipped section.
5. Orchestrator decides follow-ups from gap lists only: consequential conflicts, cross-domain questions, unclear behavior, weak evidence. Dispatch targeted scouts per brief, including scope IDs, relevant artifact paths, question/gap reference, needed evidence; scopes may cross initial domains. Prefer reusing completed scouts; total stays within mode limits. Route follow-up notes to one checker under same universal rule; unresolved gaps after follow-up -> report, never document. Complexity alone requires no extra round. No local evidence resolution by orchestrator.
6. Dispatch placement agent (Light -> same checker, explicit placement-phase permissions). Payload: verified-facts paths, existing-instruction paths/directive list, mode, assigned `placement.md` path, paths to repository analysis `## Placement`/`## Flows`/`## Shape`, bundled style rules. Agent reads verified facts and existing instructions; read-only listing/targeted source reads only for nested-file creation and same-fact duplicates, never substitute for checker verdict. Join cross-scope flows by flow ID. Plan covers each existing selected instruction file: keep, trim, delete; target/owner -> finished verified statement + authority + `<verified-facts path>#V<n>` verdict ref + flow ID group when relevant. Kept/generated process directives listed separately. Conflicting facts/locations -> short doubts artifact; orchestrator routes evidence doubts to one checker, returns verdict path to placement; decides location from placement reply. Reply: target files + fact count per file + concise fact-to-home ownership map + doubts path + conflicts/skipped. Accept placement from reply/doubts only.
7. Placement agent writes modest output, including many short files. Optional writers in either mode when parallel work pays -> disjoint file sets. Writing payload: accepted placement path, assigned files, repository root, pasted `## Generated content`, repository analysis/style paths (read both first). Light checker receives same explicit added root-file ownership. Writers use placement only as factual input, never notes/verdicts/source; write only planned facts/directives. Reply: changed paths, ownership-map changes, unresolved items. Placement agent keeps verdict mapping current after later moves/deletions/corrections; any new/changed factual statement needs checker verdict first.
8. After writes, dispatch one fresh reviewer, including root-only runs: repository analysis/style paths (read both first; follow style in edits), generated file list, concise ownership map from placement reply, pasted probe in step 10. Edit ownership = generated/updated primary instruction files only; may read repository code; Full -> no run-folder access, no notes/verdicts/placement. Light -> exact baseline paths + assigned report path allowed only for Verify/report phase; still no notes/verdicts/placement. Reviewer must:
   - Find exact and semantic duplication across and within generated files; keep copy in file supplied ownership map points to, delete others. Moving shared fact to its owner is not weakening; never drop scope, exceptions, or conditions. Disagrees with location -> report; orchestrator decides.
   - Delete pointers to, lists of, or summaries of other instruction files, except mandatory root Maintenance rule; rewrite needed cross-domain references as source paths + hazard.
   - Fix wording directly; report moved or deleted guidance.
   - Report dubious, unsupported, or missing-pointer lines, and pointers whose cited file lacks claimed thing (file + line); never delete on support grounds, never guess. Reply includes moved/deleted guidance, support findings, probe gaps, conflicts/skipped; no raw evidence.
9. Every reported line -> fixer, never orchestrator evidence read. Payload: findings, disjoint owned files, repository root, accepted placement path, repository analysis/style paths, pasted `## Generated content`. Fixer verifies in code; exact verdict-supported wording/pointer -> fix; deletion -> apply when unsupported. New/corrected fact or scope lacking verdict -> return candidate + evidence paths; orchestrator routes to checker, verdict to placement, updated placement to fixer before factual write. Location doubt -> placement decision loop. No findings -> skip. Pass fixer/reviewer move/delete replies to placement agent for mapping reconciliation.
10. Reviewer probes typical change and read-only investigation: can future agent find behavioral authority, required helpers, test harness setup, timing controls? Probe report-only: file + missing thing + reason; identify low-value guidance whose removal changes no decision. Orchestrator routes consequential probe gaps to checker; verified result -> placement -> fixer for smallest pointer/warning. Reviewer never adds probe discoveries directly. Reconcile mapping before Verify.
11. Dispatch Verify per section below; failures -> fixers through step 9, rerun failed checks after fixes. Missing architectural rationale -> optionally ask user at end why consequential choices were made; finish supported documentation first. Incorporate answer through checker/placement/fixer routing; never invent reasons. Orchestrator accepts from verify report + role replies, relays `report.md`.

## Generated content

- Default omit. Keep source pointer + reason to inspect; complex logic needs entry point, authority, and non-obvious risk, not copied walkthrough. Paths per bundled style rules. Reference detailed docs by path; never copy doc content.
- Avoid volatile implementation prose (line numbers, function bodies, transient values), inventories, exhaustive environment lists, generic coding advice, and host-provided agent or skill-routing rules.
- Root file -> global context. Full mode nested files -> subtree-only deltas; never repeat inherited rules.
- Destructive commands -> state impact and required authorization.
- Generated/runtime files -> identify only when agents might edit or commit them accidentally.
- Do not reference initializer plumbing (incl. run folder) or skill locations/discovery in generated files.
- Instruction files never reference other instruction files (harness auto-loads nested files), except mandatory root Maintenance rule, per repository analysis `## Shape`.
- `## Pitfalls` only for verified local failure modes per repository analysis; omit empty sections.

Add following rules to root instruction file only; never to nested files:

"
# Maintenance
Update this file or closest nested instruction file when guidance becomes stale; durable boundaries, hazards, sources of truth change; or reusable lessons, workarounds, user instructions emerge. AGENTS.md/CLAUDE.md conflict with repository evidence -> warn user with "WARNING".

# AI Documentation and Code Comments
AI docs and code comments -> terse facts for future agents; non-obvious architecture, decisions, cross-cutting constraints only. Default no comment; edit only when needed. Omit history, dates, code narration. One fact -> one home across docs/comments.
"

Generated files use labels or `intent unknown` -> append legend for used items only to AI Documentation paragraph: "`Invariant:` -> intended behavior, preserve. `Limitation:` -> known gap, quirk, or bug, not contract; fix only when task asks. `intent unknown` -> ask before changing."

## Verify

### Orchestrator self-check from replies

- Confirm scouts used selected scan model; all other roles inherited orchestrator model; scout total respects mode/user/host limits.
- Confirm fresh reviewer completed dedup + report-only probe, including root-only runs. Run-folder write boundary -> verify agent's baseline result, never orchestrator diff read.
- Confirm placement accepted, evidence doubts routed to checker, reported lines routed to fixers, probe gaps checked before additions, mapping reconciled, and failed checks resolved or explicitly reported.

### Agent-checkable items

Full -> dedicated verify agent; Light -> reviewer also executes these checks report-only, never repairs Verify failures. Paste this subsection into dispatch. Shared payload: repository root, file choice/mode, generated file list, actual run folder + exact manifest/baseline paths, repository analysis/style/script paths, reviewer/fixer decision replies, assigned `report.md` path. Full adds accepted `placement.md`, verified-facts paths, producer conflicts/skipped section paths (scan, checkers, placement). Light -> placement producer supplies compact final mapping + verdict refs and producer conflicts/skipped extracts as verify-only payload; reviewer receives no note/verdict/placement access. Verify role may read source/generated files and listed verification inputs, use read-only Git/baseline comparisons, run path-check script, and write assigned report only. Verify never edits instruction files; send failures to orchestrator.

- AGENTS.md -> confirm no `CLAUDE.md` or `.claude/` file changed.
- CLAUDE.md -> confirm no `AGENTS.md` or `.agents/` file changed.
- Light -> confirm no nested instruction file changed.
- Compare against captured baseline; confirm actual run folder allowed, has inner `.gitignore` (`*`) and manifest; repository `.gitignore` unchanged; no task writes outside primary instruction files and run folder.
- Confirm refuted claims absent from generated files; unresolved claims omitted or reported as gaps.
- Confirm every generated factual line maps in `placement.md` to exact confirmed/corrected verdict ref covering scope, including orientation/runtime/commands and late edits. Mandatory/generated and preserved user/process directives exempt; factual assertions embedded in directives still checked. Light -> compare final files with supplied final mapping; evidence-verdict audit belongs to checker/placement, not reviewer.
- Confirm reviewer write permissions held: Full -> no run-folder edits; Light -> only assigned report artifacts, never notes/verdicts/placement. Use baseline and producer replies.
- Review final-pass diff for lost scope, meaning, or unsupported formatting changes.
- Confirm bundled LLM-writing rules were not copied outside skill directory.
- Confirm generated files omit initializer plumbing and skill-location notes.
- Confirm no generated file references other instruction files except mandatory root Maintenance rule.
- Confirm pitfalls are evidence-backed; report empty or low-value sections for fixer removal.
- Confirm material investigation gaps are resolved or reported; nonstandard architecture is documented, rationale supported or explicitly unknown, and complex domains have actionable source pointers.
- Confirm Maintenance and AI Documentation rules appear in root instruction file only.
- Confirm explicit source pointers exist and each cited file itself contains claimed thing (not sibling or caller). Run `python -B <skill-directory>/scripts/check-paths.py <repository-root>` with any Python 3 (stdlib only); heuristic -> judge missing/format reports in context, report failures for fixer. Confirm each flow entry (under `## Flows` or sole headingless section) maps through flow ID group in placement to checked facts, meets doc-worthy threshold, lives in owning domain nested file, and appears once. Light -> use supplied mapping; distilled flow findings never create root `## Flows`.
- Confirm root instruction file starts with `# Agent instructions` + one-line project description, and has no `## Flows`.
- Confirm generated files use one-fact bullets; multi-fact entries and multi-file change triggers split into sub-bullets; nested files open with scope line (+ main entry point path when one exists); labels match checked placement wording; single-section nested files omit heading; all per repository analysis `## Shape`.
- Confirm root `## Commands` has max 5 lines, essential commands only.
- Confirm root has `## Architecture` within repository analysis scope and no separate boundaries/overview/repository-map section.
- Confirm nested instruction files have no commands.
- Confirm `## Testing` content appears only in root and harness-owning nested files per repository analysis `## Shape`.
- Review generated instructions for volatile detail and excess length. Strong-claim/exception verification belongs to checkers; questionable factual line -> failure routed through checker, never new Verify verdict.
- Review diff; unexpected writes -> report file/line and impact. Run application tests only if changes extend beyond instruction files and separately authorized; outside-write failure never authorizes more writes.
- Write short `report.md`: pass/fail + file/line per failure (artifact path/check name when no generated line), required routing, unresolved limits. Compile producer conflicts/skipped sections + own results: changed files, chosen boundaries, documented/skipped flows, validation, evidence gaps, doc/code and intent conflicts, actual kept run folder path (reusable; safe to delete), initializer directory deletable after success. Reply: report path + pass/fail + short failures; orchestrator reads/relays this decision report, never raw evidence/diff.
