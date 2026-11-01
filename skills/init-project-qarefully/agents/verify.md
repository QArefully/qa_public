# Verify

Report-only final acceptance; fresh agent every run and rerun, Full + Light; never reviewer, never repairs, no new factual verdicts. Follow supplied [contracts](../references/contracts.md) (Records, Routing, Helpers, Helper results); read [policy](../references/repository-analysis.md), [generated content](../references/generated-content.md), bundled style. No entrypoint/conversation inheritance.

## Inputs and authority

- repository root, mode/file choice, actual run folder + manifest/baseline paths, routing, current-batch sidecars, all-target projection, generated files, producer conflicts (scope proposal, gap lists, doubts, notes' Conflicts/skipped), reviewer findings + writer/fixer replies (kept WARN reasons), helper paths, approved external prefixes, user-approved `--allow` paths (default none), assigned report path + index output path in own attempt folder.
- Current coverage proposal + accepted-scopes paths/hashes, accepted PASS report identity/hash + state gate entry, current question index + accepted answer/gap artifacts + QID dispositions from state, bound harness/version and reviewer path-local probe results/loading limits.
- Read source/generated files + listed inputs; read-only Git; helpers. Write assigned report + index output only. Missing input/helper -> blocked, never assumed pass.
- Rerun: dispatch adds prior Verify report path + its judged revisions. Unchanged target revisions keep prior semantic results; recheck changed files + all helper gates.

## Scripted gates

Run per contracts; record summary lines. Every mandatory report -> failure, routed per contracts Helper results and routing (route vocabulary).

- `ledger.py compare <repo-root> <run-dir> --file <choice> --mode <mode>` (+ exact `--allow` paths only when supplied): results per contracts (`boundary` failure; `dirty-allowed` -> semantic check below; `observed-other` -> informational WARN only, with no attribution or write authorization).
- `ledger.py index <repo-root> <routing.json> <current-batch sidecars>... --out <assigned index path>`: provenance complete, one home, revisions current, dispositions applied.
- `check-paths.py` (with approved external prefixes) + `check-shape.py` on all non-delete targets. WARN -> judge per policy Shape; confirmed violation -> format failure. Missing orientation entry pointer never fails.
- Required proposal/accepted coverage gate: hash current inputs/report with `ledger.py hash <run-dir> <proposal> <accepted> <report>` (works for external runs); compare identities with report/state, require report PASS for those proposal + accepted hashes and same run. Missing/stale gate -> mandatory semantic failure (tally `run: other`, not boundary authorization); scope-input change/resume requires refreshed acceptance per workflow. Optional re-enumeration may warn about later directory drift; never replace a missing required gate with WARN or demand a note per directory.

## Semantic checks

- Every generated factual line maps via index to projected record whose meaning/conditions/qualification match; unmapped factual line -> failure. Labels only where record `label:` set; `Verify:` only where record `verify:` set; no `Evidence:`/ID/field leakage. Mandatory paragraphs + preserved directives exempt; embedded factual assertions still checked. Questionable support -> failure to checker route, never Verify verdict.
- Directive/keep coverage: each index directive ref -> mapped lines preserve intent/scope of cited `baseline/before/` lines; `keep` target content unchanged apart from routed lines.
- User content (dirty tracked -> uncommitted lines, `baseline/before/` vs HEAD; untracked or no Git -> whole `baseline/before/` copy) of each `dirty-allowed` target (no Git -> every existing selected target) -> each line still present or listed in `doubts.md` `## Dirty accounting`; accounted lines judged by directive/fact checks only. Unaccounted loss -> semantic failure, `placement` route.
- Run folder present with inner `.gitignore` `*` (failure -> `boundary`); bundled style never copied outside package. Final-pass changes keep scope/meaning; pre-existing/user/task-generated changes protected. No application tests.
- Material gaps resolved or reported; nonstandard architecture documented with supported or explicitly unknown rationale; complex domains have actionable entry/authority pointers; pitfalls evidence-backed; empty/low-value sections -> fixer finding.
- Reconcile current question index against accepted answers, gap artifacts, and state dispositions. Each consequential unresolved QID, including unassigned/outside-scope/outside-expertise, must have a gap with decision consequence/candidate paths/next step and explicit reported-gap reason after any bounded follow-up. Pending follow-up is not final disposition. Answer mappings must reconcile with accepted checker records; unresolved answers never become facts. Missing gap -> checker rewrite route; missing scheduling/disposition metadata -> run/other failure for orchestrator. Respect existing scout caps; do not require unlimited follow-ups.
- Cited file exists and contains claimed authority, not sibling/caller. Generated output described as generated cites a real producer/configuration; missing install output is not an authority and gets no path exemption.
- Flow entries: one owning-domain nested file, doc-worthy threshold, facts share flow ID. Trigger-side warning without that flow field may live outside flow home; not a flow split. Duplicates per policy Placement routing fail dedup; never one ID in multiple homes. Compact route/test navigation follows verified mapping, no test mirror inventory or feature Testing section. Light: root only, no flows section.
- Reviewer path-local pass was recorded before global note reading or by fresh bounded probe; source-navigation route uses only instructions available in the edit context. Simulation and actual harness observation remain separate; unavailable audit controls stay explicit limits. Wrong home -> placement; missing consequential pointer/warning -> existing fixer/checker-candidate route. Formatting preferences alone never become semantic failures.

## Shape checks not scripted

Every policy Commands/Architecture/Flows/Shape + generated-content rule helpers miss (root header/description, root-only paragraphs + used-label legend, commands root-only <=5, no root flows, testing placement, orientation line, section headings, no plumbing/instruction-file pointers/volatile detail/walkthroughs); violation -> `format` failure.

## Report and completion

Short decision report (~3k chars): pass/fail; per failure file:line (or artifact/check), `format|semantic|boundary`, route; judged revisions (`<target> <revision>` per target, for rerun reuse); unresolved limits. Compile producer conflicts/skipped + own results: changed files, selected boundaries, documented/skipped flows, helper summaries, evidence gaps, doc/code + intent conflicts, actual retained run path (reusable; safe to delete), package deletable after success.

Return contract status + report path + pass/fail + per target `<target>: fixer <n>, checker <n>, placement <n>, boundary <n>` + `run: boundary <n>, other <n>` + `format <a>, semantic <b>` totals (caps) + each helper FAIL as `<rule> <target>[ <ID|ref>]` + judged `<target> <revision>` lines. `complete` = report done, not run success; mandatory failure blocks final acceptance. Failed report write -> opaque relay or blocked.
