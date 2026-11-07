---
name: init-project
description: Generate or refresh root + nested AGENTS.md or CLAUDE.md giving new agents non-obvious project knowledge - architecture, conventions, pitfalls, unusual solutions, couplings, complex-logic hints
disable-model-invocation: true
---

# Init project

You = orchestrator: dispatch, route, decide waves. Never read repo code or `<run>` files; decide only from children's inline returns. Children investigate + write.

## Spawning
- Roles → `<skill>/agents/<role>.md`: general-scout, lead, scout, writer, dedup. `<skill>` = dir holding this SKILL.md.
- `<style>` = `<skill>/../llm-oriented-writing/SKILL.md`; missing → installed `llm-oriented-writing` skill's SKILL.md; neither → ask user for path, never proceed without it.
- Child prompt = `Read <skill>/agents/<role>.md, <skill>/references/content.md and <style>; follow them.` + `<skill>`, `<style>`, `<run>` paths + task inputs its profile lists.
- Models: general-scout + scout → scout model from Intake; lead, writer, dedup → inherit your model.
- Leads must be able to spawn scouts → grant subagent permission at dispatch. Host cannot → stop, tell user.
- Add only task-specific inputs; never restate role instructions.

## Intake
- Ask only unknowns: filename (`AGENTS.md` | `CLAUDE.md`), scope (root only | root + nested), scout model (suggest cheaper than yours). Harness lacks per-child model option → tell user, scouts use your model.
- Existing files with selected filename → refresh.
- Always comprehensive: never trade depth for speed, tokens or child count.

## Boundary
- Children change only files with selected filename + `<run>` = `.init-project/<run-id>/`; `<run-id>` = UTC timestamp. Never touch other instruction filename.
- `<run>` holds `.gitignore` = `*` (you create) + `analysis/<file>.md` (leads).
- No builds, tests, installs, network.

## 1. Map
1 general scout. Returns inline: domains → paths → complexity/size → why; repo-wide topics; existing instruction files.

## 2. Wave 1
- Up to 5 leads in parallel; each ≤5 scouts.
- Group domains into lead assignments: every domain + repo-wide topics (commands + test loop, architecture, conventions) owned by exactly one lead; complex/large domains get own lead.
- Input per lead: unique lead-id (`w1-<n>`), domains/topics + paths, existing instruction files in scope, output file `<run>/analysis/<lead-id>.md`, scout cap 5, scout model.

## 3. Wave 2 (if needed)
- From lead returns: gaps, shallow areas, open questions changing content, map domains no lead covered well.
- None → skip. Else up to 3 leads in parallel; each ≤3 scouts; disjoint scopes.
- Input per lead: unique lead-id (`w2-<n>`), gap scope + questions, wave-1 analysis files it may edit (each file → at most one wave-2 lead), new output file `<run>/analysis/<lead-id>.md`, scout cap 3, scout model.

## 4. Write
- Root only scope → 1 writer, owns root file.
- Root + nested → 2 writers in parallel; split repo subtrees into 2 disjoint, balanced sets covering every top-level dir, using lead nested-file hints. Writer A owns root file + its subtrees; writer B owns its subtrees.
- Input per writer: all analysis file paths, filename, scope, owned file/subtrees.

## 5. Dedup
1 dedup agent. Input: generated file paths from writer returns, analysis dir.

## 6. Report
Files written, open questions from lead returns, run folder.
