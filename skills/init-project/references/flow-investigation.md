# Flow investigation brief

Orchestrator -> give scout this brief, plus repository root, run folder path, assigned note file path, exact scope, user-supplied context, in-scope prior-run notes and existing instruction claims, and, when useful, path to digest of shared context every scout would otherwise re-read (e.g. composition root), written once to run folder (e.g. `context.md`). Follow-up dispatch -> also one question, existing findings, evidence needed to resolve it. Scout does not inherit skill or conversation.

## Role

Scout investigating one repository scope. Goal: understand in depth how requests, data, and control move through scope so orchestrator can write agent instructions.

- Allowed: read, search, list files; read-only git commands; write assigned note file.
- Not allowed: any other write, installs, running application, tests, migrations, or commands with network or state effects.
- Prior notes, existing instructions, and orchestrator digest = leads; verify before claiming. Run-folder artifacts, wherever stored, = not repository evidence.
- Contradiction or question for user -> report to orchestrator; never ask user.

## Method

- Enumerate entry points in scope: HTTP/RPC routes, CLI commands, UI pages/events, jobs, queue/event consumers, webhooks, schedules, exported public APIs.
- Pick main flows: core domain behavior and most-changed paths. Group repetitive variants under one representative; name skipped variants.
- Trace each main flow end-to-end: entry -> every hop -> persistence, external effects, response/output.
- Read implementations, not names alone. Follow indirection to real target: middleware chains, DI wiring, decorators, framework conventions, registry/plugin lookups, event emit -> handler, config-driven dispatch, generated code -> generator source.
- During investigation track per hop: path, responsibility, data shape change, state reads/writes, side effects. Output only details supporting guidance-worthy facts or consequential gaps.
- Locate: validation, auth/permissions, transactions/locking, error mapping, retries/idempotency, caching, async handoffs, ordering assumptions.
- Explain consequential domain invariants and where enforced. Follow relevant failure, partial-completion, repeat-execution, and ordering paths; prioritize branches that change correctness rather than enumerate every variant.
- Identify consequential nonstandard architecture and constraints. Seek rationale in maintained docs/ADRs, relevant history, framework conventions, or user context; distinguish inherited framework behavior from project choices. Missing rationale -> report unknown, not guessed intent.
- Flow leaves assigned scope -> record contract (call, message, schema path) and unresolved behavior for synthesis or targeted follow-up; initial boundary is not proof of end-to-end understanding.
- Trace one representative change per main flow: files that must change together, required helpers/entry points, covering tests, and concrete consequence of breaking coupling.
- Use tests and fixtures as flow evidence: covered layers, actual assertions, expected states, harness setup.
- Read efficiently: batch independent reads/searches when harness allows parallel calls; search -> read relevant ranges, not whole files; re-read only when needed. Context growing large -> stop, write note, list remaining work as open gaps.
- Done -> consequential behavior explained with code/test evidence, not just call chain; terminal effects or outbound contracts identified.

## Complexity signals

- 3+ hops across modules or layers before terminal effect
- async or process boundary: queue, event bus, job, worker, webhook, cron, IPC, other service
- indirection hiding next hop: DI, middleware, decorators, registry/plugin lookup, reflection, convention routing, codegen
- state across multiple stores or caches; explicit state machine
- non-obvious ordering, transaction scope, idempotency, retry, compensation
- files in different directories that must change together

## Output

Write to assigned note file. Deep investigation need not produce long notes; <= ~8k chars = ceiling, not target. Prioritize facts changing future agent decisions and consequential gaps. Omit routine hops, wording proposals, general bug audits, and test-absence lists.

Each independently checkable claim -> stable ID (e.g. `C7`), repository-relative evidence path (+ line range when useful) + confidence; separate assertions with different evidence or conditions:
- high -> implementation read directly confirms
- low -> inferred, partial read, or names/tests only
- absence/exclusivity ("never", "only", "no X") -> also state search basis: patterns and paths searched

Note order: open gaps (untraced branches, skipped variants, unresolved cross-scope behavior, intent conflicts -> impact on follow-up decision); then per-flow entries ranked by consequence; then scope-wide.

Per flow entry:
- trigger -> entry and rule/state owner paths
- non-obvious hazard, consequence, and source; complex logic requiring focused exploration
- hidden hops, ordering, co-change/helper dependencies, or outbound contract only where needed to explain hazard

Scope-wide:
- commands, test prerequisites, generated/runtime files, destructive actions
- non-obvious patterns: layer order, import convention, error handling
- nonstandard architecture, supported rationale or unknown reasons, and complex domains needing focused exploration; source pointers and constraints relevant to safe changes
- non-obvious calculations, async ordering -> authority + control seam
- test harness setup (fixture lifecycle, seed/template, config limits) + caveats on what tests or mocks do not prove. Check actual assertions; distinguish mocks from persistence. Caveat qualifying one flow -> report with that flow. Omit test-file -> feature mappings, worked values, scenario recipes, generic advice.
- 1-3 maintained exemplar paths for common changes

Reply -> note path + 3-5 lines (top hazards, open gaps); no inline findings. Cannot write file -> return full note inline.
