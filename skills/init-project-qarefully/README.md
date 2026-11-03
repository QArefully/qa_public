# init-project-qarefully

This skill generates or refreshes a concise root `AGENTS.md` / `CLAUDE.md`, plus nested ones, for any repository. Scouts trace important flows, checkers verify claims that need independent checking, and generated guidance must be supported by source.

## Ground rules for editing this skill

- **Get the easy wins.** Prefer deleting logic, collapsing steps, and clarifying existing instructions. Add machinery only for a concrete recurring problem with enough value to justify its cost. Put larger redesigns in a separate proposal.
- **Keep handoffs simple.** Prefer concise notes, source references, a file-placement plan, and clear ownership. IDs should help agents refer to work, not create a record-lifecycle protocol. Avoid per-line provenance, duplicate metadata, receipts, revision chains, and count matrices that ordinary edits must maintain.
- **Spend agent work on understanding.** Preserve independent checking and review where needed; reuse useful context for routine repair continuations; follow-up scouts start fresh. Avoid blanket visibility rules that require elaborate plumbing, repeated review loops, and mandatory fresh agents for administrative changes.
- **Keep the orchestrator light.** The orchestrator mainly runs agents and unblocks issues. Give large reading or synthesis jobs to agents so its context stays free for coordination. When keeping it free would overcomplicate the logic or workflow, let it do the job; if it can help with something simple, use it. Follow common sense.
- **Keep safeguards proportionate.** Preserve user edits, task boundaries, and disjoint writers. Favor simple path/shape checks and clear failure messages over elaborate coverage gates, resume state, or recovery systems. A rerun is acceptable; do not build around hypothetical failures.
- **Project-agnostic.** The skill must work for any repository. Never hardcode names, directories, frameworks, or examples from a repo where you saw a problem. Generalize the lesson instead.
- **One home per rule.** Policy lives in `references/repository-analysis.md` and `references/generated-content.md`. Agent scripts defer to it ("per policy Shape"). Edit the policy first, and touch an agent script only when that role holds the decision. Don't restate the same rule in several files.
- **Fix facts at the source stage.** Correct factual claims, labels, and qualifications in the supporting notes/checking stage. Wording and deduplication may change while preserving supported meaning. Keep source support traceable without requiring a separate inventory of every generated line. Content-selection rules belong in shared policy, not writer-specific instructions.
- **No hard numeric caps.** Use approximate guidance and rely on agents' judgment. The existing root `## Commands` limit is the exception.
- **Change scripts and rules together.** Current checks apply until deliberately changed with their callers and tests. If a check exists only to enforce obsolete bookkeeping, remove it instead of adding a workaround or compatibility layer.
- **Write AI-facing files in the bundled style.** `SKILL.md`, `references/` and `agents/` follow `/llm-oriented-markdowns`: terse, arrow relations, no filler. This README is for humans and is exempt.
- **Keep cost in mind.** Count extra calls, repeated reading, artifact maintenance, and instruction length as costs. Add work only when it improves typical investigation or generated guidance; a cleaner ledger alone is not a benefit.
- **Review against these rules.** Flag overengineering, micromanagement, redundant rules, and project-specific edits. Verify the quality of source understanding and generated guidance as well as whether scripts pass.

## Verify changes

Run from this directory:

```bash
python -m unittest discover -s tests
```

For a behavior change, run the skill on a real repository and read the generated files the way an agent would. Read ordinary source files and see what gets injected. Is it useful, well scoped, and not duplicated?
