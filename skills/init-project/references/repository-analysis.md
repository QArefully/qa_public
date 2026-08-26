# Repository analysis

## Scan

Evidence order: executable config/code -> tests/CI -> maintained docs -> existing instructions -> user context.

Start shallow. Find:

- main applications, services, packages, infrastructure, and test harnesses
- runtime and package-manager requirements
- exact install, run, build, check, and test commands
- dependency direction, state authority, and source-of-truth locations
- destructive actions, generated boundaries, external effects, and common traps
- documentation paths to reference instead of repeat

Use supporting paths. Expand only where evidence changes agent decisions.

## Select content

Except for runtime requirements and exact commands, prefer where and why over current implementation detail.

Keep:

- boundary purpose and allowed dependency direction
- authoritative definitions and extension points
- ownership of validation, state, permissions, and side effects
- durable domain or safety invariants
- fastest relevant validation and unusual test prerequisites
- plausible wrong turns not obvious from nearby code

Drop:

- file, symbol, route, dependency, or environment-variable inventories
- timings, counts, temporary status, and prose versions of code flow
- generic advice or host-provided agent workflow
- duplicated parent guidance or human documentation
- unsupported claims

## Shape

Root sections as useful: repository map, runtime, commands, architecture/domain, testing, agent hints, maintenance.

Add `## Testing` only where test structure or setup changes agent decisions. Cover relevant layers/frameworks, file or config locations, harnesses/fixtures/providers, prerequisites, and E2E ownership. Keep runnable commands only in `## Commands`; do not repeat them under Testing.

Nested files contain only local architecture, local commands, local testing, and local hazards. Create one only when the subtree has distinct decisions or risks.
