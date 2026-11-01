# init-project-qarefully

This skill generates or refreshes a concise root `AGENTS.md` / `CLAUDE.md`, plus nested ones, for any repository. It scans the repo, has scouts trace the important flows, has checkers verify every claim against source, and writes only verified facts.

## Ground rules for editing this skill

- **Keep it simple.**  If an improvement needs new logic, new scripts, new ledger fields, scope-assignment changes, or step-by-step micromanagement, without providing huge value, drop it, or write it down as a separate, deliberate redesign. Simplify, collapse instructions and flow where possible. get the easy wins. Avoid overengineering. 
- **Project-agnostic.** The skill must work for any repository. Never hardcode names, directories, frameworks, or examples from a repo where you saw a problem. Generalize the lesson instead.
- **One home per rule.** Policy lives in `references/repository-analysis.md` and `references/generated-content.md`. Agent scripts defer to it ("per policy Shape"). Edit the policy first, and touch an agent script only when that role holds the decision. Don't restate the same rule in several files.
- **Fix at the source stage.** Generated text must map to verified records. Checkers own labels and record wording, and Verify blocks the writer from changing either. Rules about what gets kept, how it's labeled, or how long it is belong in the policy or checker rules, not in writer wording.
- **No hard numeric caps.** Use approximate guidance and rely on agents' judgment. The existing root `## Commands` limit is the exception.
- **Stay compatible with the scripts.** Proposed rules must produce output that passes `check-shape.py`, `check-paths.py` and `ledger.py`. If a rule conflicts with a check, change the rule, or change the script and its tests together in a deliberate edit.
- **Write AI-facing files in the bundled style.** `SKILL.md`, `references/` and `agents/` follow `/llm-oriented-markdowns`: terse, arrow relations, no filler. This README is for humans and is exempt.
- **Keep cost in mind.** Every new kind of kept content adds checker and verify work on every run. Add it only when it changes agents' decisions in typical repos.
- **Review against these rules.** Reviewers of skill changes should treat overengineering, micromanaging, redundant, or project-specific edits as findings.

## Verify changes

Run from this directory:

```bash
python -m unittest discover -s tests
```

For a behavior change, run the skill on a real repository and read the generated files the way an agent would. Read ordinary source files and see what gets injected. Is it useful, well scoped, and not duplicated?
