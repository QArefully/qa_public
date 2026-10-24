# Repository analysis

## Scan

Evidence order: executable config/code -> tests/CI -> maintained docs -> existing instructions -> user context.

Main agent root scan -> shallow; enough to choose boundaries and brief investigators:

- main applications, services, packages, infrastructure, and test harnesses
- runtime and package-manager requirements
- exact install, run, build, check, and test commands
- flow entry points per boundary: routes, CLI commands, UI entry, jobs, consumers, webhooks, schedules
- destructive actions, generated boundaries, external effects, and common traps
- documentation paths to reference instead of repeat

Investigator scans -> deep flow tracing per references/flow-investigation.md. Main agent merges findings and joins flows crossing scopes via reported contracts; follow-up investigation per SKILL.md workflow.

## Select content

Except for runtime requirements and exact commands, prefer where and why over current implementation detail.

Keep:

- boundary purpose and allowed dependency direction
- consequential architectural decisions and nonstandard structure -> behavior, constraints, and supported rationale; unknown rationale -> mark unknown, retain verified architecture
- authoritative definitions and extension points
- ownership of validation, state, permissions, and side effects
- hidden flow ownership or ordering per `## Flows`
- durable domain or safety invariants
- fastest relevant validation and unusual test prerequisites
- verified non-obvious failure modes -> implementation, test, or observed incident evidence; omit speculative traps
- complex domains, calculations, state, or async behavior -> what complicates safe changes, entry/authority path, and coupling or ordering to inspect; test pointers where useful
- easy-to-bypass boundaries -> required helpers, layer order, transaction scope, validation/error paths, import conventions
- 1-3 maintained exemplar paths for common changes

Drop:

- file, symbol, route, dependency, or environment-variable inventories
- timings, counts, temporary status
- line-by-line code narration; flows obvious from entry point and adjacent files
- generic advice or host-provided agent workflow
- duplicated parent guidance or human documentation
- worked arithmetic, fixture values, test scenarios, ticket/rubric checklists, and coverage claims inferred from filenames
- unsupported claims

Keep investigation detail outside instructions. Test guidance -> fixture/assertion/response-control pointer + what it proves; distinguish mocks from persistence. Reuse existing guidance; omit generic checklists.

## Commands

Root `## Commands` -> max 10 lines. Group related commands on one line per purpose instead of one command per line:

- setup/run: install, dev/run, seed
- checks: typecheck, lint, format, custom static guards
- tests: per-layer or per-kind test commands
- gates: aggregate scripts with what each runs
- scoped runs: one pattern line (workspace, package, single test) with example instead of per-target commands
- destructive: own line; impact and required authorization

Keep every command agents routinely run; drop only one-off, internal, or CI-only scripts. Short purpose notes inline in parentheses. Commands live only in root; nested files never get `## Commands`. Subtree-specific runs -> covered by root scoped-run pattern.

## Flows

Complexity signal prompts investigation, not documentation. Keep flow only when hidden ownership, ordering, or coupling creates consequential wrong turn. Prefer entry/authority pointer + warning; ordinary multi-file traversal alone does not justify flow section.

Placement -> `## Flows` in nested instruction file of domain owning flow's core rules and state writes; never root. Hops outside that subtree -> repository-relative paths. Full -> create nested file at domain root when none exists. Light -> no flows section; distill flow findings into root boundaries, invariants, pitfalls. One flow lives in one file; never split or repeat it.

Per flow -> trigger/entry path, rule/state owner, consequential hazard. Add shortest hop chain, boundary, or co-change/helper pointer only when needed to explain hazard. No full trace, line numbers, function bodies, or transient config values.

## Shape

Root sections as useful: repository map, runtime, commands, architecture/domain, testing, agent hints, maintenance. Never flows.

Add `## Testing` only where test structure or setup changes agent decisions. Cover relevant layers/frameworks, file or config locations, harnesses/fixtures/providers, prerequisites, and E2E ownership. Keep runnable commands only in `## Commands`; do not repeat them under Testing.

Nested files contain only local architecture, local flows, local testing, and local hazards; no commands. Create one only when subtree has distinct decisions or risks, or owns doc-worthy flow.

Full -> root may point to owning nested instructions when consequential complex domain would otherwise be easy to miss; keep explanation only in owning file. Light -> retain concise domain guidance at root. Complexity alone does not justify walkthrough or domain inventory.
