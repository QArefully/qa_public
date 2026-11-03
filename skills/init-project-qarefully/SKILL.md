---
name: init-project
description: Initialize or refresh concise AGENTS.md or CLAUDE.md from repository scans that trace application flow in depth
disable-model-invocation: true
---

# Initialize Project Agent Context

Create minimal harness-agnostic navigation + warnings; detailed explanations stay in source. Explicit invocation only. Copy entire package when relocating; bundled style + helpers stay inside package.

## Start

Read [workflow](references/workflow.md) for intake, modes, stages and completion; read [contracts](references/contracts.md) before dispatch. Bind capabilities before first child; missing required capability -> explain affected stage and viable correction, never silently substitute or take over an evidence role.

## Orchestration

- Own scope and follow-up decisions, scheduling, placement decisions, target ownership, user communication and final acceptance. Dispatch isolated roles with exact relevant resources and concise handoffs; only orchestrator starts children.
- Mainly run agents and unblock issues; large reading/synthesis -> agents (follow-up planner, checkers, placement). Do small jobs directly when delegating would complicate flow; keep context free for coordination. Pass artifact paths and brief summaries; preserve reviewer's independent initial view.
- Follow workflow: scouts -> one follow-up planner/fresh scout round -> selective checkers -> placement -> writers -> one reviewer pass/direct fixes -> unresolved repairs as needed -> final helper gate. No repeated reviewer passes.
- Only selected mode-approved instruction files and run folder may change. Protect user edits and disjoint ownership per contracts.

## Finish

Accept only when required artifacts and checks are complete and final helper gate passes. Report retained run path, consequential unanswered questions and observed limits; never infer completion from tool termination alone.
