---
name: init-project
description: Generate root + nested AGENTS.md or CLAUDE.md giving new agents non-obvious project knowledge - architecture, conventions, pitfalls, unusual solutions, couplings, complex-logic hints
disable-model-invocation: true
---

# Init project

You = orchestrator: dispatch, route, decide waves. Never read repo code or `<run>` files; decide only from children's inline returns. Children investigate + write.

## Spawning
- Roles → `<skill>/agents/<role>.md`: general-scout, lead, scout, writer, dedup. `<skill>` = dir holding this SKILL.md.
- `<style>` = `<skill>/../llm-oriented-writing/SKILL.md`; missing → installed `llm-oriented-writing` skill's SKILL.md; neither → ask user for path, never proceed without it.
- Child prompt = `Read <skill>/agents/<role>.md and <skill>/references/content.md; follow them.` + only inputs its role file lists. Concrete file/dir paths, never bare `<run>`. Leads only → also `<skill>` path (build scout prompts).
- Writer, dedup only → prompt also says `Read <style>; follow it.` + `<style>` path. Other roles never get `<style>`.
- Models: scout → scout model from Intake; general-scout, lead, writer, dedup → inherit your model.
- Leads must be able to spawn scouts → grant subagent permission at dispatch. Host cannot → stop, tell user.
- Concurrent-subagent limit: refused spawns → queue, respawn as running children return; never do child's work yourself. Heavily limited = stated limit < 1 lead + its scout cap, or any lead stopped early on limit → stop all running children, keep `<run>`, tell user: observed limit + planned peak (parallel leads × (1 + scout cap) + yourself), where to raise it (host's concurrent-subagent / max-agents setting in harness config or env; name it if known), alternative = rerun with fewer parallel leads or lower scout caps.
- Add only task-specific inputs; never restate role instructions.

## Intake
- Ask only unknowns: filename (`AGENTS.md` | `CLAUDE.md`), scope (root only | root + nested), scout model (suggest cheaper than yours). Harness lacks per-child model option → tell user, scouts use your model.
- Existing instruction files unsupported. Search repo for `CLAUDE.md` + `AGENTS.md` (any depth; skip dependency/build dirs + `.init-project/`; include gitignored files; finding files ≠ reading code). Found → list paths, ask user: move to `<run>/archive/<original relative path>`, start from scratch? No → stop, tell user why, create nothing. Else create `<run>` + `.gitignore`; Yes → also move files; continue.
- Always comprehensive: never trade depth for speed, tokens or child count.

## Boundary
- `<run>` = `.init-project/<run-id>/`; `<run-id>` = UTC timestamp. Holds `.gitignore` = `*` + `archive/` (you, Intake) + `analysis/<lead-id>.md` (leads).
- Children change only files with selected filename + analysis files assigned to them. Only exception: you move archived files at Intake.
- Child-side rules (ignore `.init-project/`, no builds/tests/installs/network) → `references/content.md` Boundary.

## 1. Map
1 general scout. Returns inline: domains → paths → complexity/size → why; repo-wide topics.

## 2. Wave 1
- Up to 5 leads in parallel; each ≤5 scouts.
- Group domains into lead assignments: every domain + repo-wide topics (commands + test loop, architecture, conventions) owned by exactly one lead; complex/large domains get own lead.
- Input per lead: unique lead-id (`w1-<n>`), domains/topics + paths, output file `<run>/analysis/<lead-id>.md`, scout cap 5, scout model.

## 3. Wave 2 (if needed)
- From lead returns: gaps, shallow areas, open questions changing content, map domains no lead covered well.
- None → skip. Else up to 3 leads in parallel; each ≤3 scouts; disjoint scopes.
- Input per lead: unique lead-id (`w2-<n>`), gap scope + questions, wave-1 analysis files it may edit (each file → at most one wave-2 lead), new output file `<run>/analysis/<lead-id>.md`, scout cap 3, scout model.

## 4. Write
- 2 writers in parallel, disjoint owned dirs. Root only scope → 1 writer owning all (single file).
- Split from Map + lead returns: pick top-level subtrees for writer 2 so expected nested-file load ≈ writer 1's (root file + rest). Every dir → exactly one writer.
- Input per writer: `<run>/analysis/` path, filename, scope, owned dirs: writer 1 = root + everything except writer 2's subtrees (listed); writer 2 = its subtree list.

## 5. Dedup
1 dedup agent. Input: generated file paths + handoffs from all writer returns, `<run>/analysis/` path.

## 6. Report
Files written, open questions from lead returns, run folder, archive location (if files archived).
