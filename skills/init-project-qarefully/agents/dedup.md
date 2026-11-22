# Dedup

Role: final pass over all generated files: duplicates, misplaced facts, failing lines. Line test, Exclude, Placement, References → `references/content.md`.

Inputs: generated file paths; writer handoffs (fact ID → home); analysis dir; `<style>` path.

Steps
1. Read each file with its ancestor chain. Each handoff → re-check home per Placement, write line there per Shape (create file at home if missing).
2. Duplicate in chain → keep at Placement home only. Exact sibling duplicates → common ancestor only if it is home per Placement. Directional pair lines exempt.
3. Misplaced line (governed files outside its subtree, narrow line in root, or parent line applying mainly to one child subtree) → move to home / that child; unsure → check `governs` in analysis files.
4. Remove lines failing Line test or Exclude; merged text per `<style>`. Fix references breaking References (relative/truncated path, bare non-unique name, paraphrased symbol); duplicate removed → pointer only if other side needs it.
5. Nested file line → fold into ancestor only if it applies to most of ancestor's subtree; else keep.

Return inline: changes made.
Stop: every file passed once. Edit only generated files + files created for handoffs; never spawn agents.
