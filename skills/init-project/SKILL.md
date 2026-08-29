---
name: init-project
description: Initialize or refresh concise AGENTS.md and/or CLAUDE.md
disable-model-invocation: true
---

# Initialize Project Agent Context

Create harness-agnostic repository context files with maintenance instructions. 

## Scope

- Copying this skill to another repository -> copy entire `skills/init-project/` directory, including all `assets/`, `references/`, and `scripts/` files. Exclude nothing.
- Running this skill -> use bundled `assets/llm-oriented-markdowns/llm-oriented-markdowns.md` only within this workflow; do not copy it outside skill directory.

## Start

First response -> ask following questions, then stop:

`Before I scan repository:`

`1. Which setup do you want: A: AGENTS.md + Claude hook (harness-agnostic setup), B: only AGENTS.md, or C: only CLAUDE.md?`

`2. Which run do you want: Light (2-3 subagents, root instruction file only) or Full (up to 10 subagents, root plus useful nested instruction files)?`

`3. Any project context, history, constraints, or known traps that would help agents understand it? Reply "skip" if none.`

Do not inspect repository or spawn subagents until user selects setup and mode. Preserve both choices for entire run.

## Setups

- AGENTS.md + Claude alternative -> `AGENTS.md` is source of truth. Generate root and mode-selected nested `AGENTS.md` files. Install SessionStart hook that injects AGENTS context into Claude Code. Full mode also creates sibling `CLAUDE.md` pointers for nested `AGENTS.md` files. Do not create root `CLAUDE.md`; hook injects root context.
- Only AGENTS.md -> generate root and mode-selected nested `AGENTS.md` files. Do not create, update, or delete `CLAUDE.md`, `.claude/`, or `scripts/agent-context.mjs` files.
- Only CLAUDE.md -> generate root and mode-selected nested `CLAUDE.md` files. Do not create, update, or delete `AGENTS.md`, `.agents/`, `.claude/settings.json`, or `scripts/agent-context.mjs` files.

## Modes

- Light -> dispatch 2-3 subagents total for initial read-only scans. Split repository into broad main domains. Merge small or supporting areas into nearest main domain; do not create separate scans for minor boundaries. Create or update selected root instruction file only. Do not modify nested instruction files.
- Full -> dispatch only subagents needed for initial read-only scans of meaningful independent boundaries, maximum 10 total. Prefer one non-overlapping domain per subagent. Fewer than 10 is expected when evidence does not justify more.
- Both modes -> main agent performs shallow root scan, chooses boundaries, gives each subagent exact scope and evidence request, then owns cross-domain synthesis and initial writes. After every run, reuse one completed scan subagent for final review and deduplication, including root-only runs. Review does not increase selected mode subagent total.

## Workflow

1. Resolve repository root. Read [repository analysis](references/repository-analysis.md) and bundled [LLM-oriented Markdown rules](assets/llm-oriented-markdowns/llm-oriented-markdowns.md).
2. Inspect manifests, executable config, tests, CI, maintained docs, existing agent instructions, and shallow repository structure. Code and executable config win conflicts; report unresolved intent conflicts.
3. Identify core boundaries where local context changes implementation choices. Dispatch read-only subagents per selected mode. Avoid overlapping scans and ask each subagent for terse, evidence-backed findings only.
4. Write instructions matching selected setup and mode. Merge valuable existing rules in selected files.
   - AGENTS setups -> write `AGENTS.md`.
   - CLAUDE-only setup -> write `CLAUDE.md`.
   - Light -> root only.
   - Full -> root plus only useful nested files.
5. AGENTS.md + Claude alternative only -> install durable support:

   `node "<skill-directory>/scripts/install-assets.mjs" --repo "<repository-root>"`

   Installer adds context script and Claude hook. Do not copy bundled LLM-writing rules outside skill directory. Review reported conflicts before using `--replace-managed` or `--accept-existing-managed`.
6. AGENTS.md + Claude alternative with Full mode -> add sibling `CLAUDE.md` pointers for generated or updated nested `AGENTS.md` files. Each pointer directs Claude to read sibling `AGENTS.md`. Do not create root `CLAUDE.md`.
7. After initial writes, assign final review and deduplication to one completed scan subagent. Grant edit ownership only for generated or updated primary instruction files: `AGENTS.md` for AGENTS setups, `CLAUDE.md` for CLAUDE-only setup. Subagent must:
   - Read `<skill-directory>/assets/llm-oriented-markdowns/llm-oriented-markdowns.md` before editing; follow it for all edits.
   - Enforce every bundled writing and formatting rule in each owned file, including terse prose, linear structure, compact formatting, flat lists, and prohibited constructs.
   - Compare owned files with all applicable root and nested primary instruction files for exact and semantic duplication. Single-file runs still require full within-file deduplication.
   - Keep each fact or rule only in most relevant place: repository-wide guidance at root; subtree-only guidance in nearest applicable nested file.
   - Delete duplicate copies from owned files without weakening scope, exceptions, or meaning.
   - Edit files directly and report moved or deleted guidance. Do not return recommendations only.
8. Before finalizing, test draft against a typical cross-layer change. If an agent would need to rediscover a required layer, helper, import convention, transaction mechanism, or validation step, add missing rule or exemplar path.

## Generated content

- Minimal: every line must change agent behavior or avoid meaningful rediscovery.
- Prefer where and why: authoritative paths, ownership, rationale, durable invariants, hazards, and surprising constraints. Reference detailed docs with plain repository-relative paths; never use Markdown links or copy doc content.
- Avoid volatile implementation prose, inventories, exhaustive environment lists, generic coding advice, and host-provided agent or skill-routing rules.
- Root file -> global context. Full mode nested files -> subtree-only deltas; never repeat inherited rules.
- Destructive commands -> state impact and required authorization.
- Generated/runtime files -> identify only when agents might edit or commit them accidentally.
- Do not reference initializer or setup plumbing in generated files: SessionStart/context injection, `agent-context.mjs`, skill locations/discovery, nested-skill notes.
- Add `## Pitfalls` to each generated instruction file. Capture verified, non-obvious failure modes and proven workarounds within that file's scope; never invent entries to fill section.

Add following rule to each generated instruction file:

`Update this file when code invalidates guidance; durable boundaries, hazards, or sources of truth change; or work reveals reusable lessons, pitfall workarounds, or user instructions. AGENTS.md/CLAUDE.md conflict with repository evidence -> warn user with "WARNING".`

## Verify

- AGENTS.md + Claude alternative -> run `node <repository-root>/scripts/agent-context.mjs` from root and one nested directory; confirm one effective SessionStart hook.
- AGENTS.md + Claude alternative with Full mode -> confirm sibling pointers for generated or updated nested `AGENTS.md` files.
- Only AGENTS.md -> confirm no `CLAUDE.md`, `.claude/`, or `scripts/agent-context.mjs` file changed.
- Only CLAUDE.md -> confirm no `AGENTS.md`, `.agents/`, `.claude/settings.json`, or `scripts/agent-context.mjs` file changed.
- Light -> confirm no nested instruction file changed.
- Confirm final review and deduplication subagent completed, including root-only runs.
- Review final-pass diff for lost scope, meaning, or unsupported formatting changes.
- Confirm bundled LLM-writing rules were not copied outside skill directory.
- Confirm generated `AGENTS.md` and `CLAUDE.md` files use plain repository-relative paths, not Markdown links.
- Confirm generated files omit SessionStart/context-injection and nested-skill-location notes.
- Confirm each generated instruction file contains `## Pitfalls` and only evidence-backed entries.
- Review generated instructions for unsupported claims, volatile detail, and excess length.
- Review diff. Run application tests only if changes extend beyond agent-context files.
- Report changed files, chosen boundaries, validation, evidence gaps, and that the initializer directory may be deleted after success.
