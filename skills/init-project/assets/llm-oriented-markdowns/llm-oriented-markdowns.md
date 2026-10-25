# LLM-oriented agent instructions

Apply only when init-project writes or edits AI-oriented repository instruction files such as `AGENTS.md` and `CLAUDE.md`. Never apply to user chat or human docs such as `README.md`, changelogs, contributor guides, articles, or tutorials. Unclear audience -> ask.

## Writing rules

- Terse and direct: remove articles, filler, pleasantries, hedging, and repeated preambles; prefer short words; keep technical terms exact. Fragments allowed when actor and relation stay explicit; name referent, not generic noun (which snapshot, which check). Never hide relations in stacked noun chains or slash lists; few extra words beat ambiguity.
  - Bad: `Payment CAS + notification lack atomicity`. Good: `Payment status CAS and notification insert commit in separate transactions; crash between them drops notification.`
- Exact: preserve fenced code, shell commands, and config snippets verbatim. Quote identifiers, error text, URLs, paths, and versions exactly.
- Linear: put preconditions before dependent rules; avoid forward references; say each fact once.
- Definitions first: add example only when needed to remove ambiguity.

## Structure

- Prefer compact bullets, `key: value`, and `A -> B -> C` relations.
- Use inline code for identifiers.
- Paths: bare filename = file in instruction file's directory, else repository-root file (same directory wins). Same-directory target -> bare filename (`checkoutService.ts`); else repository-relative path with `/`. Never Markdown links, `./`, `../`, or absolute paths.
- Limit lists to two levels where practical. Use two-space indentation and arrow chains instead of deep nesting.
- No Mermaid, pipe or ASCII tables, horizontal rules, decorative separators, structural emoji, or ASCII art.

## Editing rules

- Read full target file and all applicable root and nested agent instruction files before editing.
- Find existing guidance before adding content. Never restate same rule in different words.
- Merge overlap into one authoritative section. Keep repository-wide guidance at root and subtree-only guidance in nearest nested file.
- Trim existing redundancy in owned files, including duplication unrelated to immediate addition.
- For new files, keep one concept per section and avoid repeating it elsewhere.
- Contradiction -> stop and ask which rule wins; never silently preserve both.
