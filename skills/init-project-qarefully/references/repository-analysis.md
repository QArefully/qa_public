# Repository analysis

## Scan

Evidence order: executable config/code -> tests/CI -> maintained docs -> existing instructions -> user context.

Scan: shallow orientation + meaningful investigation ownership, enough to brief scouts. Search/outline first; read relevant ranges in large manifests, config, tests, and docs rather than full dumps. Existing instruction files -> read fully. Deep flows and exact command verification belong to scouts/checkers. Cover:

- main applications, services, packages, infrastructure, and test harnesses
- authoritative runtime/package-manager and setup/run/build/check/test configuration + maintained docs; flag uncertainty for verification
- likely flow entry/authority paths and consequential cross-boundary behavior to investigate
- destructive actions, generated boundaries, external effects, and common traps
- documentation paths to reference instead of repeat

Write concise run-folder artifacts:

- `context.md` -> repository purpose, root authorities, shared foundation, user context, existing instruction paths. Shallow leads never substitute for evidence.
- `scan-note.md` -> root claims and existing-instruction facts, source references and questions. Scan claims require checking. Keep user/process directives separately with source and scope.
- `investigation-map.md` -> meaningful domains, primary owner, questions, intentional skips + reasons. Surface consequential cross-boundary mechanisms; assign primary owners while other scouts trace dependencies needed for their own flows. Check for missing domains; map is an investigation aid, not a directory grammar or file-generation quota.

## Investigation

Prioritize likely edit decisions. Trace each assigned question through implementation until mechanism, consequences of changes, and evidence are clear. Follow dependencies across boundaries as needed; understand their effect on the assigned flow without surveying the whole other domain. Shared ownership coordinates investigation, never prohibits overlapping reads or directly evidenced claims.

Test consequential explanations against plausible callers, branches, states, configurations, or exceptions. Verify each dependency direction independently. Stop when the edit question is supported, or record the unresolved contract and next evidence step. Notes contain consequential claims, conditions, source references and unresolved questions, not exhaustive traces. Use focused follow-ups per workflow; checkers reconcile conflicts and consequential boundary contracts.

## Select content

Scouts tag confidence; checker selects guidance-worthy candidates first, then verifies only where required. Selection applies to scan claims, scout claims, existing-instruction facts, promoted leads, late additions.

- `high` confidence means direct implementation support, not self-rated certainty; otherwise `low`.
- checker required: low confidence; absence/exclusivity ("never", "only", "all", "no X"); security/money regardless of confidence; existing-instruction and scan facts not read in implementation by scout; promoted leads; late additions; directional edit warnings and source-navigation mappings; any entry needing `Invariant:`/`Limitation:`/`intent unknown` label or `Verify:` pointer.
- Placeable: directly supported high-confidence claim outside mandatory-check categories, or checker-confirmed/corrected claim. Rejected or unresolved -> gap, never document.
- leads noticed in passing -> promote only hazards changing future agent edit decision, then verify; drop other bug/security observations.
- existing instruction files -> factual claims = leads under same rule; user/process directives exempt from factual verification, kept per `## Placement`.
- dedupe shared propositions within batch before verifying; drop non-guidance-worthy claims before expensive checks.
- Validate cited source/test paths before placeable records. Absent install/build outputs are not existing authorities: cite checked-in generator/configuration or real delegate. If output naming matters, describe it as generated in ordinary prose + cite its existing producer; never exempt missing source citations from strict path checks.

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
- root directory map + repo-wide conventions per `## Architecture`

Drop:

- file, symbol, route, dependency, or environment-variable inventories; hand-enumerated sets ("files doing X: a, b, c") rot silently -> greppable rule or enforcing test path; enumerate only short, stable sets
- timings, counts, temporary status
- line-by-line code narration; flows obvious from entry point and adjacent files
- generic advice or host-provided agent workflow
- duplicated parent guidance or human documentation
- worked numeric examples (non-obvious rule as one statement + authority path stays), fixture values, test scenarios, ticket/rubric checklists, per-test-file -> feature inventories beyond one `Verify:` pointer per `## Shape`, and coverage claims inferred from filenames. A verified conceptual route/test navigation rule per `## Placement` is permitted.

Keep investigation detail outside instructions. Scout/checker output -> guidance-worthy facts and consequential gaps, not general bug audit or test-absence inventory. Test guidance -> harness setup (fixture lifecycle, seed/template, config limits) + caveats on what tests or mocks do not prove (mock vs persistence, weak assertions). Reuse existing guidance; omit generic checklists.

## Placement

Instruction loading depends on the bound harness/version; verify its supported path context rather than assuming source reads load sibling notes. Each fact -> one home = deepest local subtree covering its edit trigger, at app/package/feature granularity per `## Shape`; feature-specific fact -> feature's own directory, never broad ancestor merely because ancestor file exists. Canonical behavior stays with its rule/state owner. A shared edit trigger spanning siblings -> nearest common parent. Repository-wide structure -> root per `## Architecture`; directory-map role record -> root, that dir's nested orientation scope/path only. Home file: existing one; none -> Full creates it (subtree fails creation rule -> nearest suitable parent), Light uses root for all concise domain guidance.

Editing D can break authority in sibling S -> separate, independently verified directional record: `When changing X in D, review Y in S because Z`. Its evidence and home serve D's edit trigger; source authority path + hazard, never copied invariant or instruction-file pointer. Verify D->S and S->D separately when both matter; shared authority does not prove reverse coupling. Parent already provides sufficiently local guidance available from D -> use it. Full permits a small pointer-only file for a verified local hazard meeting Shape; never fold it into an unavailable sibling solely for size. Parent concern implemented in child -> child source pointer + hazard only when needed; canonical fact stays in child home.

Route/test edits may need a compact source-navigation rule at their app/package common ancestor: inspect owning feature behavior/guards before editing adapters or tests. Verify the actual mapping through layout/imports/dispatch and give real exception pointers; never infer a universal basename match. One conceptual mapping, parent bullet + one trigger path per sub-bullet if needed; no test-to-feature inventory or note per mirrored test directory. A routes-local note requires route-local hazards.

File set follows placement rule, not scout scopes: one scope may feed several files or none; one file may draw on several scopes.

Placement agent procedure per [placement](../agents/placement.md). Flow joining per `## Flows`; scope boundary never defines flow ownership.

Placement produces a simple file-to-guidance plan, including existing file dispositions, relevant accepted notes and directives, substantive home alternatives, and disjoint writer ownership. Group related targets when useful; scope boundaries alone do not require separate writers. Unsupported claims stay out. Preserve user/process directives and their scope.

Deduplicate shared propositions: retain the useful occurrence at its appropriate home, regardless of note or fact identifiers. Different triggers or conditions can carry distinct information; preserve them. Apply ancestor loading when selecting a home. Real home disputes go to placement; uncertainty about facts goes to checking. Earlier plan entries do not require separately accounting for an obvious duplicate removed during review.

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

- ownership: which app/package owns which concern; essential directories agent would not spot on entry (~5-10) -> parent bullet + one `dir/` -> concern per sub-bullet, short stable set allowed despite inventory exclusions; allowed dependency direction + enforcing config
- sources of truth: where canonical logic, configuration, schemas live
- cross-boundary decisions and nonstandard solutions -> constraint + supported rationale; unknown rationale -> mark unknown
- hidden cross-boundary dependencies: couplings, build/resolution or ordering effects invisible on casual read

Exclude request/layer walkthroughs, wiring or add-a-feature recipes, process/port/env/file inventories, local style visible in neighbouring code. Keep repo-wide conventions whose violation is silent or caught only by checks agent may not run: rule + exemplar or enforcing-check path, no wiring recipe; subtree-wide conventions -> nested home per `## Placement`. Single-domain detail -> home per `## Placement`. Keep bullet only when it changes navigation or implementation decision.

## Flows

Complexity signal prompts investigation, not documentation. Keep flow only when hidden ownership, ordering, or coupling creates consequential wrong turn. Prefer entry/authority pointer + warning; ordinary multi-file traversal alone does not justify flow section.

Placement keeps each flow together regardless of investigation scope. Home -> `## Flows` in nested file per `## Placement` (domain owning flow's core rules and state writes); never root. Light -> no flows section; distill flow facts into root architecture, invariants, pitfalls. One flow lives in one file; never split or repeat it. Writer renders from accepted notes; references stay in run artifacts, never generated instructions.

Per flow -> trigger/entry path, rule/state owner, consequential hazard. Coupling hazard -> `When changing X, review Y because Z`, not descriptive "X owns Y" line. Add shortest hop chain, boundary, or helper pointer only when needed to explain hazard. No full trace, line numbers, function bodies, or transient config values. A distinct trigger-side warning outside the owning file is not a second flow entry: verify it independently and retain the relationship through source paths.

## Shape

Every file -> starts with exactly one `# Agent instructions` H1. Root -> one-line project description (what repository is/does) after H1; sections as useful: runtime, commands, architecture per `## Architecture`, testing, pitfalls, maintenance. Never flows. Sections use H2 with existing canonical names.

All files -> short bullets, one fact each: one claim + authority pointer where applicable; keep only conditions changing edit decision; mechanism shown by cited source -> drop. Edit-trigger warning: use an explicit condition, e.g. `When changing X, review Y because Z`. Preserve trigger, direction, authority, and reason. Several facts sharing subject (one flow, one cited path in one section), or one conditional warning spanning files -> parent bullet naming subject once + one sub-bullet per fact or file. Never pack several facts into one long line.

Label behavioral entry only where agent could plausibly mistake intended behavior for bug, or bug for intent, and change it wrongly; coupling, pointer, ownership lines -> no label. `Invariant:` = intended behavior, preserve; needs intent evidence (asserting test, deliberate guard/constraint, maintained doc, user); evidence required, not sufficient. `Limitation:` = known gap, quirk, or bug in current behavior, not contract; no contrary intent evidence; needs limitation evidence (TODO/FIXME, documented limitation); ordinary behavior or design choice -> no label. Neither evidenced -> no label; entry agent could wrongly preserve or fix -> end with `intent unknown`. Behavior contradicting evidenced intent -> conflict for final report, not label. Focused test proving entry exists -> append `Verify: <test path>`; one pointer, never test list or coverage claim.

`## Testing` -> only where test structure or setup changes agent decisions; only in root and nested files whose subtree owns test harness or config (app/package level). Root -> cross-cutting only: which layer/framework runs where, shared prerequisites, E2E ownership; existing harness doc -> path pointer, no restatement. Feature-level nested files -> no `## Testing`; test caveat or `Verify:` pointer goes in entry it qualifies; exception: no ancestor route/test navigation rule covers subtree and test layout not obvious -> one test-location bullet in existing section. Runnable commands only in `## Commands`.

`## Pitfalls` -> standalone verified hazards, home per `## Placement`. Hazard bound to one flow -> stays in that flow entry.

Nested files contain only local architecture, flows, testing, and pitfalls; no commands. Orientation line after H1 -> subtree scope; role text only from supported notes assigned to this file, else scope/path only; never topic of its facts; scope text exempt from cross-file dedup. Entry pointer optional, only when agent would not find entry by convention: omit conventional bootstrap/config/barrel names (`main.*`, `index.*`, `config.*`, `App.*`) unless they hold non-obvious logic; pointer targets real logic, never shim/re-export (point at delegate or omit); path cited elsewhere in same file -> no orientation repeat. Small files may omit section headings when grouping adds no value; otherwise headings from that set (`## Architecture`, `## Flows`, `## Testing`, `## Pitfalls`). Create one when subtree owns doc-worthy flow, or has distinct decisions, invariants, risks, or conventions shared by its children, not evident from its entry point. Small file fine; size alone never folds content into parent.

Instruction files never point to, list, or summarize other `AGENTS.md`/`CLAUDE.md` files, except mandatory root Maintenance rule's generic update instruction. Use source navigation independently of harness loading behavior. Cross-domain dependency -> source authority path + hazard per `## Placement`. Complexity alone does not justify walkthrough or domain inventory.
