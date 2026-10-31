# Repository analysis

## Scan

Evidence order: executable config/code -> tests/CI -> maintained docs -> existing instructions -> user context.

Scan: enough root context to propose boundaries and brief scouts; deep flow reading belongs to scouts. Search/outline first; read relevant ranges in large manifests, config, tests, and docs rather than full dumps. Existing instruction files -> read fully. Cover:

- main applications, services, packages, infrastructure, and test harnesses
- runtime and package-manager requirements
- exact install, run, build, check, and test commands
- flow entry points per boundary: routes, CLI commands, UI entry, jobs, consumers, webhooks, schedules
- destructive actions, generated boundaries, external effects, and common traps
- documentation paths to reference instead of repeat

Write assigned run-folder artifacts:

- `context.md` -> shared digest: repository root, project purpose, root entry/authority paths, shared foundation, relevant user context, existing-instruction paths. Facts remain leads until checked; digest never substitutes for source evidence.
- `scan-note.md` -> root-level claims (orientation, runtime, commands, architecture) + factual claims extracted from existing instructions, as `scan-C<n>` records per contracts Records; every scan claim `confidence: low` (shallow read; checker required). Flow IDs, tagged question records, leads per scout note schema. Existing user/process directives (workflow, authorization, style) -> separate `## Kept directives` bullets with source file:line + applicable scope; never claims.
- `scope-proposal.md` -> short decision artifact: each proposed scope's id, paths, one-line reason, prior-note paths, existing-instruction paths, scan claim and question IDs routed to that scope's checker (root-wide items -> most related scope); flag genuinely complex runtime/E2E behavior needing root scout. The orchestrator maps each ID to an accepted scope after choosing or merging scopes. End with conflicts/skipped: doc/code and intent conflicts, skipped flows, unresolved gaps.

Scan claims and questions -> area checker per routing; no separate scan checker. Scan proposes checker scopes before accepted scopes exist; the orchestrator records each scan question ID's accepted-scope assignment.

## Select content

Scouts tag confidence; checker selects guidance-worthy candidates first, then verifies only where required. Selection applies to scan claims, scout claims, existing-instruction facts, promoted leads, late additions.

- confidence: per [scout](../agents/scout.md) Confidence.
- checker required: low confidence; absence/exclusivity ("never", "only", "all", "no X"); security/money regardless of confidence; existing-instruction and scan facts not read in implementation by scout; promoted leads; late additions; any entry needing `Invariant:`/`Limitation:`/`intent unknown` label or `Verify:` pointer.
- placeable per contracts Records; `ledger.py project` enforces. Unresolved -> gap list, never document.
- leads noticed in passing -> promote only hazards changing future agent edit decision, then verify as `-F<n>` record; drop other bug/security observations.
- existing instruction files -> factual claims = leads under same rule; user/process directives exempt from factual verification, kept per `## Placement`.
- dedupe shared propositions within batch before verifying; drop non-guidance-worthy claims before expensive checks.

Checker assigns labels from evidence per `## Shape`; scout wording never sets labels. Output per [checker](../agents/checker.md).

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

- file, symbol, route, dependency, or environment-variable inventories; hand-enumerated sets ("files doing X: a, b, c") rot silently -> greppable rule or enforcing test path; enumerate only short, stable sets
- timings, counts, temporary status
- line-by-line code narration; flows obvious from entry point and adjacent files
- generic advice or host-provided agent workflow
- duplicated parent guidance or human documentation
- worked numeric examples (non-obvious rule as one statement + authority path stays), fixture values, test scenarios, ticket/rubric checklists, test-file -> feature mappings beyond one `Verify:` pointer per `## Shape`, and coverage claims inferred from filenames

Keep investigation detail outside instructions. Scout/checker output -> guidance-worthy facts and consequential gaps, not general bug audit or test-absence inventory. Test guidance -> harness setup (fixture lifecycle, seed/template, config limits) + caveats on what tests or mocks do not prove (mock vs persistence, weak assertions). Reuse existing guidance; omit generic checklists.

## Placement

Nested instruction files may not load until agent works in their subtree. Each fact -> one home = deepest owning-domain subtree covering trigger (code whose edit triggers hazard or must honor fact), at app/package/feature granularity per `## Shape` (parent files load for whole subtree beneath them -> keep lean). Trigger owner usually owns rule or state write; failure surfacing in another domain -> still trigger owner, not failure site. Trigger spans sibling domains -> nearest common parent. Repository-wide structure -> root per `## Architecture`. Home file: existing one; none -> Full creates it (subtree fails `## Shape` creation rule -> nearest parent home), Light uses root (root holds all, concise domain guidance included). Other domains needing fact -> source authority path + hazard only when needed, never instruction file. Parent entry whose concern is implemented in child subtree -> child source path (entry file or exemplar) + hazard only when needed; fact stays in child home.

File set follows placement rule, not scout scopes: one scope may feed several files or none; one file may draw on several scopes.

Placement agent procedure per [placement](../agents/placement.md). Flow joining per `## Flows`; scope boundary never defines flow ownership.

Write `routing.json` per contracts; routing metadata only, never finished wording or manuscript:

- target -> disposition, placeable fact IDs, directive refs, writer batch; flow facts routed together by flow ID to one target
- shared propositions across records -> one ID routed; duplicates -> `unplaced` with reason naming kept ID
- existing selected file -> keep/update/delete; factual content follows records; user/process directives -> refs with original file:line, preserving intent and scope
- non-placeable, low-value, or out-of-mode IDs -> `unplaced` with short reason
- policy cannot decide home -> `alternatives`, facts withheld from targets until decided
- batches: disjoint target sets sized so projection + targets fit one writer comfortably; group by subtree

Write short `doubts.md`: conflicting records/incompatible flow evidence with competing IDs + decision impact; home alternatives with reasons; conflicts/skipped. Never resolve factual dispute by wording or source read. Reply per [placement](../agents/placement.md).

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

Placement routes flow facts by flow ID; cross-scope answers retain asking flow's ID. Home -> `## Flows` in nested file per `## Placement` (domain owning flow's core rules and state writes); never root. Light -> no flows section; distill flow facts into root architecture, invariants, pitfalls. One flow lives in one file; never split or repeat it. Writer renders flow entry from routed records; flow/fact IDs stay in run artifacts, never generated instructions.

Per flow -> trigger/entry path, rule/state owner, consequential hazard. Coupling hazard -> `Change X -> review Y` trigger, not descriptive "X owns Y" line. Add shortest hop chain, boundary, or helper pointer only when needed to explain hazard. No full trace, line numbers, function bodies, or transient config values.

## Shape

Root file -> starts with `# Agent instructions` header + one-line project description (what repository is/does). Then sections as useful: runtime, commands, architecture per `## Architecture`, testing, pitfalls, maintenance. Never flows.

All files -> short bullets, one fact each; multi-fact entry (e.g. flow) -> parent bullet naming it + sub-bullets (entry, owner, hazard, `Change X -> review Y`). `Change X -> review Y` spanning several files -> own parent bullet, one sub-bullet per file stating what to update there. Never pack several facts into one long line.

Label behavioral entry only where invariant vs limitation changes what agent may change; coupling, pointer, ownership lines -> no label. `Invariant:` = intended behavior, preserve; needs intent evidence (asserting test, deliberate guard/constraint, maintained doc, user). `Limitation:` = known gap, quirk, or bug in current behavior, not contract; no contrary intent evidence; needs limitation evidence (TODO/FIXME, documented limitation or consequence). Neither evidenced -> no label; entry agent could wrongly preserve or fix -> end with `intent unknown`. Behavior contradicting evidenced intent -> conflict for final report, not label. Focused test proving entry exists -> append `Verify: <test path>`; one pointer, never test list or coverage claim.

`## Testing` -> only where test structure or setup changes agent decisions; only in root and nested files whose subtree owns test harness or config (app/package level). Root -> cross-cutting only: which layer/framework runs where, shared prerequisites, E2E ownership; existing harness doc -> path pointer, no restatement. Feature-level nested files -> no `## Testing`; test caveat or `Verify:` pointer goes in entry it qualifies. Runnable commands only in `## Commands`.

`## Pitfalls` -> standalone verified hazards, home per `## Placement`. Hazard bound to one flow -> stays in that flow entry.

Nested files contain only local architecture, flows, testing, and pitfalls; no commands. First line = orientation line -> subtree scope; scope text exempt from cross-file dedup. Entry pointer optional, only when agent would not find entry by convention: omit conventional bootstrap/config/barrel names (`main.*`, `index.*`, `config.*`, `App.*`) unless they hold non-obvious logic; pointer targets real logic, never shim/re-export (point at delegate or omit); path cited elsewhere in same file -> no orientation repeat. One section -> omit heading; several -> headings from that set (`## Architecture`, `## Flows`, `## Testing`, `## Pitfalls`). Create one when subtree owns doc-worthy flow, or has distinct decisions, invariants, or risks not evident from its entry point. Small file fine; size alone never folds content into parent.

Instruction files never point to, list, or summarize other `AGENTS.md`/`CLAUDE.md` files, except mandatory root Maintenance rule's generic update instruction. Harness auto-loads nested files; pointers to them are noise. Cross-domain dependency -> source authority path + hazard per `## Placement`. Complexity alone does not justify walkthrough or domain inventory.
