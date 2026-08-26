---
name: init-project
description: Initialize or refresh concise AGENTS.md, CLAUDE.md, or AGENTS.md with Claude Code context injection. Use for repository agent-instruction setup or regeneration.
---

# Initialize Project Agent Context

Create compact repository context that remains useful after initializer removal.

## Start

First response -> ask following questions, then stop:

`Before I scan repository:`

`1. Which setup do you want: AGENTS.md + Claude alternative, only AGENTS.md, or only CLAUDE.md?`

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
- Both modes -> main agent performs shallow root scan, chooses boundaries, gives each subagent exact scope and evidence request, then owns cross-domain synthesis and initial writes. Reuse one scan subagent for final deduplication; do not add another subagent beyond selected mode limit.

## Workflow

1. Resolve repository root. Read [repository analysis](references/repository-analysis.md) and bundled [LLM-oriented Markdown rules](assets/llm-oriented-markdowns/SKILL.md).
2. Inspect manifests, executable config, tests, CI, maintained docs, existing agent instructions, and shallow repository structure. Code and executable config win conflicts; report unresolved intent conflicts.
3. Identify core boundaries where local context changes implementation choices. Dispatch read-only subagents per selected mode. Avoid overlapping scans and ask each subagent for terse, evidence-backed findings only.
4. Write instructions matching selected setup and mode. Merge valuable existing rules in selected files.
   - AGENTS setups -> write `AGENTS.md`.
   - CLAUDE-only setup -> write `CLAUDE.md`.
   - Light -> root only.
   - Full -> root plus only useful nested files.
5. AGENTS.md + Claude alternative only -> install durable support:

   `node "<skill-directory>/scripts/install-assets.mjs" --repo "<repository-root>"`

   Installer adds the LLM-writing skill, context script, and Claude hook. Review reported conflicts before using `--replace-managed` or `--accept-existing-managed`.
6. AGENTS.md + Claude alternative with Full mode -> add sibling `CLAUDE.md` pointers for generated or updated nested `AGENTS.md` files. Each pointer directs Claude to read sibling `AGENTS.md`. Do not create root `CLAUDE.md`.
7. After instruction drafts, assign final deduplication to one completed scan subagent. Grant edit ownership only for generated or updated primary instruction files: `AGENTS.md` for AGENTS setups, `CLAUDE.md` for CLAUDE-only setup. Subagent must:
   - Light -> delete exact and semantic duplication within root instruction file. Do not edit nested files.
   - Full -> compare all root and nested primary instruction files for exact and semantic duplication, including repetition within one file.
   - Full -> keep each fact or rule only in most relevant place: repository-wide guidance at root; subtree-only guidance in nearest applicable nested file.
   - Full -> delete duplicate copies elsewhere without weakening scope, exceptions, or meaning.
   - Edit files directly and report moved or deleted guidance. Do not return recommendations only.

## Generated content

- Minimal: every line must change agent behavior or avoid meaningful rediscovery.
- Prefer where and why: authoritative paths, ownership, rationale, durable invariants, hazards, and surprising constraints. Link to detailed docs; do not copy them.
- Avoid volatile implementation prose, inventories, exhaustive environment lists, generic coding advice, and host-provided agent or skill-routing rules.
- Root file -> global context. Full mode nested files -> subtree-only deltas; never repeat inherited rules.
- Destructive commands -> state impact and required authorization.
- Generated/runtime files -> identify only when agents might edit or commit them accidentally.
- Do not reference this initializer in generated files.

Add following rule to each generated instruction file:

`Update this file only when code invalidates guidance or changes durable boundaries, hazards, or sources of truth. Any AGENTS.md or CLAUDE.md conflict with code or other repository evidence -> flag user with "WARNING".`

## Verify

- AGENTS.md + Claude alternative -> run `node <repository-root>/scripts/agent-context.mjs` from root and one nested directory; confirm one effective SessionStart hook.
- AGENTS.md + Claude alternative with Full mode -> confirm sibling pointers for generated or updated nested `AGENTS.md` files.
- Only AGENTS.md -> confirm no `CLAUDE.md`, `.claude/`, or `scripts/agent-context.mjs` file changed.
- Only CLAUDE.md -> confirm no `AGENTS.md`, `.agents/`, `.claude/settings.json`, or `scripts/agent-context.mjs` file changed.
- Light -> confirm no nested instruction file changed.
- Confirm deduplication subagent completed. Review its diff for lost scope or meaning.
- Review generated instructions for unsupported claims, volatile detail, and excess length.
- Review diff. Run application tests only if changes extend beyond agent-context files.
- Report changed files, chosen boundaries, validation, evidence gaps, and that the initializer directory may be deleted after success.
