# Driver-data branch retirement state

**Snapshot:** 2026-09-11  
**Authority:** current `main`, live GitHub and `branch-dispositions.json`.

The conservative prune is complete.

- Before cleanup: **4** remote branches.
- Current: **2** remote branches.
- `data/import-new-drivers-20260821` was deleted only after being proven `CONTAINED` by `main`.
- The merged cleanup branch was retired after PR #4 merged.
- `data/add-london-towns-20260821` is deliberately retained as `SUPERSEDED` historical reference. Its useful London/README content is represented on `main`, while its older Drivers/Towns snapshots must not be resurrected as live authority.

Current live directory authority is the CSV content on `main`.

Future automatic pruning remains limited to `CONTAINED` branches with no `protect_reason`, no open-PR dependency and fresh proof that the tip is an ancestor of `main`.
