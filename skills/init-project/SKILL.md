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

First response -> ask following questions, then stop:

`Before I scan repository:`

`1. Which file do you want: AGENTS.md or CLAUDE.md?`

`2. Which run do you want: Light (2-3 subagents, root instruction file only) or Full (up to 10 subagents, root plus useful nested instruction files)? Both trace application flow in depth.`

`3. Any project context, history, constraints, or known traps that would help agents understand it? Reply "skip" if none.`

Do not inspect repository or spawn subagents until user selects file and mode. Preserve both choices for entire run.

## Files

- AGENTS.md -> generate root and mode-selected nested `AGENTS.md` files. Do not create, update, or delete `CLAUDE.md` or `.claude/` files.
- CLAUDE.md -> generate root and mode-selected nested `CLAUDE.md` files. Do not create, update, or delete `AGENTS.md` or `.agents/` files.
- Selected file name = primary instruction file for rest of workflow.

## Modes

- Light -> use 2-3 scan subagents total across investigation rounds. Split repository into broad main domains. Merge small or supporting areas into nearest main domain; do not create separate scans for minor boundaries. Create or update selected root instruction file only. Do not modify nested instruction files. No `## Flows`; flow findings inform root architecture, invariants, pitfalls only.
- Full -> use only scan subagents needed for meaningful independent boundaries, maximum 10 total across investigation rounds. Prefer one non-overlapping domain per initial scan subagent. Fewer than 10 is expected when evidence does not justify more. Nested files may exist solely to hold domain flows.
- Both modes -> respect lower user or host agent limits. Main agent performs shallow root scan, chooses boundaries, owns cross-domain synthesis and initial writes. Subagents trace application flow in depth within assigned scope. After every run, reuse one completed scan subagent for final review and deduplication, including root-only runs. Review does not increase selected mode subagent total.

## Workflow

1. Resolve repository root. Read [repository analysis](references/repository-analysis.md) and bundled [LLM-oriented Markdown rules](assets/llm-oriented-markdowns/llm-oriented-markdowns.md).
2. Inspect manifests, executable config, tests, CI, maintained docs, existing agent instructions, flow entry points, and shallow repository structure. Code and executable config win conflicts; report unresolved intent conflicts.
3. Identify core boundaries where local context or flow changes implementation choices. Read [flow investigation brief](references/flow-investigation.md); it defines subagent method, complexity signals, and output. Dispatch read-only subagents per selected mode, each with full brief, exact non-overlapping scope, repository root, and user context. Merge findings and join flows crossing scopes.
4. Before writing, assess whether findings explain consequential behavior. Conflicting reports, unresolved cross-domain behavior, unclear invariants/failure handling, or weak evidence -> resolve locally or dispatch targeted second-round investigation. Prefer reusing completed subagents; new agents stay within selected mode limits. Give each follow-up one question, existing findings, bounded scope (may cross initial domains), and evidence needed to resolve it. Complexity alone does not require another round. Resolve material gaps or report limits explicitly; never turn uncertainty into documented fact.
5. Write selected primary instruction files per selected mode. Merge valuable existing rules in selected files.
   - Light -> root only.
   - Full -> root plus only useful nested files.
   - Flows -> apply threshold, placement, and format from repository analysis `## Flows`; below threshold -> omit. Root never gets `## Flows`.
6. After initial writes, assign final review and deduplication to one completed scan subagent. Grant edit ownership only for generated or updated primary instruction files. Subagent must:
   - Read `<skill-directory>/assets/llm-oriented-markdowns/llm-oriented-markdowns.md` before editing; follow it for all edits.
   - Enforce every bundled writing and formatting rule in each owned file, including terse prose, linear structure, compact formatting, flat lists, and prohibited constructs.
   - Compare owned files with all applicable root and nested primary instruction files for exact and semantic duplication. Single-file runs still require full within-file deduplication.
   - Keep each fact or rule only in most relevant place: repository-wide guidance at root; subtree-only guidance in nearest applicable nested file.
   - Delete duplicate copies from owned files without weakening scope, exceptions, or meaning.
   - Replace flow narration with source pointer + consequential hazard; retain hop chains only where hidden ownership or ordering needs explanation.
   - Delete pointers to, lists of, or summaries of other instruction files; rewrite needed cross-domain references as source paths + hazard.
   - Fit root `## Commands` in max 5 lines per repository analysis `## Commands`; delete non-essential commands.
   - Hold root `## Architecture` to repository analysis `## Architecture` scope; move single-domain detail to owning nested file, delete excluded content.
   - Remove any `## Commands` section or runnable commands from nested files; root scoped-run pattern covers subtree targets.
   - Edit files directly and report moved or deleted guidance. Do not return recommendations only.
7. Probe typical change and read-only investigation: can agent find behavioral authority, required helpers, fixture/assertion examples, and timing controls? Fill consequential gaps with smallest source pointer or warning. Delete guidance whose removal changes no investigation or implementation decision.
8. Missing architectural rationale after investigation -> optionally ask user at end why consequential choices were made. Finish supported documentation first; unknown rationale never blocks documenting verified nonstandard architecture. Incorporate answer when available; never invent reasons.

## Generated content

- Default omit. Keep source pointer + reason to inspect; complex logic needs entry point, authority, and non-obvious risk, not copied walkthrough. Reference detailed docs with plain repository-relative paths; never use Markdown links or copy doc content.
- Avoid volatile implementation prose (line numbers, function bodies, transient values), inventories, exhaustive environment lists, generic coding advice, and host-provided agent or skill-routing rules.
- Root file -> global context. Full mode nested files -> subtree-only deltas; never repeat inherited rules.
- Destructive commands -> state impact and required authorization.
- Generated/runtime files -> identify only when agents might edit or commit them accidentally.
- Do not reference initializer plumbing or skill locations/discovery in generated files.
- Instruction files never reference other instruction files per repository analysis `## Shape`.
- `## Pitfalls` only for verified local failure modes per repository analysis; omit empty sections.

Add following rules to root instruction file only; never to nested files:

"
# Maintenance
Update this file or closest nested instruction file when code invalidates guidance; durable boundaries, hazards, or sources of truth change; or work reveals reusable lessons, pitfall workarounds, or user instructions. AGENTS.md/CLAUDE.md conflict with repository evidence -> warn user with "WARNING".


# AI Documentation and Code Comments
Write any AI documentation (AGENTS/CLAUDE.md) or code comments in terse language, for future AI agents. Facts only, minimal language. No history, dates, just core info. Don't re-tell code, say only what can't be derived from code - architecture, decisions, cross-cutting concerns. Default is no comment at all. Leave comments and edit AI docs only if needed. No duplication between code comments or any AI docs. Information lives in one place only. 
"

## Verify

- AGENTS.md -> confirm no `CLAUDE.md` or `.claude/` file changed.
- CLAUDE.md -> confirm no `AGENTS.md` or `.agents/` file changed.
- Light -> confirm no nested instruction file changed.
- Confirm final review and deduplication subagent completed, including root-only runs.
- Review final-pass diff for lost scope, meaning, or unsupported formatting changes.
- Confirm bundled LLM-writing rules were not copied outside skill directory.
- Confirm generated instruction files use plain repository-relative paths, not Markdown links.
- Confirm generated files omit initializer plumbing and skill-location notes.
- Confirm no generated file references other instruction files.
- Confirm pitfalls are evidence-backed; remove empty or low-value sections.
- Confirm material investigation gaps are resolved or reported; nonstandard architecture is documented, rationale supported or explicitly unknown, and complex domains have actionable source pointers.
- Confirm Maintenance and AI Documentation rules appear in root instruction file only.
- Confirm each `## Flows` entry is investigator-backed, meets doc-worthy threshold, lives in owning domain nested file, appears once, and references existing paths.
- Confirm root instruction file has no `## Flows`.
- Confirm root `## Commands` has max 5 lines, essential commands only.
- Confirm root has `## Architecture` within repository analysis scope and no separate boundaries/overview/repository-map section.
- Confirm nested instruction files have no `## Commands`.
- Review generated instructions for unsupported claims, volatile detail, and excess length. Verify strong claims against implementation and meaningful exceptions.
- Review diff. Run application tests only if changes extend beyond instruction files.
- Report changed files, chosen boundaries, documented and skipped flows, validation, evidence gaps, and that the initializer directory may be deleted after success.
