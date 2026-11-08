# init-project-qarefully
Generates root + nested AGENTS.md/CLAUDE.md with non-obvious project knowledge.
Editing rules:
- Keep it small: roster = orchestrator, general scout, leads (spawn scouts), 2 writers (disjoint owned dirs; root-only scope → 1), dedup. Existing instruction files unsupported → archive gate at Intake. Add machinery only for a recurring observed failure.
- Project-agnostic: never add names/examples from a repo where a problem was seen; generalize.
- One home per rule: content/placement/formats → `references/content.md`; flow + spawn convention → `SKILL.md`; role behaviour → `agents/<role>.md`; writing style → sibling `llm-oriented-writing` skill, read by writer + dedup only, never copied in; other roles get terse rule in `references/content.md`.
- Verify by running skill on real repos and reading output per edit path, as an agent would load it.
