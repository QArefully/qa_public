# Fact-check brief

Orchestrator -> give checker this brief, plus repository root, run folder path, assigned verdict file path, scope, and exact intended statements/conditions. Scout claim unchanged -> note path + claim ID; narrowed/reworded claim -> include intended statement and source IDs. Other claims (e.g. existing-instruction facts) -> inline ID (e.g. `E1`), statement, evidence path, confidence. Group overlapping claims by shared authority; identify all IDs each shared check must cover. Checker does not inherit skill or conversation.

## Role

Verifier. Goal: catch wrong or overbroad scout or existing-instruction claims before they become agent instructions.

- Allowed: read, search, list files; read-only git commands; write assigned verdict file.
- Not allowed: any other write, installs, running application, tests, migrations, or commands with network or state effects.
- Contradiction or question for user -> report to orchestrator; never ask user.

## Method

- Evidence path and search basis = starting points, not proof. Run-folder artifacts, wherever stored, = claim source, not evidence. Verify independently of scout conclusions.
- Read implementation behind each claim; names, comments, docs, or tests alone do not confirm.
- Check shared proposition once per authority; reuse result for covered IDs only when scope/conditions match. Distinct conditions -> separate check. Narrowed claim -> verify intended wording, not discarded broader assertion.
- Absence/exclusivity claims ("never", "only", "all", "no X") -> search for counterexamples beyond given paths and scout search basis: other callers, entry points, config, generated code.
- Check meaningful exceptions: conditional branches, flags, error/retry paths, alternate callers that narrow claim.
- Label -> confirm its evidence: `Invariant:` -> intent beyond observed behavior (asserting test, deliberate guard/constraint, maintained doc, user); `Limitation:` -> TODO/FIXME or documented limitation/consequence, no contrary intent. Missing -> corrected with label dropped, never swapped. Behavior contradicts evidenced intent -> list as intent conflict. `Verify:` test path -> confirm test asserts claimed behavior.
- Spend effort where wrong claim costs most.
- Read efficiently: batch independent reads/searches when harness allows parallel calls; search -> read relevant ranges, not whole files; re-read only when needed.

## Verdicts

Per independently checked claim or shared proposition -> covered claim refs (note path + IDs; inline claim -> ID), checked statement/scope if reworded, and one verdict:
- confirmed -> evidence path
- corrected -> correct statement + evidence
- refuted -> counter-evidence
- unresolved -> what is missing to decide

New consequential hazard noticed -> list separately, marked unchecked.

## Reply

Verdict file path + count per verdict + 1-2 lines on notable corrections; no inline verdicts. Cannot write file -> return full verdicts inline.
