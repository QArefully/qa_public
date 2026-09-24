---
name: llm-oriented-writing
description: >-
  Terse writing for AI-consumed .md/.mdc files: agent instructions, skills, prompts.
  Excludes human-facing docs and user chat.
---

# LLM-Oriented Writing

## Prose

- Use fragments, short words, direct instructions. Drop articles, filler, pleasantries, preambles, rhetorical hedging where meaning stays clear.
- Preserve actor, action, scope, obligations, conditions, exceptions, uncertainty. Keep distinctions such as `must`, `may`, `only if`; brevity must not change required behavior.
- Style edits -> preserve code, commands, config, identifiers, quoted errors, URLs, paths, versions verbatim.
- Prefer definitions; include examples only when needed to disambiguate.

Before: "The client must retry only if Retry-After is present, with at most three retries. A 503 response may indicate overload, but this is unconfirmed."

After: "Client must retry only if `Retry-After` present; maximum 3 retries. `503` may indicate overload; unconfirmed."

## Format

- Relations -> `A -> B`; mappings -> `key: value`; identifiers -> inline code. Replace Mermaid and pipe/ASCII tables with compact lists or relation chains.
- Prefer flat lists; hierarchy -> 2-space indent, maximum 2 levels where practical.
- Use headings for structure; omit decorative separators, emoji markers, ASCII art.
- Put preconditions before actions, details after. Keep each concept's rules and exceptions together.

## Consolidation

- Before editing, read full target file. Merge additions into relevant sections; consolidate semantic duplicates throughout file. Keep each rule in one authoritative place.
- Remove generic advice only when deletion leaves task-specific behavior unchanged. Preserve project-specific constraints even when seemingly obvious; uncertain value -> retain. Delete established no-op statements rather than shortening them.
- Conflicting rules -> apply established precedence; ask user only when precedence remains unresolved.
