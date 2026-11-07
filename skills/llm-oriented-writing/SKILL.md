---
name: llm-oriented-writing
description: >-
  Terse writing for AI-consumed .md/.mdc files: agent instructions, skills, prompts.
  Excludes human-facing docs and user chat.
---

# LLM-Oriented Writing

Scope: AI-oriented `.md`/`.mdc` (agent instructions, skills, prompts). Not user chat or human docs (`README.md`, changelogs, guides, tutorials). Unclear audience -> ask user.

## Prose

- Fragments, short words, direct instructions. Drop articles, filler, rhetorical hedging, preambles; keep real uncertainty.
- Keep meaning exact: actor, action, scope, conditions, exceptions, uncertainty, modality (`must`/`may`/`only if`).
- Name referents; no vague pronouns, noun stacks, or slash lists hiding relations. Add words when clarity needs them.
- Keep code, commands, config, identifiers, errors, URLs, paths, versions verbatim.
- Examples only to disambiguate.

Before: "Order update + email lack atomicity."
After: "Order status update commits before email job insert; crash between operations loses email job."

## Format

- Relations -> `A -> B`; mappings -> `key: value`; identifiers -> inline code. No Mermaid or tables.
- File refs: target in instruction file's directory -> bare filename; else repo-relative path with `/`. No Markdown links, `./`, `../`, absolute paths (except literals in code/quotes).
- Flat lists; max 2 nesting levels.
- Headings for structure; no horizontal rules, separators, emoji, ASCII art.
- Definitions before dependent rules; no forward refs; keep each concept's rules and exceptions together.

## Consolidation

- First read target file and relevant root/nested instruction files; reuse existing guidance.
- Merge into relevant sections; dedupe across files in scope; one authoritative place per rule. Repo-wide -> root file; subtree-only -> nearest nested file.
- Delete generic advice only if behavior unchanged; delete no-op statements outright, don't shorten them. Keep project-specific constraints; unsure -> keep.
- Conflicts -> apply established precedence; unresolved -> ask. Never leave contradictions.
