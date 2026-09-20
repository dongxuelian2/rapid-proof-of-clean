# Reference robustness and common-mode limit

Updated 2026-09-20. The reference layer is a qualification protocol, not proof
that a coupon is chemically clean.

## Implemented qualification

For both structured and diversity features, the final workflow requires:

- a graph-consistent cluster containing at least two of three references;
- leave-one-out stability of the selected cluster;
- agreement of the cluster with a dated historical anchor after removal of
  per-pixel common exposure;
- valid anchor identity, material/finish scope and lifecycle metadata.

An independent outlier can be trimmed. A self-consistent common-mode change is
not identifiable from the current references alone; the dated anchor supplies
the additional comparison. If the anchor is absent, the code returns UNKNOWN.

## Synthetic stress results

For the selected adaptive policy, 20 FOVs were run per reference scenario:

| Scenario | Reference rejection | PASS | UNKNOWN | Interpretation |
|---|---:|---:|---:|---|
| One independently dirty reference | 0% | 100% | 0% | two clean references retained; outlier trimmed |
| Common-mode dirty references | 100% | 0% | 100% | historical anchor catches shape drift |
| Bounded common aging | 0% | 0% | 100% | anchor accepts reference set, but evidence disagreement conservatively abstains |
| Excess common aging | 100% | 0% | 100% | anchor drift rejects before acquisition |
| Historical anchor absent | 100% | 0% | 100% | common-mode cleanliness not established |

These cases perturb clean rendered observations and are not physical drift data.

## What remains unidentifiable

If the live references, historical anchor and sample share the same optical
change—or if the anchor itself was dirty when certified—the optical data contain
no clean origin. Multiple agreeing coupons do not solve that common-mode problem.
Operational controls must therefore include independently prepared anchors,
chain-of-custody, replacement intervals, blanks and periodic orthogonal checks.

## Reference lifecycle proposed for a coupon study

1. assign immutable reference ID, material lot, finish, cleaning method and date;
2. capture raw baseline frames plus an independent accepted cleanliness result;
3. store robust feature envelopes rather than a single mean image;
4. run a blank/control before each session and log pairwise/anchor distances;
5. quarantine rather than overwrite a drifting reference;
6. estimate aging distributions across days and operators;
7. force UNKNOWN for missing, stale, mismatched or unqualified anchors.

The synthetic thresholds (`0.045`, `0.060`, `0.070` log-shape units) are
preregistered starting values only. They have no physical acceptance authority.
