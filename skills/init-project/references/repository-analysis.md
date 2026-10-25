# Repository analysis

## Scan

Evidence order: executable config/code -> tests/CI -> maintained docs -> existing instructions -> user context.

Orchestrator root scan -> shallow; enough to choose boundaries and brief scouts. Search/outline first; read relevant ranges in large manifests, config, tests, and docs rather than full dumps. Existing instruction files -> read fully. Deep flow reading belongs to scouts. Shared foundation repeatedly needed -> optional compact digest in run folder or early platform/package scout; digest remains leads, each claim needs source evidence. Cover:

- main applications, services, packages, infrastructure, and test harnesses
- runtime and package-manager requirements
- exact install, run, build, check, and test commands
- flow entry points per boundary: routes, CLI commands, UI entry, jobs, consumers, webhooks, schedules
- destructive actions, generated boundaries, external effects, and common traps
- documentation paths to reference instead of repeat

## Select content

Orchestrator evidence rule, applied before placement:

- documentable -> checker confirmed/corrected (corrected statement replaces original), or high-confidence scout claim not requiring independent check
- refuted -> never document
- independent checker required -> low-confidence, absence/exclusivity, security/money claims, and existing-instruction facts not scout-verified; applies to late additions too
- unresolved or checker-listed new hazard (= low) -> verify or re-check under same rule; still open -> report as gap, never document
- existing instruction files -> factual claims = leads under same rule; user/process directives (workflow, authorization, style) exempt, kept, placed per `## Placement`

Except for runtime requirements and exact commands, prefer where and why over current implementation detail.

Keep:

- boundary purpose and allowed dependency direction
- consequential architectural decisions and nonstandard structure -> behavior, constraints, and supported rationale; unknown rationale -> mark unknown, retain verified architecture
- authoritative definitions and extension points
- ownership of validation, state, permissions, and side effects
- hidden flow ownership or ordering per `## Flows`
- durable domain or safety invariants, e.g. identity/uniqueness keys, granularity a rule applies at (item vs aggregate), write preconditions, which stale/concurrent result wins
- fastest relevant validation and unusual test prerequisites
- verified non-obvious failure modes -> implementation, test, or observed incident evidence; omit speculative traps
- complex domains, calculations, state, or async behavior -> what complicates safe changes, entry/authority path, and coupling or ordering to inspect
- easy-to-bypass boundaries -> required helpers, layer order, transaction scope, validation/error paths, import conventions
- 1-3 maintained exemplar paths for common changes

Drop:

- file, symbol, route, dependency, or environment-variable inventories
- timings, counts, temporary status
- line-by-line code narration; flows obvious from entry point and adjacent files
- generic advice or host-provided agent workflow
- duplicated parent guidance or human documentation
- worked numeric examples (non-obvious rule as one statement + authority path stays), fixture values, test scenarios, ticket/rubric checklists, test-file -> feature mappings, and coverage claims inferred from filenames

Keep investigation detail outside instructions. Scout/checker output -> guidance-worthy facts and consequential gaps, not general bug audit or test-absence inventory. Test guidance -> harness setup (fixture lifecycle, seed/template, config limits) + caveats on what tests or mocks do not prove (mock vs persistence, weak assertions). Reuse existing guidance; omit generic checklists.

## Placement

Nested instruction files load only for agents working in their subtree. Each fact -> one home = subtree root of domain owning trigger (code whose edit triggers hazard or must honor fact), at app/package/feature granularity per `## Shape`. Trigger owner usually owns rule or state write; failure surfacing in another domain -> still trigger owner, not failure site. Trigger spans sibling domains -> nearest common parent. Repository-wide structure -> root per `## Architecture`. Home file: existing one; none -> Full creates it (subtree fails `## Shape` creation rule -> nearest parent home), Light uses root (root holds all, concise domain guidance included). Other domains needing fact -> source authority path + hazard only when needed, never instruction file.

File set follows placement rule, not scout scopes: one scope may feed several files or none; one file may draw on several scopes.

## Commands

Root `## Commands` -> max 5 lines, essential only: what agent needs to set up, run, and validate typical change. One line per purpose, related commands grouped:

- setup/run: install, dev/run, seed
- checks: typecheck, lint, format check, custom static guards
- tests: main test command + one scoped-run pattern with example (workspace, package, single test)
- gates: aggregate scripts with what each runs
- destructive: impact and required authorization

Drop interactive/UI modes, tooling self-tests and profilers, repo-wide auto-fix rewriters, build chains already run by install or gates, per-layer/per-target variants derivable from aggregate or scoped pattern, one-off and CI-only scripts. Short purpose notes inline in parentheses. Commands live only in root; nested files never get `## Commands`.

## Architecture

Root `## Architecture` -> repository-wide structure no single subtree shows; replaces boundary, overview, repository-map sections. Contents:

- ownership: which app/package owns which concern; allowed dependency direction + enforcing config
- sources of truth: where canonical logic, configuration, schemas live
- cross-boundary decisions and nonstandard solutions -> constraint + supported rationale; unknown rationale -> mark unknown
- hidden cross-boundary dependencies: couplings, build/resolution or ordering effects invisible on casual read

Exclude request/layer walkthroughs, wiring or add-a-feature recipes, process/port/env/file inventories, conventions visible in neighbouring code. Single-domain detail -> home per `## Placement`. Keep bullet only when it changes navigation or implementation decision.

## Flows

Complexity signal prompts investigation, not documentation. Keep flow only when hidden ownership, ordering, or coupling creates consequential wrong turn. Prefer entry/authority pointer + warning; ordinary multi-file traversal alone does not justify flow section.

Placement -> `## Flows` in nested file per `## Placement` (domain owning flow's core rules and state writes); never root. Hops outside that subtree -> repository-relative paths. Light -> no flows section; distill flow findings into root architecture, invariants, pitfalls. One flow lives in one file; never split or repeat it.

Per flow -> trigger/entry path, rule/state owner, consequential hazard. Add shortest hop chain, boundary, or co-change/helper pointer only when needed to explain hazard. No full trace, line numbers, function bodies, or transient config values.

## Shape

Root file -> starts with `# Agent instructions` header + one-line project description (what repository is/does). Then sections as useful: runtime, commands, architecture per `## Architecture`, testing, pitfalls, maintenance. Never flows.

All files -> short bullets, one fact each; multi-fact entry (e.g. flow) -> parent bullet naming it + sub-bullets (entry, owner, hazard, co-change). Never pack several facts into one long line.

`## Testing` -> only where test structure or setup changes agent decisions; only in root and nested files whose subtree owns test harness or config (app/package level). Root -> cross-cutting only: which layer/framework runs where, shared prerequisites, E2E ownership; existing harness doc -> path pointer, no restatement. Feature-level nested files -> no `## Testing`; test caveat goes in flow entry or pitfall it qualifies. Runnable commands only in `## Commands`.

`## Pitfalls` -> standalone verified hazards, home per `## Placement`. Hazard bound to one flow -> stays in that flow entry.

Nested files contain only local architecture, flows, testing, and pitfalls; no commands. Create one when subtree owns doc-worthy flow, or has distinct decisions, invariants, or risks not evident from its entry point. Small file fine; size alone never folds content into parent.

Instruction files never point to, list, or summarize other `AGENTS.md`/`CLAUDE.md` files, except mandatory root Maintenance rule's generic update instruction. Discovery handled outside generated content. Cross-domain dependency -> source authority path + hazard per `## Placement`. Complexity alone does not justify walkthrough or domain inventory.
