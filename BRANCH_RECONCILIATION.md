# Branch reconciliation and hidden-work control

**Status:** current  
**Reconciled:** 2026-09-10  
**Canonical live-data branch:** `main`

The driver-data repository is intentionally simple: the CSV blobs on `main` define current live driver/town data. Historical branch age or ahead/behind counts must never override those files.

Before this reconciliation branch was created the repo had three branches including `main`.

- `data/import-new-drivers-20260821` is `CONTAINED`: its tip is already an ancestor of `main`.
- `data/add-london-towns-20260821` is `SUPERSEDED`: it still looks ahead in Git history, but its unique `London Towns.csv` and `README.md` blobs are byte-identical to current `main`, while its `Drivers.csv` and `Towns.csv` are older snapshots. It must not be resurrected as “newer” data.

The machine-readable classification is [`branch-dispositions.json`](branch-dispositions.json). The automated guard is [`scripts/check-branch-dispositions.py`](scripts/check-branch-dispositions.py).

## Rule for new data work

New driver/town data work starts from current `main`. An unregistered branch is allowed temporarily only while it is the head of an **open PR updated within the last 30 days**. A stale open PR is not permanent storage: after 30 days without a PR update the daily reconciliation workflow fails until the branch is explicitly classified. Closing a PR removes the exemption immediately.

For data authority, compare the actual CSV blobs/content, not branch creation date, commit count or apparent “ahead” status. A divergent historical branch can contain an older driver roster even when Git reports unique commits.

## Conservative pruning

`scripts/list-branch-prune-candidates.py` is a dry-run aid only. It lists a branch only when the registry says `CONTAINED` **and** the branch is neither the head nor the base of an open PR. It never deletes anything and deliberately excludes `SUPERSEDED` or protected historical statuses. Re-run the full branch reconciliation immediately before any later manual deletion; branch deletion remains a separate explicit operation.

## Repository visibility/data boundary

This repository is currently public. The present `Drivers.csv` is designed around public directory/profile fields and includes driver names and public contact numbers. Public repository history is nevertheless a stronger exposure boundary than a published profile page: every committed historical version remains accessible.

Therefore private operational/account fields must never be added here merely because a future import makes them convenient. In particular, authentication identifiers/tokens, billing identifiers, bank/payment data, identity documents, insurance document URLs/policy numbers, private email/address data, or other non-directory signup data belong in the private application/backend source of truth, not this public CSV repository.

Repository visibility itself is an owner decision and is not changed by this reconciliation.

No historical branch was deleted and no live CSV content was changed by this reconciliation.
