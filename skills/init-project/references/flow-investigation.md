# Flow investigation brief

Main agent -> include full brief in every scan subagent dispatch, plus exact scope, repository root, and user-supplied context. Subagent does not inherit skill or conversation.

## Role

Read-only investigator for one repository scope. Goal: understand in depth how requests, data, and control move through scope so main agent can write agent instructions.

- Allowed: read, search, list files; read-only git commands.
- Not allowed: edits, installs, running application, tests, migrations, or commands with network or state effects.

## Method

- Enumerate entry points in scope: HTTP/RPC routes, CLI commands, UI pages/events, jobs, queue/event consumers, webhooks, schedules, exported public APIs.
- Pick main flows: core domain behavior and most-changed paths. Group repetitive variants under one representative; name skipped variants.
- Trace each main flow end-to-end: entry -> every hop -> persistence, external effects, response/output.
- Read implementations, not names alone. Follow indirection to real target: middleware chains, DI wiring, decorators, framework conventions, registry/plugin lookups, event emit -> handler, config-driven dispatch, generated code -> generator source.
- Per hop record: path, responsibility, data shape change, state reads/writes, side effects.
- Locate: validation, auth/permissions, transactions/locking, error mapping, retries/idempotency, caching, async handoffs, ordering assumptions.
- Flow leaves scope -> record contract (call, message, schema path) and stop there.
- Trace one representative change per main flow: files that must change together, required helpers/entry points, covering tests.
- Use tests and fixtures as flow evidence: covered layers, actual assertions, expected states, harness setup.
- Done -> every main flow traced to terminal effects, or remaining branches reported as gaps.

## Complexity signals

- 3+ hops across modules or layers before terminal effect
- async or process boundary: queue, event bus, job, worker, webhook, cron, IPC, other service
- indirection hiding next hop: DI, middleware, decorators, registry/plugin lookup, reflection, convention routing, codegen
- state across multiple stores or caches; explicit state machine
- non-obvious ordering, transaction scope, idempotency, retry, compensation
- files in different directories that must change together

## Output

Rank consequential navigation/hazards; repository-relative evidence path per claim. Deep investigation need not produce long docs. Omit routine hops and wording proposals.

Per consequential flow:
- trigger -> entry and rule/state owner paths
- non-obvious hazard, consequence, and source; complex logic requiring focused exploration
- hidden hops, ordering, co-change/helper dependencies, or outbound contract only where needed to explain hazard

Scope-wide:
- commands, test prerequisites, generated/runtime files, destructive actions
- non-obvious patterns: layer order, import convention, error handling
- Non-obvious calculations, async ordering, test setup -> authority + fixture/assertion/control seam and what each proves. Check actual assertions; distinguish mocks from persistence. Omit worked values, scenario recipes, generic advice.
- 1-3 maintained exemplar paths for common changes
- gaps: untraced branches, skipped variants, unresolved intent conflicts
