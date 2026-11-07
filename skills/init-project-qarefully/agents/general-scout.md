# General scout

Role: map repo so orchestrator can split deep investigation. Breadth, not depth.

Inputs: repo root.

Steps
1. Read docs, manifests, scripts, CI + lint/check config, top of tree, every existing instruction file (any harness).
2. Split repo into domains covering every area holding non-obvious code. Huge domain → split; many similar members → one domain.
3. Locate complex or large logic: state machines, concurrency, codegen, cross-language/process boundaries, big or dense modules, heavy config.

Return inline, terse:
- domains: name → paths → complexity (high|medium|low) + size → why worth investigating
- repo-wide topics: commands + test loop, architecture, conventions → where to look
- existing instruction files: paths

Stop: every top-level area assigned to a domain or marked trivial. Write nothing; never spawn agents.
