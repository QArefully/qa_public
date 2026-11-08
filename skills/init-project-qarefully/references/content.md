# Content rules

All output (returns, analysis files) → terse AI-to-AI: fragments, arrows, no articles/filler/hedging.
Writer, dedup → also `<style>` (llm-oriented-writing) for instruction files. Conflict → this file wins: Shape, References.
Depth applies to investigation, not output: dig exhaustively, then cut hard.

## Boundary
- Ignore `.init-project/` except analysis files/dir named in your inputs.
- No builds, tests, installs, network.

Reader = capable agent new to repo; reads code well. Write only what it would get wrong or miss after normal exploration of files it edits. Each line costs context on every load and rots → less is more.

## Include
- Architecture → rules, not maps: allowed dependency direction + every check enforcing it; runtime/process/target split + what code may run where; source of truth for duplicated or generated data; where new code of a common kind must go when obvious place is wrong. Line only saying what a dir contains → fails.
- Conventions → patterns whose violation compiles but breaks behaviour, or is caught only by a check agent may not run. Rule + enforcing check or exemplar path.
- Unusual solutions → deviation from language/framework default + reason if known.
- Couplings → change here → also change/check there + what breaks. Priority: across language, process, codegen, config boundaries invisible in imports. Common change needing several non-adjacent edits → one line naming touch points.
- Complex logic → state owner + invariant/ordering a change can break + authority path. Longer → narration; cut.
- Pitfalls → verified traps; misleading code (looks dead but live; pattern not to copy); tests/mocks proving less than they appear → + verify-by: exact command + test path/glob that does cover it; none found → line says so.
- Commands (root) → setup, fast dev loop, check/lint, test + single-test pattern; exact, copyable; cwd if not repo root; destructive → impact. Everyday loop only: rare/alternate commands (extra runners, daemons, CI-only, smoke/e2e variants) → nested file of subtree they serve, or drop.

## Exclude
- Trees; file/class/function/symbol/dependency inventories; stack summaries.
- Numbers: counts, line numbers, timings; versions only when required to run.
- Code narration, walkthroughs, snippets.
- Anything obvious from file names, entry point or neighbouring code.
- README/docs content → point to path.
- Generic advice; rules a linter/formatter enforces → name the check.
- Speculation. Negative/absence claims ("nothing enforces X", "X unused") unless every plausible enforcer/consumer checked → line names what was checked.

## Line test
Keep only if all: new agent would plausibly get it wrong or waste time without it; survives ordinary refactors; not already said in same ancestor chain.

## Placement
Harnesses load root + ancestors of cwd at start; nested file only when agent touches a file in that dir's subtree; never siblings; search never loads.
- `governs` = trigger files: editing them → agent needs fact. Not files fact is about. Limitation of A seen from B → governs A (+ B only if editing B can trip it).
- Home → deepest dir that is ancestor of all governed files.
- Home = root but fact narrow (coupling between distant subtrees) → one directional line per side, in each side's nearest file; both sides resolve to root → one root line. Pair lines asymmetric: each states what breaks on its side.
- Generated files → governs generator input + output; line names source of truth + regen command; output unplaceable → input side.
- Test-infrastructure facts → test tree; module facts → module side.
- Needed before touching any file (commands, where things live, repo-wide rules) → root. Root stays repo-wide; few narrow path-triggered lines.
- Nested file at every home holding a kept fact; single fact enough. Parent-file line not applying to most work under that parent → move down to dir where it applies most. Siblings sharing a pattern → one file at parent.

## Shape
- Root: one-line purpose; sections only with content (typical: Commands, Architecture, Conventions, Pitfalls).
- Root Commands: few lines; one line per task = command(s) + few-word note. Caveat beyond few words → Pitfalls/Conventions/nested file, not inline; only trap making command silently wrong (stale output, wrong documented form) stays as short note.
- Nested: bullets; `##` only when grouping helps; no title/scope boilerplate.
- One fact per bullet: claim → consequence → authority path. Terse.

## References
Every reference pasteable into Read/Grep from repo root; lines get read far from their file's header (many injections, compaction, subagent prompts).
- Path → full from repo root, backticked, every line. Never relative to instruction file (`./x`, `browser/x`), never truncated. Dir → full path + trailing `/`; placeholders ok (`src/a/<feature>/`).
- Several files, one dir, one line → full dir once, then bare names: `` `src/a/b/`: `x.ts`, `y.ts` ``. Bare name standalone → only if unique in repo.
- Spot inside file → exact symbol + its file path: class, method, field, type, enum member, string key (setting, command id, message type, service id, rule id). Spelled as in code (`_` prefix, case); never paraphrase or describe in its place.
- Pattern to copy → `exemplar: <path>`.
- Fact owned by other instruction file → pointer to its full path; never restate.
- No links, no line numbers.

## Analysis files
`<run>/analysis/<lead-id>.md`, written by leads; detail for writers + dedup.
- `## Facts`, one per line:
  - <lead-id>-<n> | <kind> | <claim → consequence> | home: `dir/` | governs: `path/`, `file` | evidence: `path` `symbol` | conf: high|low
  - claim + evidence per References: full paths, exact symbols; test-weakness facts carry verify-by.
  - kind: arch | convention | unusual | coupling | logic | pitfall | command
  - home = target instruction-file dir per Placement; root → `./`. Pair lines → one fact per side.
  - Wave-2 edits: correct/remove wrong facts in place, confirmed low → high; new facts → next free ID.
  - conf high = read in implementation; low → + what would confirm.
- `## Details`: per fact ID needing it → flows, invariants, ordering, both sides of couplings; helps writers word lines, never copied verbatim.
- `## Nested files`: suggested dirs → why (local facts | own commands/runtime).
- `## Open questions`: question → why it matters → where to look.

## Lead inline return
Short; no fact lines.
- files written/edited
- coverage: area → deep | shallow
- gaps: what else needs investigating → why → where
- open questions changing content (incl. conf: low facts worth confirming): question → where to look
- limit hit (only if a spawn was refused): refusals count, limit stated in error (if any), stopped early yes/no, unstarted questions
