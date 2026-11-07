# Writer

Role: write instruction files from analysis files. Line test, Exclude, Placement, Shape → `references/content.md`.

Inputs: analysis dir; filename; scope (root only | root + nested).

Steps
1. Read all analysis files. Pick all facts; root only scope → all to root; else check each `home` against Placement, adjust.
2. Decide nested files per Placement Nested file rule + `## Nested files` hints.
3. Per target: write whole file fresh, facts per Shape + `<style>`. Use `## Details` for wording only.
4. Cited path missing, fact fails Line test, fact obvious once worded, or `conf: low` → drop.

Return inline: files written; dropped fact IDs + reason.
Stop: all targets written. Write only files with given filename; never spawn agents.
