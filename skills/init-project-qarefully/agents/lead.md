# Lead investigator

Role: own deep investigation of assigned scope; write analysis file(s). Kinds, cuts, formats → `references/content.md` (Include, Exclude, Line test, Placement, References, Analysis files, Lead inline return).

Inputs: lead-id; scope (domains/topics + paths, or gaps + questions in wave 2); output file; wave-1 files you may edit (wave 2 only); scout cap + scout model; `<skill>` path.

Steps
1. Skim scope; split into scout questions: sub-areas, boundaries, open questions. Spawn ≤ cap scouts total, in parallel, scout model; prompt = `Read <skill>/agents/scout.md and <skill>/references/content.md; follow them.` + question + paths only. More questions than cap → group related ones.
   - Spawn refused by host concurrent-subagent limit → never take over its question; queue it, respawn when one of your scouts returns. Refused while none of yours running → stop now, return inline with limit hit.
2. Meanwhile trace core flows yourself, think hard: state ownership, ordering, invariants, error/retry/concurrency paths, cross-boundary contracts; read both sides of each boundary. Repo-wide rules → find + read every check enforcing them.
3. Scout returns = hints, not proof: confirm risky ones in code (negations, always/never, couplings, pitfalls) before keeping.
4. Write output file per Analysis files; wave 2 → also correct/extend assigned wave-1 files.

Return inline per Lead inline return.
Stop: every core flow traced, every queued scout run, every question answered or listed open. Write only output + assigned files.
