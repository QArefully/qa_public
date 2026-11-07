# Dedup

Role: final pass over all generated files: duplicates, misplaced facts, failing lines. Line test, Exclude, Placement, Existing instruction files → `references/content.md`.

Inputs: generated file paths; analysis dir.

Steps
1. Read each file with its ancestor chain.
2. Duplicate in chain → keep at Placement home only. Exact sibling duplicates → common ancestor only if it is home per Placement. Directional pair lines exempt.
3. Misplaced line (governed files outside its subtree, or narrow line in root) → move to home; unsure → check `governs` in analysis files.
4. Remove lines failing Line test or Exclude; merged text per `<style>`. Directives never removed or moved.
5. Near-empty nested file created this run → fold into ancestor; pre-existing file → never delete, keep directives.

Return inline: changes made.
Stop: every file passed once. Edit only generated files; never spawn agents.
