---
name: init-project
description: Initialize or refresh concise AGENTS.md or CLAUDE.md from repository scans that trace application flow in depth
disable-model-invocation: true
---

# Initialize Project Agent Context

Create minimal harness-agnostic navigation and warnings; leave detailed explanations in source.

## Scope

- Copying this skill to another repository -> copy entire `skills/init-project/` directory, including all `assets/` and `references/` files. Exclude nothing.
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
- Holds scout notes, checker verdicts, placement plan; orchestrator assigns each subagent its output path. Scouts and checkers = subagents whose only write = assigned run-folder file. Harness lacks write-capable subagents -> subagent returns content inline; orchestrator saves it to assigned path.
- Kept after run for cheap re-analysis. Prior notes/verdicts = leads, never fact; manifest commit = HEAD and clean tree -> higher priority, still verify.

## Modes

- Light -> 2-3 scouts total across investigation rounds. Split repository into broad main domains; merge small or supporting areas into nearest main domain; no separate scans for minor boundaries. Create or update selected root instruction file only; do not modify nested instruction files.
- Full -> only scouts needed for meaningful independent boundaries, max 20 total across rounds. Prefer one narrow, non-overlapping domain per initial scout; large domain -> split across scouts rather than stretch one scout's context (cost and accuracy degrade as context grows). Fewer than 20 expected when evidence does not justify more.
- Roles: orchestrator = this agent; scouts = scan subagents (initial + follow-up), only role counted toward mode total, use selected scan model; checkers (fact-check), writers, reviewer, fixers -> no model override (inherit orchestrator model), not counted. Respect lower user or host agent limits.
- Payloads -> pass file paths (briefs, rules, plan, notes) when subagent can read files; paste content only when it cannot, or when source is this file (subagents never read it).
- Orchestrator does shallow root scan, chooses boundaries; never delegates follow-up decisions, placement plan, or final verification. Every dispatch states: use only tools role needs, no skill invocations or task tracking; writer, reviewer, fixer dispatches also state: contradiction or open question -> report to orchestrator; only orchestrator asks user (briefs carry same rule).

## Workflow

1. Resolve repository root. Read [repository analysis](references/repository-analysis.md) and bundled [LLM-oriented Markdown rules](assets/llm-oriented-markdowns/llm-oriented-markdowns.md). Create allowed run folder; check prior runs. Check Git availability once; capture relevant status/diff baseline when available. Otherwise save before-state copies or hashes and file inventory in run folder sufficient to verify write boundaries and instruction changes.
2. Inspect bounded root context per repository analysis `## Scan`. Code and executable config win conflicts. Report doc/code and intent conflicts to user in final report; never record them in generated files.
3. Identify core boundaries where local context or flow changes implementation choices. Read [flow investigation brief](references/flow-investigation.md). Dispatch scouts per selected mode on selected scan model ("inherit" -> no model override), non-overlapping scopes, payload per brief; choose order from dependencies, not fixed sequence. Read each note once (re-read only for specific doubt); join flows crossing scopes via reported contracts.
4. Assess whether findings explain consequential behavior. Conflicting reports, unresolved cross-domain behavior, unclear invariants/failure handling, or weak evidence -> resolve locally or dispatch targeted follow-up scouts (scope may cross initial domains; payload per brief). Prefer reusing completed scouts; new ones stay within mode limits. Complexity alone does not require another round. Resolve material gaps or report limits explicitly; never turn uncertainty into documented fact.
5. Select exact claims and intended scope worth retaining in generated files or final report per repository analysis `## Select content` before checking; narrow overbroad wording first. Independent checker required when: low confidence; absence/exclusivity ("never", "only", "no X"); security or money regardless of confidence; existing-instruction facts not verified by scouts. Group overlapping claims by authority; check shared proposition once, map verdict to all covered claim IDs, and check distinct conditions separately. Batch by area/files into few checkers (split when one would read many notes), payload per [fact-check brief](references/fact-check.md). Apply verdicts per repository analysis `## Select content`.
6. After verdicts, write compact `placement.md` per repository analysis `## Placement`: target file/owner -> verified fact or finished wording + authority path + note path/claim ID + verdict when checked. Apply corrections; reuse finished wording rather than draft prose twice. Covers each existing instruction file: keep, trim, or delete.
7. Write only planned facts. Modest output -> orchestrator writes directly, including many short files. Writers optional when parallel work saves effort; assign disjoint file sets and provide placement plan path, assigned files, repository root, this file's `## Generated content` section pasted verbatim, and paths to repository analysis and bundled style rules (read both first). Writers read plan only, never notes/verdicts.
8. After writes, dispatch one fresh reviewer, including root-only runs, with paths to bundled style rules and repository analysis (read both first; follow style in all edits), generated file list, and concise fact-to-home ownership map pasted from placement plan. Edit ownership = generated or updated primary instruction files only; may read repository code; no run folder access. Reviewer must:
   - Find exact and semantic duplication across and within generated files; keep copy in file `## Placement` points to, delete others. Moving shared fact to its owner is not weakening; never drop scope, exceptions, or conditions. Disagrees with location -> report; orchestrator decides.
   - Delete pointers to, lists of, or summaries of other instruction files, except mandatory root Maintenance rule; rewrite needed cross-domain references as source paths + hazard.
   - Fix wording directly; report moved or deleted guidance.
   - Report dubious, unsupported, or missing-pointer lines (file + line); never delete on support grounds, never guess.
9. Reported lines -> orchestrator re-checks directly when few; else dispatch fixers with findings, owned files, repository root, paths to bundled style rules and repository analysis. Fixer verifies in code, then corrects, adds pointer, or deletes claim. Required independent checks from step 5 still apply. None -> skip.
10. Probe typical change and read-only investigation: can agent find behavioral authority, required helpers, test harness setup, and timing controls? Fill consequential gaps with smallest source pointer or warning, verified under step 5 evidence rules. Delete guidance whose removal changes no investigation or implementation decision.
11. Missing architectural rationale after investigation -> optionally ask user at end why consequential choices were made. Finish supported documentation first; unknown rationale never blocks documenting verified nonstandard architecture. Incorporate answer when available; never invent reasons.

## Generated content

- Default omit. Keep source pointer + reason to inspect; complex logic needs entry point, authority, and non-obvious risk, not copied walkthrough. Reference detailed docs with plain repository-relative paths; never use Markdown links or copy doc content.
- Avoid volatile implementation prose (line numbers, function bodies, transient values), inventories, exhaustive environment lists, generic coding advice, and host-provided agent or skill-routing rules.
- Root file -> global context. Full mode nested files -> subtree-only deltas; never repeat inherited rules.
- Destructive commands -> state impact and required authorization.
- Generated/runtime files -> identify only when agents might edit or commit them accidentally.
- Do not reference initializer plumbing (incl. run folder) or skill locations/discovery in generated files.
- Instruction files never reference other instruction files, except mandatory root Maintenance rule, per repository analysis `## Shape`.
- `## Pitfalls` only for verified local failure modes per repository analysis; omit empty sections.

Add following rules to root instruction file only; never to nested files:

"
# Maintenance
Update this file or closest nested instruction file when guidance becomes stale; durable boundaries, hazards, sources of truth change; or reusable lessons, workarounds, user instructions emerge. AGENTS.md/CLAUDE.md conflict with repository evidence -> warn user with "WARNING".

# AI Documentation and Code Comments
AI docs and code comments -> terse facts for future agents; non-obvious architecture, decisions, cross-cutting constraints only. Default no comment; edit only when needed. Omit history, dates, code narration. One fact -> one home across docs/comments.
"

## Verify

- AGENTS.md -> confirm no `CLAUDE.md` or `.claude/` file changed.
- CLAUDE.md -> confirm no `AGENTS.md` or `.agents/` file changed.
- Light -> confirm no nested instruction file changed.
- Compare against captured baseline; confirm actual run folder allowed, has inner `.gitignore` (`*`) and manifest; repository `.gitignore` unchanged; no task writes outside primary instruction files and run folder.
- Confirm scouts used selected scan model; checkers, writers, reviewer, fixers inherited orchestrator model.
- Confirm refuted claims absent from generated files; unresolved claims omitted or reported as gaps.
- Confirm every retained claim requiring independent check under step 5, incl. additions in steps 9-10, has checker verdict (confirmed/corrected) covering exact scope.
- Confirm fresh reviewer completed deduplication, including root-only runs, and did not edit run folder.
- Review final-pass diff for lost scope, meaning, or unsupported formatting changes.
- Confirm bundled LLM-writing rules were not copied outside skill directory.
- Confirm generated instruction files use plain repository-relative paths, not Markdown links.
- Confirm generated files omit initializer plumbing and skill-location notes.
- Confirm no generated file references other instruction files except mandatory root Maintenance rule.
- Confirm pitfalls are evidence-backed; remove empty or low-value sections.
- Confirm material investigation gaps are resolved or reported; nonstandard architecture is documented, rationale supported or explicitly unknown, and complex domains have actionable source pointers.
- Confirm Maintenance and AI Documentation rules appear in root instruction file only.
- Confirm explicit source pointers exist; check path tokens in context, not every prose slash. Confirm each `## Flows` entry is scout-backed, meets doc-worthy threshold, lives in owning domain nested file, and appears once.
- Confirm root instruction file has no `## Flows`.
- Confirm root `## Commands` has max 5 lines, essential commands only.
- Confirm root has `## Architecture` within repository analysis scope and no separate boundaries/overview/repository-map section.
- Confirm nested instruction files have no `## Commands`.
- Confirm `## Testing` appears only in root and harness-owning nested files per repository analysis `## Shape`.
- Review generated instructions for unsupported claims, volatile detail, and excess length. Verify strong claims against implementation and meaningful exceptions.
- Review diff. Run application tests only if changes extend beyond instruction files.
- Report changed files, chosen boundaries, documented and skipped flows, validation, evidence gaps, doc/code conflicts, kept run folder path (reusable for re-analysis; safe to delete), and that the initializer directory may be deleted after success.
