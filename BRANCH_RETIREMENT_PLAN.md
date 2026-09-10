# Driver-data branch retirement plan

**Snapshot:** 2026-09-10  
**Authority:** `branch-dispositions.json` + `scripts/list-branch-prune-candidates.py` at execution time.  
**Action level:** non-destructive planning only. This file does not authorize deletion.

The data repository has a deliberately small branch surface. Current CSV blobs on `main` are the live authority.

## Current contained retirement candidate (1)

- `data/import-new-drivers-20260821` — its tip is already contained by `main` and it is not used by an open PR.

## Not an automatic retirement candidate

- `data/add-london-towns-20260821` is `SUPERSEDED`, not `CONTAINED`. Its unique London-town/README blobs are already represented on `main`, while its Drivers/Towns snapshots are older. Keep it out of ordinary pruning until a deliberate provenance-retention decision is made.
- `ops/branch-reconciliation-20260910` is the active head of PR #4 and is excluded while the PR remains open.

## Retirement procedure

1. Merge the reconciliation/control-plane PR first so branch authority and public-data guards exist on `main`.
2. Re-run branch reconciliation and `scripts/list-branch-prune-candidates.py` against fresh refs/open PR metadata.
3. Delete only a branch still emitted by the script.
4. Update `branch-dispositions.json` in the same cleanup so absent branches do not leave stale authority records.
5. Re-run both Branch reconciliation and Public data boundary CI.

Do not use branch age or an ahead count to decide which CSV data is current; only the current files on `main` define the live directory representation.
