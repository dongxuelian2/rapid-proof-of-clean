# Research evidence system

The ledgers in this directory are the traceability layer for future work. Phase 0 creates their structure but does not add technical-solution literature.

## `source_ledger.csv`

One row per source. Use stable source IDs, record the access date, and distinguish source type from relevance. Public citation metadata is allowed; restricted full text is not automatically allowed.

## `claims_ledger.csv`

One row per material claim. `source_ids` should reference one or more source IDs. Suggested claim statuses are:

- `UNVERIFIED`
- `SUPPORTED`
- `CONTRADICTED`
- `NEEDS_REVIEW`

Do not mark a claim supported merely because a source exists; record the evidence type and review status.
