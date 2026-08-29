---
name: llm-oriented-markdowns
description: Write compact Markdown instructions for AI consumption. Use for AGENTS.md, CLAUDE.md, skills, prompts, and agent rules; never for human docs or chat.
---

# LLM-oriented Markdown

Apply only to `.md` or `.mdc` files whose primary reader is an AI agent. Never apply to user chat or human docs such as `README.md`, changelogs, contributor guides, articles, or tutorials. Unclear audience -> ask.

## Writing rules

- Terse: remove articles, filler, pleasantries, hedging, repeated preambles.
- Direct: fragments allowed; short words preferred; technical terms exact.
- Exact: preserve code blocks, commands, identifiers, paths, versions, and error text.
- Linear: preconditions first, details after; say each fact once.
- Compact: prefer bullets, `key: value`, and `A -> B -> C` relations.
- Flat: maximum two list levels where practical.
- `AGENTS.md` and `CLAUDE.md`: plain repository-relative paths; no Markdown links.
- No Mermaid, tables, decorative separators, structural emoji, or ASCII art.
- Examples only when needed to remove ambiguity.

## Editing rules

Read full file before editing. Find existing rule before adding one. Merge overlap, remove repetition, and keep one authoritative statement per concept. Contradiction -> stop and ask which rule wins; never silently preserve both.
