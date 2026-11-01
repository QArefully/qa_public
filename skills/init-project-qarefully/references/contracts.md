# Handoff Contracts

## Capability binding

Before first child, inspect actual exposed controls; retain compact binding in `state.md` for scheduling/resume:

- dispatch/isolation: fresh bounded child without parent conversation; child can load assigned role/resources.
- model: requested + observable effective model/effort/profile; distinguish unobservable effective choice. `inherit` retains immediate parent's binding, including when native profile defaults would differ. Exact named profile only when user requests it; verify availability. Never silently substitute. Unverifiable required binding -> report limit/ask for viable authorized binding.
- visibility/writes: recipient resolves package/input/output paths; disjoint owned targets writable. Map paths across workspaces explicitly. Cannot write -> opaque relay below; no usable dispatch/isolation -> capability issue, never local role takeover.
- helpers: Python 3 available to each runner role below; missing -> affected check blocked, never assumed pass.
- capacity: actual concurrent slot ceiling + lower user limit; reserve slots before dispatch, queue when full. Mode scout total separate. No nested delegation; only orchestrator starts children.
- wait/cancel: actual wait/terminal signaling and cancellation behavior. Prefer completion notifications/bounded waits; no short polling, repeated nudges, or empty status updates beyond host-required intervals. Never treat commentary/tool return as done. Inability to stop writer -> retain ownership until terminal, block conflicting work.

## Fresh agents and continuations

- One agent -> one role + one bounded assignment. New independent assignment -> fresh agent given relevant artifact paths; never accumulated conversation or earlier role context.
- Continuation only completes/corrects same bounded assignment before substantial work: missing input/path fixed, `needs_user` answer before deep work (e.g. scan root ambiguity), write failure before output. Agent already did substantial work -> fresh agent continues from saved artifacts.
- Always fresh: retry attempt 2, follow-up scout, checker for candidates/doubts/late facts/rechecks, placement routing revision, writer/fixer after routing revision or user conflict decision, targeted re-review, Verify rerun after repair.
- Administrative operations (hashes, inventory, mapping, question index, manifests) -> helpers, never extra agent turns.

## Dispatch

Transport binds run/stage/attempt when possible; otherwise include explicit identity. Resolve paths in recipient's workspace, including paths inside selected Markdown sections. Give exact relevant contract sections + workflow boundary rules; child must read/follow bound role and selected policy/style sections. No child reads entrypoint or assumes inherited instructions.

```md
role: <ID + resolved agents/<role>.md path>
task: <bounded objective>
run: <root/location hint; actual run path after scan>
choices: <filename; mode; selected scout binding>
binding: <this role's requested/effective model; tools; helper paths; no nested children>
constraints: <user/host restrictions; approved external prefixes; task boundary; preserve others' edits>
ids: <assigned record ID prefix, when role writes records>
inputs:
- <resolved path>#<section> -> <purpose; accepted revision>
writes:
- <exact owned path> -> <consumer; expected prior target revision if mutable>
budget: <scope paths/IDs; artifact ceiling; completion criterion>
done: <role result + checks>
limits: <attempt; remaining scout/slot capacity when relevant>
```

Budget = ceiling, not target. Defaults: scout note ~8k chars; gap list, doubts, reviewer findings, Verify report each ~3k chars; routing metadata only; records one statement each. Output prioritizes decisions affecting future edits.

No common transcript/task-wide payload. Role tools: read/search/list/read-only Git where role permits + assigned artifact/product writes + bundled helpers per runner roles below. No application/tests/install/migration/network/state effects. Only orchestrator asks user. Contradictory instructions -> return issue; no hidden expansion.

Parallel mutable targets require disjoint ownership. All workers share workspace: preserve user/other workers' edits. Role procedure narrows read/write scope further.

## Records

- Record = `### <ID>` heading line -> body until next `#`, `##`, or `###` heading. Only claim/fact/question records use `###` in record files; no sub-headings inside a record (fields after one -> `unparsed-record`). Fields = unindented `- key: value` lines with bare values (`high`, never backticked/bold). Rest of body = statement with exact conditions; optional trailing `Evidence:` paragraph (search basis, ranges, label evidence, correction reason).
- Rendered into instructions: body statement (with `qualification:` condition) + `label:`/`verify:` only. `Evidence:`, IDs, other fields never rendered; statement carries any source pointer to render.
- IDs unique in run, never reused for different content. Scope IDs from `accepted-scopes.md`; scan uses `scan`. Prefix = scope ID for scan/initial scouts/initial checkers; orchestrator assigns each follow-up scout and each candidate/late/recheck checker dispatch unique prefix `<scopeID>-R<k>` (`ids:` line). Claim `<prefix>-C<n>`, question `<prefix>-Q<n>`, flow `<prefix>-FL<n>` (cross-scope continuation keeps original flow ID), checker-originated fact (late addition, promoted lead, question answer, candidate) `<prefix>-F<n>`.
- Checker reuses claim ID only for first verification of claim in its assigned notes/routed scan claims. Re-verification/correction of ID already checked or routed -> new `<prefix>-F<n>` + `- supersedes: <oldID>`. Any new/corrected record after placement -> fresh placement revision (updates `inputs` + routed IDs) before projection.
- Scout/scan claim: `confidence: high|low` required; `authority: <path#symbol|path:line>` required; `flow:` optional.
- Checker record (files always named `facts.md`): `verdict: confirmed|corrected|refuted|conflict` required; `authority:` required; `label: invariant|limitation|none`, `verify: <test path>`, `flow:`, `qualification:`, `supersedes:` optional. Body = exact placeable statement (corrected -> corrected statement); refuted/conflict -> rejected proposition + Evidence.
- Question: `flow:` asking flow, `contract:` what must be answered (+ contract path), `owner: <scopeID|unassigned>`, `status: open|answered|gap`, `answer: <ID>` when answered.
- Question routing: scan proposes a checker scope for each scan QID before accepted scopes exist; the orchestrator maps every scan QID to an accepted scope in `accepted-scopes.md`. Resolve an explicit QID mapping first; otherwise resolve the accepted or merged/rejected scope named by `owner`, or for `unassigned`, the asking scope from the QID prefix through the same mapping. An explicit QID mapping assigns the question to that scope's checker without requiring a scan pseudo-scope.
- Question disposition: each consequential unresolved QID must appear in checker `gaps.md` with decision consequence, candidate paths/owner, next evidence step + reason code `outside-scope|unassigned|insufficient-evidence|outside-expertise|unavailable-evidence|intent-unknown|bounded-followup`. Checker returns QID + code, not evidence. Parent records QID -> follow-up assignment or explicit reported-gap reason in state; missing gap entry -> checker author rewrite. Ownership resolution alone never discharges investigation. Keep existing `answered: <QID> -> <ID>` format; final Verify reconciles index/gaps/dispositions. No unresolved answer becomes a fact.
- Placeable = checker confirmed|corrected, or scout/scan `confidence: high` claim with no checker record; never when any refuted|conflict or superseding record exists for ID. Labels/`Verify:` only from checker `label:`/`verify:`; unchecked high claim -> unlabeled, no `Verify:`.
- Evidence set for `ledger.py project` = routing `inputs` + every `facts.md` under run dir except `quarantine/` + `baseline/`; unlisted refuted/conflict/supersedes still count.

## Scope grammar

Authoritative machine sections in `scope-proposal.md` (normal decision text + scan claim/question mappings stay outside these sections):

```md
## Container: .
## Container: apps
## Scope: api
- path: apps/api -> Investigate API boundaries and configuration.
## Skipped: tools -> Generated by checked-in scripts/generate.py; inspect its producer.
```

Fragment only; real proposals classify every required child. Parse unfenced sections only; fenced examples ignored. Headers/lines use exactly `## Container: <directory>`, `## Scope: <unique ID>`, `- path: <directory> -> <nonempty per-directory investigation/merge reason>`, `## Skipped: <directory> -> <nonempty reason>`. Each scope has >=1 path line; scope IDs match `[A-Za-z0-9][A-Za-z0-9_.-]*`. Machine sections contain only their machine lines + blanks; mappings/decision prose require a separate nonmachine heading. Paths are literal repository-relative directories (`.` for root), optionally paired backticks; normalize separators once. Reject malformed recognized sections/lines, duplicate container/skip declarations or scope IDs/owners, braces, globs, absolute paths, `..`, nonexistent/orphan paths, and canonical escapes. Compare path components with host case semantics. A scope ID may combine directories, but each retains its own reason.

- Root container `.` required. Every container connects to `.` through declared parent containers. Each immediate child directory, including empty ones, is explicitly scoped, skipped, or delegated to a declared child container. Scope paths must be immediate children of a declared container or the declared container itself. Scoping a container does not discharge its child obligations; a scope + container refinement is allowed, skip + scope/container is not. Deeper descendants never account for parents; broad ancestor membership never implicitly covers declared feature children.
- Container selection and deeper semantic-domain discovery -> [policy Scan](repository-analysis.md#scan). Structural PASS checks declared directory assignments, not semantic completeness; checker/reviewer sample consequential boundaries/skips independently.
- Do not follow directory links/junctions; list linked children as explicit skips with reason, never investigated targets. `.git` + current run are excluded by helper; nested run ancestors still need ordinary classification. Generated/vendor/data directories need explicit evidence-shaped skips (generated by X, data consumed by Y, wrapper delegated to Z); `small`, `out of scope`, or `budget` alone is insufficient. Do not recursively walk skipped trees.
- `accepted-scopes.md` uses only `## Scope:` + exact `- path:` machine grammar, with scan-ID/QID and merged/rejected-scope mappings outside machine sections. Container/skip authority remains proposal; accepted files must not redeclare them. Accepted investigation path set must equal proposal set, retaining each reason; scope IDs may merge. Rejected scope paths must be reassigned. Changed investigation paths/container/skip decisions require scan proposal revision + both checks again. Workflow owns mode-specific root-scout eligibility.

Coverage is an investigation-assignment gate in both modes, never a requirement to generate one file per directory. Proposal/accepted input hashes + current PASS report identity belong in state; changed input or resume invalidates gate until hashes/identity are checked per recovery.

## Routing, provenance, index

- `routing.json` (placement writes; no prose): `revision`, `inputs` (run-relative record files), `targets` -> `<repo-rel path>` -> `disposition: create|update|keep|delete`, `facts: [IDs]`, `directives: [refs]`, `batch: "<string>"`; `alternatives: [{facts, homes, reason}]`; `unplaced: [{id, reason}]`. Lives inside run dir (helpers find baseline from its ancestors). One home: ID in at most one target's `facts`; delete target routes no facts. Target keys = exact strings for every helper target arg, sidecar key, and reply path.
- Directive ref = `<repo-rel path>:<line>[-<end>]` in existing selected file. Consumers read only cited lines from `<run>/baseline/before/<path>`.
- `provenance-<batch>.json` at `<run>/provenance/`: `batch` (routing batch string), `targets` -> `<routing key>` -> `revision` (string: `ledger.py hash`; `absent` for deleted), `facts: {ID: [1-based line ints]}`, `directives: {ref: [1-based line ints]}` (ref keys = routing directive refs, exact string). Every create/update/keep target in batch has entry, even with zero facts; every routed fact + directive mapped. One owner per sidecar at a time; later owner of target updates its entry only.
- Sidecar retirement after placement revision: every batch whose targets, routed IDs/directives, or membership changed -> fresh writer if batch never written, else fresh fixer, for that current batch rewrites own sidecar to exactly current batch targets (moved target -> new owner writes entry; old batch drops it). Batch absent from new routing -> orchestrator moves its sidecar to `quarantine/`. Index input = sidecars of current routing batches only.
- Final index = `ledger.py index` output; one authoritative target -> revision/facts/lines/directives map. No LLM mapping reconciliation, hash lists, or manuscript revisions.

## Helpers and runner roles

Bundled in package `scripts/`; Python 3.8+ stdlib; run `python -B <resolved package>/scripts/<helper>`. Exit 0 pass, 1 reports/failures, 2 usage/input error. Output = identity only: paths, hashes, counts, PASS/FAIL/WARN lines. Helpers never edit instruction files. Every `--out` = fresh path inside run dir attempt folder; guard needs `<run>/baseline/inventory.json` (coverage/project/questions via run-dir arg; manifest/index via routing.json ancestor). Refused (exit 2, nothing touched): `AGENTS.md`/`CLAUDE.md`/`facts.md` basename, same file as any command input, `.agents`/`.claude` segment, under `<run>/baseline/`, inside repository outside run dir. Guard passed + exit 1|2 -> stale `--out` deleted, except completed coverage exit-1 report retained. Target args = exact routing keys.

- `ledger.py baseline <repo-root> <run-dir> [--external-run]` -> scan, once; immutable (refuses existing baseline). Baseline v4 stores Git tracked names and per-file `other` signatures; no aggregate cap. Summary line includes `ignored <n>` (Git) or `tree <n>` (no Git) -> scan reply. Any other baseline version -> exit 2 -> start new run.
- `ledger.py coverage <run-dir> <scope-proposal.md> [--accepted <accepted-scopes.md>] --out <report>` -> scan for proposal; orchestrator after scope selection with accepted input or to refresh gates on resume; Verify may re-enumerate optionally into an assigned fresh report path. Root comes only from immutable baseline. Inputs belong to same run, outside baseline; output under current run `attempts/<attempt>/`, outside protected paths/input aliases. Versioned report retains input identities/SHA256, fixed counts, sorted uncovered paths + diagnostic reasons/assignments/skips; reasons stay artifact-only. Exit 0 + PASS identity/hash/counts -> gate; exit 1 -> retained diagnostic report, no acceptance; exit 2 -> no pass + safe stale output cleared (rejected destination untouched). Parent never opens report payload. Coverage hashes bind gates to exact proposal/accepted bytes.
- `ledger.py questions <run-dir> <note>... [--answers <gaps.md>...] --out <file>` -> orchestrator, rebuilt before each check round over scan note + all accepted notes + accepted gaps files. Lines `<ID> | flow | contract | owner | status | answer`; gaps `answered: <QID> -> <ID>` lines set answered status.
- `ledger.py project <run-dir> <routing.json> --out <file> <target>...` -> orchestrator; targets = every routed target of batch, verbatim from placement reply (delete included), or every routed target for Verify. Output = assigned placeable records + directives only.
- `ledger.py manifest <repo-root> <routing.json> --out <file>` -> orchestrator; sanitized reviewer manifest: target, disposition, sha256; no fact IDs/evidence.
- `ledger.py index <repo-root> <routing.json> <provenance-*.json>... --out <file>` -> orchestrator after writing/repair; Verify reruns into own attempt folder.
- `ledger.py hash <repo-root> <path>...` -> orchestrator, writer, fixer; current target revisions. `ledger.py hash <repo-root> --baseline <run-dir> <path>...` -> orchestrator; `<rel> <sha256|absent>` from baseline inventory (first-writer expected revision).
- `ledger.py hash <run-dir> <proposal> <accepted-scopes> <coverage-report>...` -> orchestrator + Verify for run-artifact identities only; use run dir as hash root even when run is external to repository. Output path/hash only; never exposes payload. Verify compares report input identities/state; parent compares stored hashes without opening reports. Resume refreshes acceptance only after current input/report hashes match saved PASS identities; mismatch/missing -> required coverage rerun at fresh outputs.
- `ledger.py compare <repo-root> <run-dir> --file AGENTS.md|CLAUDE.md --mode light|full [--allow <rel>]...` -> Verify. `--allow` accepts only exact orchestrator-supplied user-approved paths; default none. An explicitly allowed ignored/other path has no report.
- `check-paths.py <repo-root> [--allow-external <abs-prefix>]... <file>...` + `check-shape.py <repo-root> <file>...` -> non-delete targets only: writer/fixer on owned targets before handoff; Verify on all. No non-delete target -> skip (no-file call walks all). Unbackticked extensionless token checked only when ending `/`; missing `.env`/`.env.local` skipped -> writer/fixer backticks every path token meant to be checked.

Coverage report schema 1: `status: pass|fail`, `root`, `run_dir`, `proposal`, `proposal_sha256`, `accepted`, `accepted_sha256` (accepted pair null for proposal-only); `counts` keys `containers,directories,proposed_scopes,proposed_paths,accepted_scopes,accepted_paths,skipped,linked,excluded,uncovered,issues`; sorted unique `uncovered`; sorted `issues: [{path,code,reason}]` (`unclassified|linked-unclassified|accepted-dropped`); `assignments: {proposal: [{path,scope,reason}], accepted: [...]|null}`, `skips: [{path,reason}]`, `excluded: [{path,code,reason}]` (`git|run`). Stdout gives proposal/optional accepted/report paths + SHA256 and `PASS|FAIL: coverage` counts only. Complete report retained on exit 1 lets a fresh scan consume diagnostics without parent evidence access.

## Helper results and routing

Single home for helper failure + finding routes. Failure detail names target/ID; orchestrator maps target -> batch from placement reply.

- Route vocabulary (reviewer/fixer/Verify replies give counts per target per route; orchestrator dispatches from reply alone, never opens findings/candidates/reports except passing final Verify report, read for relay only): `fixer` -> fresh fixer for owning batch given source findings/report path(s) or FAIL lines; `checker` -> fresh checker (new `-R<k>` prefix) given artifact path -> placement revision -> re-project -> fresh fixer; `placement` -> fresh placement revision given artifact path (+ sidecar retirement); `boundary` -> compare route below.
- Reviewer routes: `wording`, `support`, `probe`, `dedup` (fixer splits: same ID -> edit, else placement-route candidate) -> `fixer`; home change `move`, `delete`, `location` -> `placement`. Fixer candidates -> checker-route | placement-route file per fixer role; both -> checker route before placement. Batch with both placement- and fixer-route work -> placement revision first; resulting fresh writer/fixer gets retirement + pending fixer-route items together.

- Any helper exit 2 (incl malformed routing/sidecar/baseline JSON) -> runner returns `blocked` + stderr line; never pass. Coverage schema/input correction may create a fresh bounded scope-rewrite assignment; accepted identity-format correction is administrative, changed boundaries require scan.
- `check-paths.py` report (`missing`, `format`) + `check-shape.py` FAIL -> mandatory; writer/fixer fixes before handoff; unfixable -> blocked with line + reason (missing path from projected record -> blocked-ID route). `check-shape.py` WARN -> writer/fixer judges per policy Shape, fixes or keeps with one-line reason in reply; Verify rejudges, confirmed violation -> `format` failure; WARN alone never blocks.
- Author rewrite = fresh author (checker facts/gaps, scout note, scan `note-rewrite` or `scope-rewrite`) given failure/required correction + relevant artifact paths, writes new attempt path; replaced file -> `quarantine/`; file in routing `inputs` -> placement revision (updates inputs) before re-project (else exit 2 `routing input missing`). Scan note rewrite owns only assigned scan note; scope rewrite consumes proposal + coverage diagnostic paths, reuses immutable baseline/context, writes new proposal + proposal coverage report, never reruns bootstrap or deep-investigates source. Coverage exit 1 -> scope rewrite; accepted merges dropping paths require reassignment, changed boundaries require revised proposal + both checks. Attempt caps apply; exhausted required gate -> incomplete.
- project `unparsed-record: <file> <ID>` (ID `<prefix>-C<n>|-F<n>`, prefix incl `-R<k>`, lacks both `verdict` + `confidence`; index never parses records) -> author rewrite of file.
- project: `invalid-verdict`, `duplicate-checker` -> checker author rewrite of affected IDs; `duplicate-claim` -> scout/scan author rewrite (scout new ID prefix); `low-confidence` -> fresh checker for IDs -> placement revision; `refuted`, `missing`, `superseded` -> placement revision; `unrouted-target` -> orchestrator corrects target args.
- index: `fact-multiple-targets`, `unrouted-target`, `batch-mismatch`, `multiple-owners`, `delete-has-facts` -> placement revision + sidecar retirement; `missing-provenance` (`<target>` = create/update target lacks sidecar entry; `<target> <ID|ref>` = routed fact/directive ref absent), `unrouted-fact`, `stale-revision`, `line-out-of-range`, `target-missing`, `delete-present` -> fresh fixer for owning batch.
- compare last line `PASS|FAIL: compare <file> <mode>: <n> changed, <f> fail, <w> warn`. FAIL = boundary (`head-changed`, `git-unavailable`, `outside-write`, `counterpart`, `gitignore`, `dirty-changed`) -> orchestrator asks user (needs_user), run reported incomplete; no repair route. Boundary failure never authorizes more writes, including restoring/repairing outside writes. WARN alone exit 0: `dirty-allowed` (allowed path incl `--allow`, dirty at baseline, now changed) -> Verify dirty-edit check (unaccounted loss only, per placement dirty accounting); `observed-other` -> informational only, no attribution or write authorization. Emit `observed-other` only with Git available at baseline and compare time, for changed paths in baseline/current per-file `other` sets, excluding inventory/protected paths, baseline dirty paths, baseline/current tracked names, current status paths, and other run dirs. No-Git ordinary non-inventory paths remain strict. An explicitly allowed `other` path is silent.
- questions FAIL `duplicate-id` (nothing written) -> author rewrite of note owning ID. WARN `unknown-question` (gaps `answered:` cites QID absent from notes) -> answer line ignored, question keeps prior status; not failure.
- Verify run metadata/gate failures use existing `run: other` tally (semantic, mandatory), never boundary authorization or a new finding route: missing/stale coverage -> orchestrator refreshes gates or fresh scan scope rewrite; missing QID disposition -> orchestrator records decision, missing gap -> fresh checker rewrite. Fresh Verify checks repaired prerequisites before acceptance; existing repair/attempt caps remain.

## Return and acceptance

```md
status: <complete | blocked | needs_user>
artifact: <owned output paths | none>
issue: <blocked/needs_user: exact cause, affected dependency, correction/decision>
```

Add only stage-specific decision facts requested by workflow/role: changed artifact paths/revisions, required counts, helper identities/results, unresolved QIDs + reason codes/decisions, finding counts by route + per target, failures, kept WARNs. Scan adds concise scope alternatives + coverage input hashes/report identity/counts; placement retains batch identity + complete current target keys needed for opaque scheduling/project. Complete unchanged target sets stay in stable artifacts unless scheduling/Verify revision checks require them; other replies report changes/exceptions only. Never echo notes/records/routing payload. Include attempt identity only when transport cannot bind it.

- `complete`: all required outputs present at assigned paths, checks met, required work terminal. Artifact existence alone insufficient. Orchestrator checks binding + path presence + decision facts + helper exit; cannot infer absent result from successful tool execution.
- `blocked`: missing input/resource, write/tool/context failure, unresolvable evidence/authority issue; useful partial artifact may remain, dependent stage waits. No unsupported claims to fill gap.
- `needs_user`: unresolved root/authority/model/scope/target-conflict/dirty-user-content choice requiring user; identify decision. Orchestrator asks, continues independent ready work.
- Pending producer -> scheduling state, never evidence gap or extra verification assignment.
- End substantive producer artifacts with `## Conflicts/skipped` (`none` when empty); routing.json uses `unplaced`/`alternatives`, doubts artifact carries conflicts. Verify compiles report.

## Opaque relay

Write-incapable child returns assigned-path payload separately from compact decision return. Orchestrator mechanically saves producer bytes verbatim to reserved owned path; no reading, interpretation, summarization, or acting on evidence. Relay cannot bypass write boundary or recipient path visibility. Failed/unsupported opaque save -> block affected output; do not claim artifact exists. Child remains content owner; orchestrator only transport. Same rule covers generated-file payloads.

## Revisions, ownership, and recovery

- Scan bootstraps run and returns actual paths; later dispatches reserve unique `attempts/<stage>-<attempt>/` paths. Never overwrite another attempt's evidence. Mutable target writers return revisions via `ledger.py hash`. `state.md` tracks identities/pointers, never payloads.
- Accept only active attempt at current prerequisites. Replaced record/routing/target invalidates affected downstream acceptance; cancel/wait affected active writers before replacing input or transferring target ownership. Late/cancelled/stale/unaccepted artifacts (failed checker `facts.md`, retired sidecars, replaced notes) -> orchestrator moves path to `<run>/quarantine/` without reading; never promoted implicitly.
- Every mutable target + its sidecar entry has one owner. Writer -> fixer transfer only after prior owner terminal. Never let older repair overwrite newer accepted target.
- Expected revision: first writer of target -> baseline revision (`ledger.py hash --baseline`, supplied in `writes:`); later writer/fixer -> last accepted revision. Worker compares current `ledger.py hash` to expected before first write, and to own last write before each later write.
- Target conflict: mismatch (start or mid-run) -> worker never writes that target, stops, returns `needs_user` naming it. Orchestrator asks user incorporate|stop: incorporate -> fresh writer/fixer with new expected revision preserving that edit; stop -> incomplete. Never overwrite or restore user edits.
- Per assignment: <=2 attempts (initial + one corrected/transient retry), fresh agent, unique output paths. Unchanged repeated failure -> blocked with recheck condition; explicit changed scope/input/user decision may create new bounded assignment. Scout new-agent attempts count toward mode cap. No unlimited follow-up/retry loop.
- Writer blocked IDs -> fresh checker (ID + writer reason as candidate) -> placement revision -> re-project -> fresh fixer for batch (writer already wrote) = new assignment with own attempts. One such round per ID; still blocked -> placement revision unplaces it as reported gap. Blocked-ID route precedes index: `ledger.py index` for pass runs only after every blocked-ID round resolves (rewritten or unplaced).
- Repair caps per writing pass (initial writers -> final acceptance): semantic <=2 repair/Verify cycles, review-triggered repairs included; formatting-only (every routed failure `format`, plus index-FAIL repair rounds) <=2 cycles, separate counter. Placement revision never resets either cap. Exhausted with mandatory failure -> incomplete report + required decision.
- Unchanged target revisions keep prior semantic acceptance; changed targets rechecked.
- Context overflow -> child saves bounded partial output + exact remaining question/scope; fresh agent continues or orchestrator splits compatible remaining work within caps. Partial output not accepted as complete; no silent truncation or wider read takeover.
- Write failure -> preserve partials + exact path/error; correct permission/path/capability or use relay, then retry. Oversized command/argument -> bounded patch writes; never pass whole artifacts as shell arguments. Do not broaden ownership to work around failure.
- Cancellation -> mark attempt cancelled; request stop; wait terminal before conflicting target writer. Unstoppable child -> block ownership transfer. Late output never changes accepted state.
- Resume -> validate run identity, choices/binding, baseline presence, accepted input revisions/output existence, target owners + `ledger.py hash` revisions. Changed target -> target-conflict rule; orchestrator never reads diff. Preserve task-generated files and user edits: never restore baseline or reset directory. Recheck affected review/Verify stages.
- Coverage invalidation: proposal/accepted bytes or path/container/skip decisions changed -> invalidate both gate states + downstream scope acceptance; stop/wait affected assignments before replacement. Resume invalidates cached gate acceptance until proposal/accepted hashes and PASS report input identities/existence are checked; mismatch/missing identity -> rerun required checks at fresh attempt outputs. Never accept a stale PASS. Targeted QID follow-up alone leaves standing scopes intact; changing accepted standing paths requires scope revision + both gates.
- Missing report/artifact/dependency -> block dependent completion; independent accepted work may continue. Exhausted attempts with mandatory failure -> report incomplete + exact route, never label run successful.

## Usage

Orchestrator records in `state.md` `## Usage` per role/phase/attempt when host exposes: model calls, input (cached/uncached), output/reasoning tokens, duration, artifact bytes. Unexposed -> `unavailable`; never estimate as measured.
