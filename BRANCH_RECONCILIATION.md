# Driver-data branch reconciliation

**Status:** current  
**Reconciled:** 2026-09-11  
**Canonical branch:** `main`

This repository owns the current directory CSV representation. Branch age is not data authority.

## Current branch surface

There are now **2 remote branches**:

- `main` — live directory-data authority.
- `data/add-london-towns-20260821` — retained `SUPERSEDED` history for reference only.

The former `data/import-new-drivers-20260821` branch was proven fully contained in `main` and retired. The merged 2026-09-10/11 cleanup head was also retired.

No CSV row content was changed by the control-plane merge or branch prune.

## Retention rule

A historical branch is deleted routinely only if it is `CONTAINED`, has no explicit protection, has no open-PR dependency and is freshly proven an ancestor of current `main`.

`SUPERSEDED` history is retained by default because it can still provide useful provenance. Do not use old branch CSV snapshots as live data merely because they appear newer or differently named.

The machine-readable authority is `branch-dispositions.json`; the branch-reconciliation workflow enforces the boundary.
