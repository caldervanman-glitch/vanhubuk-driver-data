# Branch reconciliation and hidden-work control

**Status:** current  
**Reconciled:** 2026-09-10  
**Canonical live-data branch:** `main`

The driver-data repository is intentionally simple: the CSV blobs on `main` define current live driver/town data. Historical branch age or ahead/behind counts must never override those files.

Before this reconciliation branch was created the repo had three branches including `main`.

- `data/import-new-drivers-20260821` is `CONTAINED`: its tip is already an ancestor of `main`.
- `data/add-london-towns-20260821` is `SUPERSEDED`: it still looks ahead in Git history, but its unique `London Towns.csv` and `README.md` blobs are byte-identical to current `main`, while its `Drivers.csv` and `Towns.csv` are older snapshots. It must not be resurrected as “newer” data.

The machine-readable classification is [`branch-dispositions.json`](branch-dispositions.json). The automated guard is [`scripts/check-branch-dispositions.py`](scripts/check-branch-dispositions.py).

New data work starts from current `main`. An unregistered branch is allowed only while it is the head of an open PR. The daily branch-reconciliation workflow fails on unregistered abandoned branches and on any branch incorrectly labelled `CONTAINED`.

No historical branch was deleted by this reconciliation.
