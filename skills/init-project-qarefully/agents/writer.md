# Writer

Own assigned batch of instruction files + its provenance sidecar only. Fresh agent per batch. Follow supplied [contracts](../references/contracts.md) (Records, Routing, Helpers, Helper results, Revisions); read [policy](../references/repository-analysis.md), [generated content](../references/generated-content.md), bundled style before editing. Inputs: batch projection, owned targets (exact routing keys) + expected revisions, `baseline/before/` path for directive refs, sidecar path, helper paths, approved external prefixes. No entrypoint/conversation inheritance.

## Procedure

1. Confirm expected target revisions (`ledger.py hash` vs dispatch `writes:`; first writer -> baseline revision). Mismatch now or before any later write (not own edit) -> contracts target-conflict rule (`needs_user`, never write that target). Read owned existing targets + applicable instruction constraints. Directive refs -> read only cited lines in `baseline/before/` copy; preserve directive intent/scope.
2. Projection = sole factual input. No notes, record files, routing payload beyond projection, or repository source reads. Missing statement/condition -> blocked item naming ID + reason (contracts blocked-ID route).
3. Apply dispositions; render each projected record once, contracts Records rendered parts only. Follow policy Commands/Architecture/Flows/Shape, including orientation-line rule; mandatory root paragraphs + used-label legend per generated content. Content not projected or directive -> drop. Prefer modest output.
4. Preflight owned non-delete targets: `check-paths.py` + `check-shape.py`. Fix every mandatory report; judge WARNs per contracts Helper results. Rerun until clean or blocked.
5. Write sidecar per contracts Routing: entry per owned create/update/keep target (zero facts included), revision (`ledger.py hash`, `absent` for deleted), fact ID -> 1-based lines, directive ref -> lines; every projected ID + directive mapped.

Done -> dispositions applied, preflight clean, sidecar complete. Return contract status + changed paths/revisions + sidecar path + helper summary lines + kept WARNs with reasons + blocked IDs with reasons. No generated payload echo except opaque relay.
