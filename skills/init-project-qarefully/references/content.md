# Content rules

Writing style → `<style>` (llm-oriented-writing). Conflict → this file wins: Analysis files, Shape, path form.
Depth applies to investigation, not output: dig exhaustively, then cut hard.

Reader = capable agent new to repo; reads code well. Write only what it would get wrong or miss after normal exploration of files it edits. Each line costs context on every load and rots → less is more.

## Include
- Architecture → rules, not maps: allowed dependency direction + every check enforcing it; runtime/process/target split + what code may run where; source of truth for duplicated or generated data; where new code of a common kind must go when obvious place is wrong. Line only saying what a dir contains → fails.
- Conventions → patterns whose violation compiles but breaks behaviour, or is caught only by a check agent may not run. Rule + enforcing check or exemplar path.
- Unusual solutions → deviation from language/framework default + reason if known.
- Couplings → change here → also change/check there + what breaks. Priority: across language, process, codegen, config boundaries invisible in imports. Common change needing several non-adjacent edits → one line naming touch points.
- Complex logic → state owner + invariant/ordering a change can break + authority path. Longer → narration; cut.
- Pitfalls → verified traps; misleading code (looks dead but live; pattern not to copy); tests/mocks proving less than they appear.
- Commands (root) → setup, fast dev loop, check/lint, test + single-test pattern; exact; destructive → impact.

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
- Home → deepest dir that is ancestor of all governed files; no file there (per Nested file rule below) → nearest ancestor with one.
- Home = root but fact narrow (coupling between distant subtrees) → one directional line per side, in each side's nearest file; both sides resolve to root → one root line. Pair lines asymmetric: each states what breaks on its side.
- Generated files → governs generator input + output; line names source of truth + regen command; output unplaceable → input side.
- Test-infrastructure facts → test tree; module facts → module side.
- Needed before touching any file (commands, where things live, repo-wide rules) → root. Root stays repo-wide; few narrow path-triggered lines.
- Nested file when subtree has several kept local facts, or its commands/runtime differ from root's. Siblings sharing a pattern → one file at parent.

## Shape
- Root: one-line purpose; sections only with content (typical: Commands, Architecture, Conventions, Pitfalls).
- Nested: bullets; `##` only when grouping helps; no title/scope boilerplate.
- One fact per bullet: claim → consequence → authority path. Terse.
- Paths repo-relative, backticked. No links, no line numbers.

## Analysis files
`<run>/analysis/<lead-id>.md`, written by leads; detail for writers + dedup.
- `## Facts`, one per line:
  - <lead-id>-<n> | <kind> | <claim → consequence> | home: `dir/` | governs: `path/`, `file` | evidence: `path` | conf: high|low
  - kind: arch | convention | unusual | coupling | logic | pitfall | command
  - home = target instruction-file dir per Placement; root → `./`. Pair lines → one fact per side.
  - Wave-2 edits: correct/remove wrong facts in place, confirmed low → high; new facts → next free ID.
  - conf high = read in implementation; low → + what would confirm.
- `## Details`: per fact ID needing it → flows, invariants, ordering, both sides of couplings; helps writers word lines, never copied verbatim.
- `## Nested files`: suggested dirs → why (several local facts | own commands/runtime).
- `## Open questions`: question → why it matters → where to look.

## Lead inline return
Short; no fact lines.
- files written/edited
- coverage: area → deep | shallow
- gaps: what else needs investigating → why → where
- open questions changing content (incl. conf: low facts worth confirming): question → where to look
