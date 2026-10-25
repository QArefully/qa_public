---
name: llm-oriented-writing
description: >-
  Terse writing for AI-consumed .md/.mdc files: agent instructions, skills, prompts.
  Excludes human-facing docs and user chat.
---

# LLM-Oriented Writing

Apply to AI-oriented `.md` and `.mdc` files: agent instructions, skills, prompts. Exclude user chat and human docs such as `README.md`, changelogs, contributor guides, articles, tutorials. Unclear audience -> ask before applying.

## Prose

- Use fragments, short words, direct instructions. Drop articles, filler, pleasantries, preambles, rhetorical hedging where meaning stays clear.
- Preserve actor, action, scope, obligations, conditions, exceptions, uncertainty. Keep distinctions such as `must`, `may`, `only if`; brevity must not change required behavior.
- Name specific referents; avoid vague pronouns, stacked noun chains, and slash lists hiding relations. Add words when needed for clarity.
- Style edits -> preserve fenced code, shell commands, config snippets verbatim. Keep identifiers, quoted errors, URLs, literal paths, versions exact.
- Prefer definitions; include examples only when needed to disambiguate.

Before: "Order update + email lack atomicity."

After: "Order status update commits before email job insert; crash between operations loses email job."

## Format

- Relations -> `A -> B`; mappings -> `key: value`; identifiers -> inline code. Replace Mermaid and pipe/ASCII tables with compact lists or relation chains.
- File references: bare filename resolves in instruction file's directory first, else repository root. Same-directory target -> bare filename; other targets -> repository-relative path using `/`. No Markdown links, `./`, `../`, or absolute paths for file references; preserve literal paths in code, commands, config, and quotes.
- Prefer flat lists; hierarchy -> 2-space indent, maximum 2 levels where practical.
- Use headings for structure; omit horizontal rules, decorative separators, structural emoji, ASCII art.
- Put definitions and preconditions before dependent rules, details after. Avoid forward references. Keep each concept's rules and exceptions together.

## Consolidation

- Before editing, read full target file and applicable root and nested agent instruction files. Find existing guidance before adding content.
- Merge additions into relevant sections; consolidate semantic duplicates throughout owned files, including redundancy unrelated to immediate addition. Keep each rule in one authoritative place. Repository-wide guidance -> root instruction file; subtree-only guidance -> nearest nested instruction file.
- New files -> one concept per section; state each fact once.
- Remove generic advice only when deletion leaves task-specific behavior unchanged. Preserve project-specific constraints even when seemingly obvious; uncertain value -> retain. Delete established no-op statements rather than shortening them.
- Conflicting rules -> apply established precedence; unresolved -> stop and ask which rule wins. Never leave contradictory rules active.
