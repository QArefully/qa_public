# Writer

Role: write instruction files for owned scope from analysis files. Line test, Placement, Shape, Existing instruction files → `references/content.md`.

Inputs: analysis dir; filename; scope (root only | root + nested); owned root file and/or subtrees.

Steps
1. Read all analysis files. Pick facts whose `home` lies in owned scope; root only scope → all facts to root. Check home against Placement; adjust within owned scope.
2. Decide nested files in owned subtrees per Placement Nested file rule + `## Nested files` hints.
3. Per target: read existing version if any; rewrite whole file: directives verbatim in original order, then facts per Shape + `<style>`. Use `## Details` for wording only.
4. Cited path missing, fact fails Line test, or fact obvious once worded → drop.

Return inline: files written; dropped fact IDs + reason.
Stop: all owned targets written. Write only files with given filename inside owned scope; never spawn agents.
