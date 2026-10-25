# Handoff Contracts

## Capability binding

Before first child, inspect actual exposed controls; retain compact binding for scheduling/resume:

- dispatch/isolation: fresh bounded child without parent conversation; child can load assigned role/resources. Related completed scout may be reused with bounded follow-up, not session dump.
- model: requested + observable effective model/effort/profile; distinguish unobservable effective choice. `inherit` retains immediate parent's binding, including when native profile defaults would differ. Exact named profile only when user requests it; verify availability. Never silently substitute. Unverifiable required binding -> report limit/ask for viable authorized binding.
- visibility/writes: recipient resolves package/input/output paths; disjoint owned targets writable. Map paths across workspaces explicitly. Cannot write -> opaque relay below; no usable dispatch/isolation -> capability issue, never local role takeover.
- capacity: actual concurrent slot ceiling + lower user limit; reserve slots before dispatch, queue when full. Mode scout total separate. No nested delegation; only orchestrator starts children.
- wait/cancel: actual wait/terminal signaling and cancellation behavior. Long work -> wait controls + concise user progress; never treat commentary/tool return as done. Inability to stop writer -> retain ownership until terminal, block conflicting work.

## Dispatch

Transport binds run/stage/attempt when possible; otherwise include explicit identity. Resolve paths in recipient's workspace, including paths inside selected Markdown sections. Give exact relevant contract sections + workflow boundary rules; child must read/follow bound role and selected policy/style sections. No child reads entrypoint or assumes inherited instructions.

```md
role: <ID + resolved agents/<role>.md path>
task: <bounded objective; explicit phase for merged role>
run: <root/location hint; actual run path after scan>
choices: <filename; mode; selected scan binding>
binding: <this role's requested/effective model; tools; no nested children>
constraints: <user/host restrictions; task boundary; preserve others' edits>
inputs:
- <resolved path>#<section> -> <purpose; accepted revision>
writes:
- <exact owned path> -> <consumer; expected prior target revision if mutable>
done: <role result + checks>
limits: <scope/context; attempt; remaining scout/slot capacity when relevant>
```

No common transcript/task-wide payload. Only role tools: read/search/list/read-only Git where role permits; no application/tests/install/migration/network/state effects. Exceptions: assigned artifact/product writes + Verify path helper. Only orchestrator asks user. Contradictory instructions -> return issue; no hidden expansion.

Parallel mutable targets require disjoint ownership. All workers share workspace: preserve user/other workers' edits. Role procedure narrows read/write scope further. Existence/identity checks are allowed for orchestration; payload analysis stays with assigned role.

## Return and acceptance

```md
status: <complete | blocked | needs_user>
artifact: <owned output paths | none>
issue: <blocked/needs_user: exact cause, affected dependency, correction/decision>
```

Add only stage-specific decision facts requested by workflow/role: scope alternatives, counts, changed paths/revisions, compact ownership map, gaps/findings, moves/deletes, conflicts/skipped, pass/fail. Never echo notes/verdicts/placement evidence. Include attempt identity only when transport cannot bind it. Multiple artifact paths allowed in one compact return.

- `complete`: all required outputs present at assigned paths, checks met, required work terminal. Artifact existence alone insufficient. Orchestrator checks current binding + path presence + decision facts; cannot infer absent result from successful tool execution.
- `blocked`: missing input/resource, write/tool/context failure, unresolvable evidence/authority issue; useful partial artifact may remain, dependent stage waits. No unsupported claims to fill gap.
- `needs_user`: unresolved root/authority/model/scope choice requiring user; identify decision. Orchestrator asks, continues independent ready work.
- End substantive producer artifacts with `## Conflicts/skipped` (`none` when empty). Reviewer uses reply; Verify compiles report. Decision artifacts stay short, evidence stays in assigned payload.

## Opaque relay

Write-incapable child returns assigned-path payload separately from compact decision return. Orchestrator mechanically saves producer bytes verbatim to reserved owned path; no reading, interpretation, summarization, or acting on evidence. Relay cannot bypass write boundary or recipient path visibility. Failed/unsupported opaque save -> block affected output; do not claim artifact exists. Child remains content owner; orchestrator only transport. Same rule covers generated-file payloads.

## Revisions, ownership, and recovery

- Initial scan bootstraps run under supplied location rule and returns actual paths; subsequent dispatches reserve exact unique stage-attempt artifact directories. Never overwrite another attempt's evidence. Producer states input revisions and resulting artifact revision in artifact; mutable target writers return changed target revisions (hash or host revision). State tracks identities/pointers, not payloads.
- Accept only active attempt at current prerequisites. Replaced note/verdict/placement/target invalidates affected downstream acceptance; cancel/wait affected active writers before replacing input or transferring target ownership. Ignore late/cancelled/stale results; quarantine old artifact paths, never promote them implicitly.
- Every mutable target has one owner. Writer -> reviewer -> fixer transfer only after prior owner terminal. Reviewer move/delete + fixer corrections -> placement reconciliation -> new mapping revision. Never let an older repair overwrite newer accepted target.
- Per stage: <=2 attempts for same bounded assignment (initial + one corrected/transient retry), unique output paths. Unchanged repeated failure -> blocked with recheck condition; explicit changed scope/input/user decision may create new bounded assignment. At most 2 repair/Verify cycles per accepted writing pass; remaining mandatory failure -> incomplete report + required decision before another cycle. Scout new-agent attempts still count toward mode cap. No unlimited follow-up/retry loop.
- Context overflow -> child saves bounded partial output + exact remaining question/scope; orchestrator requests focused projection or splits compatible remaining work within caps. Partial output not accepted as complete; no silent truncation or wider read takeover.
- Write failure -> preserve useful partials + exact path/error; correct permission/path/capability or use relay, then retry current inputs. Do not broaden ownership to work around failure.
- Cancellation -> mark attempt cancelled; request stop; wait terminal before conflicting target writer. Unstoppable child -> block ownership transfer. Late output never changes accepted state.
- Resume -> validate run identity, choices/binding, baseline presence, accepted input revisions/output existence, current target ownership/revisions. Assign worker to assess changed inputs/targets; orchestrator never reads diff. Preserve task-generated files and user edits: never restore baseline or reset directory to retry. Repair from current owned targets + current accepted placement; changed outside edits -> worker reports conflict before overwrite. Recheck affected review/Verify stages.
- Missing report/artifact/dependency -> block dependent completion; independent accepted work may continue. Exhausted attempts with mandatory failure -> report incomplete + exact route, never label run successful.
