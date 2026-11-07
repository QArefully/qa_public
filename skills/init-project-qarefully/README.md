# init-project-qarefully
Generates root + nested AGENTS.md/CLAUDE.md with non-obvious project knowledge.
Editing rules:
- Keep it small: roster = orchestrator, general scout, leads (spawn scouts), 2 writers, dedup. Add machinery only for a recurring observed failure.
- Project-agnostic: never add names/examples from a repo where a problem was seen; generalize.
- One home per rule: content/placement/formats → `references/content.md`; flow + spawn convention → `SKILL.md`; role behaviour → `agents/<role>.md`; writing style → sibling `llm-oriented-writing` skill, never copied in.
- Verify by running skill on real repos and reading output per edit path, as an agent would load it.
